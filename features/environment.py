import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def browser_init(context):
    """
    Initialize browser based on BROWSER variable.
    Default = Chrome
    """

    browser = os.getenv("BROWSER", "chrome")


    if browser == "chrome":
        options = webdriver.ChromeOptions()

        # Headless mode option
        if os.getenv("HEADLESS") == "true":
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=service, options=options)



    elif browser == "firefox":
        options = webdriver.FirefoxOptions()

        # Headless mode option
        if os.getenv("HEADLESS") == "true":
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        context.driver = webdriver.Firefox(service=service, options=options)



    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Basic setup
    context.driver.maximize_window()
    context.driver.implicitly_wait(2)




def before_scenario(context, scenario):
    print("\nStarted scenario:", scenario.name)
    browser_init(context)


def before_step(context, step):
    print("\nStarted step:", step.name)


def after_step(context, step):
    if step.status == "failed":
        print("\nStep failed:", step.name)


def after_scenario(context, scenario):
    context.driver.quit()