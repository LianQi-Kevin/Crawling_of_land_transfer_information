import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://yewu.ghzrzyw.beijing.gov.cn/gwxxfb/tdgltdcrjg/index.html"


def log_set(Log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(Log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(Log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# download chrome driver and use it
def set_driver(headless_mode: bool = True) -> webdriver.Chrome:
    """
    :param headless_mode: Whether to use headless mode
    """
    options = Options()
    if headless_mode:
        logging.info("Use headless mode")
        options.add_argument('headless')
    return webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


# 检查元素是否存在
def check_element_exists(driver: webdriver.Chrome, element: str, find_model=By.CLASS_NAME) -> bool:
    """
    :param driver: browser drive
    :param element: WebElement
    :param find_model: The selenium locator, default By.CLASS_NAME
    :return: bool, whether the element exists
    """
    try:
        driver.find_element(find_model, element)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    browser = set_driver(headless_mode=False)
    browser.get(BASE_URL)

