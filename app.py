from flask import Flask, request, render_template, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters
DATABASE_URL = "dbname='TradingJournal' user='postgres' host='localhost' port='5002'"

@app.route('/')
def index():
    # Fetch trades and pairs from the database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trades;")
    trades = cursor.fetchall()
    cursor.execute("SELECT * FROM currencypairs;")
    pairs = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', trades=trades, pairs=pairs)

@app.route('/add_trade', methods=['POST'])
def add_trade():
    # Extracting form data
    pair_id = request.form['pair_id']
    entry_date = request.form['entry_date']
    entry_price = request.form['entry_price']
    direction = request.form['direction']
    position_size = request.form['position_size']
    notes = request.form['notes']

    # Connect to the database and insert the data
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Trades (pair_id, entry_date, entry_price, direction, position_size, notes) VALUES (%s, %s, %s, %s, %s, %s);",
        (pair_id, entry_date, entry_price, direction, position_size, notes)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/add_pair', methods=['POST'])
def add_pair():
    # Extracting form data
    base_currency = request.form['base_currency']
    quote_currency = request.form['quote_currency']

    # Connect to the database and insert the data
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO currencypairs (base_currency, quote_currency) VALUES (%s, %s);",
        (base_currency, quote_currency)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


# ... [Your existing code] ...

@app.route('/delete_trade/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Trades WHERE trade_id = %s;", (trade_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(status='success')
    except Exception as e:
        print(e)
        return jsonify(status='error', message=str(e))

@app.route('/edit_trade/<int:trade_id>', methods=['GET', 'POST'])
def edit_trade(trade_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        pair_id = request.form['pair_id']
        entry_date = request.form['entry_date']
        entry_price = request.form['entry_price']
        direction = request.form['direction']
        exit_date = request.form.get('exit_date')  # Using get in case it's not provided
        exit_price = request.form.get('exit_price')
        position_size = request.form['position_size']
        notes = request.form['notes']

        cursor.execute(
            "UPDATE Trades SET pair_id=%s, entry_date=%s, entry_price=%s, direction=%s, exit_date=%s, exit_price=%s, position_size=%s, notes=%s WHERE trade_id=%s;",
            (pair_id, entry_date, entry_price, direction, exit_date, exit_price, position_size, notes, trade_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    else:
        cursor.execute("SELECT * FROM Trades WHERE trade_id = %s;", (trade_id,))
        trade = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_trade.html', trade=trade)

@app.route('/delete_pair/<int:pair_id>')
def delete_pair(pair_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM currencypairs WHERE pair_id = %s;", (pair_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_pair/<int:pair_id>', methods=['GET', 'POST'])
def edit_pair(pair_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        base_currency = request.form['base_currency']
        quote_currency = request.form['quote_currency']

        cursor.execute(
            "UPDATE currencypairs SET base_currency=%s, quote_currency=%s WHERE pair_id=%s;",
            (base_currency, quote_currency, pair_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    else:
        cursor.execute("SELECT * FROM currencypairs WHERE pair_id = %s;", (pair_id,))
        pair = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_pair.html', pair=pair)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.5',port=5003)
