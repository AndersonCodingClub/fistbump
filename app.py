import os
import base64
from database import Database
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/wall')
def wall():
    # placeholder for database logic
    paths = [os.path.join('/static/images', path) for path in os.listdir('static/images')]
    
    return render_template('wallfeed.html', paths=paths)

@app.route('/camera')
def camera():
    current_streak = 5 #Streak.current_streak
    return render_template('camera.html', streak=current_streak)

@app.route('/capture', methods=['POST'])
def capture():
    data_url = request.json['dataURL']
    data = data_url.split(',')[1]
    decoded_data = base64.b64decode(data.encode('utf-8'))
    
    with open('static/images/image_1.jpeg', 'wb') as f:
        f.write(decoded_data)
    
    return 'Image captured and saved'

if __name__ == '__main__':
    app.run(port=3000, debug=True)