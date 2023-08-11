import time

import pyperclip
from loguru import logger

from mobile_reger.src.models.action_automation.init_appium.UI_inherit_class import UIBaseAct
from mobile_reger.src.models.exceptions import SendPhoneNumberException, NoCodeSentException
from mobile_reger.src.models.sms_activate.sms_api import _receive_sms


class AutoRegTelegramX(UIBaseAct):
    def __wait_tg_loading(self):
        self.wait_loading(driver=self.TG_DRIVER)

    # ____________________________________________________________________________ Support method
    def __btn_right_arrow(self):
        logger.info('click on the right arrow')

        xpath_btn = '//android.view.View[@resource-id="org.thunderdog.challegram:id/btn_done"]'
        self._click_element(driver=self.TG_DRIVER, value=xpath_btn)

        self.__wait_tg_loading()

    # _____________________________________________________________________________ base method
    # _____________________________________________________________ 1 page
    def startMessaging(self):
        logger.info('prepare click StartMessaging')
        self._switch_to_NATIVE_APP_context()

        self.__wait_tg_loading()

        xpath_btn = '//android.widget.TextView[contains(@resource-id, "org.thunderdog.challegram:id/btn_done")]'
        self._click_element(driver=self.TG_DRIVER, value=xpath_btn)

        logger.info('Executed click StartMessaging')

    # _____________________________________________________________ 2 page
    def enterPhoneNumbers(self, dict_info_PhoneNumber: dict):
        logger.info("Enter number of phone")

        # Send country
        # xpath_country = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_country"]'
        # self._send_text(driver=self.TG_DRIVER, value=xpath_country, message=dict_info_PhoneNumber['country_name'],
        #                 after_send_tap=True)

        # Send Country code
        xpath_code_country = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_code"]'
        self._send_text(driver=self.TG_DRIVER, value=xpath_code_country, message=dict_info_PhoneNumber["code_country"])

        # Send body number of phone
        xpath_body_number = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_phone"]'
        self._send_text(driver=self.TG_DRIVER, value=xpath_body_number, message=dict_info_PhoneNumber["phone_number"])

        logger.info("Successfully sent a number of phone")

        self.__btn_right_arrow()
        time.sleep(2)

        if self._elem_exists(driver=self.TG_DRIVER, value=xpath_body_number, wait=1):
            raise SendPhoneNumberException('Somthing wrong with sending a phone number!')

    # _____________________________________________________________ 3 page
    def sendCodeToTg(self, phone_number: str, activation_id: str, second_try: bool = False):
        logger.info("Enter number of phone")
        self.__wait_tg_loading()

        xpath_field = '//android.widget.EditText'
        code = _receive_sms(phone_number=phone_number, activation_id=activation_id)

        xpath_not_sent_code = '//android.widget.TextView[@resource-id="org.thunderdog.challegram:id/btn_forgotPassword"]'

        if code:
            self._send_text(driver=self.TG_DRIVER, value=xpath_field, message=code)

            # Todo check if this exists recovery account
            logger.info("Successfully sent a number of phone")

            self.__btn_right_arrow()

        else:
            if not second_try:
                self._click_element(driver=self.TG_DRIVER, value=xpath_not_sent_code)
                self.sendCodeToTg(phone_number=phone_number, activation_id=activation_id, second_try=True)
            else:
                raise NoCodeSentException('Telegram did not send the code to the sms')

    # _____________________________________________________________ 4 page
    def create_first_last_name(self, firstname: str, lastname: str = None):
        self.__wait_tg_loading()

        # send firstname
        xpath_first_name = '//android.widget.FrameLayout[@resource-id="org.thunderdog.challegram:id/edit_first_name"]//android.widget.EditText'
        self._send_text(driver=self.TG_DRIVER, value=xpath_first_name, message=firstname)

        if lastname:
            # send lastname
            xpath_last_name = '//android.widget.FrameLayout[@resource-id="org.thunderdog.challegram:id/edit_last_name"]//android.widget.EditText'
            self._send_text(driver=self.TG_DRIVER, value=xpath_last_name, message=lastname)

    # _____________________________________________________________ After Create Account
    def __pop_tg_find_contacts(self):
        xpath_pop_find_contacts = '//android.widget.TextView[contains(@text, "Find Contacts")]'
        if self._elem_exists(driver=self.TG_DRIVER, value=xpath_pop_find_contacts, wait=10):
            xpath_btn_never = '//android.widget.Button[contains(@text, "NEVER")]'
            self._click_element(driver=self.TG_DRIVER, value=xpath_btn_never, intercepted_click=True)
            self.__wait_tg_loading()

    def __pop_terms_of_service(self):
        xpath_title = '//android.widget.TextView[@resource-id="android:id/alertTitle"]'
        if self._elem_exists(driver=self.TG_DRIVER, value=xpath_title, wait=10):
            xpath_btn_ok = '//android.widget.Button[@resource-id="android:id/button1"]'
            self._click_element(driver=self.TG_DRIVER, value=xpath_btn_ok, intercepted_click=True)
            self.__wait_tg_loading()

    def tg_popups_after_create(self):
        self.__wait_tg_loading()

        self.__pop_terms_of_service()
        self.__pop_tg_find_contacts()

    # __________________________________________________________________________ Browser's code for get api
    def __decoding_text_clipboard(self):
        try:
            copied_text = pyperclip.paste()
            clipboard_code = copied_text.split("\n")[1]
            return clipboard_code

        except IndexError:
            logger.error('No text in clipboard')
            input("What to do? ")

    def parce_message_code_for_api(self) -> str:
        """
         This method is for get API data from https://my.telegram.org/
         the function grub code from telegram's message via copy
         message's content and then grab them out from buffering memory
        """
        self._switch_to_NATIVE_APP_context()
        self.__wait_tg_loading()

        # for click by message in telegram's main menu
        xpath_msg_main_menu = '//android.view.View[@resource-id="org.thunderdog.challegram:id/chat"]'
        self._click_element(driver=self.TG_DRIVER, value=xpath_msg_main_menu, intercepted_click=True)
        self.__wait_tg_loading()

        # for click by message's menu
        xpath_text_msg = '//androidx.recyclerview.widget.RecyclerView[@resource-id="org.thunderdog.challegram:id/msg_list"]//android.view.View'
        self._click_element(driver=self.TG_DRIVER, value=xpath_text_msg)
        self.__wait_tg_loading()

        # copy message
        xpath_screen = '/hierarchy/android.widget.FrameLayout'
        self._action_touch_by_coord(driver=self.TG_DRIVER, x=343, y=2772, xpath_value=xpath_screen)

        # decoding text from clipboard
        code = self.__decoding_text_clipboard()

        return code
