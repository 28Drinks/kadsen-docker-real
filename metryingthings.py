from base64 import encode
from encodings import utf_8
from operator import index
from textwrap import indent
from tokenize import Special
from turtle import position
from unittest import result
import requests
import json
from lxml import html
from bs4 import BeautifulSoup
from helium import *

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import yaml
import time
from datetime import datetime

from sqlalchemy import Integer, insert, DateTime
from my_project import db
from my_project.models import Winner, Staker, Lotto, Jackpot, currentJackpot, currentLotto

from typing import Union

# log in data
# conf = yaml.load(open('loginDetails.yml'))
# myRBEmail = conf['rb_user']['email']
# myRBPassword = conf['rb_user']['password']

# CLASSSES for future use:

# css-czr64w => "96 of 100 BTC blocks mined  - Winner will be picked using hash of Bitcoin block #741630"

# css-1rzv8cf => div with btc bloks ( green ones, the already minted one => css-1a7sos8 [not minted ones => style: ["background: rgb(16, 18, 27); box-shadow: none;"])

# css-tf0u7e => div,"ALL BLOCKS HAVE BEEN MINTED, AND THE WINNER ARE..."
# if lottery is not running, the text changes to "Stake your rlb for a chance to win the lottery"

# css-1f9ay8i => h3 tag, above wheel, "Winner #XX - $0.00"
# css-1sdyziv => Lotto spinner wheel div


# Idee => Lottery, lottery. Stake togther and one gets all website :D

class DbWriter():
   @staticmethod
   def write_winner_data_to_db(data):
      for a in data:
         newWinner = Winner(
            position=a["position"],
            name=a["name"],
            amount=a["amount"],
            image=a["image"]
         )
         db.session.add(newWinner)
         db.session.commit()
   def write_staker_data_to_db(data):
      for a in data:
         newStaker = Staker(
            name=a["name"],
            amount=a["amount"],
            team=a["team"]
         )
         db.session.add(newStaker)
         db.session.commit()
   def write_current_stats_to_db(data):
      for key in data:
         updateLotto = currentLotto(
            number=key["number"],
            amount=key["amount"],
            at_time=key["at_time"]
         )
         updateJackpot = currentJackpot(
            jackpot_total=key["amount"],
            at_time=key["at_time"]
         )
         db.session.add(updateJackpot, updateLotto)
         db.session.commit()
   def write_lottery_data_to_db(data):
      for a in data:
         lottery = Lotto(
            number=a["number"],
            date=a["date"],
            amount=a["amount"],
            jackpot=a["jackpot"],
            prizes_won=a["prizes_won"],
            total_stake=a["total_stake"]
         )
         jackpots = Jackpot(
            jackpot_total=a["jackpot"],
            date=a["date"]
         )
         db.session.add(lottery, jackpots)
         db.session.commit()


class JsonWriter():
   @staticmethod
   def write_data_to_file(filename: str, data):
      with open(filename + '.json', 'w' , encoding="utf-8") as f:
         json.dump(data, f, ensure_ascii=False, indent=4)
         pass


class Rollbit():
   def __init__(self, validation_url: str, stakes_url: str, prev_winner_url: str, lottery_url: str, previous_lottery: str, driver: webdriver.Chrome):
      self.validation_url = validation_url
      self.stakes_url = stakes_url
      self.prev_winner_url = prev_winner_url
      self.lottery_url = lottery_url
      self.previous_lottery = previous_lottery
      self.driver = driver

   def validate(self):
      '''Visit website before calling stake url, otherwise not validated exception would be thrown.'''
      self.driver.get(self.validation_url)

      # get the #number for the current lottery as an int
   def get_lotto_number(self):
      self.driver.get(self.previous_lottery)
      self._block_until_found_element("css-751ivu")
      current_lotto_number = int(self.driver.find_element_by_class_name("css-751ivu").text[1:]) + 1

      return current_lotto_number

   # get the current count of mined btc blocks. Runns at 100
   def get_btc_count(self):
      self.driver.get(self.lottery_url)
      self._block_until_found_elements("css-1jje1nd")
      response_string = self.driver.find_element_by_class_name("css-1jje1nd").text
      current_count: int = response_string[0:2]
      print(current_count)
      return current_count

   # get the current lottery and jackpot value / price pool as a string
   def get_lottery_and_jackpot(self):
      print('get lottery stats')
      self.driver.get(self.lottery_url)
      self._block_until_found_elements("css-b5iyfx")
      lottery_and_jackpot_amount: list["WebElement"] = self.driver.find_elements_by_class_name("css-nr9v78")
      all_digits = ""
      # lotto_number = self.get_lotto_number()
      lotto_amount = ""
      jackpot_amount = ""

      for lot_jac in lottery_and_jackpot_amount:
         one_digit = lot_jac.text
         all_digits += one_digit

      lotto_amount += all_digits[:-6]
      jackpot_amount += all_digits[-6:]

      now = datetime.now()

      current_lotto_data = {
         "number": int(lotto_number),
         "amount": int(lotto_amount),
         "at_time": now
      }
      current_jackpot_data = {
         "at_time": now,
         "amount": int(jackpot_amount)
      }
      return current_lotto_data, current_jackpot_data

   # get the total amout of currently staked RLB
   def get_total_staked(self):
      self.driver.get(self.lottery_url)
      self._block_until_found_element("css-ccnumj")
      total_staked_amount = self.driver.find_element_by_class_name("css-ccnumj").text
      print(total_staked_amount)
      return total_staked_amount

   # returns a: total RLB supply left. b: total RLB burned. Both as a string
   def get_total_supply_and_burn(self):
      self.driver.get(self.lottery_url)
      self._block_until_found_element("css-fkvr3n")
      find_both = self.driver.find_elements_by_class_name("css-fkvr3n")
      amount = ""
      for x in find_both:
         amount += x.text
      split_string = amount.split('RLB')
      total_supply_left = split_string[0]
      total_burned = split_string[1]

      return total_supply_left, total_burned

   # find last 99 Lotterys data (+ jackpot)
   def get_last_lotto_data_v2(self):
      self.driver.get(self.previous_lottery)
      self._block_until_found_element("css-1c8jobn")

      lotto_list: list["WebElement"]  = self.driver.find_elements_by_class_name("css-1c8jobn")
      parsed_lotto_list = []

      i = 1
      for lotto_element in lotto_list:
         print("finding elements")
         print(i)
         number: str = lotto_element.find_element_by_xpath("(//tr[" + str(i) + "]/td[" + str(1) +"][@class='css-751ivu'])").text
         date: str = lotto_element.find_element_by_xpath("(//tr[" + str(i) + "]/td[" + str(2) +"][@class='css-751ivu'])").text

         amount: str = lotto_element.find_element_by_xpath("(//tr[" + str(i) + "]/td[" + str(3) +"][@class='css-1t3xppg'])").text
         jackpot: str = lotto_element.find_element_by_xpath("(//tr[" + str(i) + "]/td[" + str(4) +"][@class='css-1t3xppg'])").text
         prizes_won: str = lotto_element.find_element_by_xpath("(//tr[" + str(i) + "]/td[" + str(5) +"][@class='css-1t3xppg'])").text
         total_stake: str = lotto_element.find_element_by_xpath("(//tr[" + str(i) + "]/td[" + str(6) +"][@class='css-1t3xppg'])").text

         specialChars = "#"
         for specialChar in specialChars:
            index_key_x: int = number.replace(specialChar,'')
         index_key: int = index_key_x

         print(f"[LOTTERY] Found {number} - {amount} - {index_key} - {date}")
         parsed_lotto_list.append({ "number": number, "date": date, "amount": amount, "jackpot": jackpot, "prizes_won": prizes_won, "total_stake": total_stake, "index_key": index_key})
         i += 1

      return parsed_lotto_list


   # get all stakers data
   def get_staker_data_v2(self):
      print('Get Stakes URL')
      self.driver.get(self.stakes_url)
      self._block_until_found_elements("css-899asd")
      self._block_until_found_element("css-7o6tkw")

      show_more_btn_visible = True

      while show_more_btn_visible:
         try:
            print('Trying to get "show more" button')
            show_more_btn = self.driver.find_element_by_class_name("css-7o6tkw")
            print('Clicking "show more" button')
            self.driver.execute_script("arguments[0].click();", show_more_btn)
            self._block_until_found_element("css-7o6tkw", timeout=2)
         except NoSuchElementException:
            print('Cannot find "show more" button')
            show_more_btn_visible = False
            # tiny error, this will also fail if not enough people have staked for a "show more button" to exist.

      print('Select all stakers')
      staker_list: list["WebElement"]  = self.driver.find_elements_by_class_name("css-899asd")
      parsed_staker_list = []

      for staker_element in staker_list:
         name: str = staker_element.find_element_by_class_name("css-u419s0").text
         amount: str = staker_element.find_element_by_class_name("css-rc8k8e").text
         number: int = lotto_number
         team = ''

         team_element = self._get_team_element(staker_element, yellow_tag_class_name="css-12dsv6w", gray_tag_class_name="css-1sagzet")

         if team_element:
            team = team_element.text

            if team == '':
               print(f'{name} with {amount} has an empty team')

            if name.startswith(team) and team != '':
               name = name.split(team, 1)[1]

         print(f"[STAKER] Found {name} - {amount}")

         parsed_staker_list.append({'name': name, 'amount': amount, 'lotto_number': number, 'team': team,})

      return parsed_staker_list





   # get all 100 winners data
   def get_prev_winner_data(self):
      print('Get Winner URL')
      self.driver.get(self.prev_winner_url)
      self._block_until_found_elements("css-3p82s6")

      winner_list: list["WebElement"]  = self.driver.find_elements_by_class_name("css-3p82s6")

      parsed_winner_list = []

      for winner_element in winner_list:
         position = winner_element.find_element_by_class_name("css-114zf33").text
         name = winner_element.find_element_by_class_name("css-1ko6wxu").text
         amount = winner_element.find_element_by_class_name("css-rc8k8e").text
         image = winner_element.find_element_by_tag_name("img").get_attribute("src")
         number = lotto_number - 1
         team = ''

         team_element = self._get_team_element(winner_element, yellow_tag_class_name="css-12dsv6w", gray_tag_class_name="css-1sagzet")

         if team_element:
            team = team_element.text

            if team == '':
               print(f'{name} with {amount} has an empty team')

            if name.startswith(team) and team != '':
               name = name.split(team, 1)[1]


         print(f"[WINNER] Found {position} - {name} - {amount}")

         parsed_winner_list.append({'position': position, 'name': name,'amount': amount, "lotto_number": number, "image": image, "team": team})

      return parsed_winner_list


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

   def _block_until_found_elements(self, class_name: str, timeout: int = 10):
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



   def _block_until_found_element(self, class_name: str, timeout: int = 10):
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







if __name__ == '__main__':
   # web driver settings
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   options.add_experimental_option("excludeSwitches", ["enable-logging"])

   driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\28Drinks\Desktop\Test_Roll\chromedriver.exe')

   try:
      rollbit = Rollbit(validation_url="https://rollbit.com/validate", stakes_url="https://rollbit.com/rlb/lottery/stakes", prev_winner_url='https://rollbit.com/rlb/lottery/current', lottery_url='https://rollbit.com/rlb/lottery/current', previous_lottery='https://rollbit.com/rlb/lottery/previous', driver=driver)
      rollbit.validate()
      lotto_number = rollbit.get_lotto_number()
      # rollbit.get_lottery_and_jackpot()
      # rollbit.get_total_staked()
      # rollbit.get_total_supply_and_burn()
      # rollbit.get_last_lotto_data_v2()
      # rollbit.get_btc_count()
   #write to json file
      # JsonWriter.write_data_to_file('data', rollbit.get_staker_data_v2())
      # JsonWriter.write_data_to_file('winner', rollbit.get_prev_winner_data())
      # JsonWriter.write_data_to_file('amounts', rollbit.get_lottery_and_jackpot())
   #write to db
      # DbWriter.write_winner_data_to_db(rollbit.get_prev_winner_data())
      # DbWriter.write_staker_data_to_db(rollbit.get_staker_data_v2())
      # DbWriter.write_lottery_data_to_db(rollbit.get_last_lotto_data_v2())
      DbWriter.write_current_stats_to_db(rollbit.get_lottery_and_jackpot())
   finally:
      driver.quit()



# # main function / scrape & format data from Rollbit Lottery
# def login(url, url_2, login_buttonId ,usernameId, username, passwordId, password, submit_buttonId):
#    # open base url
#    driver.get(url)
#    time.sleep(10)
#    # find log in button
#    driver.find_element_by_class_name(login_buttonId).click()
#    time.sleep(1)
#    # enter username / password
#    driver.find_element_by_name(usernameId).send_keys(username)
#    driver.find_element_by_name(passwordId).send_keys(password)
#    time.sleep(5)
#    # log in
#    driver.find_element_by_class_name(submit_buttonId).click()
#    time.sleep(5)
#    # open second url and get all staker data
#    driver.get(url_2)
#    body_html = driver.find_element_by_xpath("/html/body/pre")
#    data = body_html.get_attribute("innerHTML")

#    # create stakers 'data' json and write to it
#    results_staker = json.loads(data)

#    with open('data.json', 'w' , encoding="utf-8") as f:
#       json.dump(results_staker, f, ensure_ascii=False, indent=4)

#    time.sleep(5)
#    # open third url to scrape winner data
#    driver.get(url_3)
#    time.sleep(5)

#    # get number , name , amount ( jackpot) data
#    data_nr = driver.find_elements_by_class_name("css-114zf33") #list?
#    data_name = driver.find_elements_by_class_name("css-1ko6wxu")
#    data_amount = driver.find_elements_by_class_name("css-rc8k8e")
#    jackpot = driver.find_elements_by_class_name("css-1toon3p")

#    # list of the 100 winners (+jackpot)
#    winnerList = []

#    # check if jackpot won and if, append to "winnerList"
#    jackpot_text = []
#    for i in jackpot:
#       jackpot_text.append(i.text)

#    if jackpot_text != []:
#       print("jackpot won")
#       winnerList.append(jackpot_text)
#    else:
#       print("no jackpot won")
#       pass

#    # create list's for scraped winner data
#    values_nr = []
#    values_name = []
#    values_amount = []

#    # loop over scraped winner data & append to lists above
#    for i in data_nr:
#       values_nr.append(i.text)
#    for i in data_name:
#       values_name.append(i.text)
#    for i in data_amount:
#       values_amount.append(i.text)

#    # loop over the lists created above and create a dict for each winner
#    # and append to winnerList
#    keys = range(100)

#    for key in keys:
#       winnerDict = {}
#       winnerDict['key'] = key
#       winnerDict['number'] = values_nr[key]
#       winnerDict['name'] = values_name[key]
#       winnerDict['amount'] = values_amount[key]
#       winnerList.append(winnerDict)

#    # create and write list to json 'winner' file
#    with open('winner.json', 'w' , encoding="utf-8") as f:
#       json.dump(winnerList, f, ensure_ascii=False, indent=4)

#    driver.quit()

# # call main function with arguments
# login("https://rollbit.com", "https://rollbit.com/public/lottery/stakes/current", "css-1wkotyo", "email", myRBEmail, "password", myRBPassword, "css-abwl8h" )



   # #28s try
   # def get_all_elements(self, data_elements_class):
   #    data_list: list["WebElement"]  = self.driver.find_elements_by_class_name(data_elements_class)
   #    return data_list

   # #28s  try
   # def loop_data_list(self, data_list, position_class: str, name_class: str, amount_class: str, team_class: str ):

   #    parsed_data_list  = []

   #    for data_element in data_list:
   #       position = data_element.find_element_by_class_name(position_class).text
   #       name = data_element.find_element_by_class_name(name_class).text
   #       amount = data_element.find_element_by_class_name(amount_class).text
   #       team = ''

   #       print(f"[WINNER] Found {position} - {name} - {amount} - {team}")

   #       parsed_data_list.append({'position': position, 'name': name,'amount': amount, 'team': team})

   #    return parsed_data_list
   # #28s try
   # def winner(self):
   #    data_elements_class = "css-3p82s6"
   #    position_class = "css-114zf33"
   #    name_class = "css-1ko6wxu"
   #    amount_class = "css-rc8k8e"
   #    team_class = ""
   #    self.driver.get(self.prev_winner_url)
   #    self._block_until_found_elements(data_elements_class)

   #    winner_list = self.get_all_elements(data_elements_class)
   #    parsed_winner_list = self.loop_data_list(
   #       data_list=winner_list, position_class=position_class, name_class=name_class, amount_class=amount_class, team_class=team_class
   #       )
   #    return parsed_winner_list




   #stuff lol

   # get the last (finished) lottery data
   # def get_last_lotto_data(self):
   #    self.driver.get(self.previous_lottery)
   #    self._block_until_found_element("css-1t3xppg")

   #    last_lotto_number = int(self.driver.find_element_by_class_name("css-751ivu").text[1:])
   #    last_lotto_value_str = self.driver.find_element_by_class_name("css-1t3xppg").text

   #    specialChars = "$K"
   #    for specialChar in specialChars:
   #       last_lotto_value_str = last_lotto_value_str.replace(specialChar,'')
   #    last_lotto_value =last_lotto_value_str
   #    print(last_lotto_value)
   #    return last_lotto_number, last_lotto_value

   # def get_staker_data(self):
   #    self.driver.get(self.stakes_url)
   #    body_html = self.driver.find_element_by_xpath("/html/body/pre")
   #    data = body_html.get_attribute("innerHTML")

   #    # create stakers 'data' json and write to it
   #    print(data)
   #    return json.loads(data)
