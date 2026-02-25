from flask import Flask, jsonify
import urllib.request
import json
import math

app = Flask(__name__)

GOLD_API_KEY = 'goldapi-1kvaizsmm14nx8l-io'
USD_THB = 34.82

def fetch_gold():
    try:
        req = urllib.request.Request(
            'https://www.goldapi.io/api/XAU/USD',
            headers={'x-access-token': GOLD_API_KEY}
        )
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read())
            price = data.get('price', 0)
            ch    = data.get('ch', 0)
            chp   = data.get('chp', 0)
            thai  = round(price * USD_THB * 0.9653 * 0.4729)
            return {'price': price, 'ch': ch, 'chp': chp,
                    'thai': thai, 'usdthb': USD_THB,
                    'xauThb': round(price * USD_THB)}
    except Exception as e:
        return {'price': 0, 'ch': 0, 'chp': 0,
                'thai': 0, 'usdthb': USD_THB, 'xauThb': 0, 'error': str(e)}

@app.route('/')
def index():
    return open('index.html', encoding='utf-8').read()

@app.route('/api/gold')
def gold():
    return jsonify(fetch_gold())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
