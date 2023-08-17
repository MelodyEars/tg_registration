from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from loguru import logger

from mobile_reger.src.models.action_automation.init_appium.app_capabilities import TELEGRAM_capabilities
from mobile_reger.src.models.action_automation.init_appium.param_virtual_machine import APPIUM_HOST, APPIUM_PORT


class ServerRemote:
    def __enter__(self):
        # add our capabilities in options
        tg_options = UiAutomator2Options().load_capabilities(TELEGRAM_capabilities)
        self.TG_DRIVER = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=tg_options)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            folder = Path('mistakes')
            folder.mkdir(exist_ok=True)

            if self.TG_DRIVER:
                self.TG_DRIVER.get_screenshot_as_file(folder / 'mistake_TG.png')
            else:
                logger.error('No active TG Driver')

        if self.TG_DRIVER:
            self.TG_DRIVER.quit()
