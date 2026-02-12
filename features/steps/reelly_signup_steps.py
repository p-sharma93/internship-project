from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@given("Open the registration page")
def open_signup(context):
    context.driver.get("https://soft.reelly.io/sign-up")
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "Full-Name"))
    )


@when("I enter some test information into the registration fields")
def enter_signup_info(context):

    # Full Name
    context.driver.find_element(By.ID, "Full-Name").send_keys("test+priyanka+careerist")

    # Phone
    context.driver.find_element(By.ID, "phone2").send_keys("+971 test careerist")

    # Email
    context.driver.find_element(By.ID, "Email-3").send_keys("test@email.com")
    time.sleep(5)

@then("Verify the right information is present in the fields")
def verify_signup_info(context):

    expected_name = "test+priyanka+careerist"
    actual_name = context.driver.find_element(By.ID, "Full-Name").get_attribute("value")
    assert expected_name == actual_name, f"Expected {expected_name}, but got {actual_name}"

    expected_phone = "+971 test careerist"
    actual_phone = context.driver.find_element(By.ID, "phone2").get_attribute("value")
    assert expected_phone == actual_phone, f"Expected {expected_phone}, but got {actual_phone}"

    expected_email = "test@email.com"
    actual_email = context.driver.find_element(By.ID, "Email-3").get_attribute("value")
    assert expected_email == actual_email, f"Expected {expected_email}, but got {actual_email}"