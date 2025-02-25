import json

from get_data import fetch_data, print_data, api_host
import requests
import time
import argparse

WFM_API2 = "https://api.warframe.market/v2"

def get_item_orders(item):

    item_url = item.replace(" ", "_")
    item_url = item_url.replace("-", "_")
    item_url = item_url.replace("&", "and")
    item_url = item_url.lower()
    url = f"/v1/items/{item_url}/orders"

    data = fetch_data(api_host,url)

    if "Prime Set" in item:
        filtered_orders = [
                {"platinum": d["platinum"], "order_type": d["order_type"], "quantity": d["quantity"]}
                for d in data["payload"]["orders"] if d["user"]["status"] == "ingame"]
        filtered_orders = sorted(filtered_orders, key=lambda x: x["platinum"])
        return filtered_orders

    elif ("Arcane" in item or "Molt" in item) and (item.count(" ") == 1):
        filtered_orders =  [{"platinum": d["platinum"], "order_type": d["order_type"], "quantity": d["quantity"]}
                for d in data["payload"]["orders"] if d["user"]["status"] == "ingame" and d["mod_rank"] == 5]
        filtered_orders = sorted(filtered_orders, key= lambda x:x["platinum"])
        return filtered_orders

    elif "Primed" in item:
        filtered_orders = [{"platinum": d["platinum"], "order_type": d["order_type"], "quantity": d["quantity"]}
                           for d in data["payload"]["orders"] if d["user"]["status"] == "ingame" and d["mod_rank"] == 10]
        filtered_orders = sorted(filtered_orders, key=lambda x: x["platinum"])
        return filtered_orders

    else:
        return []


def fetch_item_statistics(item, days):
    item_url = item.replace(" ", "_")
    item_url = item_url.replace("-", "_")
    item_url = item_url.replace("&", "and")
    item_url = item_url.lower()
    url = f"/v1/items/{item_url}/statistics"
    data = fetch_data(api_host, url)
    NinetyDay = data["payload"]["statistics_closed"]["90days"]
    variable_day_stat = []
    last = len(NinetyDay)
    if "primed" in item_url:
        days = days * 2
        for i in range(1, days, 2):
            if NinetyDay[last - (i+1)]["mod_rank"] == 10:
                day_data = NinetyDay[last - (i+1)]
                variable_day_stat.append({"avg_price": day_data["avg_price"],
                                          "median": day_data["median"], "volume": day_data["volume"]})
    elif "prime_set" in item_url:
        for i in range(1, days):
            day_data = NinetyDay[last - (i+1)]
            variable_day_stat.append({"avg_price": day_data["avg_price"],
                                        "median": day_data["median"], "volume": day_data["volume"]})



    return variable_day_stat


def fetch_items(keyword=None):
    url = f"{WFM_API2}/items"
    print(url)
    request = requests.get(url=url)
    data = request.json()
    data = data["data"]
    if keyword is not None:
        items_filtered = [(i["urlName"], i["id"])for i in data
                          if any(word in i["i18n"]["en"]["name"] for word in keyword)]
        return items_filtered
    else:
        return [(i["i18n"]["en"]["name"], i["id"])for i in data]




def item_top(item_name):
    item_url = item_name.replace(" ", "_")
    item_url = item_url.replace("-", "_")
    item_url = item_url.replace("&", "and")
    item_url = item_url.lower()
    url = f"{WFM_API2}/orders/item/{item_url}/top"
    print(url)
    filtered_orders = []
    if "primed" in item_url or "arcane" in item_url:
        payload = {
            "maxRank": "true"
        }
        try:
            request = requests.get(url=url, params=payload)
            data = request.json()
            time.sleep(0.35)

            for order in data["data"]["buy"]:
                filtered_orders.append({"platinum": order["platinum"], "quantity": order["quantity"],
                                        "rank": order["rank"], "order_type": "buy"
                                        })
            for order in data["data"]["sell"]:
                filtered_orders.append({"platinum": order["platinum"], "quantity": order["quantity"],
                                        "rank": order["rank"], "order_type": "sell"
                                        })
        except requests.exceptions.RequestException as err:
            print(f"error occurred: {err}")
        except TypeError:
            print("Ain't shit in here")

    elif "prime_set" in item_url:

        try:
            request = requests.get(url=url)
            data = request.json()
            time.sleep(0.35)

            if data["data"]["buy"]:
                for order in request.json()["data"]["buy"]:
                    filtered_orders.append({"platinum": order["platinum"], "quantity": order["quantity"],
                                            "order_type": "buy"
                                            })
            for order in data["data"]["sell"]:
                filtered_orders.append({"platinum": order["platinum"], "quantity": order["quantity"],
                                        "order_type": "sell"
                                        })

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            print(f"The current url is {url}")
        except:
            print("sumthin happened")


    return filtered_orders



def main():
    parser = argparse.ArgumentParser(description='Get orders for an item')
    parser.add_argument('--keyword', type=str, default="Primed Pressure Point",
                        help='Keyword(s) to search for')
    args = parser.parse_args()
    print_data(item_top(args.keyword))







if __name__ == "__main__":
    main()


