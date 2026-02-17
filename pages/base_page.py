from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Base class for all page objects.
    Contains common methods like click, input_text, wait, etc.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)

    def find_element(self, *locator):
        """Find a single element"""
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        """Find multiple elements"""
        return self.driver.find_elements(*locator)

    def click(self, *locator):
        """Click on an element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self, text, *locator):
        """Enter text into an input field"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def clear_and_input_text(self, text, *locator):
        """Clear field and enter text"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, *locator):
        """Get text from an element"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def get_attribute(self, attribute_name, *locator):
        """Get attribute value from an element"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.get_attribute(attribute_name)

    def wait_for_element_visible(self, *locator):
        """Wait for element to be visible"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, *locator):
        """Wait for element to be clickable"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_disappear(self, *locator):
        """Wait for element to disappear"""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url

    def verify_url_contains(self, expected_url_part):
        """Verify URL contains expected text"""
        current_url = self.get_current_url()
        assert expected_url_part.lower() in current_url.lower(), \
            f"Expected '{expected_url_part}' to be in URL, but got '{current_url}'"

    def verify_partial_url(self, expected_partial_url):
        """Verify partial URL"""
        actual_url = self.driver.current_url
        assert expected_partial_url in actual_url, \
            f"Expected '{expected_partial_url}' to be in '{actual_url}'"

    def verify_text(self, expected_text, *locator):
        """Verify element contains expected text"""
        actual_text = self.get_text(*locator)
        assert expected_text == actual_text, \
            f"Expected '{expected_text}', but got '{actual_text}'"

    def verify_attribute_value(self, expected_value, attribute_name, *locator):
        """Verify element attribute has expected value"""
        actual_value = self.get_attribute(attribute_name, *locator)
        assert expected_value == actual_value, \
            f"Expected '{expected_value}', but got '{actual_value}'"
