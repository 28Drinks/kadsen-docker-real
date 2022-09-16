from selenium import webdriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException
import time
import json
from sqlalchemy import Integer, insert, DateTime
from datetime import date

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from my_project.db_connector import DbWriter


class Rollbit():

    #  static block-till-element-found
    @staticmethod
    def _get_team_element(element: WebElement, yellow_tag_class_name: str, gray_tag_class_name: str):
        yellow_tag_element: Union[WebElement, None] = None
        gray_tag_element: Union[WebElement, None] = None
        try:
            yellow_tag_element = element.find_element_by_class_name(yellow_tag_class_name)
        except NoSuchElementException:
            pass

        try:
            gray_tag_element = element.find_element_by_class_name(gray_tag_class_name)
        except NoSuchElementException:
            pass

        return yellow_tag_element or gray_tag_element

    def _block_until_found_elements(self, class_name: str, timeout: int = 60):
        print(f'Starting to block, Trying to find elements with class name {class_name}')
        found = False
        start_time = time.time()

        while not found:
            if len(self.driver.find_elements_by_class_name(class_name)):
                found = True
            else:
                if time.time() - start_time >= timeout:
                    print(f'Cannot find element by class name {class_name}. Timing out...')
                    raise NoSuchElementException
                print(f'Cannot find elements by class name {class_name}. Continue blocking...')
                time.sleep(0.5)



    def _block_until_found_element(self, class_name: str, timeout: int = 30):
        print(f'Starting to block, Trying to find element with class name {class_name}')
        found = False
        start_time = time.time()

        while not found:
            try:
                self.driver.find_element_by_class_name(class_name)
                found = True
            except NoSuchElementException:
                if time.time() - start_time >= timeout:
                    print(f'Cannot find element by class name {class_name}. Timing out...')
                    raise NoSuchElementException
                print(f'Cannot find element by class name {class_name}. Continue blocking...')
                time.sleep(0.5)


    #  starts here!
    def __init__(self, validation_url: str, url: str, driver: webdriver.Chrome):
        self.validation_url = validation_url
        self.url = url
        self.driver = driver

    def validate(self):
        '''Visit website before calling stake url, otherwise not validated exception would be thrown.'''
        self.driver.get(self.validation_url)
        time.sleep(1)

    def get_sportsbots_profit(self):
        url_list = [
            "24",
            "15",
            "18",
            "39",
            "5",
            "109",
            "57",
            "45",
            "25",
            "10",
            "375",
            "155",
            "376",
            "2",
            "14",
            "558",
            "289",
            "336",
            "68",
            "120",
            "64",
            "713",
            "261",
            "1170",
            "87",
            "214",
            "689",
            "3",
            "99",
            "854",
            "911",
            "680"
        ]
        sport_list = []
        value_list = []
        for number in url_list:
            print(number)
            self.driver.get(self.url + number)

            self._block_until_found_elements("css-3v97he")

            data = self.driver.find_elements_by_class_name("css-3v97he")
            for x in data:
                all = x.find_element_by_class_name("css-1s77kt0").text
                if all == "Sport":
                    sport = x.find_element_by_class_name("css-unm689").text
            print(sport)

            self._block_until_found_element("css-15cgovt")

            unformatted_share = self.driver.find_element_by_class_name("css-15cgovt").text
            value_striped = unformatted_share.replace('$','')
            value = "{:.2f}".format(float(value_striped))
            print(value)
            time.sleep(1)

            sport_list.append(sport)
            value_list.append(value)

        #special
        self.driver.get(self.url + "132")
        sport = "Special"
        unformatted_share = self.driver.find_element_by_class_name("css-15cgovt").text
        value_striped = unformatted_share.replace('$','')
        value = "{:.2f}".format(float(value_striped))
        sport_list.append(sport)
        value_list.append(value)

        sport_value_dict = dict(zip(sport_list, value_list))

        return sport_value_dict

if __name__ == '__main__':

    # web driver settings
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\28Drinks\Desktop\Test_Roll\chromedriver.exe')
    today = date.today()

    try:
        rollbit = Rollbit(validation_url="https://rollbit.com/", driver=driver, url="https://rollbit.com/nft/eth:0x1de7abda2d73a01aa8dca505bdcb773841211daf/")
        rollbit.validate()
        my_dict = rollbit.get_sportsbots_profit()

        with open('valueShares.json', 'w') as fp:
            json.dump(my_dict, fp)

        calculated_dict = {}

        with open('valueShares.json') as f:
            value = json.load(f)

        with open('totalShares.json') as s:
            quantity = json.load(s)

        for key in quantity:
            q = quantity[key]
            v = float(value[key])
            v2 = float("{:.2f}".format(v))

            calculated_dict[key] = round((q * v), 2)

        total = 0
        for x in calculated_dict:
            total += float(calculated_dict[x])
        calculated_dict["total"] = total

        DbWriter.write_share_data_to_db(calculated_dict)

    finally:
      driver.quit()