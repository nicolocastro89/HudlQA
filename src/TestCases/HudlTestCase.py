import logging
import config
import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class HudlTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(config.driver_path)
        self.wait = WebDriverWait(self.driver, config.default_wait_time)

    def assertExpectedCondition(self, expected_condition, error_message):
        try:
            self.wait.until(expected_condition)
        except TimeoutException:
            self.fail(error_message)
    def assertPageLoaded(self, page, error_message=None):
        """Helper method to assert the given page has been loaded
        """
        logging.debug(f'Asserting page {page.Title} is loaded')
        try:
            self.wait.until(page)
        except TimeoutException:
            self.fail(error_message)
        except:
            self.fail(error_message)
