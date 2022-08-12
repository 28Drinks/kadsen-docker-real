
from selenium import webdriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException
import time
import json


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\28Drinks\Desktop\Test_Roll\chromedriver.exe')

# def validate():
#     lottery_url = "https://rollbit.com/rlb/lottery/current"
#     driver.get(lottery_url)
#     time.sleep(2)


def get_sportbots():
    lottery_url = "https://rollbit.com/rlb/lottery/current"
    driver.get(lottery_url)
    time.sleep(2)
    sportbots_url = "https://rollbit.com/public/nft/marketplace?collection=eth%3A0x1de7abda2d73a01aa8dca505bdcb773841211daf&direction=asc&limit=3000&sort=price"
    driver.get(sportbots_url)
    bots_list_str = driver.find_element_by_xpath("/html/body/pre").text
    bots_list = json.loads(bots_list_str)

    paresd_bot_list = []
    x = 0

    for bot in bots_list:
        x += 1
        print(x)
        name = bot["nft"]["sportsbot"]["name"]
        img = bot["nft"]["sportsbot"]["image_url"]
        share = bot["nft"]["sportsbot"].get("sportsbook_profit", 0.0)
        # share = int(float(unformated_share))
        # formated_share = "{:.2f}".format(unformated_share)
        # share = int(formated_share)
        bet = bot["nft"]["sportsbot"].get("freebet_amount", 0)
        # sport = bot["nft"]["sportsbot"][traits].get("sport")
        # body = bot["nft"]["sportsbot"][traits].get("body")
        token_id = bot["nft"].get("token_id")
        price = bot["listed_price"]

        yearly_return: int = share * 12 + bet * 12 / 2
        unformated_roi: int = yearly_return / ( price / 100)

        roi: int = "{:.2f}".format(unformated_roi)
        display_share = "{:.2f}".format(share)

        paresd_bot_list.append({'img': img, 'share': display_share, 'bet': bet, "name": name, "price": price, "token_id": token_id, "roi": roi})

    driver.quit()

    return paresd_bot_list
