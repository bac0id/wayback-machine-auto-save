import argparse
import os

def load_app_args():
    parser = argparse.ArgumentParser(description="Wayback Machine Auto Save")
    parser.add_argument("urls_list_filename", help="Filename of list of URLs to save")
    parser.add_argument("-c", "--cookies", default=None, help="Cookies of Wayback Machine")
    parser.add_argument("-p", "--proxy", default=None, help="Http(s) proxy")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            parser.print_help()
            return None
        else:
            return None

    urls_list_filename = args.urls_list_filename
    cookies = args.cookies
    if cookies is not None:
        cookies = cookies.strip()
        cookies = {
            "logged-in-sig": cookies
        }
    proxy = args.proxy
    if proxy is not None:
        proxy = proxy.strip()
        proxies = {
            "http": proxy,
            "https": proxy,
        }
    else:
        proxies = None

    return urls_list_filename, cookies, proxies

def is_running_in_github_actions():
    """
    Is running in GitHub Actions?
    """
    github_actions = os.environ.get("GITHUB_ACTIONS")
    if github_actions == "true":
        return True
    else:
        return False

def load_cookies(filename="cookies-logged-in-sig.ini"):
    if is_running_in_github_actions():
        return os.environ.get("COOKIES_LOGGED_IN_SIG")
    else:
        try:
            with open(filename, "r") as f:
                content = f.read().strip()

            if len(content) == 0:
                return None

            cookies = {
                "logged-in-sig": content
            }
            return cookies
        except Exception as e:
            print("Exception:", e)
    return None

def load_proxies(filename="proxy.ini"):
    if is_running_in_github_actions():
        return None
    else:
        try:
            with open(filename, "r") as f:
                content = f.read().strip()
            proxies = {
                "http": content,
                "https": content,
            }
            return proxies
        except Exception as e:
            print("Exception:", e)
        return None

def load_urls(filename="saving_urls.ini"):
    if is_running_in_github_actions():
        urls = os.environ.get("SAVING_URLS")
        urls = urls.split()
        return urls
    else:
        try:
            with open(filename, 'r') as f:
                urls = f.read()
            urls = urls.split()
            return urls
        except Exception as e:
            print("Exception:", e)
        return None
        