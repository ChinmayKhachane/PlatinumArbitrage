from get_orders import api_host, item_top, fetch_item_statistics, fetch_items, get_item_orders
from get_data import print_data
import argparse
def find_profitable(margin, buy_cost, keyword):

    d = fetch_items(keyword)
    profitable = []
    for name, id in d:
        orders = item_top(name)
        try:
            stats = fetch_item_statistics(name, 7)
        except IndexError:
            print("Not enough data")
            stats = False
        if orders:
            sell_orders = []
            buy_orders = []
            for order in orders:
                if order["order_type"] == "sell":
                    sell_orders.append(order)
                elif order["order_type"] == "buy":
                    buy_orders.append(order)

            top_sell = sell_orders[0]["platinum"]
            if buy_orders:
                top_buy = buy_orders[0]["platinum"]
            else:
                top_buy = top_sell - 30

            if top_sell - top_buy > margin and top_buy < buy_cost and stats:
                profitable.append({"id": id, "item": name, "profit": top_sell-top_buy,
                                   "top buy": top_buy, "top sell": top_sell, "volume": stats[0]["volume"]})

    return profitable


def sell_flip(margin, buy_cost, keywords):
    d = fetch_items(keywords)
    profitable = []
    for name, id in d:
        orders = get_item_orders(name)
        if orders:
            sell_orders = []
            for order in orders:
                if order["order_type"] == "sell":
                    sell_orders.append(order)
            avg_plat = 0
            for order in sell_orders[1:5]:
                avg_plat += order["platinum"]

            avg_plat = avg_plat / 4

            if sell_orders[0]["platinum"] - avg_plat > margin and sell_orders[0]["platinum"] < buy_cost:
                profitable.append({"id": id, "item": name, "profit": sell_orders[0]["platinum"] - avg_plat})

    return profitable


def main():
    parser = argparse.ArgumentParser(description='Find and print profitable items.')
    parser.add_argument('--min_value', type=int, default=25, help='Minimum margin')
    parser.add_argument('--max_value', type=int, default=300, help='Maximum cost of buying')
    parser.add_argument('--keyword', type=str, nargs='+', default=["Primed"], help='Keyword(s) to search for')
    args = parser.parse_args()
    x = find_profitable(args.min_value, args.max_value, args.keyword)
    if x:
        print_data(x)
    else:
        print("Its empty")


if __name__ == "__main__":
    main()





