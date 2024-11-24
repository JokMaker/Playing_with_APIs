import requests

API_URL = "https://v6.exchangerate-api.com/v6/ab67ba98d49ff093a0e1e5c9/latest"

def get_exchange_rates(base_currency="USD"):
    try:
        response = requests.get(f"{API_URL}/{base_currency}")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        if data["result"] != "success":
            raise Exception("API request failed.")
        return data["conversion_rates"]
    except Exception as e:
        print(f"Error fetching rates: {e}")
        return None
