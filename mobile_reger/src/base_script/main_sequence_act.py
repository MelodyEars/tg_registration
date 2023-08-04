from mobile_reger.src.action_automation.app_scripts.browser_google import BrowserGetInfoAccount
from mobile_reger.src.action_automation.app_scripts.telegramX_reger import AutoRegTelegramX
from mobile_reger.src.sms_activate.sms_api import buy_new_number


class SequenceOfActions(BrowserGetInfoAccount, AutoRegTelegramX):

    def test_tg_registration(self):
        self.dict_info_PhoneNumber = buy_new_number()

        self.startMessaging()
        self.enterPhoneNumbers(self.dict_info_PhoneNumber)
        phone_number = self.dict_info_PhoneNumber['phone_number']
        self.sendCodeToTg(phone_number)
