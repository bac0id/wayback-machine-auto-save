# wayback-machine-auto-save

A worker to save web pages on list to the Internet Archive's [Wayback Machine](https://web.archive.org/) (WM). 

## Limitation

WM seems to allow about **240 successful requests per day per client**, whether the user is logged in or not. This counter resets at 00:00 UTC. 

## Quick Start

### File of URLs

Prepare a file containing a list of urls to save. Both `txt` and `json` are accepted. 

*   TXT format

    Script loads one line as one url. Example: 
        
    ```
    https://www.gnu.org/fun/
    https://www.gnu.org/fun/jokes/10-kinds-of-people.html
    ```

*   JSON format

    Script loads all `url` attr value from JSON. Example: 

    ```
    [
    {"url": "https://www.gnu.org/fun/"},
    {"url": "https://www.gnu.org/fun/jokes/10-kinds-of-people.html"}
    ]
    ```

### Save to Wayback Machine

Save urls in `urls.txt` to WM. Command: 

```
python main.py urls.txt
```

Example output:

```
cookies: None
proxies: None
WaybackMachineAPI inited.
urls: ['https://www.gnu.org/fun/', 'https://www.gnu.org/fun/jokes/10-kinds-of-people.html']

Http post: https://web.archive.org/save/https://www.gnu.org/fun/
status_code: 200
WM accept saving https://www.gnu.org/fun/, job_id: spn2-51ef937fdcccbcf485e2d092417ee320a2043b52
Save page successful: https://www.gnu.org/fun/, job_id: spn2-51ef937fdcccbcf485e2d092417ee320a2043b52

Http post: https://web.archive.org/save/https://www.gnu.org/fun/jokes/10-kinds-of-people.html
status_code: 200
WM accept saving https://www.gnu.org/fun/jokes/10-kinds-of-people.html, job_id: spn2-60a192c5877dd50c7eb416a0565cfc345e6003c0
Save page successful: https://www.gnu.org/fun/jokes/10-kinds-of-people.html, job_id: spn2-60a192c5877dd50c7eb416a0565cfc345e6003c0
```

### Optional Arguments

#### Cookies

Simply provide the value of the `logged-in-sig` of cookies. The length of this value is about 300. 

Argument: `-c COOKIES`. 

Example: `-c "123456 XXXXXXXXXX"`

#### Proxy

Set proxy for http and https. 

Argument: `-p PROXY`

Example: `-p http://127.0.0.1:8888`

#### Example of Save with Cookies And Proxy

```
python main.py urls.txt -p http://127.0.0.1:8888 -c "123456 XXXXXXXXXX"
```
