import time

from appium import webdriver
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mobile_reger.src.action_automation.init_appium.init_driver import ServerRemote


class AppiumActions(ServerRemote):

    def __scroll_to_elem(self, driver: webdriver, element: WebElement) -> None:
        """ Simple Scroll to element for Android and IOS """

        platform = driver.desired_capabilities['platformName'].lower()
        if platform == 'android':
            driver.execute_script('mobile: scroll', {'element': element.id})
        elif platform == 'ios':
            driver.execute_script('mobile: scroll', {'direction': 'toVisible', 'element': element.id})

    def __intercepted_click(self, elem_for_click) -> None:
        """ Recurse call this function, if element intercepted """

        try:
            elem_for_click.click()
        except ElementClickInterceptedException:
            time.sleep(.5)
            self.__intercepted_click(elem_for_click)

    def _elem_exists(self,
                     driver: webdriver, value: str,
                     by=AppiumBy.XPATH, wait=120, return_xpath=False, scroll_to=False

                     ) -> bool | WebElement:
        """ Check and Scroll to element """

        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            wait = WebDriverWait(driver, wait, ignored_exceptions=ignored_exceptions)
            take_xpath = wait.until(EC.presence_of_element_located((by, value)))

            if scroll_to:
                self.__scroll_to_elem(driver=driver, element=take_xpath)

            exist = take_xpath if return_xpath else True

        except TimeoutException:
            exist = False

        return exist

    def _click_element(self,
                       driver: webdriver, value: str,
                       by=AppiumBy.XPATH, wait=60, scroll_to=False, intercepted_click=False, return_xpath=False

                       ) -> bool | WebElement:

        """ Wait and Click element """

        if scroll_to:
            self._elem_exists(driver=driver, value=value, by=by, wait=wait, scroll_to=True)

        try:
            wait = WebDriverWait(driver, wait)
            elem_for_click: WebElement = wait.until(EC.element_to_be_clickable((by, value)))
            if intercepted_click:
                self.__intercepted_click(elem_for_click)
            else:
                elem_for_click.click()

            exist = elem_for_click if return_xpath else True

        except TimeoutException:
            exist = False

        return exist

    def _send_text(self,
                   driver: webdriver, value: str, message: str,
                   by: AppiumBy = AppiumBy.XPATH, wait: int = 60, scroll_to: bool = False,
                   intercepted_click: bool = False, after_send_tap: bool = False
                   ) -> None:
        """ Send your message"""

        xpath_elem: WebElement = self._click_element(
            driver=driver, value=value, by=by, wait=wait, scroll_to=scroll_to, intercepted_click=intercepted_click,
            return_xpath=True
        )

        xpath_elem.clear()
        xpath_elem.send_keys(str(message))

        # if after_send_tap:
        #     xpath_elem.send_keys("\uE007")
