from flask import Flask, jsonify
import requests
import os
import time

app = Flask(__name__)

GOLD_API_KEY = os.environ.get("GOLD_API_KEY")

if not GOLD_API_KEY:
    raise ValueError("GOLD_API_KEY not set in Environment Variables")

CACHE = {
    "data": None,
    "timestamp": 0
}

CACHE_TTL = 60

def get_usdthb():
    try:
        res = requests.get(
            "https://api.frankfurter.app/latest?from=USD&to=THB",
            timeout=8
        )
        res.raise_for_status()
        return res.json()["rates"]["THB"]
    except:
        try:
            res = requests.get(
                "https://open.er-api.com/v6/latest/USD",
                timeout=8
            )
            res.raise_for_status()
            return res.json()["rates"]["THB"]
        except:
            return 33.5

def fetch_gold():
    if CACHE["data"] and time.time() - CACHE["timestamp"] < CACHE_TTL:
        return CACHE["data"]

    try:
        gold_res = requests.get(
            "https://www.goldapi.io/api/XAU/USD",
            headers={"x-access-token": GOLD_API_KEY},
            timeout=8
        )
        gold_res.raise_for_status()
        gold_data = gold_res.json()

        spot = gold_data.get("price", 0)
        ch   = gold_data.get("ch", 0)
        chp  = gold_data.get("chp", 0)

        usdthb = get_usdthb()

        BAHT_WEIGHT = 15.244
        PURITY = 0.965
        TROY = 31.1035
        PREMIUM = 1.2

        thai = ((spot + PREMIUM) * usdthb * BAHT_WEIGHT * PURITY) / TROY

        result = {
            "price": spot,
            "usdthb": usdthb,
            "thai": round(thai),
            "xauThb": round(spot * usdthb),
            "ch": ch,
            "chp": chp
        }

        CACHE["data"] = result
        CACHE["timestamp"] = time.time()

        return result

    except Exception as e:
        if CACHE["data"]:
            return CACHE["data"]

        return {
            "price": 0,
            "usdthb": 0,
            "thai": 0,
            "xauThb": 0,
            "ch": 0,
            "chp": 0,
            "error": str(e)
        }

@app.route("/")
def index():
    return open("index.html", encoding="utf-8").read()

@app.route("/api/gold")
def gold():
    return jsonify(fetch_gold())
@app.route("/backtest")
def backtest():
    return open("backtest.html", encoding="utf-8").read()

if __name__ == "__main__":
    app.run(debug=True)