import time

from loguru import logger
from mobile_reger.src.action_automation.init_appium.UI_inherit_class import UIBaseAct
from mobile_reger.src.exceptions.appium_exception import SendPhoneNumberException
from mobile_reger.src.sms_activate.sms_api import buy_new_number, _receive_sms


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
    def enterPhoneNumbers(self):
        logger.info("Enter number of phone")

        self.dict_info_PhoneNumber = buy_new_number()

        # Send country
        xpath_country = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_country"]'
        self._send_text(value=xpath_country, message=self.dict_info_PhoneNumber['country_name'] + '\n')

        # Send Country code
        xpath_code_country = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_code"]'
        self._send_text(value=xpath_code_country, message=self.dict_info_PhoneNumber["code_country"])

        # Send body number of phone
        xpath_body_number = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_phone"]'
        self._send_text(value=xpath_body_number, message=self.dict_info_PhoneNumber["phone_number"])

        logger.info("Successfully sent a number of phone")

        self.__btn_right_arrow()
        time.sleep(2)

        if self._elem_exists(value=xpath_body_number, wait=1):
            raise SendPhoneNumberException('Somthing wrong with sending a phone number!')

    # _____________________________________________________________ 3 page
    def sendCodeToTg(self):
        logger.info("Enter number of phone")
        self.wait_loading()

        xpath_field = '//android.widget.EditText'
        code = _receive_sms(self.dict_info_PhoneNumber["phone_number"])

        xpath_not_sent_code = '//android.widget.TextView[@resource-id="org.thunderdog.challegram:id/btn_forgotPassword"]'

        if code:
            self._send_text(value=xpath_field, message=code)

            # Todo check if this exists recovery account
            logger.info("Successfully sent a number of phone")

            self.__btn_right_arrow()
            # TODO: checker

        else:
            self._click_element(xpath_not_sent_code)
