<<<<<<< HEAD
from flask import Flask, jsonify
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from supabase import create_client, Client

app = Flask(__name__)

# 🔹 Supabase Credentials (Replace with your actual project details)
SUPABASE_URL = "https://jpvbpekpgqqavcuvtuxv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpwdmJwZWtwZ3FxYXZjdXZ0dXh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA3NDcyMDAsImV4cCI6MjA1NjMyMzIwMH0.IWlQMkq7G0v90a_yUjH79vAsKyn4orL3sXyiNVIQxQQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Binance API Endpoint
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

# 🔹 Top 15 Crypto Symbols
TOP_15_CURRENCIES = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
                     "DOGEUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT",
                     "BCHUSDT", "LINKUSDT", "XLMUSDT", "UNIUSDT", "AVAXUSDT"]

# 🔹 Fetch real-time crypto prices
@app.route('/crypto-prices', methods=['GET'])
def get_crypto_prices():
    prices = []
    for symbol in TOP_15_CURRENCIES:
        response = requests.get(f"{BINANCE_API_URL}?symbol={symbol}")
        data = response.json()
        if "price" in data:
            price_entry = {
                "symbol": symbol,
                "price": float(data["price"]),
                "timestamp": datetime.utcnow()
            }
            prices.append(price_entry)
    
    # 🔹 Store in Supabase
    supabase.table("crypto_prices").insert(prices).execute()
    
    return jsonify(prices)

# 🔹 Train ML Model & Predict Future Prices
@app.route('/predict-prices', methods=['GET'])
def predict_prices():
    predictions = []
    
    for symbol in TOP_15_CURRENCIES:
        # 🔹 Fetch historical prices from Supabase
        response = supabase.table("crypto_prices").select("*").eq("symbol", symbol).order("timestamp", desc=True).limit(10).execute()
        rows = response.data

        if len(rows) < 5:
            continue  # Need at least 5 data points for training

        # 🔹 Prepare Data for ML Model
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"]).astype(int) // 10**9  # Convert to seconds

        X = df["timestamp"].values.reshape(-1, 1)  # Time as feature
        y = df["price"].values  # Prices as target

        # 🔹 Train Linear Regression Model
        model = LinearRegression()
        model.fit(X, y)

        # 🔹 Predict Future Price (Next timestamp)
        future_time = np.array([[df["timestamp"].max() + 3600]])  # Predict 1 hour ahead
        predicted_price = model.predict(future_time)[0]

        predictions.append({
            "symbol": symbol,
            "predicted_price": round(predicted_price, 2)
        })

        # 🔹 Store prediction in Supabase
        supabase.table("crypto_prices").insert({
            "symbol": symbol,
            "price": None,  # No real price, only predicted
            "timestamp": datetime.utcnow(),
            "predicted_price": predicted_price
        }).execute()

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, jsonify
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from supabase import create_client, Client

app = Flask(__name__)

# 🔹 Supabase Credentials (Replace with your actual project details)
SUPABASE_URL = "https://jpvbpekpgqqavcuvtuxv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpwdmJwZWtwZ3FxYXZjdXZ0dXh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA3NDcyMDAsImV4cCI6MjA1NjMyMzIwMH0.IWlQMkq7G0v90a_yUjH79vAsKyn4orL3sXyiNVIQxQQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Binance API Endpoint
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

# 🔹 Top 15 Crypto Symbols
TOP_15_CURRENCIES = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
                     "DOGEUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT",
                     "BCHUSDT", "LINKUSDT", "XLMUSDT", "UNIUSDT", "AVAXUSDT"]

# 🔹 Fetch real-time crypto prices
@app.route('/crypto-prices', methods=['GET'])
def get_crypto_prices():
    prices = []
    for symbol in TOP_15_CURRENCIES:
        response = requests.get(f"{BINANCE_API_URL}?symbol={symbol}")
        data = response.json()
        if "price" in data:
            price_entry = {
                "symbol": symbol,
                "price": float(data["price"]),
                "timestamp": datetime.utcnow()
            }
            prices.append(price_entry)
    
    # 🔹 Store in Supabase
    supabase.table("crypto_prices").insert(prices).execute()
    
    return jsonify(prices)

# 🔹 Train ML Model & Predict Future Prices
@app.route('/predict-prices', methods=['GET'])
def predict_prices():
    predictions = []
    
    for symbol in TOP_15_CURRENCIES:
        # 🔹 Fetch historical prices from Supabase
        response = supabase.table("crypto_prices").select("*").eq("symbol", symbol).order("timestamp", desc=True).limit(10).execute()
        rows = response.data

        if len(rows) < 5:
            continue  # Need at least 5 data points for training

        # 🔹 Prepare Data for ML Model
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"]).astype(int) // 10**9  # Convert to seconds

        X = df["timestamp"].values.reshape(-1, 1)  # Time as feature
        y = df["price"].values  # Prices as target

        # 🔹 Train Linear Regression Model
        model = LinearRegression()
        model.fit(X, y)

        # 🔹 Predict Future Price (Next timestamp)
        future_time = np.array([[df["timestamp"].max() + 3600]])  # Predict 1 hour ahead
        predicted_price = model.predict(future_time)[0]

        predictions.append({
            "symbol": symbol,
            "predicted_price": round(predicted_price, 2)
        })

        # 🔹 Store prediction in Supabase
        supabase.table("crypto_prices").insert({
            "symbol": symbol,
            "price": None,  # No real price, only predicted
            "timestamp": datetime.utcnow(),
            "predicted_price": predicted_price
        }).execute()

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 800d364f366768be7534733ffad35f6c31b3e4bf
