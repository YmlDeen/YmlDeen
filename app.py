from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }
        .card {
            text-align: center;
            padding: 50px 60px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }
        .dot {
            width: 14px; height: 14px;
            background: #00e676;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.3); }
        }
        h1 { font-size: 2.5rem; margin: 20px 0 10px; }
        p { color: rgba(255,255,255,0.6); font-size: 1rem; }
        .badge {
            margin-top: 25px;
            display: inline-block;
            padding: 6px 18px;
            background: rgba(0,230,118,0.15);
            border: 1px solid #00e676;
            border-radius: 20px;
            color: #00e676;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <div><span class="dot"></span><span style="color:#00e676">Online</span></div>
        <h1>🚀 Server is Running</h1>
        <p>ระบบทำงานปกติ พร้อมให้บริการ</p>
        <div class="badge">Status: Active</div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run()