import base64
from streak import Streak
from database import Database
from save import save_image_file
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)
app.secret_key = 'secret key'

@app.route('/')
def home():
    Streak.check_streak()
    
    d = Database()
    rows = list(reversed(d.get_images()))
    paths = [row[2] for row in rows]
    
    return render_template('index.html', paths=paths, streak=Streak.current_streak)

@app.route('/camera')
def camera():
    current_streak = Streak.current_streak
    return render_template('camera.html', streak=current_streak)

@app.route('/capture', methods=['POST'])
def capture():
    d = Database()
    
    data_url = request.json['dataURL']
    data = data_url.split(',')[1]
    decoded_data = base64.b64decode(data.encode('utf-8'))
    
    saved_path = save_image_file(decoded_data)
    d.add_image(1, saved_path)
    Streak.add_streak()
    
    return 'Successful Upload'

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']        
        user_id = Database().validate_user(username, password)
        if user_id is not None:
            session['user_id'] = user_id
            
            if request.referrer.endswith('signup'):
                return redirect('/')
            else:
                return redirect(request.referrer)
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
            
            if request.referrer.endswith('login'):
                return redirect('/')
            else:
                return redirect(request.referrer)
        else:
            return render_template('signup.html', bad_attempt=True)
    else:
        return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/auth/login')
    return 'Profile'

if __name__ == '__main__':
    app.run(port=3000, debug=True)