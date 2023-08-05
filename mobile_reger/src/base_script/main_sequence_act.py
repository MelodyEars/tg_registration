
import unittest

from mobile_reger.src.action_automation.app_scripts.browser_google import BrowserGetInfoAccount
from mobile_reger.src.action_automation.app_scripts.telegramX_reger import AutoRegTelegramX
from mobile_reger.src.sms_activate.sms_api import buy_new_number


class SequenceOfActions(unittest.TestCase):

    def test_tg_registration(self):
        with AutoRegTelegramX() as reg_tg:

            reg_tg.startMessaging()

            # TODO buy number before create virtual machine
            self.dict_info_PhoneNumber = buy_new_number()
            input("press enter: ")
            reg_tg.enterPhoneNumbers(self.dict_info_PhoneNumber)

            phone_number = self.dict_info_PhoneNumber['phone_number']
            reg_tg.sendCodeToTg(phone_number)

            firstname = "Subaru"
            reg_tg.create_first_last_name(firstname)

            reg_tg.tg_popups_after_create()


if __name__ == '__main__':
    unittest.main()




