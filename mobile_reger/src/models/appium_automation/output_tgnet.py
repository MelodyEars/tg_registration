from loguru import logger

from mobile_reger.src.models.appium_automation.app_scripts import AutoRegTelegramX
from mobile_reger.src.models.personality_generator import gen_personality
from mobile_reger.src.models.sms_activate import buy_new_number


def get_TgnetDat_fromAndroid():
    logger.info('Init class AutoRegTelegramX')

    with AutoRegTelegramX() as autoreg:
        logger.debug('Start work with instance AutoRegTelegramX')

        autoreg.startMessaging()
        logger.debug('the METHOD 1(page 1) has finished working')

        dict_info_PhoneNumber = buy_new_number()
        logger.warning(f'received data: {dict_info_PhoneNumber}')
        autoreg.enterPhoneNumbers(dict_info_PhoneNumber=dict_info_PhoneNumber)
        logger.debug('the METHOD 2(page 2) has finished working')

        autoreg.sendCodeToTg()
        logger.debug('the METHOD 3(page 3) has finished working')

        firstname, lastname = gen_personality(dict_info_PhoneNumber=dict_info_PhoneNumber)
        autoreg.create_first_last_name(firstname=firstname, lastname=lastname)
        logger.debug('the METHOD 4(page 4) has finished working')

        path_save = autoreg.tg_copy_file_dat()
        logger.debug(f'the file is located {path_save}')

        return path_save


