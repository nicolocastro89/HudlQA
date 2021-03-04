import logging
import config
from HudlPageObjectModels.HudlBasePage import HudlBasePage
from HudlPageObjectModels import LoginPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class HomePage(HudlBasePage):
    """Model of the Personal Home page of Hudl
    """


    def __init__(self, driver, wait=None, defaultWaitTime = 5):
        HudlBasePage.__init__(self,driver, defaultWaitTime)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)
        return



    def __call__(self, driver):
        """Checks whether the page is loaded by comparing the current title and current url
        """
        self.logger.info('Checking all required elements on Home Page are loaded')
        self.logger.debug(f'Checking that the title of the page is {self.title}')
        if driver.title != self.title:
            self.logger.error(f'Title of page is in fact {driver.title}')
            return False
        self.logger.debug('Page title is correct')
        self.logger.debug(f'Checking that the url of the page ends in /home')
        if "/home" not in driver.current_url:
            self.logger.error(f'Url of page does nt contain /home: {driver.current_url}')
            return False
        self.logger.debug(f'Url of the page contains /home')
        return self

    @property
    def title(self):
        return "Home - Hudl"

    