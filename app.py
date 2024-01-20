import base64
from database import Database
from save import save_image_file, get_file_names_by_time
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/wall')
def wall():
    # placeholder for database logic
    paths = get_file_names_by_time('static/images')
    
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
    save_image_file(decoded_data)
        
    return 'Image captured and saved'

if __name__ == '__main__':
    app.run(port=3000, debug=True)