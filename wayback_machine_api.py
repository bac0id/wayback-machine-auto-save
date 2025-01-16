import requests
import re
import json
import utils
import time
import random

from save_page_options import SavePageOptions
from job_result import JobResult

class WaybackMachineAPI:
    def __init__(self, cookies, proxies=None, host="https://web.archive.org"):
        self.cookies = cookies
        self.proxies = proxies
        self.host = host

    def get_api_url_of_save_page(self, saving_url):
        """
        Get API url of save page of Wayback Machine. 
        Its http response is html. 
        Invoked when click "SAVE PAGE" at https://web.archive.org/save . 
        Args:
            saving_url: Url of web site to save.
        Returns:
            A string of API url of save page.
        Examples:
            saving_url:
                "https://example.com/"
            Returns:
                "https://web.archive.org/save/https://example.com/"
        """
        url = f"{self.host}/save/{saving_url}"
        return url

    def get_job_id_from_response_of_api_of_save_page(self, response_content):
        """
        Get job_id from response of API of save page. 
        Args:
            response_content: Response content of `get_api_url_of_save_page()`
        Returns:
            job_id: a string of Job id formatted like `spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123`
        Examples:
            response_content:
                "<script>spn.watchJob("spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123","/_static/",6000);</script>"
            Returns:
                "spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123"
        """
        # match substr between 'spn.watchJob("' and '"'
        pattern = r'spn\.watchJob\("([^"]+)"'
        match = re.search(pattern, response_content)
        if match:
            spn_id = match.group(1)
            return spn_id
        else:
            return None

    def get_job_id_from_response_of_api_of_save_page(self, response_content):
        """
        Get job_id from response of API of save page. 
        Args:
            response_content: Response content of `get_api_url_of_save_page()`
        Returns:
            job_id: a string of Job id formatted like `spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123`
        Examples:
            response_content:
                "<script>spn.watchJob("spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123","/_static/",6000);</script>"
            Returns:
                "spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123"
        """
        # match substr between 'spn.watchJob("' and '"'
        pattern = r'spn\.watchJob\("([^"]+)"'
        match = re.search(pattern, response_content)
        if match:
            spn_id = match.group(1)
            return spn_id
        else:
            return None

    def get_api_url_of_watch_job(self, job_id):
        """
        Get API url of watch job of Wayback Machine. 
        Its http response is json. 

        Invoked periodically during saving process. 
        By default, invoked about 35 times per 6 seconds. 

        We use this API not only to monitor the progress of job, but also to ensure WM doesn't prematurely terminate the job. 
        Args:
            job_id: Job id of an archive job. Found from http response of `get_api_url_of_save_page()`, refer to 'get_job_id_from_response_of_api_of_save_page()'
        Returns:
            A string of API url of watch job of given `job_id`.
        Examples:
            `response_content`:
                "spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123"
            Returns: 
                "https://web.archive.org/save/status/spn2-abcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123?_t=1736749056297"
        """
        current_timestamp = utils.get_unix_time()
        url = f"{self.host}/save/status/{job_id}?_t={current_timestamp}"
        return url

    # # Invoked for 4 times after success of watch_job. Usage is unknown. 
    # # Return example: https://web.archive.org/web/timemap/?url=https://example.com/&from=2025011300000&limit=1&_t=1736754128831
    # def get_api_url_of_claim_archive(self, original_url, success_timestamp):
    #     current_timestamp = utils.get_unix_time()
    #     url = f"{self.host}/web/timemap/?url={original_url}&from={success_timestamp}&limit=1&_t={current_timestamp}"
    #     return url


    def get_job_result_from_response_of_api_watch_job(self, response_content):
        """
        Get job result from response of API of watch job. 
        Args:
            response_content: Response content of `get_api_url_of_watch_job()`
        Returns:
            An instance of `JobResult`
        """
        try:
            json_obj = json.loads(response_content)
            result = JobResult(
                job_id=json_obj.get("job_id"),
                status=json_obj.get("status"),
                timestamp=json_obj.get("timestamp"),
                outlinks=json_obj.get("outlinks"),
                counters=json_obj.get("counters"),
                duration_sec=json_obj.get("duration_sec"),
                http_status=json_obj.get("http_status"),
                original_url=json_obj.get("original_url"),
                resources=json_obj.get("resources"),
                screenshot=json_obj.get("screenshot"),
            )
            return result
        except Exception as e:
            print(f"Exception: {e}")
            return None

    def save_page(self, saving_url):
        options = SavePageOptions(capture_outlinks=False,capture_screenshot=False)

        number_of_try_to_resend_job = 2
        while number_of_try_to_resend_job > 0:
            try:
                api_url = self.get_api_url_of_save_page(saving_url)
                http_post_data_of_options = options.to_wayback_machine_http_post_data_dict(saving_url)
                print("Http post:",api_url)
                response = requests.post(url=api_url, data=http_post_data_of_options, cookies=self.cookies, proxies=self.proxies)
                response.raise_for_status()
                print("status_code:",response.status_code)

                job_id = self.get_job_id_from_response_of_api_of_save_page(response.text)
                if job_id is not None:
                    print(f"WM accept saving {saving_url}, job_id: {job_id}")
                    break
                else:
                    print(f"WM REFUSE saving {saving_url}, Resending...")
                    number_of_try_to_resend_job -= 1
            except Exception as e:
                print(f"Error: {e}. Resending...")

            time.sleep(self.get_sleep_duration())
        
        if job_id is None:
            print(f"Save page failed: {saving_url}.")
            return False

        number_of_successful_call_of_api_of_watch_job = 0
        while number_of_successful_call_of_api_of_watch_job < 0:
            try:
                api_url = self.get_api_url_of_watch_job(job_id)
                print("Http get:",api_url)
                response = requests.get(url=api_url, cookies=self.cookies, proxies=self.proxies)
                response.raise_for_status()
                #print("status_code:",response.status_code)

                number_of_successful_call_of_api_of_watch_job += 1

                job_result = self.get_job_result_from_response_of_api_watch_job(response.text)
                if job_result.status == 'success':
                    print(job_result)
                    break
            except Exception as e:
                print(f"Error: {e}. Retrying...")

            time.sleep(self.get_sleep_duration())

        # for i in range(4):
        #     time.sleep(5)
        #     try:
        #         api_url = get_api_url_of_claim_archive(watch_job_result.original_url, watch_job_result.timestamp)
        #         print("Http get:",api_url)
        #         response = requests.get(url=api_url, cookies=self.cookies, proxies=self.proxies)
        #         print(f"status_code: {response.status_code}")
        #         #print(f"resonse.text: {response.text}")
        #     except Exception as e:
        #         print(f"Error: {e}")
        
        print(f"Save page successful: {saving_url}, job_id: {job_id}")
        return True

    def get_sleep_duration(self):
        return self.get_random_sleep_duration()

    def get_random_sleep_duration(self):
        duration = random.randint(5,10)
        return duration
