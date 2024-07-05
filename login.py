import requests
import json
from get_data import fetch_data
WFM_API = "https://api.warframe.market/v1"


def login(
    user_email: str, user_password: str, platform: str = "pc", language: str = "en"
):

    headers = {
        "Content-Type": "application/json; utf-8",
        "Accept": "application/json",
        "Authorization": "JWT",
        "platform": platform,
        "language": language,
    }
    content = {"email": user_email, "password": user_password, "auth_type": "header"}
    response = requests.post(f"{WFM_API}/auth/signin", data=json.dumps(content), headers=headers)
    if response.status_code != 200:
        print(response)
        return None, None
    ingame_name = response.json()["payload"]["user"]["ingame_name"]
    jwt_token = response.headers["Authorization"]
    headers["Authorization"] = jwt_token
    headers["auth_type"] = "header"
    return headers



def place_order(headers, item_id, item_name, quantity, platinum, order_type, rank=5):

    url = f"{WFM_API}/profile/orders"
    if "Arcane" in item_name:
        payload = {
            "item":item_id,
            "order_type": order_type,
            "platinum": platinum,
            "quantity": quantity,
            "rank": rank,
            "visible": True

        }
    elif "Prime Set" in item_name:
        payload = {
            "item": item_id,
            "order_type": order_type,
            "platinum": platinum,
            "quantity": quantity,
            "visible": True

        }
    elif "Primed" in item_name:
        payload = {
            "item": item_id,
            "order_type": order_type,
            "platinum": platinum,
            "quantity": quantity,
            "rank": 10,
            "visible": True
        }
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Order for {item_name} created successfully")
        return response.json()

    except:
        print("Failed to create order: " + str(item_name) + " error code: " + str(response.status_code))
        print(json.dumps(response.json(), indent=2))
        return None1


def delete_order(headers, order_id):

    url = f"{WFM_API}/profile/orders/{order_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print("Order deleted successfully!")
        stuff = response.json()
        res = json.dumps(stuff, indent=2)
        return res
    else:
        print(f"Failed to delete order. Item id: {order_id}. Response code: {response.status_code}")
        error_data = response.json()
        print(json.dumps(error_data, indent=2))  # Pretty-print the JSON error response
        return None


def get_profile(username, headers):

    url = f"{WFM_API}/profile/{username}/orders"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
        return response.json()

    else:
        print(response.status_code)
        print(json.dumps(response.json(), indent=2))
        return None

if __name__ == "__main__":
    headers = login("email", "password")
    get_profile("in_game_name", headers)







