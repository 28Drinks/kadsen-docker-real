import requests
from collections import defaultdict
import json

sports = []
values = []
x = 0
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
        traits = response["assets"][0]["traits"]

        for trait in traits:
            if trait["trait_type"] == "Sportshares":
                values.append(trait["value"])

        for trait in traits:
            if trait["trait_type"] == "Sport":
                sports.append(trait["value"])

    except:
        pass
    x += 1


my_dict = defaultdict(int)
for k, v in zip(sports, values):
    my_dict[k] += v

with open('totalShares.json', 'w') as fp:
    json.dump(my_dict, fp)
