from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from loguru import logger

from mobile_reger.src.action_automation.init_appium.app_capabilities import BROWSER_capabilities, TELEGRAM_capabilities
from mobile_reger.src.action_automation.init_appium.param_virtual_machine import APPIUM_HOST, APPIUM_PORT


class ServerRemote:
    def __enter__(self):
        # add our capabilities in options
        browser_options = UiAutomator2Options().load_capabilities(BROWSER_capabilities)
        tg_options = UiAutomator2Options().load_capabilities(TELEGRAM_capabilities)

        self.BROWSER_DRIVER = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=browser_options)

        self.TG_DRIVER = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=tg_options)
        # self.TG_actions = TouchAction(self.TG_DRIVER)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            folder = Path('mistakes')
            folder.mkdir(exist_ok=True)

            if self.TG_DRIVER:
                self.TG_DRIVER.get_screenshot_as_file(folder / 'mistake_TG.png')
            else:
                logger.error('No active TG Driver')

            if self.BROWSER_DRIVER:
                self.BROWSER_DRIVER.get_screenshot_as_file(folder / 'mistake_BROWSER.png')
            else:
                logger.error('No active Browser Driver')

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

    def _switch_to_NATIVE_APP_context(self) -> webdriver:
        # self.TG_DRIVER.activate_app('org.thunderdog.challegram')
        self.TG_DRIVER.switch_to.context('NATIVE_APP')

    def _switch_to_CHROMIUM_context(self) -> webdriver:
        # self.BROWSER_DRIVER.activate_app('com.android.chrome')
        self.BROWSER_DRIVER.switch_to.context('CHROMIUM')

    def _switch_BROWSER_to_NATIVE_APP_context(self) -> webdriver:
        """This bone need for method collection_API_data() in browser_google.py"""
        self.BROWSER_DRIVER.switch_to.context('NATIVE_APP')
        self._active_app_BROWSER()

    def _active_app_TELEGRAM(self) -> webdriver:
        self.TG_DRIVER.activate_app('org.telegram.messenger')

    def _active_app_BROWSER(self) -> webdriver:
        self.BROWSER_DRIVER.activate_app('com.android.chrome')



