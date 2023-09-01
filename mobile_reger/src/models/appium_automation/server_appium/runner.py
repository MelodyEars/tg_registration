import contextlib
import time
from pathlib import Path

from appium.webdriver.appium_service import AppiumService
from loguru import logger


@contextlib.contextmanager
def appium_service(APPIUM_HOST, APPIUM_PORT):
    logger.info('Starting Appium service')
    service = AppiumService()

    # folder_logs_path = list(Path(__file__).parents)[-5]
    # Path(folder_logs_path / 'logs', mkdir=True)
    # with open('AppiumServicelog.txt', 'w') as f:
    #     service.start(stdout=f, stderr=f,
    #                   args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT), '--base-path', '/wd/hub'])
    service.start(args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT), '--base-path', '/wd/hub'])

    try:
        logger.info('Appium service started')
        assert service.is_running
        assert service.is_listening
        yield
    finally:
        logger.info('Stopping Appium service')
        service.stop()
        assert not service.is_running
        assert not service.is_listening


if __name__ == '__main__':
    with appium_service('127.0.0.1', 4723) as service:
        folder_path = Path(__file__).parents
        print(list(folder_path)[-5])
        time.sleep(5)
