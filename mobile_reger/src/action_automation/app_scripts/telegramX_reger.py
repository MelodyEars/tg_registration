import time

from loguru import logger
from mobile_reger.src.action_automation.init_appium.UI_inherit_class import UIBaseAct
from mobile_reger.src.exceptions.appium_exception import SendPhoneNumberException
from mobile_reger.src.sms_activate.sms_api import _receive_sms


class AutoRegTelegramX(UIBaseAct):
    # ____________________________________________________________________________ Support method
    def __btn_right_arrow(self):
        logger.info('click on the right arrow')

        xpath_btn = '//android.view.View[@resource-id="org.thunderdog.challegram:id/btn_done"]'
        self._click_element(xpath_btn)

        self.wait_loading()

    # _____________________________________________________________________________ base method
    # _____________________________________________________________ 1 page
    def startMessaging(self):
        logger.info('prepare click StartMessaging')
        self.wait_loading()

        # xpath_btn = '//android.widget.TextView[contains(@resource-id, "org.thunderdog.challegram:id/btn_done")]'
        # self._click_element(xpath_btn)
        self.__btn_right_arrow()

        logger.info('Executed click StartMessaging')

    # _____________________________________________________________ 2 page
    def enterPhoneNumbers(self, dict_info_PhoneNumber: dict):
        logger.info("Enter number of phone")

        # Send country
        xpath_country = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_country"]'
        self._send_text(value=xpath_country, message=dict_info_PhoneNumber['country_name'] + '\n')

        # Send Country code
        xpath_code_country = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_code"]'
        self._send_text(value=xpath_code_country, message=dict_info_PhoneNumber["code_country"])

        # Send body number of phone
        xpath_body_number = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_phone"]'
        self._send_text(value=xpath_body_number, message=dict_info_PhoneNumber["phone_number"])

        logger.info("Successfully sent a number of phone")

        self.__btn_right_arrow()
        time.sleep(2)

        if self._elem_exists(value=xpath_body_number, wait=1):
            raise SendPhoneNumberException('Somthing wrong with sending a phone number!')

    # _____________________________________________________________ 3 page
    def sendCodeToTg(self, phone_number: str):
        logger.info("Enter number of phone")
        self.wait_loading()

        xpath_field = '//android.widget.EditText'
        code = _receive_sms(phone_number=phone_number)

        xpath_not_sent_code = '//android.widget.TextView[@resource-id="org.thunderdog.challegram:id/btn_forgotPassword"]'

        if code:
            self._send_text(value=xpath_field, message=code)

            # Todo check if this exists recovery account
            logger.info("Successfully sent a number of phone")

            self.__btn_right_arrow()
            # TODO: checker

        else:
            self._click_element(xpath_not_sent_code)

    # _____________________________________________________________ 4 page
    def create_first_last_name(self, firstname: str, lastname: str = None):
        self.wait_loading()

        # send firstname
        xpath_first_name = '//android.widget.FrameLayout[@resource-id="org.thunderdog.challegram:id/edit_first_name"]//android.widget.EditText'
        self._send_text(value=xpath_first_name, message=firstname)

        if lastname:
            # send lastname
            xpath_last_name = '//android.widget.FrameLayout[@resource-id="org.thunderdog.challegram:id/edit_last_name"]//android.widget.EditText'
            self._send_text(value=xpath_last_name, message=lastname)

    # _____________________________________________________________ After Create Account
    def pop_tg_find_contacts(self):
        xpath_pop_find_contacts = '//android.widget.TextView[contains(@text, "Find Contacts")]'
        if self._elem_exists(value=xpath_pop_find_contacts, wait=10):
            xpath_btn_never = '//android.widget.Button[contains(@text, "NEVER")]'
            self._click_element(value=xpath_btn_never, intercepted_click=True)
            self.wait_loading()

    def tg_popups_after_create(self):
        self.wait_loading()
        # TODo add popups

    def parce_message_code_for_api(self):
        pass
