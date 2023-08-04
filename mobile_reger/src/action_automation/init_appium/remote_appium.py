import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.touch_action import TouchAction

from loguru import logger

from mobile_reger.src.action_automation.init_appium.app_capabilities import BROWSER_capabilities, TELEGRAM_capabilities

APPIUM_HOST = '127.0.0.1'
APPIUM_PORT = 4723


class DriverDescriptor:
    def __get__(self, obj, objtype):
        return obj.__get_active_driver()


class ServerRemote(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

        self.DRIVER = DriverDescriptor()

    def setUp(self) -> None:
        # add our capabilities in options
        browser_options = UiAutomator2Options().load_capabilities(BROWSER_capabilities)
        tg_options = UiAutomator2Options().load_capabilities(TELEGRAM_capabilities)

        self.TG_DRIVER = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=tg_options)
        # self.TG_actions = TouchAction(self.TG_DRIVER)

        self.BROWSER_DRIVER = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=browser_options)

    def tearDown(self) -> None:
        if self.TG_DRIVER:
            self.TG_DRIVER.quit()

        if self.BROWSER_DRIVER:
            self.BROWSER_DRIVER.quit()

    def __get_active_driver(self) -> webdriver:
        context = self.TG_DRIVER.current_context
        logger.info(f'All contexts: {self.TG_DRIVER.contexts}')
        logger.info(f'Current context: {context}')

        if context == 'CHROMIUM':
            return self.BROWSER_DRIVER

        elif context == 'NATIVE_APP':
            return self.TG_DRIVER

        raise Exception("Unknown context")

    def __switch_to_NATIVE_APP_context(self) -> webdriver:
        # self.TG_DRIVER.activate_app('org.thunderdog.challegram')
        self.TG_DRIVER.switch_to.context('NATIVE_APP')

    def __switch_to_CHROMIUM_context(self) -> webdriver:
        # self.BROWSER_DRIVER.activate_app('com.android.chrome')
        self.BROWSER_DRIVER.switch_to.context('CHROMIUM')

    def __switch_BROWSER_to_NATIVE_APP_context(self) -> webdriver:
        """This bone need for method collection_API_data() in browser_google.py"""
        self.BROWSER_DRIVER.switch_to.context('NATIVE_APP')

    def __active_app_TELEGRAM(self) -> webdriver:
        self.TG_DRIVER.activate_app('org.telegram.messenger')

    def __active_app_BROWSER(self) -> webdriver:
        self.BROWSER_DRIVER.activate_app('com.android.chrome')

if __name__ == '__main__':
    unittest.main()
