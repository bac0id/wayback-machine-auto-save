
from threading import Thread
import concurrent.futures
from collections import deque

from app_args_loader import *
from urls_list_loader import load_urls_from_file
from save_page_options import SavePageOptions
from wayback_machine_api import WaybackMachineAPI

def start_saving_by_threading(wayback_machine_api, urls):
    number_of_urls = len(urls)

    is_save_successful = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        threads = [executor.submit(wayback_machine_api.save_page,url) for url in urls]
        for thread in concurrent.futures.as_completed(threads):
            is_save_successful.append(thread.result())

def start_saving_by_queueing(wayback_machine_api, urls):
    queue = deque(urls)
    while len(queue) > 0:
        url = queue.popleft()
        is_save_successful = wayback_machine_api.save_page(url)
        if not is_save_successful:
            continue
            queue.append(url)

def main():
    urls_list_filename, cookies, proxies = load_app_args()

    #cookies = load_cookies()
    # cookies = None
    print(f"cookies: {cookies}")

    # proxies = load_proxies()
    print(f"proxies: {proxies}")

    api = WaybackMachineAPI(cookies=cookies, proxies=proxies)
    print("WaybackMachineAPI inited.")
    
    urls = load_urls_from_file(urls_list_filename)
    print("urls:", urls)
    #start_saving_by_threading(api, urls)
    start_saving_by_queueing(api, urls)

if __name__=="__main__":
    main()
