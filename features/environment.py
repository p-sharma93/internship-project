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
    Supports:
    - Chrome
    - Firefox
    - Headless
    - BrowserStack remote execution
    """
    # Check if BrowserStack mode is enabled
    if os.getenv("BROWSERSTACK") == "true":
        browserstack_init(context)
        return

    # Local browser setup
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


def browserstack_init(context):
    """
    Initialize BrowserStack remote browser
    """

    bs_username = os.getenv("BROWSERSTACK_USERNAME")
    bs_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

    if not (bs_username and bs_access_key):
        raise ValueError(
            "BrowserStack credentials not found! "
        )

    capabilities = {
      "browserName": "chrome",
        "browserVersion": "latest",

        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",

            "sessionName": "Reelly Signup Test",
            "buildName": "Internship Automation Run",

            "debug": True,
            "consoleLogs": "verbose",
            "networkLogs": True

        }
    }

    url = f'https://{bs_username}:{bs_access_key}@hub-cloud.browserstack.com/wd/hub'

    context.driver = webdriver.Remote(
        command_executor=url,
        options=webdriver.ChromeOptions()
    )

    context.driver.implicitly_wait(10)
    print(f"\nBrowserStack session started successfully")


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
    print("\nBrowser closed successfully!")