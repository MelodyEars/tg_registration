
import unittest

from loguru import logger

from mobile_reger.src.action_automation.app_scripts.browser_google import BrowserGetInfoAccount
from mobile_reger.src.action_automation.app_scripts.telegramX_reger import AutoRegTelegramX
from mobile_reger.src.sms_activate.sms_api import buy_new_number


class SequenceOfActions(unittest.TestCase):

    # def test_tg_registration(self):
    #     logger.info('Start registration')
    #     with AutoRegTelegramX() as reg_tg:
    #
    #         reg_tg.startMessaging()
    #
    #         # TODO buy number before create virtual machine
    #         self.dict_info_PhoneNumber = buy_new_number()
    #
    #         reg_tg.enterPhoneNumbers(self.dict_info_PhoneNumber)
    #
    #         phone_number = self.dict_info_PhoneNumber['phone_number']
    #         activation_id = self.dict_info_PhoneNumber['activationId']
    #         reg_tg.sendCodeToTg(phone_number=phone_number, activation_id=activation_id)
    #
    #         firstname = "Subaru"
    #         reg_tg.create_first_last_name(firstname)
    #
    #         reg_tg.tg_popups_after_create()
    #
    #         logger.info('Registration completed')

    def test_browser_part(self):
        # phone_number = self.dict_info_PhoneNumber['code_country'] + self.dict_info_PhoneNumber['phone_number']
        phone_number = "996223876109"
        # part Browser
        with BrowserGetInfoAccount() as browser_get_api:
            browser_get_api.run_browser()
            browser_get_api.enter_number_phone(number_phone=phone_number)

            # part Telegram
            confirm_code = input("Enter code: ")

            # part Browser
            browser_get_api.enter_password(confirmation_code=confirm_code)
            browser_get_api.nav_by_your_telegram_core()
            self.api_id, self.api_hash = browser_get_api.collection_API_data()


if __name__ == '__main__': 
    unittest.main()
