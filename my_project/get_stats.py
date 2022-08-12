
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import time


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\28Drinks\Desktop\Test_Roll\chromedriver.exe')

def _block_until_found_elements(class_name: str, timeout: int = 10):
    print(f'Starting to block, Trying to find elements with class name {class_name}')
    found = False
    start_time = time.time()

    while not found:
        if len(driver.find_elements_by_class_name(class_name)):
            found = True
        else:
            if time.time() - start_time >= timeout:
                print(f'Cannot find element by class name {class_name}. Timing out...')
                raise NoSuchElementException
            print(f'Cannot find elements by class name {class_name}. Continue blocking...')
            time.sleep(0.5)


def get_stats():
    lottery_url = "https://rollbit.com/rlb/lottery/current"
    driver.get(lottery_url)
    _block_until_found_elements("css-nr9v78")
    lottery_and_jackpot_amount: list[WebElement] = driver.find_elements_by_class_name("css-nr9v78")
    all_digits = ""
    lotto_amount = ""
    jackpot_amount = ""

    for lot_jac in lottery_and_jackpot_amount:
        one_digit = lot_jac.text
        all_digits += one_digit

    lotto_amount += all_digits[:-6]
    jackpot_amount += all_digits[-6:]

    _block_until_found_elements("css-1jje1nd")
    response_string = driver.find_element_by_class_name("css-1jje1nd").text
    current_count: int = response_string[0:2]

    driver.quit()

    return lotto_amount,jackpot_amount,current_count
