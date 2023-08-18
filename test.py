import subprocess
import sys
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from loguru import logger

# Шлях до LDPlayer
ldplayer_path = r'C:\LDPlayer\LDPlayer9\LDPlayer.exe'

# Запуск віртуальної машини
vm_name = 'TestVM'
ram = 2048
cpu_cores = 2

logger.info("Hospodi Boje pomoji")
subprocess.run([ldplayer_path, 'create', f'--name {vm_name}', f'--ram {ram}', f'--cpu {cpu_cores}'])
time.sleep(10)  # Зачекайте деякий час для завершення старту віртуальної машини
logger.info("Uf it's impressive")
# APPIUM_HOST та APPIUM_PORT
APPIUM_PORT = 4723  # Порт, на якому працюватиме Appium сервер
APPIUM_HOST = '127.0.0.1'

# Підключення до Appium сервера
service = AppiumService()
service.start(args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)], timeout_ms=20000)
logger.info("Appium started")

# Налаштування capabilities для підключення до віртуальної машини
TELEGRAM_capabilities: dict = {
    "platformName": "Android",
    "appium:automationName": "uiautomator2",
    "appium:language": "en",
    "appium:locale": "US",
    "appium:app": r"C:\Users\King\PycharmProjects\tg_registration\mobile_reger\apps_and_drivers\apk\telegram-9-7-6.apk",
    "appium:uiautomator2ServerInstallTimeout": 120000,
    "appium:adbExecTimeout": 120000,
}

logger.debug("init driver")
# Створення підключення до додатку на віртуальній машині
tg_options = UiAutomator2Options().load_capabilities(TELEGRAM_capabilities)
driver = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}/wd/hub', options=tg_options)

# Ваші тестові дії тут
input("nu sho? ")
# Закриття підключення до додатку та віртуальної машини

logger.info("Driver stopped")
driver.quit()
logger.info("Appium stopped")
service.stop()  # Зупинка Appium сервера
logger.info("turn off LDPlayer")
subprocess.run([ldplayer_path, 'kill', f'--name {vm_name}'])  # Зупинка віртуальної машини
logger.info("Successfully turn off LDPlayer")

