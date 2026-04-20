
# Intelligent Stock Predictor

## About Project

This project is a simple web application that predicts stock prices and gives Buy/Sell/Hold suggestions. It uses Linear Regression along with RSI and Moving Average to analyze the stock trend.

The main aim of this project is to help users understand stock behavior easily without needing deep financial knowledge.

---

## Features

* Takes stock symbol as input
* Fetches real-time data using yFinance
* Predicts next-day price
* Calculates RSI and Moving Average
* Gives Buy / Sell / Hold recommendation
* Works for both Indian and US stocks

---

## Technologies Used

* Python
* Flask
* Pandas, NumPy
* Scikit-learn
* yFinance
* HTML

---

## How It Works

1. User enters stock name
2. System fetches stock data
3. Last 15 days data is used
4. Linear Regression predicts next price
5. RSI and Moving Average are calculated
6. Final recommendation is shown

---

## How to Run

1. Install libraries:
   pip install -r requirements.txt

2. Run the file:
   python app.py

3. Open in browser:
   http://127.0.0.1:5000/

---

## Output

* Current Price
* Expected Price
* RSI Value
* Recommendation (Buy/Sell/Hold)

---

## Limitations

* Prediction is based on simple model
* Does not consider news or sudden market changes

---

## Future Scope

* Add news sentiment analysis
* Improve accuracy using advanced models
* Add user portfolio tracking

---



