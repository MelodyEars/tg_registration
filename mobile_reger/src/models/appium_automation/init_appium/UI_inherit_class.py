from loguru import logger

from appium import webdriver

from mobile_reger.src.models.appium_automation.init_appium.actions_appium import AppiumActions


class UIBaseAct(AppiumActions):

    def _popups_close_app(self, driver: webdriver) -> None:
        """ When you attend in first time VM. You will get popups for close app UI or ets"""
        xpath_ErrorUI = '//android.widget.Button[@resource-id="android:id/aerr_close"]'

        if self._elem_exists(value=xpath_ErrorUI, wait=1):
            logger.info('Popups Exists')
            xpath_btn_wait = '//android.widget.Button[@resource-id="android:id/aerr_wait"]'
            self._click_element(value=xpath_btn_wait, intercepted_click=True)
            self.wait_loading(driver=driver)

        else:
            logger.info('Alles ist gut!')

    def wait_loading(self, driver: webdriver) -> None:
        """ Wait loading elements and then check if exists popups """
        xpath_frame_body = "//android.widget.FrameLayout"  # here, I wanted to get analog for body in browser
        if self._elem_exists(value=xpath_frame_body, wait=120):
            logger.info('Elements uploaded')
            self._popups_close_app(driver=driver)

        else:
            raise Exception(f"Not loading {xpath_frame_body} through 120s")
