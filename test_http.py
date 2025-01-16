import requests
import threading

def save_page(saving_url, options=SavePageOptions()):
    while True:
        try:
            api_url = self.get_api_url_of_save_page(saving_url)
            http_post_data_of_options = options.to_wayback_machine_http_post_data_dict(saving_url)
            print("Http post:",api_url)
            response = requests.post(url=api_url, cookies=self.cookies, data=http_post_data_of_options)
            print("status_code:",response.status_code)

            job_id = self.get_job_id_from_response_of_api_of_save_page(response.text)
            print("job_id:",job_id)
            if job_id is not None:
                break
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)

    while True:
        try:
            api_url = self.get_api_url_of_watch_job(job_id)
            print("Http get:",api_url)
            response = requests.get(url=api_url, cookies=self.cookies)
            print("status_code:",response.status_code)

            job_result = self.get_job_result_from_response_of_api_watch_job(response.text)
            print("job_result.status:",job_result.status)
            if job_result.status == 'success':
                print(job_result)
                break
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)

    print("Save page successful:",saving_url)
    return True

if __name__ == "__main__":
    if save_page():
        print("success")
    else:
        print("failed")
