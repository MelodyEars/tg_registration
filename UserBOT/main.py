# Импорт необходимых библиотек
import os
import json
import random
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import telebot
from telebot.utils import register_user

from loguru import logger

from telethon import TelegramClient, errors


from telethon.sessions import StringSession

from config import (APP_PAIRS_FILE, APP_VERSIONS_FILE, DEVICES_FILE, FIRSTNAMES_FILE, LASTNAMES_FILE,
                    LANG_CODES_FILE, SDKS_FILE, SYSTEM_LANG_CODES_FILE, ACCOUNTS_DIR, API_KEY)

from smsactivate.api import SMSActivateAPI
sa = SMSActivateAPI(API_KEY)

# ______________________________________________________ API __________________________________________________________

# def _get_cheapest_country(data: dict) -> dict:
#
#     data = {key: value for key, value in data.items() if value['country'] == 12 or value['country'] == 187}
#     struct_data = [value for value in data.values()]
#     for info in sorted(struct_data, key=lambda x: x['price']):
#         if info["count"] > 0:
#             return info


def buy_new_number(service: str) -> tuple:
    logger.info(f'Buying new number for {service}')
    countries = [0, 1, 2, 11, 34, 35, 51, 85, 148]
    while countries:
        country = countries.remove(random.choice(countries))
        print(country)

        # country = sa.getTopCountriesByService(service)
        # best_country = _get_cheapest_country(country)
        number = sa.getNumberV2(service=service, country=country, verification="false")

        if 'error' in number.keys():
            logger.error(f'number not sent for this {country}')
            print(number)
            continue

        logger.warning(number)
        return number['activationId'], number['phoneNumber'],

    else:
        raise Exception('Failed to get new number. No countries available.')


def cancel_number(activation_id: str) -> bool:
    response = sa.setStatus(id=activation_id, status=8)
    if response == "ACCESS_CANCEL":
        return True
    return False


def _get_amount_sms(phone_number: str) -> int:
    try:
        for active in sa.getActiveActivations()['activeActivations']:
            if active['phoneNumber'] == phone_number:
                return len(active['smsText'])
    except Exception as err:
        logger.error(err)
        return 0


def _receive_sms(phone_number: str):
    old_messages_amount = _get_amount_sms(phone_number)

    try:
        while True:
            logger.info('Waiting for new messages 5 sec...')
            time.sleep(5)

            actives = sa.getActiveActivations()
            logger.info(f'actives:  {actives}')

            active_list = actives['activeActivations']

            for active in active_list:
                logger.info(f'in loop for active: {active}')

                if phone_number == active['phoneNumber']:
                    messages = active['smsText']
                    logger.info(f'messages: {messages}')
                    if messages:
                        if old_messages_amount == 0:
                            logger.warning(f'New message: {messages[0]}')
                            return messages[0]
                        elif old_messages_amount > 1:
                            if len(messages) > old_messages_amount:
                                logger.warning(messages[-1])
                                return messages[-1]

            logger.info('No new messages')

    except KeyError:
        pass


def get_balance() -> str:
    resp = sa.getBalance()
    return resp['balance'] + ' rub'


def request_new_sms(activation_id: str):
    response = sa.setStatus(id=activation_id, status=3)
    print(response)
    if response == "ACCESS_CANCEL":
        return True
    return False



# Функция для получения нового номера телефона от SMS-man
# def get_new_phone_number(country, service):
#     # url = f'http://api.sms-man.ru/control/get-number?token={api_key}&country_id={country}&application_id=3'
#     url = f'https://sms-activate.org/stubs/handler_api.php?api_key=${SMSACTIVATE_API_KEY}&action=getNumberV2&service=${service}&forward=$forward&operator=$operator&ref=$ref&country=${country}&phoneException=$phoneException&maxPrice=maxPrice&verification=$verification'
#
#     response = requests.get(url)
#
#     data = response.json()
#     if 'phoneNumber' in data:
#         logger.info(f"Spend: {data['activationCost']}")
#         return data['phoneNumber'], data['activationId']
#     else:
#         raise Exception('Failed to get new number.')


# Функция для получения SMS-кода от SMS-man
# def get_sms(id):
#     'http://api.sms-man.ru/control/get-sms?token={api_key}&request_id={id}'
#     url = 'https://api.sms-activate.org/stubs/handler_api.php?api_key=$api_key&action=getActiveActivations'
#     while True:
#         response = requests.get(url)
#         data = response.json()
#         if 'sms_code' in data:
#             return data['sms_code']
#         elif 'wait_sms' in data and data['error_code'] == 'Number are banned':
#             raise Exception('Number are banned.')
#         time.sleep(5)  # Подождите перед следующим запросом


# Загрузка данных из текстовых файлов
def load_data(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        data = [line.strip() for line in file.readlines()]
    return data


# Создание и сохранение JSON
def save_account_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Регистрация аккаунта
def register_account(data, phone_number):
    logger.info(f"Registering account {phone_number}")
    async with TelegramClient(StringSession(), data["app_id"], data["app_hash"], proxy=data["proxy"]) as client:
        try:
            client.connect()
            if not client.is_user_authorized():
                logger.info(f"Send code to {phone_number}")
                client.send_code_request(phone_number)

                logger.info(f"Successfully sent {phone_number}")

                # with ThreadPoolExecutor() as executor:
                #     try:
                #         code = asyncio.wait_for(
                #             asyncio.get_running_loop().run_in_executor(executor, _receive_sms, phone_number),
                #             timeout=180
                #         )
                #
                #     except asyncio.TimeoutError:
                #         logger.error("Timeout occurred. Restarting process...")
                #         raise Exception("did not wait for the code")

                code = _receive_sms(phone_number)
                logger.info(f"MAIN Got SMS code {code}")

                try:
                    user = client.sign_up(
                        code,
                        data["first_name"],
                        data["last_name"]
                    )
                    if data["avatar"]:
                        client.upload_profile_photo(data["avatar"])
                    if data["username"]:
                        client.update_username(data["username"])
                    if data["twoFA"]:
                        client.account.set_2fa_password(password=str(data["twoFA"]))
                    data["session_file"] = StringSession.save(client.session)
                    save_account_data(data, os.path.join(data["account_path"], f"{phone_number}.json"))
                    print(f"Аккаунт {phone_number} успешно зарегистрирован.")
                except errors.SessionPasswordNeededError:
                    print(f"Аккаунт {phone_number} уже существует и защищен паролем.")
                except errors.PhoneNumberOccupiedError:
                    print(f"Аккаунт {phone_number} уже зарегистрирован в Telegram.")
                except errors.PhoneNumberBannedError:
                    print(f"Номер телефона {phone_number} заблокирован в Telegram.")
        except Exception as e:
            print(f"Ошибка при регистрации аккаунта {phone_number}: {e}")


# Генерация данных для регистрации
def generate_account_data(phone, account_path, app_pairs, app_versions, devices, firstnames, lastnames, lang_codes, sdks, system_lang_codes):
    app_id, app_hash = random.choice(app_pairs).split(":")
    data = {
        "phone": phone,
        "account_path": account_path,
        "app_id": app_id,
        "app_hash": app_hash,
        "status": "No limits",
        "register_time": 1679616000,
        "avatar": None,
        "first_name": random.choice(firstnames),
        "last_name": random.choice(lastnames),
        "username": None,
        "bio": None,
        "twoFA": 12345,
        "session_file": f"{phone}",
        "device": random.choice(devices),
        "lang_pack": random.choice(lang_codes),
        "system_lang_pack": random.choice(system_lang_codes),
        "sdk": random.choice(sdks),
        "app_version": random.choice(app_versions),
        "is old": False,
        # "proxy": (
        #     "http",
        #     "isp2.hydraproxy.com",
        #     9989,
        #     "netw21534imie54794",
        #     "593Th0Ty7pxpTPOf_country-Kazakhstan"
        # )
    }
    return data


def main():
    # Загрузка данных из текстовых файлов
    app_pairs = load_data(APP_PAIRS_FILE)
    app_versions = load_data(APP_VERSIONS_FILE)
    devices = load_data(DEVICES_FILE)
    firstnames = load_data(FIRSTNAMES_FILE)
    lastnames = load_data(LASTNAMES_FILE)
    lang_codes = load_data(LANG_CODES_FILE)
    sdks = load_data(SDKS_FILE)
    system_lang_codes = load_data(SYSTEM_LANG_CODES_FILE)
    logger.info("MAIN Loaded data from files")

    # Получение нового номера телефона
    # country = '5'

    service = 'tg'

    phone_number, id = buy_new_number(service)
    logger.info(f"MAIN Got new phone number {phone_number} with id {id}")

    # Получение SMS-кода
    # code = get_sms(id)


    # Генерация данных аккаунта и регистрация аккаунта
    account_data = generate_account_data(phone_number, ACCOUNTS_DIR, app_pairs, app_versions, devices, firstnames,
                                         lastnames, lang_codes, sdks, system_lang_codes)
    logger.info(f"MAIN Generated account data for {account_data}")

    register_account(account_data, phone_number)
    logger.info("MAIN Succesfully ended")


# Запуск главной функции
if __name__ == "__main__":
    # asyncio.run(main())
    main()

    x = get_balance()
    print(x)
    # 1127.26 rub