import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # display symbol, name, share, price, Total
    stocks = db.execute(
        'SELECT stocks.symbol, stocks.name, stocks.shares, stocks.price, stocks.total_amount FROM stocks LEFT JOIN users ON stocks.person_id = users.id WHERE person_id = ?', session["user_id"])
    cash = db.execute('SELECT cash FROM users WHERE id = ?', session["user_id"])

    total = cash[0]['cash']

    for stock in stocks:
        total += stock['total_amount']
        stock['price'] = usd(stock['price'])
        stock['total_amount'] = usd(stock['total_amount'])

    formatted_cash = usd(cash[0]['cash'])
    formatted_total = usd(total)

    return render_template('index.html', stocks=stocks, cash=formatted_cash, total=formatted_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        stock = lookup(symbol)

        if shares.isnumeric():
            shares = int(float(shares))
        else:
            return apology('Enter a valid number')

        if not symbol:
            return apology("Please insert symbol")
        elif not stock:
            return apology("Symbol does not exist")
        elif not shares:
            return apology("Enter amount of shares")
        elif shares < 0:
            return apology("Enter a positive number")
        elif not isinstance(shares, int):
            return apology("Enter a valid number")

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        total_amount = stock["price"] * shares

        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if user_cash[0]["cash"] < total_amount:
            return apology("You don't have enough cash")

        transaction = {
            'person': session['user_id'],
            'symbol': stock['symbol'],
            'name': stock['name'],
            'shares': shares,
            'price': stock['price'],
            'total_amount': total_amount,
            'date': date_now,
            'transaction_type': 'buy'
        }

        get_symbol = db.execute('SELECT symbol FROM stocks WHERE symbol = ?', transaction['symbol'])

        if len(get_symbol) > 0:
            db.execute('UPDATE stocks SET shares = shares + ?, total_amount = total_amount + ? WHERE symbol = ?',
                       transaction['shares'],
                       transaction['total_amount'],
                       transaction['symbol']
                       )
        else:
            db.execute("INSERT INTO stocks (person_id, symbol, name, shares, price, total_amount) VALUES(?, ?, ?, ?, ?, ?)",
                       transaction['person'],
                       transaction['symbol'],
                       transaction['name'],
                       transaction['shares'],
                       transaction['price'],
                       transaction['total_amount']
                       )
        db.execute('INSERT INTO transactions (person_id, symbol, name, shares, price, date, transaction_type) VALUES(?, ?, ?, ?, ?, ?, ?)',
                   transaction['person'],
                   transaction['symbol'],
                   transaction['name'],
                   transaction['shares'],
                   transaction['price'],
                   transaction['date'],
                   transaction['transaction_type']
                   )
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_amount, session["user_id"])

        return redirect('/')
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE person_id = ?", session["user_id"])

    return render_template('history.html', transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Save username and password from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username was submitted
        if not username:
            return apology("must provide username")

        # Verify if username already exist
        check_username = db.execute("SELECT username FROM users WHERE username = ?", username)

        if len(check_username) > 0:
            return apology("username already exists")

        # Check if passwords were submitted
        elif not password or not confirmation:
            return apology("must provide password")

        # Verify if passwords match
        elif not password == confirmation:
            return apology("passwords must match")

        # Hash password
        hash = generate_password_hash(password)

        # Insert username and hashed password into db
        db.execute('INSERT INTO users (username, hash) VALUES(?, ?)', username, hash)
        print(f"user {username} registered")

        # Redirect to login page
        return redirect("/login")

    # Redirect user to register form
    else:
        return render_template("register.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == 'POST':
        symbol = request.form.get("symbol")
        symbol_details = lookup(symbol)

        if symbol == None:
            return apology("Please enter symbol")
        elif symbol_details == None:
            return apology("Symbol does not exist")

        result = {
            'name': symbol_details['name'],
            'symbol': symbol_details['symbol'],
            'price': usd(symbol_details['price'])
        }

        return render_template("quote.html", result=result)
    else:
        return render_template("quote.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    owned_stocks_symbols = db.execute('SELECT symbol FROM stocks WHERE person_id = ?', session["user_id"])

    owned_symbols_lst = []
    for s in owned_stocks_symbols:
        owned_symbols_lst.append(s['symbol'])

    if request.method == 'POST':
        symbol = request.form.get('symbol')
        shares = int(request.form.get('shares'))
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        transaction_type = 'sell'

        if symbol == None:
            return apology("Please select symbol")

        owned_shares = db.execute('SELECT shares, price, total_amount, name FROM stocks WHERE symbol = ?', symbol)

        if not symbol in owned_symbols_lst:
            return apology("You don't own shares for that stock")
        elif shares < 0:
            return apology("Insert a positive number")
        elif shares > owned_shares[0]['shares']:
            return apology("You don't own that many shares")

        sell_amount = shares * owned_shares[0]['price']
        total_amount = owned_shares[0]['total_amount'] - sell_amount

        db.execute('UPDATE stocks SET shares = shares - ?, total_amount = ? WHERE symbol = ?', shares, total_amount, symbol)
        db.execute('UPDATE users SET cash = cash + ? WHERE id = ?', sell_amount, session["user_id"])
        db.execute('DELETE FROM stocks WHERE shares = 0;')
        db.execute('INSERT INTO transactions (person_id, symbol, name, shares, price, date, transaction_type) VALUES(?, ?, ?, ?, ?, ?, ?)',
                   session['user_id'],
                   symbol,
                   owned_shares[0]['name'],
                   -shares,
                   owned_shares[0]['price'],
                   date,
                   transaction_type
                   )

        return redirect('/')

    return render_template('sell.html', symbols=owned_stocks_symbols)
