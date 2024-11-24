from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing
import requests
from dotenv import load_dotenv
import os

# Load environment variables (API_KEY)
load_dotenv()

app = Flask(__name__)

# Set up the secret key for session management and user authentication
app.secret_key = os.getenv("SECRET_KEY")  # Store your secret key in .env

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in

# User model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the password against the stored hash."""
        return check_password_hash(self.password, password)

# Dummy database (In real-world applications, use a database like SQLite or PostgreSQL)
users = {
    "admin": User(1, "admin", "password")  # Example user (use hashed passwords in real apps)
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Flask-WTF form for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

# Flask-WTF form for registration
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

# Currency API setup
API_KEY = os.getenv("API_KEY")
API_URL = "https://v6.exchangerate-api.com/v6/{}/latest/{}"

currency_symbols = {
    "USD": "$", "AED": "د.إ", "AFN": "Af", "ALL": "L", "AMD": "֏", "ANG": "ƒ",
    "AOA": "Kz", "ARS": "$", "AUD": "$", "AWG": "ƒ", "AZN": "₼", "BAM": "KM",
    # Add more currency symbols...
}

@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        # If logged in, show the currency conversion page
        currencies = currency_symbols.keys()
        return render_template("index.html", currencies=currencies, symbols=currency_symbols)
    else:
        # Redirect to login page if not authenticated
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = users.get(username)
        if user and user.check_password(password):  # Use hashed password check
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Check if user already exists
        if username in users:
            flash("Username already exists", "danger")
        else:
            new_user = User(len(users) + 1, username, password)
            new_user.set_password(password)  # Store the hashed password
            users[username] = new_user
            login_user(new_user)  # Log in the new user
            return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route("/convert", methods=["POST"])
@login_required
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