import config
import logging
from selenium.webdriver.support.ui import WebDriverWait

class HudlBasePage(object):
    """Base class used to model all the pages used in the tests
    """

    def __init__(self, driver, wait= None, defaultWaitTime = 5):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, defaultWaitTime)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)
        return

    def isLoaded(self):
        """Helper method used to return whether the page is loaded by checking all required elements are loaded
        """
        if(self(self.driver)):
            return True
        return False

    def __call__(self, driver):
        """Makes the page useable as an expected_condition in WebDriverWait.until
        """
        return True
    
    @property
    def Title(self):
        """Title of the html page.
        """
        return ""