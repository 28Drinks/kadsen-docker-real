import requests

from my_project.db_connector import DbWriter


# get all v2 bots from OpenSea and write their data to db
# !!! only executed ones => no need to run again cause "os_v2_update.py"!!!

class V2OS():
    def get_all_v2_bot_from_os():

        v2_list = []

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

            name = response["assets"][0].get("name")
            image_url = response["assets"][0].get("image_original_url")
            token_id = response["assets"][-1].get("token_id")

            v2_list.append({"token_id": token_id, "name": name, "image_url": image_url})

            x += 1

        return v2_list

if __name__ == '__main__':
    DbWriter.write_sportsbots_data_to_db(V2OS.get_all_v2_bot_from_os())