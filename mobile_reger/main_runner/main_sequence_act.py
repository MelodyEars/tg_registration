from loguru import logger

from mobile_reger.src.models import convert_tgnet_to_session
from mobile_reger.src.models import get_TgnetDat_fromAndroid
from mobile_reger.src.models.appium_automation.server_appium.runner import appium_service
from mobile_reger.src.models.sms_activate import buy_new_number
from mobile_reger.src.models.vm_manager import run_vm_manager


VM_PORT = '5554'

APPIUM_PORT = '4723'
APPIUM_HOST = '127.0.0.1'


@logger.catch
def thread_main():
    dict_info_PhoneNumber = buy_new_number()

    with run_vm_manager(name_avd=dict_info_PhoneNumber['phone_number'],
                        timezone=dict_info_PhoneNumber['abbreviated_country'],
                        vm_port=VM_PORT):

        with appium_service(APPIUM_HOST, APPIUM_PORT):
            path_save = get_TgnetDat_fromAndroid(
                dict_info_PhoneNumber=dict_info_PhoneNumber,
                APPIUM_HOST=APPIUM_HOST,
                APPIUM_PORT=APPIUM_PORT
            )

            convert_tgnet_to_session(path_save)


if __name__ == '__main__':
    thread_main()
