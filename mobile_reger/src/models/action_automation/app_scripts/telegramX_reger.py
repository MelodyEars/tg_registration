import base64

from loguru import logger

from SETTINGS import BASE_ROOT
from mobile_reger.src.models.action_automation.init_appium.UI_inherit_class import UIBaseAct
from mobile_reger.src.models.exceptions.appium_exception import SendPhoneNumberException, NoCodeSentException, \
    BannedPhoneNumberException

from mobile_reger.src.models.sms_activate.sms_api import receive_sms, InfoNumberPhone


class AutoRegTelegramX(UIBaseAct):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.phone_number = ""
        self.activation_id = ""

    def __wait_tg_loading(self):
        self.wait_loading(driver=self.TG_DRIVER)

    # ____________________________________________________________________________ Support method
    def __btn_right_arrow(self):
        logger.info('click on the right arrow')

        xpath_btn = '//android.widget.FrameLayout[@content-desc="Done"]/android.view.View'
        self._click_element(value=xpath_btn)

        self.__wait_tg_loading()

    def __btn_pop_continue(self):
        # Press "Continue"
        xpath_btn_continue = '(//android.widget.TextView[@package="org.telegram.messenger.web"])[2]'
        if self._click_element(value=xpath_btn_continue):
            logger.info('Press "Continue"')
        else:
            logger.critical('Not Press "Continue"')
            raise

    # _____________________________________________________________________________ base method
    # _____________________________________________________________ 1 page
    def startMessaging(self):
        logger.info('prepare click StartMessaging')

        self.__wait_tg_loading()

        xpath_btn = '(//android.widget.TextView[@package="org.telegram.messenger.web"])[3]'
        self._click_element(value=xpath_btn)

        logger.info('Executed click StartMessaging')

    # _____________________________________________________________ 2 page
    def __popups_manage_phone_calls(self):
        # don't allow
        xpath_btn_not_allow = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"]'
        if self._click_element(value=xpath_btn_not_allow):
            logger.info('Click not allow on popups "to make and manage phone calls"')
        else:
            logger.critical('Not Click on popups "to make and manage phone calls"')

    def __popups_2_manage_phone_calls(self):
        """Allow Telegram to make and manage phone calls"""
        xpath_btn_allow = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button"]'
        if self._click_element(value=xpath_btn_allow):
            logger.info('Click allow on popups "to make and manage phone calls"')

        else:
            logger.critical('Not Click on popups "to make and manage phone calls"')

    def enterPhoneNumbers(self, dict_info_PhoneNumber: InfoNumberPhone = None):
        logger.info("Enter number of phone")

        xpath_popup_confirm_num_phone = '//android.widget.FrameLayout[@resource-id="android:id/content"]'
        if (not dict_info_PhoneNumber) or self._elem_exists(value=xpath_popup_confirm_num_phone, wait=1):
            logger.info('Popups about "to make and manage phone calls"')

            if dict_info_PhoneNumber:
                self.__btn_pop_continue()
                self.__popups_manage_phone_calls()

                self.phone_number = dict_info_PhoneNumber["code_country"] + dict_info_PhoneNumber["phone_number"]
                print("Number phone: ", self.phone_number)
                self.activation_id = dict_info_PhoneNumber["activationId"]

            if not dict_info_PhoneNumber:
                xpath_body_number = '//android.widget.EditText[@content-desc="Phone number"]'
                self._elem_exists(value=xpath_body_number, return_xpath=True).clear()

            # Send Country code
            xpath_code_country = '//android.widget.EditText[@content-desc="Country code"]'
            self._send_text(value=xpath_code_country, message=self.phone_number)

            logger.info("Successfully sent a number of phone")

            self.__btn_right_arrow()

            # popups
            """Is this the correct number?"""
            self.__btn_right_arrow()  # yes (the same xpath)

            # popups message
            """
            Please allow Telegram to receive calls and read the call log
            so that we can automatically enter your code for you.
            """
            self.__btn_pop_continue()

            # again same question about "to make and manage phone calls"
            self.__popups_manage_phone_calls()
            self.__popups_2_manage_phone_calls()

            # popups check "This phone number is banned."
            xpath_ban = '//android.widget.TextView[@text="This phone number is banned."]'
            if self._elem_exists(value=xpath_ban, wait=5):
                logger.error('This phone number is banned.')
                raise BannedPhoneNumberException(f'This phone {self.phone_number} number is banned.')
            else:
                logger.warning('This phone number is not banned.')

            if self._elem_exists(value=xpath_code_country, wait=1):
                logger.critical('Stayed on the same web page')
                raise

        else:
            logger.critical("No popup, more likely, no pass first page")
            self.startMessaging()
            self.enterPhoneNumbers()

    # _____________________________________________________________ 3 page
    def __is_already_registered(self):
        xpath_btn_send_sms = '//android.widget.TextView[@text="Tap to get a code via SMS"]'
        if self._click_element(value=xpath_btn_send_sms, wait=1):
            logger.warning(f"{self.phone_number} is already registered")

            xpath_error = '//android.widget.TextView[@text="An internal error occurred. Please try again later."]'
            if self._elem_exists(value=xpath_error, wait=5):
                raise SendPhoneNumberException(f'This phone {self.phone_number} is not for attendance.')

    def sendCodeToTg(self,  second_try: bool = False):
        logger.info("Enter number of phone")
        self.__wait_tg_loading()
        self.__is_already_registered()

        xpath_field = '(//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText)[1]'

        code = receive_sms(activation_id=self.activation_id, phone_number=self.phone_number)

        if code:
            self._send_text(value=xpath_field, message=code)

            # Todo check if this exists recovery account
            logger.info("Successfully sent a number of phone")
            self.__btn_right_arrow()

        else:
            if not second_try:
                xpath_not_sent_code = '//android.widget.TextView[@text="Didn\'t get the code?"]'
                self._click_element(value=xpath_not_sent_code)
                # popups Sorry "if you didn't get the code by SMS or call..."
                xpath_edit_num = '//android.widget.TextView[@text="Edit number"]'
                self._click_element(value=xpath_edit_num)
                # than we're arraying to page 2
                self.enterPhoneNumbers()
                self.sendCodeToTg(second_try=True)
            else:
                raise NoCodeSentException('Telegram did not send the code to the sms')

    # _____________________________________________________________ 4 page
    def create_first_last_name(self, firstname: str, lastname: str = None):
        self.__wait_tg_loading()
        # send firstname
        xpath_first_name = '//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.EditText'
        self._send_text(value=xpath_first_name, message=firstname)

        if lastname:
            # send lastname
            xpath_last_name = '//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.EditText'
            self._send_text(value=xpath_last_name, message=lastname)

        self.__btn_right_arrow()
        self.__btn_pop_continue()

    # _____________________________________________________________ After Create Account
    def tg_copy_file_dat(self) -> str:
        """
        This func analog command in console:
        adb root
        adb shell
        command_for_copy = f'adb pull ' + path_to_android_file + path_save
        """

        logger.info("Start copy file from Android")
        path_to_android_file = '/data/data/org.telegram.messenger.web/files/tgnet.dat '
        path_save = str(BASE_ROOT / fr'mobile_reger\output_files\tgnets\{self.phone_number}.dat')

        file_data = self.TG_DRIVER.pull_file(path_to_android_file)
        logger.info("File data successfully copied to local")

        if file_data:
            logger.info("File exists on Android")

            with open(path_save, 'wb') as f:
                logger.info("File successfully opened")
                f.write(base64.b64decode(file_data))
                logger.info("File successfully written")

        else:
            logger.critical("File in Android not found")
            raise

        return path_save
