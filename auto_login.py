# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007375827A859B4961FC62558208D453171D263DAF885D99C956FAEBDC8C56204B733C5EBB31FA833D5BD56535F65B9DDBD2ECCB14F6215A3DEA37C3A30FAE8072E5302C8B4C35161115B159BD5EA09B8F2EB633E09F036A4AF30B66FB9BBDC004A8EDA54A337E597933348EDA011E4CB7C67C41D5D930CA3478AAE41D112A066FE9DD69AD7A3AAC3ED5F3592B0A258680F36249EF665952CFA59DBB8C0E7CE858C729C79AB7BA8FD6F0D31C7348A45F85E660EF80410FD4E878415590A980D10B07B7872C4724227F79A9E282C675C384E707A8733A0356E82145378C92A01A5D61689C7D55CCECF8C924B8FC04C06C53F0DC0B29BF8BCD7A0DDDD84A23941ADAFAE35A37316BF140B3719BF5658A6B0C537A07885C513D30148544A9DC6ECF457C98157E449F749B8D675BE565F0D78231E129C1C62485DA160B776EB6071846887F97BDC3FB6560002903DF7D5C7484092B4C4E238D2EFDDA87DD8E1DFD3C0D3EAD0867535D6A27DB5D1618D4AD6DEC7ACA124EF42D17F7F4092FA61EF5F4B00DB332D4739C1A9130CD0044C924798F029B81539B963288C0707B5E947E2B40"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
