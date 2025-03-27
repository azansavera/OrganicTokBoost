from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        quantity = int(request.form['quantity'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = int(quantity * 0.95)
        fails = quantity - success
        log_session(video_url, quantity, success, fails, timestamp)
        return render_template('index.html', success=success, fails=fails, quantity=quantity, url=video_url)
    return render_template('index.html')

def log_session(video_url, quantity, success, fails, timestamp):
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append({
        "video": video_url,
        "timestamp": timestamp,
        "requested": quantity,
        "success": success,
        "fails": fails
    })

    with open("history.json", "w") as f:
        json.dump(history, f, indent=2)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
