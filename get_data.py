import http.client
import json

api_host = "api.warframe.market"


def print_data(filtered_orders):
    for x in filtered_orders:
        print(x)

def fetch_data(api_host, url):
    conn = http.client.HTTPSConnection(api_host)
    conn.request("GET", url)

    response = conn.getresponse()

    # Check the status code
    if response.status in (301, 302, 303, 307, 308):

        redirect_url = response.getheader('Location')
        print(f"Redirecting to: {redirect_url}")

        # Close the current connection
        conn.close()

        # Extract the path from the redirect URL
        # Assuming the redirect URL is relative and same host
        return fetch_data(api_host, redirect_url)
    elif response.status == 200:
        # Read and decode the response body
        data = response.read()
        decoded_data = data.decode("utf-8")
        if data:
            try:
                data = json.loads(decoded_data)
                return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    else:
        print(f"Error: {response.status} {response.reason}")
        return None

