
# phone_number = "380508426096"

import unittest

from loguru import logger

from mobile_reger.src.models.action_automation.app_scripts.browser_google import BrowserGetInfoAccount
from mobile_reger.src.models.action_automation.app_scripts.telegramX_reger import AutoRegTelegramX
from mobile_reger.src.models.sms_activate.sms_api import buy_new_number
from mobile_reger.src.models.telethon_part.auth_telegram import get_tg_session_telethon_sync


class SequenceOfActions(unittest.TestCase):
    "2e234d5d-4a26-4da2-a1e9-6e92887c61a2"
    def test_tg_registration(self):
        logger.info('Start registration')
        with AutoRegTelegramX() as reg_tg:

            reg_tg.startMessaging()

            # TODO buy number before create virtual machine
            self.dict_info_PhoneNumber = buy_new_number()
            logger.warning(self.dict_info_PhoneNumber)

            # enter phone in telegram
            logger.info('Enter number of phone')
            reg_tg.enterPhoneNumbers(self.dict_info_PhoneNumber)

            # send code to smsActivate
            phone_number = self.dict_info_PhoneNumber['phone_number']
            activation_id = self.dict_info_PhoneNumber['activationId']
            logger.info(phone_number, activation_id)
            logger.info('Send code to smsActivate')
            reg_tg.sendCodeToTg(phone_number=phone_number, activation_id=activation_id)

            firstname = "Subaru"
            lastname = None
            logger.info(firstname)
            logger.info('Create first and last name')
            reg_tg.create_first_last_name(firstname, lastname=lastname)

            logger.info('Close popups after registration')
            reg_tg.tg_popups_after_create()

            logger.info('Registration completed')

            # __________________________________________________________ browser work
            phone_number = self.dict_info_PhoneNumber['code_country'] + self.dict_info_PhoneNumber['phone_number']

            # part Browser
            logger.info('Init instance BrowserGetInfoAccount')
            browser_get_api = BrowserGetInfoAccount()

            logger.info('Switch to browser and attend link')
            browser_get_api.run_browser()

            logger.info('Enter number phone and wait on code')
            browser_get_api.enter_number_phone(number_phone=phone_number)

            # part Telegram
            logger.info('Grab confirmation code from clipboard')
            confirm_code = reg_tg.parce_message_code_for_api()

            # part Browser
            logger.info(f'Enter password "{confirm_code}" from telegram to browser')
            browser_get_api.enter_password(confirmation_code=confirm_code)

            logger.info('Switch browser on NATIVE_APP and get API data')
            self.api_id, self.api_hash = browser_get_api.collection_API_data()
            logger.info(f'API ID: {self.api_id}, API HASH: {self.api_hash}')

            get_tg_session_telethon_sync(phone_number=phone_number, api_id=self.api_id, api_hash=self.api_hash)


if __name__ == '__main__':
    unittest.main()
