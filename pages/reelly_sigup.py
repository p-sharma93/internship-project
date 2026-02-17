from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class ReallySignupPage(BasePage):

    # LOCATORS
    FULL_NAME_INPUT = (By.ID, "Full-Name")
    PHONE_INPUT = (By.ID, "phone2")
    EMAIL_INPUT = (By.ID, "Email-3")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://soft.reelly.io/sign-up"

    def open_signup_page(self):
        """Navigate to Reelly signup page and wait for it to load"""
        self.open_url(self.url)
        self.wait_for_element_visible(*self.FULL_NAME_INPUT)

    def enter_full_name(self, name):
        """
        Enter full name in the signup form
        Args:
            name: Full name to enter
        """
        self.input_text(name, *self.FULL_NAME_INPUT)

    def enter_phone(self, phone):
        """
        Enter phone number in the signup form
        Args:
            phone: Phone number to enter
        """
        self.input_text(phone, *self.PHONE_INPUT)

    def enter_email(self, email):
        """
        Enter email in the signup form
        Args:
            email: Email address to enter
        """
        self.input_text(email, *self.EMAIL_INPUT)
        time.sleep(5)  # Wait for form validation/processing

    def fill_signup_form(self, name, phone, email):
        """
        Complete method to fill entire signup form
        Args:
            name: Full name
            phone: Phone number
            email: Email address
        """
        self.enter_full_name(name)
        self.enter_phone(phone)
        self.enter_email(email)

    def get_full_name_value(self):
        """Get the current value of the full name field"""
        return self.get_attribute("value", *self.FULL_NAME_INPUT)

    def get_phone_value(self):
        """Get the current value of the phone field"""
        return self.get_attribute("value", *self.PHONE_INPUT)

    def get_email_value(self):
        """Get the current value of the email field"""
        return self.get_attribute("value", *self.EMAIL_INPUT)

    def verify_full_name(self, expected_name):
        """
        Verify the full name field contains expected value
        Args:
            expected_name: Expected name in the field
        """
        self.verify_attribute_value(expected_name, "value", *self.FULL_NAME_INPUT)

    def verify_phone(self, expected_phone):
        """
        Verify the phone field contains expected value
        Args:
            expected_phone: Expected phone number in the field
        """
        self.verify_attribute_value(expected_phone, "value", *self.PHONE_INPUT)

    def verify_email(self, expected_email):
        """
        Verify the email field contains expected value
        Args:
            expected_email: Expected email in the field
        """
        self.verify_attribute_value(expected_email, "value", *self.EMAIL_INPUT)

    def verify_all_signup_info(self, name, phone, email):
        """
        Verify all signup fields contain expected values
        Args:
            name: Expected full name
            phone: Expected phone number
            email: Expected email
        """
        self.verify_full_name(name)
        self.verify_phone(phone)
        self.verify_email(email)