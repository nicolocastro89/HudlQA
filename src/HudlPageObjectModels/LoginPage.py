import logging
import config
from HudlPageObjectModels.HudlBasePage import HudlBasePage
from HudlPageObjectModels.HomePage import HomePage
from Common.CustomExpectedConditions import keys_are_sent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class LoginPage(HudlBasePage):
    """Model of the pages used to login in Hudl's personal page
    """

    # List of stirngs used to identify important elements in the page
    _login_form_xpath = ".//form[contains(@class,'login-container')]"
    _reset_form_xpath = ".//form[contains(@class,'reset-container')]"
    _username_input_id = 'email'
    _password_input_id = 'password'
    _remember_me_id = 'remember-me'
    _remember_me_xpath = ".//label[@for='remember-me']"
    _logIn_button_id = 'logIn'
    _logIn_error_class = 'fade-in-expand'
    _logIn_error_visible_class = 'login-error'
    _reset_button_id = 'resetBtn'
    _forgot_email_id = 'forgot-email'
    _forgot_password_link = 'forgot-password-link'

    def __init__(self, driver, wait = None, defaultWaitTime = 5):
        HudlBasePage.__init__(self,driver, wait, defaultWaitTime)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)
        return

    def login(self, username, password, remember_me = False):
        """Login using the provided username and password. If remember_me is se to true will flas the Remember me checkbox.
        Returns an instance of the HomePage class
        """
        logging.debug(f'Starting to log in as {username}')
        self.insertUsername(username)

        self.insertPassword(password)

        if(remember_me):
            logging.debug('Remember me functionality enabled')
            self.remember_me_label.click()
            logging.debug(f'Remember me checked:{self.remember_me_checkbox.is_selected()}')

        self.login_button.click()
        logging.debug('Logged in and returning the home page')
        return HomePage(self.driver, self.wait)

    def insertUsername(self, username):
        self.wait.until(keys_are_sent(self.username_input, username))

    def insertPassword(self, password):
        self.wait.until(keys_are_sent(self.password_input, password))

    def insertForgotEmail(self, email):
        self.wait.until(keys_are_sent(self.forgot_email_input, email))

    def loginErrorMessageVisible(self):
        """Checks whether the error div is visible in the page
        """
        self.wait.until(EC.presence_of_element_located(self.error_div_BY))
        loginErrorDivClasses = self.error_div.get_attribute('class').split(' ')
        return  self._logIn_error_visible_class in loginErrorDivClasses

    def __call__(self, driver):
        """Checks if the username, password and login button are present in the page to assert that the page is loaded
        """
        logging.info('Checking all required elements on Login Page are loaded')
        try:
            logging.debug('Checking presence of username input')
            self.username_input
            logging.debug('Username input found')
        except NoSuchElementException:
            logging.error('Username input not found')
            return False
        try:
            logging.debug('Checking presence of password input')
            self.password_input
            logging.debug('Password input found')
        except NoSuchElementException:
            logging.error('Password input not found')
            return False

        try:
            logging.debug('Checking presence of login button')
            self.login_button
            logging.debug('Login button found')
        except NoSuchElementException:
            logging.error('Login button not found')
            return False

        return self

    @property
    def Title(self):
        return "Log In - Hudl"

    @property
    def login_form(self):
        return self.driver.find_element_by_xpath('_login_form_xpath')

    @property
    def reset_form(self):
        return self.driver.find_element_by_xpath('_login_form_xpath')

    @property
    def username_input(self):
        return self.driver.find_element_by_id(self._username_input_id)
    @property
    def password_input(self):
        return self.driver.find_element_by_id(self._password_input_id)
    @property
    def remember_me_checkbox(self):
        return self.driver.find_element_by_id(self._remember_me_id)

    @property
    def remember_me_label(self):
        return self.driver.find_element_by_xpath(self._remember_me_xpath)

    @property
    def error_div_BY(self):
        return (By.CLASS_NAME, self._logIn_error_class)
    
    @property
    def error_div(self):
        return self.driver.find_element_by_class_name(self._logIn_error_class)
    
    @property
    def reset_password_link(self):
        return self.error_div.find_element_by_tag_name('a')

    @property
    def reset_password_button(self):
        return self.driver.find_element_by_id(self._reset_button_id)

    @property
    def forgot_email_input(self):
        return self.driver.find_element_by_id(self._forgot_email_id)

    @property
    def forgot_password_link(self):
        return self.driver.find_element_by_id(self._forgot_password_link)

    @property
    def login_button(self):
        return self.driver.find_element_by_id(self._logIn_button_id)
