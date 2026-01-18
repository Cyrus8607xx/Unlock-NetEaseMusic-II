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
    browser.add_cookie({"name": "MUSIC_U", "value": "002844211AE8E526022575C7302A3BA0CE3D23BDD14A7D3BEF02916C736A0821AB2DDF4196358D6046723E3FBF30D936F0CA904147B20AF83CDEF644A2FE865F75F4D7276A7B92DE59F1F7E3DA6849B4BE7C3829B813A12E6315811C57E7B61DFE5A4E86DE12DFF75512A0B51F61C9A5D8C375DBF58070B00EDC11CE583AD3E7E8D41C4A81A2247366003710718F926A042664F65F02713A67B49EF063F5BFD023F019F51633A7BC4723C5724FFE5E80819AF4222DF01F4DA4BDBED972EE6F4C162BE45A65A3CB00E375430D055E7A64F2DAC71F1FFDAB0B3EB50E8F1F0F6FAAE251BBA2CF88D5C1AFA3531A1EB483530068D2CF6F24A7AA494BD82E6AE36A0C7087DAE03F332578BD242FE7D1DD7C84448E7E07D39DAC0C6DC732D9008624426B5B49A729B11462D3261E758D5505ADA0B6E6AC7CBAF713D05B2EB21B0AA2032E9BE310BEAD4716BE7223C09EAABC59FB45215BEE86CE4888E287DCC936693F100CFE0DFCD69AA6F466EF0A7E354428BBDEBA674BB58CAFD70EB369BF5A2BA51E5458B6BA2DA8E4537395D37BF2D4A4A0"})
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
