
from loguru import logger
from mobile_reger.src.action_automation.init_appium.UI_inherit_class import UIBaseAct


class AutoRegTelegramX(UIBaseAct):
    def startMessaging(self):
        logger.info('prepare click StartMessaging')

        xpath_btn = '//android.widget.TextView[contains(@resource-id, "org.thunderdog.challegram:id/btn_done")]'
        self._click_element(xpath_btn)

        logger.info('Executed click StartMessaging')

    def enterPhoneNumbers(self, phone_number):
        logger.info("Enter number of phone")

        xpath_field = '//android.widget.EditText[@resource-id="org.thunderdog.challegram:id/login_phone"]'
        self._send_text(value=xpath_field, message=phone_number)

        logger.info("Successfully sent a number of phone")
