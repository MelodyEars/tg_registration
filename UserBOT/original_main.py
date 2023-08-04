# Импорт необходимых библиотек
import os
import json
import random
import requests
import asyncio
import time

from loguru import logger

from telethon import TelegramClient, errors
from telethon.sessions import StringSession


from config import (APP_PAIRS_FILE, APP_VERSIONS_FILE, DEVICES_FILE, FIRSTNAMES_FILE, LASTNAMES_FILE,
                    LANG_CODES_FILE, SDKS_FILE, SYSTEM_LANG_CODES_FILE, ACCOUNTS_DIR, API_KEY)


'37477168672'

# Функция для получения нового номера телефона от SMS-man
def get_new_phone_number(country):
    url = f'http://api.sms-man.ru/control/get-number?token={api_key}&country_id={country}&application_id=3'
    response = requests.get(url)
    data = response.json()
    if 'number' in data:
        return data['number'], data['request_id']
    else:
        raise Exception('Failed to get new number.')


# Функция для получения SMS-кода от SMS-man
def get_sms(id):
    'http://api.sms-man.ru/control/get-sms?token={api_key}&request_id={id}'
    url = 'https://api.sms-activate.org/stubs/handler_api.php?api_key=$api_key&action=getActiveActivations'
    while True:
        response = requests.get(url)
        data = response.json()
        if 'sms_code' in data:
            return data['sms_code']
        elif 'wait_sms' in data and data['error_code'] == 'Number are banned':
            raise Exception('Number are banned.')
        time.sleep(5)  # Подождите перед следующим запросом


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
async def register_account(data, phone_number, code):
    logger.info(f"Registering account {phone_number} with code {code}")
    async with TelegramClient(StringSession(), data["app_id"], data["app_hash"], proxy=data["proxy"]) as client:
        try:
            await client.connect()
            if not await client.is_user_authorized():
                logger.info(f"Send code to {phone_number}")
                await client.send_code_request(phone_number, force_sms=True)
                logger.info(f"Successfully sent {phone_number}")
                try:
                    user = await client.sign_up(
                        code,
                        data["first_name"],
                        data["last_name"]
                    )
                    if data["avatar"]:
                        await client.upload_profile_photo(data["avatar"])
                    if data["username"]:
                        await client.update_username(data["username"])
                    if data["twoFA"]:
                        await client.account.set_2fa_password(password=str(data["twoFA"]))
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
        "proxy": (
            "http",
            "isp2.hydraproxy.com",
            9989,
            "netw21534imie54794",
            "593Th0Ty7pxpTPOf_country-Russia"
        )
    }
    return data


async def main():
    # Загрузка данных из текстовых файлов
    app_pairs = load_data(APP_PAIRS_FILE)
    app_versions = load_data(APP_VERSIONS_FILE)
    devices = load_data(DEVICES_FILE)
    firstnames = load_data(FIRSTNAMES_FILE)
    lastnames = load_data(LASTNAMES_FILE)
    lang_codes = load_data(LANG_CODES_FILE)
    sdks = load_data(SDKS_FILE)
    system_lang_codes = load_data(SYSTEM_LANG_CODES_FILE)
    logger.info("Loaded data from files")
    # Получение нового номера телефона
    country = '5'
    phone_number, id = get_new_phone_number(country)
    logger.info(f"Got new phone number {phone_number} with id {id}")

    # Получение SMS-кода
    code = get_sms(id)
    logger.info(f"Got SMS code {code}")

    # Генерация данных аккаунта и регистрация аккаунта
    account_data = generate_account_data(phone_number, ACCOUNTS_DIR, app_pairs, app_versions, devices, firstnames,
                                         lastnames, lang_codes, sdks, system_lang_codes)
    logger.info(f"Generated account data for {account_data}")

    await register_account(account_data, phone_number, code)
    logger.info("Succesfully ended")


# Запуск главной функции
if __name__ == "__main__":
    asyncio.run(main())
