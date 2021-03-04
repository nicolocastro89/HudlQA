import config
import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .HudlTestCase import HudlTestCase
from HudlPageObjectModels.LoginPage import LoginPage
from HudlPageObjectModels.MainPage import MainPage
from HudlPageObjectModels.HomePage import HomePage
from Common.CustomExpectedConditions import keys_are_sent, value_in_element_is,element_enabled_state_is

class HudlLoginTestCase(HudlTestCase):
    """Test cases to test the functionalities offered by the login page """

    def setUp(self):
        self.username = config.login_params['username']
        self.password = config.login_params['password']
        self.options = webdriver.ChromeOptions()
        self.options.headless = config.headless
        self.driver = webdriver.Chrome(config.driver_path, chrome_options=self.options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, config.default_wait_time)

    def tearDown(self):
        self.driver.close()

    def test_successful_login(self):
        """Test logging in to hudl from the main page to the home page using the correct credentials
        """
        
        driver = self.driver
        
        driver.get("http://www.hudl.com")
        mainPage = MainPage(driver, self.wait)
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")

        
        loginForm = mainPage.navigateToLogin()
        self.assertPageLoaded(loginForm, 'Login page not loaded after clicking on the login button in the Main Page')


        homePage = loginForm.login(self.username, self.password)
        self.assertPageLoaded(homePage, 'Personal Home Page not loaded after attempting login')

    def test_successful_logout_on_cookie_deletion(self):
        """Test login removing cookies without remeember me enabled will cause the user to have to login again when 
        trying to login back again.
        """
        driver = self.driver
        
        driver.get("http://www.hudl.com")
        mainPage = MainPage(driver)
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")
        
        loginForm = mainPage.navigateToLogin()
        self.assertPageLoaded(loginForm, 'Login page not loaded after clicking on the login button in the Main Page')

        homePage = loginForm.login(self.username, self.password)
        self.assertPageLoaded(homePage, 'Personal Home Page not loaded after attempting login')

        cookies = self.driver.get_cookies()

        for cookie in cookies:
            if ('expiry' not in cookie.keys()):
                self.driver.delete_cookie(cookie['name'])

        driver.get("http://www.hudl.com")
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")

    def test_successful_login_restart_with_remember_me(self):
        """Test that loggin into Hudle checking the Remember Me flag will auto-login next time the hom peage
        is navigate to 
        """
        driver = self.driver
        
        driver.get("http://www.hudl.com")
        mainPage = MainPage(driver)
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")

        
        loginForm = mainPage.navigateToLogin()
        self.assertPageLoaded(loginForm, 'Login page not loaded after clicking on the login button in the Main Page')

        homePage = loginForm.login(self.username, self.password, remember_me = True)
        self.assertPageLoaded(homePage, 'Personal Home Page not loaded after attempting login')

        cookies = self.driver.get_cookies()

        for cookie in cookies:
            if ('expiry' not in cookie.keys()):
                self.driver.delete_cookie(cookie['name'])
        
        self.driver.get("http://www.hudl.com")
        self.assertPageLoaded(homePage, 'Navigating to the main page after selecting the Remember Be option should automatically bring you to the personal page')

    def test_unsuccessful_login(self):
        """Test that logging in using incorrect credentials the error div is displayed
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        self.assertIn("Log In - Hudl", driver.title)
        loginForm = LoginPage(driver)
        homePage = loginForm.login(self.username, self.password[:-2])

        self.assertRaises(TimeoutException, self.wait.until,homePage)
        
        self.assertTrue(loginForm.loginErrorMessageVisible(), "Error div is not visible in login page after inserting incorrect credentials")

    def test_multiple_unsuccessful_login(self):
        """Test that loggin in using incorrect credentials multiple times results in the error message to change and allow
        the user to reset the password.
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")

        loginForm = LoginPage(driver)
        self.assertPageLoaded(loginForm)

        for _ in range(6):
            loginForm.username_input.clear()
            loginForm.password_input.clear()
            homePage = loginForm.login(self.username, self.password[:-2])
            self.assertRaises(TimeoutException, self.wait.until,homePage, "Personal HomePage loaded even if wrong credentials were provided")
            self.assertExpectedCondition(EC.visibility_of_element_located(loginForm.error_div_BY),
            "Error message is not visible even after inserting wrong credentials")
            #self.assertRaises(TimeoutException, loginForm.login, config.login_params['username'], config.login_params['password'][:-2])
            
        
        self.assertExpectedCondition(
            EC.visibility_of_element_located(loginForm.error_div_BY),
            "Error message is not visible even after inserting wrong credentials")
        self.assertIn('reset',loginForm.error_div.text, "After multiple wrong attempts the error message should provide the possibility to reset the password")

        loginForm.reset_password_link.click()

        self.wait.until(EC.visibility_of(loginForm.forgot_email_input))
        self.assertExpectedCondition(
            value_in_element_is(loginForm.forgot_email_input, config.login_params['username']), 
            "E-mail not auto-filled when trying to reset password after wrong attempt")
    
    def test_forgot_password_with_username(self):
        """Test that clicking the "need help" link displays the reset password form, with the inserted username populated
        and the reset button enabled
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        loginForm = LoginPage(driver)
        self.assertPageLoaded(loginForm, 'Login page did not load')

        loginForm.insertUsername(self.username)

        loginForm.forgot_password_link.click()
        
        self.assertExpectedCondition(
            value_in_element_is(loginForm.forgot_email_input, self.username), 
            "E-mail field not populated when trying to reset passoword having previously inserted e-mail")

        self.assertExpectedCondition(
            element_enabled_state_is(loginForm.reset_password_button, True),
            "Reset password button not enabled even if e-mail field is filled out")
        
    def test_forgot_password_without_username(self):
        """Test that clicking the "need help" link displays the reset password form, with the username field empty
        and the reset button disabled
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        loginForm = LoginPage(driver)
        self.assertPageLoaded(loginForm, 'Login page did not load')

        loginForm.forgot_password_link.click()
        
        self.assertExpectedCondition(
            value_in_element_is(loginForm.forgot_email_input, ''),
            "Email field not empty even if the username filed had not been filled out"
        )
        self.assertExpectedCondition(
            element_enabled_state_is(loginForm.reset_password_button, False),
             "Reset password button is enabled even if the email field is empty")

        loginForm.insertForgotEmail(self.username)

        self.assertExpectedCondition(
            element_enabled_state_is(loginForm.reset_password_button, True),
            "Reset password button not enabled even after entering the email in the input")

    

class HudlMobileLoginTestCase(HudlTestCase):
    """Test cases to test the functionalities offered by the login page """

    def setUp(self):
        self.username = config.login_params['username']
        self.password = config.login_params['password']

        mobile_emulation = {
            "deviceMetrics": { "width": config.mobile_width, "height": config.mobile_height, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }
        options = webdriver.ChromeOptions()
        options.headless = config.headless
        #options.add_argument(f"window-size={config.mobile_size}")
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(executable_path=config.driver_path,options=options)

        self.wait = WebDriverWait(self.driver, 2)

    def tearDown(self):
        self.driver.close()

    def test_successful_login(self):
        """Test logging in to hudl from the main page to the home page using the correct credentials
        """
        mobile_emulation = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }

        
        driver = self.driver
        options = driver.create_options()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        driver.get("http://www.hudl.com")
        mainPage = MainPage(driver)
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")

        
        loginForm = mainPage.navigateToLogin()
        self.assertPageLoaded(loginForm, 'Login page not loaded after clicking on the login button in the Main Page')


        homePage = loginForm.login(self.username, self.password)
        self.assertPageLoaded(homePage, 'Personal Home Page not loaded after attempting login')

    def test_successful_logout_on_cookie_deletion(self):
        """Test logging in to hudl from the main page to the home page using the correct credentials
        """
        driver = self.driver
        
        driver.get("http://www.hudl.com")
        mainPage = MainPage(driver)
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")
        
        loginForm = mainPage.navigateToLogin()
        self.assertPageLoaded(loginForm, 'Login page not loaded after clicking on the login button in the Main Page')

        homePage = loginForm.login(self.username, self.password)
        self.assertPageLoaded(homePage, 'Personal Home Page not loaded after attempting login')

        cookies = self.driver.get_cookies()

        for cookie in cookies:
            if ('expiry' not in cookie.keys()):
                self.driver.delete_cookie(cookie['name'])

        driver.get("http://www.hudl.com")
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")

    def test_successful_login_restart_with_remember_me(self):
        """Test logging in to hudl from the main page to the home page using the correct credentials
        """
        driver = self.driver
        
        driver.get("http://www.hudl.com")
        mainPage = MainPage(driver)
        self.assertPageLoaded(mainPage, "Hudl's main page failed to load")

        
        loginForm = mainPage.navigateToLogin()
        self.assertPageLoaded(loginForm, 'Login page not loaded after clicking on the login button in the Main Page')

        homePage = loginForm.login(self.username, self.password, remember_me = True)
        self.assertPageLoaded(homePage, 'Personal Home Page not loaded after attempting login')

        cookies = self.driver.get_cookies()

        for cookie in cookies:
            if ('expiry' not in cookie.keys()):
                self.driver.delete_cookie(cookie['name'])
        
        self.driver.get("http://www.hudl.com")
        self.assertPageLoaded(homePage, 'Navigating to the main page after selecting the Remember Be option should automatically bring you to the personal page')

    def test_unsuccessful_login(self):
        """Test that logging in using incorrect credentials the error div is displayed
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        self.assertIn("Log In - Hudl", driver.title)
        loginForm = LoginPage(driver)
        homePage = loginForm.login(self.username, self.password[:-2])
        self.assertRaises(TimeoutException, self.wait.until,homePage)
        
        self.assertTrue(loginForm.loginErrorMessageVisible(), "Error div is not visible in login page after inserting incorrect credentials")

    def test_multiple_unsuccessful_login(self):
        """Test that loggin in using incorrect credentials multiple times results in the error message to change and allow
        the user to reset the password.
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        self.assertIn("Log In - Hudl", driver.title)
        loginForm = LoginPage(driver)

        for _ in range(6):
            loginForm.username_input.clear()
            loginForm.password_input.clear()
            homePage = loginForm.login(self.username, self.password[:-2])
            self.assertRaises(TimeoutException, self.wait.until,homePage, "Personal HomePage loaded even if wrong credentials were provided")
            self.assertTrue(loginForm.loginErrorMessageVisible(), "Error message is not visible even after inserting wrong credentials")
            #self.assertRaises(TimeoutException, loginForm.login, config.login_params['username'], config.login_params['password'][:-2])
            
        
        self.assertExpectedCondition(
            EC.visibility_of_element_located(loginForm.error_div_BY),
            "Error message is not visible even after inserting wrong credentials")
        self.assertIn('reset',loginForm.error_div.text, "After multiple wrong attempts the error message should provide the possibility to reset the password")

        loginForm.reset_password_link.click()
        self.wait.until(EC.visibility_of(loginForm.forgot_email_input))
        self.assertExpectedCondition(
            value_in_element_is(loginForm.forgot_email_input, config.login_params['username']), 
            "E-mail not auto-filled when trying to reset password after wrong attempt")
        
    def test_forgot_password_with_username(self):
        """Test that clicking the "need help" link displays the reset password form, with the inserted username populated
        and the reset button enabled
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        loginForm = LoginPage(driver)
        self.wait.until(loginForm)

        loginForm.insertUsername(self.username)

        loginForm.forgot_password_link.click()
        
        self.assertExpectedCondition(
            value_in_element_is(loginForm.forgot_email_input, self.username), 
            "E-mail field not populated when trying to reset passoword having previously inserted e-mail")

        self.assertExpectedCondition(
            element_enabled_state_is(loginForm.reset_password_button, True),
            "Reset password button not enabled even if e-mail field is filled out")
        
    def test_forgot_password_without_username(self):
        """Test that clicking the "need help" link displays the reset password form, with the username field empty
        and the reset button disenabled
        """
        driver = self.driver
        driver.get("http://www.hudl.com/login")
        loginForm = LoginPage(driver)
        self.wait.until(loginForm)

        loginForm.forgot_password_link.click()
        
        self.assertExpectedCondition(
            value_in_element_is(loginForm.forgot_email_input, ''), 
            "Email field not empty even if the username filed had not been filled out")
        self.assertExpectedCondition(
            element_enabled_state_is(loginForm.reset_password_button, False),
             "Reset password button is enabled even if the email field is empty")
        
        loginForm.insertForgotEmail(self.username)

        self.assertExpectedCondition(
            element_enabled_state_is(loginForm.reset_password_button,True),
            "Reset password button not enabled even after entering the email in the input")

