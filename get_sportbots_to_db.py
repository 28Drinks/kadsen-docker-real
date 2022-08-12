
from selenium import webdriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException
import time
import json

from sqlalchemy import Integer, insert, DateTime
from my_project import db
from my_project.models import SportsBots

class DbWriter():
   @staticmethod
   def write_sportsbots_to_db(data):
      for a in data:
         newBot = SportsBots(
            image=a["image"],
            name=a["name"],
            display_share=a["display_share"],
            bet=a["bet"],
            token_id=a["token_id"],
            price=a["price"],
            roi=a["roi"]
         )
         db.session.add(newBot)
         db.session.commit()

class Rollbit():
    def __init__(self, validation_url: str, sportsbots_url: str, driver: webdriver.Chrome):
        self.validation_url = validation_url
        self.sportsbots_url = sportsbots_url
        self.driver = driver

    def validate(self):
        '''Visit website before calling stake url, otherwise not validated exception would be thrown.'''
        self.driver.get(self.validation_url)
        time.sleep(1)

    def get_sportsbots(self):
        self.driver.get(self.sportsbots_url)
        bots_list_str = self.driver.find_element_by_xpath("/html/body/pre").text
        print(bots_list_str)
        bots_list = json.loads(bots_list_str)

        bot_list = []

        x = 0

        for bot in bots_list:
            x += 1
            print(x)
            name = bot["nft"]["sportsbot"]["name"]
            image = bot["nft"]["sportsbot"]["image_url"]
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

            bot_list.append({'image': image, 'display_share': display_share, 'bet': bet, "name": name, "price": price, "token_id": token_id, "roi": roi})

        driver.quit()

        return bot_list


if __name__ == '__main__':
    # web driver settings
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\28Drinks\Desktop\Test_Roll\chromedriver.exe')

    try:
        rollbit = Rollbit(validation_url="https://rollbit.com/", sportsbots_url="https://rollbit.com/public/nft/marketplace?collection=eth%3A0x1de7abda2d73a01aa8dca505bdcb773841211daf&direction=asc&limit=3000&sort=price", driver=driver)
        rollbit.validate()
        DbWriter.write_sportsbots_to_db(rollbit.get_sportsbots())
    finally:
      driver.quit()