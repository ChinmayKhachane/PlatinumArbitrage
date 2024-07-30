from finddiff import find_profitable
from login import login, place_order, delete_order, get_profile
from get_data import print_data
from get_orders import get_item_orders
import argparse

def PlaceDaOrders(margin, threshold, keyword, headers):
    profitable_list = find_profitable(margin, threshold, keyword)
    order_json = []
    for i in profitable_list:
        buying_point = i["top buy"]  + 1
        order = place_order(headers, i["id"], i["item"], 1, buying_point, "buy")
        order_json.append((order["payload"]["order"]["id"], order["payload"]["order"]["order_type"],
                           order["payload"]["order"]["platinum"]))

    return order_json


def CheckDaOrders(headers, margin):
    buy_orders = get_profile("ValidPhoenix88", headers)
    order_details = [(i["id"], i["platinum"], i["item"]["en"]["item_name"], i["item"]["id"])
                     for i in buy_orders["payload"]["buy_orders"]]

    for i in order_details:
        current = get_item_orders(i[2])

        try:
            highest_buy = max([j for j in current if j["order_type"] == "buy"], key=lambda x: x["platinum"])
            highest_buy = highest_buy["platinum"]
        except ValueError as e:
            if str(e) == "max() arg is an empty sequence":
                highest_buy = 0
                print("No orders for " + str(i[2]))
            else:
                raise

        try:
            lowest_sell = min([j for j in current if j["order_type"] == "sell"], key=lambda x: x["platinum"])
            lowest_sell = lowest_sell["platinum"]
        except ValueError as e:
            if str(e) == "min() arg is an empty sequence":
                lowest_sell = None
            else:
                raise
        if lowest_sell:
            if highest_buy > i[1] and lowest_sell - highest_buy >= 26:
                delete_order(headers, i[0])
                place_order(headers, i[3], i[2], 1, highest_buy + 1, "buy")

            elif lowest_sell - i[1] < 20:
                delete_order(headers, i[0])

    return "Your done"


def main():
    parser = argparse.ArgumentParser(description='Place orders for profitable items.')
    parser.add_argument('--min_value', type=int, default=25, help='Minimum margin')
    parser.add_argument('--max_cost', type=int, default=300, help='Maximum cost of buying')
    parser.add_argument('--keyword', type=str, nargs='+', default=["Primed"], help='Keyword(s) to search for')
    args = parser.parse_args()
    headers = login("email", "password")
    PlaceDaOrders(args.min_value, args.max_cost, headers=headers, keyword=args.keyword)








if __name__ == "__main__":
    main()
