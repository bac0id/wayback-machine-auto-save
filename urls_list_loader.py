import os
import json

def load_urls_from_txt(filename):
    urls_str = load_all_content_from_file(filename)
    urls = urls_str.split()
    return urls
        
def load_urls_from_json(filename):
    json_str = load_all_content_from_file(filename)
    try:
        json_obj = json.loads(json_str)
        urls = [item["url"] for item in json_obj]
        return urls
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON format.")
        return []

def load_urls_from_file(filename):
    extension = os.path.splitext(filename)[1].lower()
    if extension == ".txt":
        return load_urls_from_txt(filename)
    elif extension == ".json":
        return load_urls_from_json(filename)
    else:
        print(f"Error: Unsupported file format for {filename}")
        return []

def load_all_content_from_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Exception: {e}")
    return ""
