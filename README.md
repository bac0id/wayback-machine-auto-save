# wayback-machine-auto-save

A worker to save web pages on list to the Internet Archive's [Wayback Machine](https://web.archive.org/). 

## Quick Start

### List of URLs

Prepare a file containing a list of urls. One URL per line in the file. Example as follows: 
    
```
https://www.gnu.org/fun/
https://www.gnu.org/fun/jokes/10-kinds-of-people.html
https://www.gnu.org/fun/jokes/any-key.html
```

### Run with Default Arguments

```
python main.py urls.txt
```

Example output:

```
cookies: None
proxies: None
WaybackMachineAPI inited.
urls: ['https://www.gnu.org/fun/', 'https://www.gnu.org/fun/jokes/10-kinds-of-people.html', 'https://www.gnu.org/fun/jokes/any-key.html']

Http post: https://web.archive.org/save/https://www.gnu.org/fun/
status_code: 200
WM accept saving https://www.gnu.org/fun/, job_id: spn2-51ef937fdcccbcf485e2d092417ee320a2043b52
Save page successful: https://www.gnu.org/fun/, job_id: spn2-51ef937fdcccbcf485e2d092417ee320a2043b52
Http post: https://web.archive.org/save/https://www.gnu.org/fun/jokes/10-kinds-of-people.html
status_code: 200
WM accept saving https://www.gnu.org/fun/jokes/10-kinds-of-people.html, job_id: spn2-60a192c5877dd50c7eb416a0565cfc345e6003c0
Save page successful: https://www.gnu.org/fun/jokes/10-kinds-of-people.html, job_id: spn2-60a192c5877dd50c7eb416a0565cfc345e6003c0
Http post: https://web.archive.org/save/https://www.gnu.org/fun/jokes/any-key.html
status_code: 200
WM accept saving https://www.gnu.org/fun/jokes/any-key.html, job_id: spn2-a1f399f86e33bd76e194e677200eea6ce0759bf9
Save page successful: https://www.gnu.org/fun/jokes/any-key.html, job_id: spn2-a1f399f86e33bd76e194e677200eea6ce0759bf9
```

### Run with Cookies And Proxy

#### About Cookies

Simply provide the value of the `logged-in-sig`. The length of this value is about 300. 

```
python main.py urls.txt -p http://proxy.example.com:8080 -c "123456 XXXXXXXX"
```
