import requests

def fetch_conversion_rate(base_currency, target_currency):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for a failed request
        data = response.json()
        
        # Check if the target currency is available in the response
        if target_currency in data['rates']:
            return data['rates'][target_currency]
        else:
            raise ValueError("Target currency not available")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except ValueError as ve:
        print(ve)
        return None
