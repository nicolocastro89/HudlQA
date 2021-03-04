import logging
import config
from HudlPageObjectModels.HudlBasePage import HudlBasePage
from HudlPageObjectModels.LoginPage import LoginPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class MainPage(HudlBasePage):
    """Model of the page displayed when navigating to hudl.com without being logged in
    """

    # List of stirngs used to identify important elements in the page
    _login_button_xpath = ".//li/a[contains(@class,'login')]"
    _mobile_login_button_xpath = ".//div[contains(@class,'mobile-nav-only')]/a"
    _navbar_xpath = ".//div[contains(@class,'elite-nav')"
    _mobile_navbar_xpath = ".//div[contains(@class,'mobile-nav-only')]"

    def __init__(self, driver, wait= None, defaultWaitTime = 5):
        HudlBasePage.__init__(self,driver, wait, defaultWaitTime)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)
        return

    def navigateToLogin(self):
        """ Click on the Login button
        """
        self.login_button.click()
        return LoginPage(self.driver, self.wait)

    def __call__(self, driver):
        """Checks whether the login button is loaded (only interesting element on this page
        """
        logging.info('Checking all required elements on Login Page are loaded')
        try:
            logging.debug('Checking that the login button is present')
            self.login_button 
            logging.debug('Login button found')
        except NoSuchElementException:
            logging.error('Login button not found')
            return False
        
        return self

    @property
    def Title(self):
        return "Hudl: We Help Teams and Athletes Win"

    @property 
    def navbar(self):
        return self.driver.find_element_by_xpath(self._navbar_xpath) 

    @property 
    def mobile_navbar(self):
        return self.driver.find_element_by_xpath(self._mobile_navbar_xpath) 

    @property
    def login_button(self):
        """Generic login button viable for desktop and mobile. If mobile navbar is visible then returns the mobile login button
        else returns the standard login button
        """
        if(self.mobile_navbar.is_displayed()):
            return self.mobile_login_button
        return self.driver.find_element_by_xpath(self._login_button_xpath)

    @property
    def mobile_login_button(self):
        return self.driver.find_element_by_xpath(self._mobile_login_button_xpath)