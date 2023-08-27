import time

from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException

from mobile_reger.src.models.appium_automation.init_appium.init_driver import ServerRemote


class AppiumActions(ServerRemote):

    def __scroll_to_elem(self, element: WebElement) -> None:
        """ Simple Scroll to element for Android and IOS """

        platform = self.TG_DRIVER.desired_capabilities['platformName'].lower()
        if platform == 'android':
            self.TG_DRIVER.execute_script('mobile: scroll', {'element': element.id})
        elif platform == 'ios':
            self.TG_DRIVER.execute_script('mobile: scroll', {'direction': 'toVisible', 'element': element.id})

    def __intercepted_click(self, elem_for_click) -> None:
        """ Recurse call this function, if element intercepted """

        try:
            elem_for_click.click()
        except ElementClickInterceptedException:
            time.sleep(.5)
            self.__intercepted_click(elem_for_click)

    def _elem_exists(self, value: str, by=AppiumBy.XPATH, wait=120, return_xpath=False, scroll_to=False
                     ) -> bool | WebElement:
        """ Check and Scroll to element """

        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            wait = WebDriverWait(self.TG_DRIVER, wait, ignored_exceptions=ignored_exceptions)
            take_xpath = wait.until(EC.presence_of_element_located((by, value)))

            if scroll_to:
                self.__scroll_to_elem(element=take_xpath)

            exist = take_xpath if return_xpath else True

        except TimeoutException:
            exist = False

        return exist

    def _click_element(self,
                       value: str,
                       by=AppiumBy.XPATH, wait=60, scroll_to=False, intercepted_click=False, return_xpath=False

                       ) -> bool | WebElement:

        """ Wait and Click element """

        if scroll_to:
            self._elem_exists(value=value, by=by, wait=wait, scroll_to=True)

        try:
            wait = WebDriverWait(self.TG_DRIVER, wait)
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
                   value: str, message: str,
                   by: AppiumBy = AppiumBy.XPATH, wait: int = 60, scroll_to: bool = False,
                   intercepted_click: bool = False, after_send_tap: bool = False
                   ) -> None:
        """ Send your message"""

        xpath_elem: WebElement = self._click_element(
            value=value, by=by, wait=wait, scroll_to=scroll_to, intercepted_click=intercepted_click,
            return_xpath=True
        )

        xpath_elem.clear()
        xpath_elem.send_keys(str(message))

        # if after_send_tap:
        #     xpath_elem.send_keys("\uE007")

    def _action_touch_by_coord(self,
                               xpath_value: str,
                               x: int, y: int,
                               by: AppiumBy = AppiumBy.XPATH, wait: int = 60, scroll_to: bool = False):

        elem = self._elem_exists(value=xpath_value, by=by, wait=wait, scroll_to=scroll_to, return_xpath=True)
        act = TouchAction()
        act.press(elem).move_to(x=x, y=y).release()
