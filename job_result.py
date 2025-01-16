class JobResult:
    def __init__(self, job_id=None, status=None, timestamp=None, outlinks=None, counters=None, duration_sec=None, http_status=None, original_url=None, resources=None, screenshot=None):
        self.job_id = job_id
        self.status = status
        self.timestamp = timestamp
        self.outlinks = outlinks if outlinks is not None else []  # Initialize outlinks as an empty list if not provided
        self.counters = counters
        self.duration_sec = duration_sec
        self.http_status = http_status
        self.original_url = original_url
        self.resources = resources if resources is not None else []  # Initialize resources as an empty list if not provided
        self.screenshot = screenshot

    def __str__(self):
        # Improved output formatting for readability
        return f"JobResult {{\n  job_id: '{self.job_id}'\n  status: '{self.status}'\n  timestamp: '{self.timestamp}'\n  outlinks: {self.outlinks[:5]}...\n  counters: {self.counters}\n  duration_sec: {self.duration_sec}\n  http_status: {self.http_status}\n  original_url: '{self.original_url}'\n  resources: {self.resources[:5]}...\n  screenshot: '{self.screenshot}'\n}}"
