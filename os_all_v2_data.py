import requests
from collections import defaultdict
import json
from my_project.db_connector import DbWriter

all_bots = []
x = 8001

while x < 10000:
    print(x)
    url = "https://api.opensea.io/api/v1/assets?token_ids=" + str(x) + "&collection=sportsbots&order_direction=desc&limit=1&include_orders=false"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": ""
    }
    response1 = requests.request("GET", url, headers=headers)
    response = response1.json()


    try:
        bot_data_dict = dict()
        traits = response["assets"][0]["traits"]

        bot_data_dict["name"] = response["assets"][0]["name"]
        bot_data_dict["image_url"] = response["assets"][0]["image_url"]

        if not traits:
            bot_data_dict["revealed"] = False

        else:
            bot_data_dict["revealed"] = True
            for trait in traits:
                bot_data_dict[trait["trait_type"]] = trait["value"]


    except:
        pass

    x += 1

    bot_data_dict = {k.lower(): v for k, v in bot_data_dict.items()}

    all_bots.append(bot_data_dict)


    
DbWriter.write_os_sportbot_data_to_db(all_bots)