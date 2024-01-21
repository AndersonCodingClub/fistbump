import os
import base64
from streak import Streak
from database import Database
from dotenv import load_dotenv
from save import save_image_file
from flask import Flask, render_template, redirect, request, session


load_dotenv('config.env')

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

@app.route('/')
def home():
    if not session.get('current_streak') or not session.get('user_id'):
        session['current_streak'] = 0
    else:
        session['current_streak'] = Streak(session['user_id']).get_streak(session['current_streak'], increment=False)

    d = Database()
    rows = list(reversed(d.get_images()))
    image_dicts = []
    for row in rows:
        _, creator_user_id, img_path, img_date_published = row
        img_creator_name = Database().get_user_row(creator_user_id)[1]
        formatted_date_published = str(img_date_published)
        
        image_dicts.append({'creator_name':img_creator_name, 'img_path':img_path, 'formatted_date_published':formatted_date_published})
    
    return render_template('index.html', paths=image_dicts, streak=session['current_streak'])

@app.route('/camera')
def camera():
    if not session.get('user_id'):
        return redirect('/auth/login')
    
    db = Database()
    matched_user_name = db.get_user_row(db.get_random_user())[1]
    
    session['current_streak'] = Streak(session['user_id']).get_streak(session['current_streak'], increment=False)
    return render_template('camera.html', streak=session['current_streak'], match_name=matched_user_name)

@app.route('/capture', methods=['POST'])
def capture():
    d = Database()
    
    data_url = request.json['dataURL']
    data = data_url.split(',')[1]
    decoded_data = base64.b64decode(data.encode('utf-8'))
    
    saved_path = save_image_file(decoded_data)
    d.add_image(session['user_id'], saved_path)
    
    session['current_streak'] = Streak(session['user_id']).get_streak(session['current_streak'], increment=True)
    
    return 'Successful Upload'

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']        
        user_id = Database().validate_user(username, password)
        if user_id is not None:
            session['user_id'] = user_id
            
            formatted_referrer = '/'+request.referrer.split('/')[-1]
            if formatted_referrer != '/signup':
                return redirect('/')
            else:
                return redirect(formatted_referrer)
        else:
            return render_template('login.html', bad_attempt=True)
    else:
        return render_template('login.html')

@app.route('/auth/signup', methods=['GET', 'POST'])
def auth_signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        major, year = request.form.get('major'), request.form.get('year')
        if year:
            year = int(year)
        
        if not Database().validate_user(username, password):
            user_id = Database().add_user(name, username, password, major, year)
            session['user_id'] = user_id
            
            formatted_referrer = '/'+request.referrer.split('/')[-1]
            if formatted_referrer != '/login':
                return redirect('/')
            else:
                return redirect(formatted_referrer)
        else:
            return render_template('signup.html', bad_attempt=True)
    else:
        return render_template('signup.html')
    
@app.route('/logout')
def logout():
    session['user_id'] = None
    return redirect('/')

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect('/auth/login')
    
    d = Database()
    rows = list(reversed(d.get_images(session['user_id'])))
    paths = [row[2] for row in rows]
    
    return render_template('profile.html', paths=paths)

if __name__ == '__main__':
    app.run(port=3000, debug=True)