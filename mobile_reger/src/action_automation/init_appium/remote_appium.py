
import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.touch_action import TouchAction

options = UiAutomator2Options()

capabilities: dict = {
    "platformName": "Android",
    "appium:automationName": "uiautomator2",
    "appium:deviceName": "Android",
    "appium:language": "en",
    "appium:locale": "US",
    "appium:app": "C:\\Users\\King\\PycharmProjects\\tg_registration\\mobile_reger\\src\\apk\\telegram-x.apk",
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardwareKeyboard": True
    }


appium_server_url = 'http://localhost:4723'


class ServerRemote(unittest.TestCase):
    def setUp(self) -> None:
        # add our capabilities in options
        for key, value in capabilities.items():
            options.set_capability(key, value)

        self.DRIVER = webdriver.Remote(appium_server_url, options=options)
        self.actions = TouchAction(self.DRIVER)

    def tearDown(self) -> None:
        if self.DRIVER:
            self.DRIVER.quit()


if __name__ == '__main__':
    unittest.main()
