from flask import Flask, jsonify
import requests
import time

app = Flask(name)

CACHE = {"data": None, "time": 0}
CACHE_TTL = 60

def usdthb():
try:
r = requests.get("https://api.frankfurter.app/latest?from=USD&to=THB", timeout=8)
return r.json()["rates"]["THB"]
except:
r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8)
return r.json()["rates"]["THB"]

def gold():

if CACHE["data"] and time.time() - CACHE["time"] < CACHE_TTL:
    return CACHE["data"]

try:

    r = requests.get(
        "https://api.metals.live/v1/spot/gold",
        timeout=8
    )

    data = r.json()

    price = data[0]["price"]

    ch = 0
    chp = 0

    rate = usdthb()

    BAHT = 15.244
    PURE = 0.965
    TROY = 31.1035
    PREM = 1.2

    thai = ((price + PREM) * rate * BAHT * PURE) / TROY

    result = {
        "price": price,
        "usdthb": rate,
        "thai": round(thai),
        "ch": ch,
        "chp": chp
    }

    CACHE["data"] = result
    CACHE["time"] = time.time()

    return result

except Exception as e:
    return {"error": str(e)}

@app.route("/")
def index():
return open("index.html", encoding="utf-8").read()

@app.route("/api/gold")
def api():
return jsonify(gold())

if name == "main":
app.run(debug=True)