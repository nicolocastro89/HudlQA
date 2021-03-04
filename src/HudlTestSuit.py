import sys
sys.path.append('.')
import unittest
from TestCases.HudlLogin import HudlLoginTestCase, HudlMobileLoginTestCase



def suite():
    suite = unittest.TestSuite()
    suite.addTest(HudlLoginTestCase('test_successful_login'))
    suite.addTest(HudlLoginTestCase('test_successful_logout_on_cookie_deletion'))
    suite.addTest(HudlLoginTestCase('test_successful_login_restart_with_remember_me'))
    suite.addTest(HudlLoginTestCase('test_unsuccessful_login'))
    suite.addTest(HudlLoginTestCase('test_multiple_unsuccessful_login'))
    suite.addTest(HudlLoginTestCase('test_forgot_password_with_username'))
    suite.addTest(HudlLoginTestCase('test_forgot_password_without_username'))

    #Mobile version
    suite.addTest(HudlMobileLoginTestCase('test_successful_login'))
    suite.addTest(HudlMobileLoginTestCase('test_successful_logout_on_cookie_deletion'))
    suite.addTest(HudlMobileLoginTestCase('test_successful_login_restart_with_remember_me'))
    suite.addTest(HudlMobileLoginTestCase('test_unsuccessful_login'))
    suite.addTest(HudlMobileLoginTestCase('test_multiple_unsuccessful_login'))
    suite.addTest(HudlMobileLoginTestCase('test_forgot_password_with_username'))
    suite.addTest(HudlMobileLoginTestCase('test_forgot_password_without_username'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
