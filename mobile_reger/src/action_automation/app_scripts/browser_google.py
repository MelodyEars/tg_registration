from appium.webdriver import webdriver
from loguru import logger

from mobile_reger.src.action_automation.init_appium.UI_inherit_class import UIBaseAct


class BrowserGetInfoAccount(UIBaseAct):

    # ____________________________________________________________________________ Support methods
    def __wait_loading(self) -> None:
        xpath_body = "//body"
        if self._elem_exists(driver=self.BROWSER_DRIVER, value=xpath_body, wait=120):
            logger.info('Elements uploaded')

            self._popups_close_app(driver=self.BROWSER_DRIVER)

    def _btn_sign_in(self):
        xpath_btn_sign_in = '//form[@id="my_login_form"]/div[4]/button'
        self._click_element(driver=self.BROWSER_DRIVER, value=xpath_btn_sign_in)

        self.__wait_loading()

    # ___________________________________________________________________________ base methods
    def run_browser(self):
        self._switch_to_CHROMIUM_context()
        self._active_app_BROWSER()
        self.__wait_loading()

        self.BROWSER_DRIVER.get('https://my.telegram.org/')

    def enter_number_phone(self, number_phone):
        xpath_field_phone_number = '//input[@id="my_login_phone"]'
        message = "+" + number_phone + "\n"
        self._send_text(driver=self.BROWSER_DRIVER, value=xpath_field_phone_number, message=message)

        self.__wait_loading()

    def enter_password(self, confirmation_code):
        self._switch_to_CHROMIUM_context()

        xpath_confirm_code = '//input[@id="my_login_password"]'
        message = confirmation_code
        self._send_text(driver=self.BROWSER_DRIVER, value=xpath_confirm_code, message=message)

        self._btn_sign_in()

    def nav_by_your_telegram_core(self):
        xpath_btn_api_development = '//a[@href="/apps"]'
        if self._elem_exists(driver=self.BROWSER_DRIVER, value=xpath_btn_api_development, wait=1):
            self._click_element(driver=self.BROWSER_DRIVER, value=xpath_btn_api_development)
        else:
            logger.error("Can't find button")
            input("this new way")

        self.__wait_loading()

    def collection_API_data(self) -> tuple[str, str]:
        """
        Problem on WEBVIEW the data encryption.

         This solve for get API data from https://my.telegram.org/
          the solution is that switch context to "NATIVE_APP" and get API data
           via xpath for "NATIVE_APP"
          """

        xpath_api_id = '//android.view.View[@resource-id="app_edit_form"]/android.view.View[2]/android.widget.TextView'
        xpath_api_hash = '//android.view.View[@resource-id="app_edit_form"]/android.view.View[5]/android.widget.TextView'

        self._switch_BROWSER_to_NATIVE_APP_context()
        api_id = self._elem_exists(driver=self.BROWSER_DRIVER, value=xpath_api_id, return_xpath=True).get_attribute("@text")
        api_hash = self._elem_exists(driver=self.BROWSER_DRIVER, value=xpath_api_hash, return_xpath=True).get_attribute("@text")

        self._switch_to_CHROMIUM_context()

        return api_id, api_hash
