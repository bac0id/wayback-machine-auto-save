import unittest

from save_page_options import SavePageOptions

class TestSavePageOptions(unittest.TestCase):

    def test_default_options(self):
        options = SavePageOptions()
        data = options.to_wayback_machine_http_post_data_dict("http://example.com")
        self.assertEqual(data["url"], "http://example.com")
        self.assertEqual(data["capture_outlinks"], "0")
        self.assertEqual(data["capture_all"], "on")
        self.assertEqual(data["capture_screenshot"], "off")
        self.assertEqual(data["wm-save-mywebarchive"], "off")
        self.assertEqual(data["email_result"], "off")
        self.assertEqual(data["wacz"], "off")

    def test_custom_options(self):
        options = SavePageOptions(capture_outlinks=True, capture_all=False, capture_screenshot=True, wm_save_mywebarchive=True, email_result=True, wacz=True)
        data = options.to_wayback_machine_http_post_data_dict("https://www.example.net")
        self.assertEqual(data["url"], "https://www.example.net")
        self.assertEqual(data["capture_outlinks"], "1")
        self.assertEqual(data["capture_all"], "off")
        self.assertEqual(data["capture_screenshot"], "on")
        self.assertEqual(data["wm-save-mywebarchive"], "on")
        self.assertEqual(data["email_result"], "on")
        self.assertEqual(data["wacz"], "on")

    def test_none_saving_url(self):
        options = SavePageOptions()
        with self.assertRaises(ValueError) as context:
             options.to_wayback_machine_http_post_data_dict(None)
        self.assertEqual(str(context.exception), "Must have saving_url.")

    def test_empty_saving_url(self):
        options = SavePageOptions()
        with self.assertRaises(ValueError) as context:
             options.to_wayback_machine_http_post_data_dict("")
        self.assertEqual(str(context.exception), "Must have saving_url.")

    def test_whitespace_saving_url(self):
        options = SavePageOptions()
        with self.assertRaises(ValueError) as context:
             options.to_wayback_machine_http_post_data_dict("   ")
        self.assertEqual(str(context.exception), "Must have saving_url.")
    
    def test_saving_url_with_leading_and_trailing_whitespace(self):
        options = SavePageOptions()
        data = options.to_wayback_machine_http_post_data_dict("  http://example.com  ")
        self.assertEqual(data["url"], "http://example.com")

if __name__ == '__main__':
    unittest.main()
