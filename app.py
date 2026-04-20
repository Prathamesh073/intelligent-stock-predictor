from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import yfinance as yf 
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    loss = loss.replace(0, 0.001)
    rs = gain / loss
    return 100 - (100 / (1 + rs))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    raw_symbol = request.form['symbol'].upper().strip()
    
    try:
        # === 1. SPECIAL HANDLING FOR INDICES (NIFTY/SENSEX) ===
        if raw_symbol in ['NIFTY', 'NIFTY 50', '^NSEI']:
            search_symbol = "^NSEI"
            chart_symbol = "NSE:NIFTY"
            display_symbol = "NIFTY 50"
        elif raw_symbol in ['SENSEX', '^BSESN']:
            search_symbol = "^BSESN"
            chart_symbol = "BSE:SENSEX"
            display_symbol = "SENSEX"
        else:
            # === 2. MARKET DETECTOR (US vs INDIA) ===
            indian_list = ['TCS', 'RELIANCE', 'INFY', 'HDFCBANK', 'SBIN', 'ICICIBANK', 'TATAMOTORS']
            
            if any(raw_symbol.endswith(x) for x in ['.NS', '.BO']):
                search_symbol = raw_symbol
            elif raw_symbol in indian_list or len(raw_symbol) > 4:
                search_symbol = raw_symbol + ".NS"
            else:
                search_symbol = raw_symbol 

            display_symbol = raw_symbol.replace(".NS", "").replace(".BO", "")
            # Set chart symbol based on search_symbol suffix
            chart_symbol = f"NASDAQ:{display_symbol}" if ".NS" not in search_symbol else f"NSE:{display_symbol}"

        # === 3. DATA FETCHING ===
        data = yf.download(search_symbol, period="1y", interval="1d")
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Fallback for Indian stocks if search_symbol failed
        if data.empty and ".NS" not in search_symbol and "^" not in search_symbol:
            data = yf.download(raw_symbol + ".NS", period="1y", interval="1d")
            search_symbol = raw_symbol + ".NS"
            chart_symbol = f"NSE:{display_symbol}"
            
        if data.empty:
            return f"Stock/Index '{raw_symbol}' not found.", 404

        # Data cleanup
        close_prices = data['Close'].squeeze() 
        current_price = float(close_prices.iloc[-1])

        # === 4. AI EXPECTED PRICE (Linear Regression) ===
        prediction_days = 15
        df_pred = close_prices.tail(prediction_days)
        X = np.array(range(len(df_pred))).reshape(-1, 1)
        y = df_pred.values.reshape(-1, 1)
        
        model = LinearRegression().fit(X, y)
        predicted_price = float(model.predict(np.array([[prediction_days]]))[0][0])

        # --- SMART INDICATORS ---
        ma20 = float(close_prices.rolling(20).mean().iloc[-1])
        rsi_series = calculate_rsi(close_prices)
        current_rsi = round(float(rsi_series.iloc[-1]), 2)

        # === 5. SIGNAL LOGIC ===
        if current_price > ma20 and current_rsi < 65:
            rec = "BUY 📈"
            expected_price = predicted_price * 1.01 
        elif current_price < ma20 or current_rsi > 75:
            rec = "SELL 📉"
            expected_price = predicted_price * 0.99 
        else:
            rec = "HOLD ⚖️"
            expected_price = predicted_price

        return render_template('index.html',
                               price=round(current_price, 2),
                               expected_price=round(float(expected_price), 2),
                               recommendation=rec,
                               symbol=display_symbol,
                               chart_symbol=chart_symbol,
                               rsi=current_rsi)

    except Exception as e:
        return f"System Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)