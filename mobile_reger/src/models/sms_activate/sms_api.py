import random
import time
from typing import TypedDict

from loguru import logger
from smsactivate.api import SMSActivateAPI

from SETTINGS import API_KEY
from mobile_reger.src.models.exceptions import NoCodeSentException

sa = SMSActivateAPI(API_KEY)


# ____________________________________________________ TYPING _________________________________________________________
class InfoNumberPhone(TypedDict):
    phone_number: str
    activationId: str
    country_name: str
    code_country: str
    language: str
    abbreviated_country: str


# ______________________________________________________ API __________________________________________________________
def buy_new_number() -> InfoNumberPhone:
    #  TODO call this func, before create vm

    service = 'tg'
    logger.info(f'Buying new number for {service}')

    info_countries = {
        0: ('Russia', '7', 'ru', 'RU'),
        1: ('Ukraine', '380', 'uk', 'UA'),
        2: ('Kazakhstan', '77', 'kk', 'KZ'),
        11: ('Kyrgyzstan', '996', 'ky', 'KG'),
        34: ('Estonia', '372', 'et', 'EE'),
        35: ('Azerbaijan', '994', 'az', 'AZ'),
        51: ('Belarus', '375', 'be', 'BY'),
        85: ('Moldova', '373', 'ro', 'MD'),
        148: ('Armenia', '374', 'hy', 'AM')
    }

    available_countries = list(info_countries.keys())
    logger.info(available_countries)

    while available_countries:
        logger.debug(available_countries)
        api_code_country = random.choice(available_countries)
        logger.debug(api_code_country)

        number = sa.getNumberV2(service=service, country=api_code_country, verification="false")
        logger.warning(number)

        if 'error' in number.keys():
            logger.error(f'number not sent for this {api_code_country}')
            available_countries.remove(api_code_country)
            continue

        country_name, code_country_phone_number, lang, abbreviated_country = info_countries[api_code_country]

        phone_number = str(number['phoneNumber'])[len(code_country_phone_number):]

        return {
            'phone_number': phone_number,
            'activationId': str(number['activationId']),
            'country_name': country_name,
            'code_country': code_country_phone_number,
            'language': lang,
            'abbreviated_country': abbreviated_country,
        }

    else:
        raise Exception('Failed to get new number. No countries available.')


def cancel_number(activation_id: str) -> bool:
    response = sa.setStatus(id=activation_id, status=8)
    if response == "ACCESS_CANCEL":
        return True
    return False


# def _get_amount_sms(phone_number: str) -> int:
#     try:
#         for active in sa.getActiveActivations()['activeActivations']:
#             if active['phoneNumber'] == phone_number:
#                 return len(active['smsText'])
#     except Exception as err:
#         logger.error(err)
#         return 0
#
#
# def _receive_sms(phone_number: str):
#     old_messages_amount = _get_amount_sms(phone_number)
#
#     try:
#         time_check = 300
#         while time_check:
#             time_check -= 1
#             print(f'Attempt {time_check}')
#
#             try:
#                 actives = sa.getActiveActivations()
#                 logger.info(f'actives:  {actives}')
#
#                 active_list = actives.get('activeActivations', [])
#                 logger.debug(active_list)
#
#             except Exception as e:
#                 logger.error(f'Error fetching active activations: {e}')
#
#                 logger.info('Waiting for new messages 5 sec...')
#                 time.sleep(5)
#
#                 continue
#
#             for active in active_list:
#                 logger.info(f'in loop for active: {active}')
#
#                 if phone_number == active.get('phoneNumber'):
#                     messages = active.get('smsText', [])
#                     logger.info(f'messages: {messages}')
#                     if messages:
#                         if old_messages_amount == 0:
#                             logger.warning(f'New message: {messages[0]}')
#                             return messages[0]
#                         elif old_messages_amount > 1:
#                             if len(messages) > old_messages_amount:
#                                 logger.warning(messages[-1])
#                                 return messages[-1]
#
#             logger.info('No new messages')
#             logger.info('Waiting for new messages 5 sec...')
#             time.sleep(5)
#         else:
#             return False
#
#     except KeyError:
#         return False


def check_status(activation_id: str, phone_number: str) -> tuple[bool, bool]:
    time_check = 20

    status = sa.getStatus(id=activation_id)
    logger.warning(status)

    while status == "STATUS_WAIT_CODE":
        status = sa.getStatus(id=activation_id)
        logger.debug(status)
        time.sleep(30)

        time_check -= 1
        logger.debug(f"Attempt is {time_check}")
        if time_check == 0:
            return False, False

    logger.debug(f'phone_number: {phone_number}, status: {status}')
    try:
        status_ok, code = status.split(":")
        return status_ok, code
    except Exception as e:
        logger.error(e)

    if 'error' in status.keys():
        raise NoCodeSentException

    return False, False


def _receive_sms(activation_id: str, phone_number: str) -> str | bool:
    status_ok, code = check_status(activation_id=activation_id, phone_number=phone_number)

    if status_ok == 'STATUS_OK':
        return code
    #     try:
    #         response = requests.get(
    #             'https://sms-activate.org/stubs/handler_api.php?api_key=' + API_KEY + '&action=getActiveActivations&id=' + activation_id)
    #         content = response.json()
    #         code = content[activation_id]['code']
    #         logger.debug(f"phone_number: {phone_number}, code: {code}")
    #         return code
    #     except Exception as e:
    #         logger.error(f'Error fetching active activations: {e}')

    else:
        return False


def get_balance() -> str:
    resp = sa.getBalance()
    print(resp)
    return resp['balance'] + ' rub'


def request_new_sms(activation_id: str):
    response = sa.setStatus(id=activation_id, status=3)
    print(response)

    if response == "ACCESS_CANCEL":
        return True
    return False


if __name__ == '__main__':
    print(buy_new_number())
    #  {'activationId': '1616312782', 'phoneNumber': '37379114625'}

    # x = '37477168672'
    # print(_receive_sms(x))
    print(get_balance())
