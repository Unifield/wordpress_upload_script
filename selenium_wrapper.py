from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import copy, os


class SeleniumWrapper():
    def __init__(self, url, selector_dictionary=None, default_timeout=None, firefox_binary=None, highlight=False,
                 geckodriver="geckodriver_linux"):
        self.selector_dictionary = selector_dictionary
        self.default_timeout = default_timeout if default_timeout is not None else 30
        self.highlight = highlight
        self.driver = webdriver.Firefox(firefox_binary=firefox_binary, executable_path=geckodriver)

        self.driver.get(url)

    def get_driver(self):
        return self.driver

    def deinit(self):
        try:
            self.driver.quit()
        except:
            print("The driver couldn't be properly closed because of an unknown reason.")

    def find_element(self, locator, timeout=None, suppress_error=False):
        timeout = timeout if timeout is not None else self.default_timeout

        def unpack_locator(locator):
            if isinstance(locator, tuple):
                selector_type = locator[0]
                selector_definition = locator[1]
            elif isinstance(locator, str):
                if self.selector_dictionary is None:
                    raise AssertionError("The selector dictionary is empty")
                try:
                    selector_type = self.selector_dictionary(locator[0])
                    selector_definition = self.selector_dictionary(locator[1])
                except KeyError:
                    print("The string is not contained inside of the selector dictionary. Please check your inputs")
                    raise
            else:
                raise AssertionError("The locator is neither a string or a tuple. Please check your inputs")

            return selector_type, selector_definition

        def check_if_selector_is_allowed(selector_type):
            allowed_selector_types = ["id", "xpath", "link text", "partial link text", "name", "tag name", "class name",
                                      "css selector"]
            if selector_type not in allowed_selector_types:
                raise AssertionError("""
                Selector type is not allowed. The allowed selector types are:
                ["id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector"]
                """)

        def highlight(self, element):
            """
            Highlights a selenium webdriver element.
            """

            def apply_style(style, element):
                self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)

            apply_style("background: yellow; border: 2px solid red;", element)

        selector_type, selector_definition = unpack_locator(locator)

        check_if_selector_is_allowed(selector_type)

        # Wait for the element to appear
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((selector_type, selector_definition)))
        except TimeoutException:
            if suppress_error:
                return None
            else:
                print("Selenium timeout. The '{}' element is not visible even after waiting {}s".format(
                    selector_definition, timeout))
                raise

        # Get the element
        try:
            element = self.driver.find_element(selector_type, selector_definition)
        except NoSuchElementException:
            if suppress_error:
                return None
            else:
                print("The element with the definition of {}:'{}' cannot be found on the webpage".format(selector_type,
                                                                                                         selector_definition))
                raise

        if self.highlight:
            highlight(element)

        return element

    def get_action_chains(self):
        from selenium.webdriver import ActionChains
        return ActionChains(self.driver)

    def wait_for_element(self, locator):
        try:
            element = WebDriverWait(self.driver, timeout=30).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print("Loading took too much time!")
            raise
        else:
            return element
