from flask import Flask, jsonify
import requests
import os
import time

app = Flask(__name__)

# ✅ ดึง key จาก Environment Variable
GOLD_API_KEY = os.environ.get("GOLD_API_KEY")

if not GOLD_API_KEY:
    raise ValueError("GOLD_API_KEY not set in Environment Variables")

# Cache กัน API ล่ม
CACHE = {
    "data": None,
    "timestamp": 0
}

CACHE_TTL = 60  # วินาที

def fetch_gold():

    # ใช้ cache ถ้ายังไม่หมดเวลา
    if CACHE["data"] and time.time() - CACHE["timestamp"] < CACHE_TTL:
        return CACHE["data"]

    try:
        # 1️⃣ ดึง Spot Gold
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

        # 2️⃣ ดึง USDTHB
        fx_res = requests.get(
            "https://api.exchangerate.host/latest?base=USD&symbols=THB",
            timeout=8
        )
        fx_res.raise_for_status()
        usdthb = fx_res.json()["rates"]["THB"]

        # 3️⃣ สูตรทองไทย 96.5%
        BAHT_WEIGHT = 15.244
        PURITY = 0.965
        TROY = 31.1035
        PREMIUM = 1.2  # ปรับทีละ 0.1 ถ้าต้องการจูน

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
        # ถ้า API ล่ม ใช้ค่าล่าสุดแทน
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