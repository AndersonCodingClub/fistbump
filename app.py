import os
#from streak import Streak
from database import Database
from flask import Flask, render_template, redirect, session


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

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    return 'Image captured and saved'

if __name__ == '__main__':
    app.run(port=3000, debug=True)