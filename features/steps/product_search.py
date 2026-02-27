from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then


SEARCH_INPUT = (By.NAME, 'q')


@given('Open Google page')
def open_google(context):
    context.driver.get('https://www.google.com/')


@when('Input {search_word} into search field')
def input_search(context, search_word):
    wait = WebDriverWait(context.driver, 10)

    search = wait.until(EC.visibility_of_element_located(SEARCH_INPUT))

    search.clear()
    search.send_keys(search_word)
    search.send_keys(Keys.RETURN)


@then('Product results for {search_word} are shown')
def verify_found_results_text(context, search_word):
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.url_contains(search_word))

    assert search_word.lower() in context.driver.current_url.lower(), \
        f'Expected query not in {context.driver.current_url.lower()}'
