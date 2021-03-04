# Automation testing suit for Hudl's Login Page
Simple project to test the basic functionalities for the login page of Hudl's website

## Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Running the Tests](#running-the-tests)

## General Info
All tests start from www.hudl.com and proceed to the login page by clicking on the login button. The current test cases include:
 - Navigation to the login page on a full screen web browser
 - Navigation to the login page when the web browser is reduced (mobile view)
 - Login using correct credentials
 - 'Remember me' functionality
 - Failed login using incorrect credentials
 - 'Reset password' functionality

 ## Technologies
 These testes where written in Python 3.7, and make use of the following packages:
 * logging
 * unittest
 * selenium : 3.141

 For a succcessful run the tests also require: 
 * chromium driver

 ## Setup
 In order to run the test a valid username and password need to be provided in the config.py file by placing them in the loginParams dictionary:
 config.py
 ```python
 login_params = dict(
    username='<username>',
    password='<password>'
)
 ```
 For the correct functioning of the tests the program also requires the correct chromium driver. You can download the driver from [here](https://chromedriver.chromium.org/). Make sure you download the correct driver, matching the version to the version of chrome installed on your computer. Place the driver in an easy to find directory, and specify it in the config.py file using either relative or absolute path. 
 config.py
 ```python
 driver_path = 'chromedriver.exe'

 ```
 If you wish to use a different browser make sure you edit the tests accordingly. This is done by opending the .py files in the TestCases folder, and changing the 
```python
webdriver.ChromeDriver()
```
lines to use the driver of your preferences. Also make sure that you create the options specific to the driver you are going to use, by switching the 
```python
webdriver.ChromeOptions()
```
line with the correct version for your driver.
To accomodate loading times of the web page, most of the interactions/asserts on the page ae given a set amount of time to work before declaring the test failed. The default time set in the config file is 7 seconds, but can be adjusted to adapt to the needs and situation by changing the default_wait_time parameter and providing a different time in seconds
```python
default_wait_time = 7

 ```
By default the tests are run displaying what the test is doing, however it is possible to run the tests in headless mode by setting the headless option to True in the config file. In some cases this actually makes the tests run a bit better, as there is minimum interaction with the graphic rendering.
```python
headeless = True

 ```
Some of the tests try to simulate a mobile environment, to test the reactive rendering of the page. The size of the mobile screen can be set by editing the mobile_height and mobile_width parameters in the config:
```python
mobile_width = 375
mobile_height = 800
```

## Running the Tests
 In order to run the tests open the Terminal/Command Promp, and navigate to the folder containing the HudlTestSuit.py file. then launch the following command:
  ```
  python HudlTestSuit.py
  ```

  The tests will run, openining and closing the browser window autonomously.

