import logging
import config
import selenium
from selenium.common.exceptions import ElementNotInteractableException

class keys_are_sent:
    """Custom expected condition to be used with Selenium's WebDriverWait. Ensures that keys are sent to the
    element avoiding errors when the page is not loaded fast enough
    """
    def __init__(self, element, keys_to_send):
        self.element = element
        self.keys_to_send = keys_to_send
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)

    def __call__(self, driver):
        self.logger.info(f'Sending {self.keys_to_send} to element')
        try:
            self.element.send_keys(self.keys_to_send)
            if self.element.get_attribute('value') == self.keys_to_send:
                self.logger.info('Keys sent successfuly')
                return True
            else:
                self.logger.debug('not all keys succesfully sent')
                self.element.clear()
                return False
        except ElementNotInteractableException:
            self.logger.error('Failed to send keys, element not interactable')
            return False
        except:
            self.logger.error('Failed to send keys')
            self.element.clear()
            return False

class value_in_element_is:
    """Custom expected condition to be used with Selenium's WebDriverWait. Ensures that the value of the provided element is 
    equal to the provided value
    """
    def __init__(self, element, expected_value):
        self.element = element
        self.expected_value = expected_value
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)

    def __call__(self, driver):
        self.logger.info(f'Asserting value of element is {self.expected_value}')
        try:
            if self.element.get_attribute('value') == self.expected_value:
                return self.element  
            else:
                self.logger.error(f'Value of element was {self.element.get_attribute("value")}')
                return False
        except:
            
            return False

class attribute_of_element_is:
    """Custom expected condition to be used with Selenium's WebDriverWait. Ensures that the value of the provided element is 
    equal to the provided value
    """
    def __init__(self, element, attribute_name,expected_value):
        self.element = element
        self.attribute_name = attribute_name
        self.expected_value = expected_value
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)

    def __call__(self, driver):
        self.logger.info(f'Asserting {self.attribute_name} of element is {self.expected_value}')
        try:
            return self.element if  self.element.get_attribute(self.attribute_name) == self.expected_value else False
        except:
            self.logger.error(f'{self.attribute_name} of element is {self.expected_value}')
            return False

class element_enabled_state_is:
    """Custom expected condition to be used with Selenium's WebDriverWait. Ensures that the enabled state of the provided element is 
    equal to the provided value
    """
    def __init__(self, element, is_enabled):
        self.element = element
        self.is_enabled = is_enabled
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.loggingLevel)

    def __call__(self, driver):
        self.logger.debug(f'Asserting element is { "" if self.is_enabled else "not"} enabled')
        try:
            if self.element.is_enabled()==self.is_enabled:
                return self.element  
            else:
                self.logger.debug(f'Element is { "" if self.element.is_enabled() else "not"} enabled')
                return False
        except:
            self.logger.debug(f'Element is { "" if self.element.is_enabled() else "not"} enabled')
            return False