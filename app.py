from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
import os

# Load environment variables (API_KEY)
load_dotenv()

app = Flask(__name__)

# Set up the secret key for session management
app.secret_key = os.getenv("SECRET_KEY")  # Store your secret key in .env

# Currency API setup
API_KEY = os.getenv("API_KEY")
API_URL = "https://v6.exchangerate-api.com/v6/{}/latest/{}"

currency_symbols = {
    "USD": "$", "AED": "د.إ", "AFN": "Af", "ALL": "L", "AMD": "֏", "ANG": "ƒ",
    "AOA": "Kz", "ARS": "$", "AUD": "$", "AWG": "ƒ", "AZN": "₼", "BAM": "KM",
    "BDT": "৳", "BGN": "лв", "BHD": "د.ب", "BIF": "FBu", "BMD": "$", "BND": "$",
    "BOB": "Bs.", "BRL": "R$", "BSD": "$", "BTN": "Nu.", "BWP": "P", "BYN": "₽",
    "BZD": "$", "CAD": "$", "CDF": "FC", "CHF": "CHF", "CLP": "$", "CNY": "¥",
    "COP": "$", "CRC": "₡", "CUP": "$", "CVE": "$", "CZK": "Kč", "DJF": "Fdj",
    "DKK": "kr", "DOP": "RD$", "DZD": "د.ج", "EGP": "ج.م", "ERN": "Nkf", "ESP": "€",
    "ETB": "Br", "EUR": "€", "FJD": "$", "FKP": "£", "FOK": "kr", "GBP": "£",
    "GEL": "₾", "GHS": "₵", "GIP": "£", "GMD": "D", "GNF": "FG", "GTQ": "Q",
    "GYD": "$", "HKD": "$", "HNL": "L", "HRK": "kn", "HTG": "G", "HUF": "Ft",
    "IDR": "Rp", "ILS": "₪", "INR": "₹", "IQD": "د.ع", "IRR": "﷼", "ISK": "kr",
    "JMD": "$", "JOD": "د.ا", "JPY": "¥", "KES": "KSh", "KGS": "с", "KHR": "៛",
    "KMF": "CF", "KRW": "₩", "KWD": "د.ك", "KYD": "$", "KZT": "₸", "LAK": "₭",
    "LBP": "ل.ل", "LKR": "Rs", "LRD": "$", "LSL": "M", "LTL": "Lt", "LVL": "Ls",
    "LYD": "د.ل", "MAD": "د.م.", "MDL": "lei", "MGA": "Ar", "MKD": "ден", "MMK": "Ks",
    "MNT": "₮", "MOP": "MOP", "MUR": "₨", "MVR": "Rf", "MWK": "MK", "MXN": "$",
    "MYR": "RM", "MZN": "MT", "NAD": "$", "NGN": "₦", "NIO": "C$", "NOK": "kr",
    "NPR": "Rs", "NZD": "$", "OMR": "ر.ع.", "PAB": "B/.", "PEN": "S/.", "PGK": "K",
    "PHP": "₱", "PKR": "₨", "PLN": "zł", "PYG": "Gs", "QAR": "ر.ق", "RON": "lei",
    "RSD": "дин", "RUB": "₽", "RWF": "FRw", "SAR": "ر.س", "SBD": "$", "SCR": "₨",
    "SEK": "kr", "SGD": "$", "SHP": "£", "SLL": "Le", "SOS": "Sh", "SRD": "$",
    "SSP": "SSP", "STN": "Db", "SYP": "ل.س", "SZL": "L", "THB": "฿", "TJS": "SM",
    "TMT": "m", "TND": "د.ت", "TOP": "T$", "TRY": "₺", "TTD": "$", "TWD": "$",
    "TZS": "TSh", "UAH": "₴", "UGX": "UGX", "UYU": "$", "UZS": "сум", "VEB": "Bs.",
    "VND": "₫", "VUV": "Vt", "WST": "T", "XOF": "CFA", "XPF": "CFA", "YER": "ر.ي",
    "ZAR": "R", "ZMK": "K", "ZWL": "$"
}

@app.route("/", methods=["GET", "POST"])
def home():
    currencies = currency_symbols.keys()
    return render_template("index.html", currencies=currencies, symbols=currency_symbols)

@app.route("/convert", methods=["POST"])
def convert():
    base_currency = request.form["base_currency"]
    target_currency = request.form["target_currency"]
    amount = float(request.form["amount"])

    try:
        response = requests.get(API_URL.format(API_KEY, base_currency))
        data = response.json()

        if response.status_code != 200 or "conversion_rates" not in data:
            return render_template("error.html", message="Error: Unable to fetch exchange rates. Try again later.")

        rates = data["conversion_rates"]
        if target_currency not in rates:
            return render_template("error.html", message="Error: Invalid target currency.")

        converted_amount = round(amount * rates[target_currency], 2)
        return render_template("result.html", 
                               base_currency=base_currency,
                               target_currency=target_currency,
                               amount=amount,
                               converted_amount=converted_amount,
                               symbols=currency_symbols)

    except Exception as e:
        return render_template("error.html", message=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
