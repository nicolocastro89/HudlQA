#Set the level of logging desired. Can be DEBUG-INFO-WARNING-ERROR-CRITICAL
loggingLevel = "ERROR"

#Credentials used to login to Hudle.com
login_params = dict(
    username='',
    password=''
)

#Path to the driver used to run the tests. 
# Either absolute or relative to where the test suit is launched from
driver_path = 'chromedriver.exe'

#If True will run the tests in headless mode (without showing the opened pages)
headless = True

#default wait time in seconds used when waiting for an element to load 
# before launching an exception
default_wait_time = 7

#Size of the window to trigger mobile render
mobile_width = 375
mobile_height = 800