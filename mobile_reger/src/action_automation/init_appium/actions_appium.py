import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mobile_reger.src.action_automation.init_appium.remote_appium import ServerRemote


class AppiumActions(ServerRemote):
    def __scroll_to_elem(self, element):
        platform = self.DRIVER.desired_capabilities['platformName'].lower()
        if platform == 'android':
            self.DRIVER.execute_script('mobile: scroll', {'element': element.id})
        elif platform == 'ios':
            self.DRIVER.execute_script('mobile: scroll', {'direction': 'toVisible', 'element': element.id})

    def __intercepted_click(self, elem_for_click):
        try:
            elem_for_click.click()
        except ElementClickInterceptedException:
            time.sleep(.5)
            self.__intercepted_click(elem_for_click)

    def _elem_exists(self, value, by=MobileBy.XPATH, wait=120, return_xpath=False, scroll_to=False):
        try:
            ignored_exceptions = (NoSuchElementException,)
            wait = WebDriverWait(self.DRIVER, wait, ignored_exceptions=ignored_exceptions)
            take_xpath = wait.until(lambda driver: driver.find_element(by, value))

            if scroll_to:
                self.__scroll_to_elem(take_xpath)

            exist = take_xpath if return_xpath else True

        except TimeoutException:
            exist = False

        return exist

    def _click_element(self, value, by=MobileBy.XPATH, wait=60, scroll_to=False, intercepted_click=False) -> bool:
        if scroll_to:
            self._elem_exists(value=value, by=by, wait=wait, scroll_to=True)

        try:
            wait = WebDriverWait(self.DRIVER, wait)
            elem_for_click = wait.until(EC.element_to_be_clickable((by, value)))
            if intercepted_click:
                self.__intercepted_click(elem_for_click)
            else:
                elem_for_click.click()
            return True

        except TimeoutException:
            return False
