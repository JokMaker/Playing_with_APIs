from flask import Flask, render_template, request
from fetch_rates import fetch_conversion_rate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_currency = request.form['base_currency']
        target_currency = request.form['target_currency']
        amount = float(request.form['amount'])
        
        rate = fetch_conversion_rate(base_currency, target_currency)
        
        if rate is not None:
            converted_amount = amount * rate
            return render_template('index.html', rate=rate, converted_amount=converted_amount, 
                                   base_currency=base_currency, target_currency=target_currency, 
                                   amount=amount)
        else:
            return render_template('index.html', error="Could not fetch conversion rate. Please try again.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
