import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from openpyxl import Workbook

BASE_URL = "http://yewu.ghzrzyw.beijing.gov.cn/gwxxfb/tdgltdcrjg/index.html"


def log_set(log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
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


# 解析每个条目的详情界面
def decode_subpage(tr_pages: list):
    title = ['受让方名称', '土地位置', '区县', '宗地面积（平方米）',
             '规划建筑面积（平方米）', '规划用地', '其它商服用地',
             '土地成交价（万元）', '宗地四至', '签约时间',
             '合同约定开工时间', '合同约定竣工时间', '容积率（地上）']
    content = []
    # go in
    for page in tr_pages:
        # time.sleep(555)
        page.find_element(By.CSS_SELECTOR, "td[data-field='tableBar'] div a").click()
        trs = []
        time.sleep(333)
        for msg in page.find_element(By.CSS_SELECTOR, "div[id='detailDiv'] table tbody").find_elements(By.ID, "tr"):
            # for msg in page.find_elements(By.CSS_SELECTOR, "table[class='layui-table.layui-text'] tbody tr"):
            print(msg.find_element(By.TAG_NAME, "td").text)
            # trs.append()


def main(year: int, key_word: str, headless_mode: bool = False):
    # set browser
    browser = set_driver(headless_mode=headless_mode)
    browser.get(BASE_URL)

    # set year
    time.sleep(2)
    logging.info("Send key word and year")
    browser.find_element(By.CSS_SELECTOR, "input[id='receivename']").send_keys(key_word)
    browser.find_element(By.CSS_SELECTOR, "input[id='year']").click()
    browser.find_element(By.CSS_SELECTOR, f"ul[class*='laydate-year-list'] li[lay-ym='{year}'").click()
    browser.find_element(By.CSS_SELECTOR, "div[class='laydate-footer-btns'] span").click()
    browser.find_element(By.CSS_SELECTOR, "button[data-type='reload']").click()

    # get all data
    tr_pages = browser.find_element(By.CSS_SELECTOR, "div.layui-tablist div[class*='layui-table-body'] table tbody").find_elements(By.CSS_SELECTOR, "tr")
    for tr_page in tr_pages:
        btn = tr_page.find_element(By.CSS_SELECTOR, "td[data-field='tableBar'] a")

        ActionChains(browser).move_to_element(btn).double_click(btn).perform()
        # tr_page.find_element(By.XPATH, '//a[text()="详情"]').click()
    # time.sleep(100)
    # for tr_page in tr_pages:
    #     tr_page.find_element(By.CSS_SELECTOR, "td[data-field='tableBar'] a").click()

    time.sleep(333)


if __name__ == '__main__':
    log_set(logging.INFO)
    main(year=2018, key_word="公司", headless_mode=False)

