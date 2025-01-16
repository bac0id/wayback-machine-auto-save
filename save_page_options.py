class SavePageOptions:
    def __init__(self, capture_outlinks=False, capture_all=True, capture_screenshot=False, wm_save_mywebarchive=False, email_result=False, wacz=False):
        self.capture_outlinks = capture_outlinks
        self.capture_all = capture_all
        self.capture_screenshot = capture_screenshot
        self.wm_save_mywebarchive = wm_save_mywebarchive
        self.email_result = email_result
        self.wacz = wacz

    # Argument `saving_url` is required in data in http post .
    def to_wayback_machine_http_post_data_dict(self, saving_url):
        if saving_url is None:
            raise ValueError("Must have saving_url.")
        saving_url = saving_url.strip()
        if len(saving_url) == 0:
            raise ValueError("Must have saving_url.")

        options = {
            "url": saving_url,
            "capture_outlinks": "1" if self.capture_outlinks else "0",
            "capture_all": "on" if self.capture_all else "off",
            "capture_screenshot": "on" if self.capture_screenshot else "off",
            "wm-save-mywebarchive": "on" if self.wm_save_mywebarchive else "off",
            "email_result": "on" if self.email_result else "off",
            "wacz": "on" if self.wacz else "off",
        }
        return options
