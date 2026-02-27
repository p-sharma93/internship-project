import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def browser_init(context, scenario_name):
    """
    Initializes browser based on environment variables.

    Supported:
    - Local Chrome
    - Local Firefox
    - Headless mode
    - Mobile emulation (Chrome)
    - BrowserStack desktop
    - BrowserStack real mobile
    """


    #BROWSERSTACK

    if os.getenv("BROWSERSTACK") == "true":
        bs_username = os.getenv("BROWSERSTACK_USERNAME")
        bs_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

        if not bs_username or not bs_access_key:
            raise ValueError("BrowserStack credentials not set!")

        url = f"https://{bs_username}:{bs_access_key}@hub-cloud.browserstack.com/wd/hub"

        options = ChromeOptions()

        # Desktop
        if os.getenv("BS_MOBILE") != "true":
            options.set_capability("browserName", "chrome")
            options.set_capability("browserVersion", "latest")
            options.set_capability("bstack:options", {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": scenario_name,
                "buildName": "Internship Automation Run",
                "debug": True,
                "consoleLogs": "verbose",
                "networkLogs": True
            })

        # Mobile
        else:
            options.set_capability("browserName", "chrome")
            options.set_capability("bstack:options", {
                "deviceName": "Samsung Galaxy S23",
                "realMobile": True,
                "osVersion": "13.0",
                "sessionName": scenario_name,
                "buildName": "Internship Automation Run",
                "debug": True
            })

        context.driver = webdriver.Remote(
            command_executor=url,
            options=options
        )

        context.driver.implicitly_wait(10)
        context.driver.wait = WebDriverWait(context.driver, 10)

        print("\n BrowserStack session started")
        return

    # LOCAL BROWSER MODE
    browser = os.getenv("BROWSER", "chrome")

    if browser == "chrome":
        options = ChromeOptions()

        # Mobile Emulation (Local)
        if os.getenv("MOBILE") == "true":
            device_name = os.getenv("MOBILE_DEVICE", "iPhone 12 Pro")
            mobile_emulation = {"deviceName": device_name}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            print(f"\n Mobile emulation: {device_name}")

        # Headless
        if os.getenv("HEADLESS") == "true":
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()

        if os.getenv("HEADLESS") == "true":
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        context.driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    context.driver.maximize_window()
    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 10)

    print(f"\n Local {browser} browser started")

#Behave

def before_scenario(context, scenario):
    print("\nStarted scenario:", scenario.name)
    browser_init(context, scenario.name)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
        print("\n Browser closed")


def before_step(context, step):
    print("Started step:", step.name)


def after_step(context, step):
    if step.status == "failed":
        print("Step failed:", step.name)