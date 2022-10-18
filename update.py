import requests
import logging
from my_project import db
from my_project.models import SportBot
from collections import defaultdict
import json
from my_project.db_connector import DbWriter
from sqlalchemy import update
import time



# check all the non revealed v2 bots (revealed=False) and if any have gotten revealed change them to (revealed=True)
class Update():

    def update_total_shares():
        sports = []
        values = []

        all_bots_from_db = SportBot.query.filter(SportBot.revealed==True).all()

        for bot in all_bots_from_db:
            print(bot.id)

            sports.append(bot.sport)
            values.append(bot.sportshares)

        my_dict = defaultdict(int)
        for k, v in zip(sports, values):
            my_dict[k] += v

        with open('totalShares1022.json', 'w') as fp:
            json.dump(my_dict, fp)

    
    def update_total_bots():

        sports = []

        all_bots_from_db = SportBot.query.filter(SportBot.revealed==True).all()

        for bot in all_bots_from_db:
            print(bot.id)
            sports.append(bot.sport)


        my_dict = {i:sports.count(i) for i in sports}

        print(my_dict) 


        with open('TEEEEST.json', 'w') as fp:
            json.dump(my_dict, fp)



    def update_stats(data):
        try:
            botToUpdate = SportBot.query.filter(SportBot.id == str(data)).first()
            print(botToUpdate)
            print(botToUpdate.revealed)
            botToUpdate.revealed = True
            db.session.commit()
        except:
            logging.exception("message")
            print("Error in update_stats")



    def check_unrevealed():
        v2_update_list = []
        unrevealed = SportBot.query.filter_by(revealed=False)

        for x in unrevealed:
            time.sleep(0)
            print(x)
            print(str(x.id - 1))

            url = "https://api.opensea.io/api/v1/assets?token_ids=" + str(x.id - 1) + "&collection=sportsbots&order_direction=desc&limit=1&include_orders=false"
            headers = {
                "Accept": "application/json",
                "X-API-KEY": ""
            }
            response1 = requests.request("GET", url, headers=headers)

            response = response1.json()

            token_id = response["assets"][-1]["token_id"]

            if response["assets"][0]["traits"] == []:
                pass
            else:
                # Update.update_stats(token_id)

                bot_data_dict = dict()
                traits = response["assets"][0]["traits"]

                bot_data_dict["name"] = response["assets"][0]["name"]
                bot_data_dict["image_url"] = response["assets"][0]["image_url"]
                for trait in traits:
                    bot_data_dict[trait["trait_type"]] = trait["value"]

                bot_data_dict = {k.lower(): v for k, v in bot_data_dict.items()}
                v2_update_list.append(bot_data_dict)
                print(v2_update_list)

        print(v2_update_list)
        # return a list of the changed v2 bots ( if non got revealed => list is empty )
        return v2_update_list

if __name__ == '__main__':
    # write the changed bots #numbers to update list
    # Update.check_unrevealed()
    # Update.update_total_shares()
    # Update.update_total_bots()

