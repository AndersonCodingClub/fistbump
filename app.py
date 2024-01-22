import os
import base64
import datetime as dt
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

    db = Database()

    feed_type = request.args.get('feed-type', 'global')
    if feed_type == 'fyp' and not session.get('user_id'):
        return redirect('/auth/login')
    elif feed_type == 'fyp':
        following = db.get_following(session['user_id'])
    
    rows = list(reversed(db.get_images()))
    image_dicts = []
    for row in rows:
        _, creator_user_id, match_user_id, img_path, img_date_published = row
        if feed_type == 'fyp':
            if creator_user_id not in following:
                continue
        
        img_creator_name = Database().get_user_row(creator_user_id)[1]
        img_match_name = Database().get_user_row(match_user_id)[1]
        formatted_date_published = img_date_published.strftime('%Y-%m-%d %I:%M:%S %p')
        
        image_dicts.append({'creator_user_id':creator_user_id, 'creator_name':img_creator_name, 'match_user_id':match_user_id,
                            'match_name':img_match_name, 'img_path':img_path, 'formatted_date_published':formatted_date_published})
    
    return render_template('index.html', paths=image_dicts, streak=session['current_streak'], feed_type=feed_type)

@app.route('/camera')
def camera():
    if not session.get('user_id'):
        return redirect('/auth/login')
    
    db = Database()
    matched_user_id = db.get_random_user(session['user_id'])
    matched_user_name = db.get_user_row(matched_user_id)[1]
    
    session['current_streak'] = Streak(session['user_id']).get_streak(session['current_streak'], increment=False)
    return render_template('camera.html', streak=session['current_streak'], match_id=matched_user_id, match_name=matched_user_name)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/capture', methods=['POST'])
def capture():
    db = Database()
    
    data_url = request.json['dataURL']
    fistbump_match_id = request.json['matchID']
    data = data_url.split(',')[1]
    decoded_data = base64.b64decode(data.encode('utf-8'))
    
    saved_path = save_image_file(decoded_data)
    db.add_image(session['user_id'], saved_path, fistbump_match_id)
    
    session['current_streak'] = Streak(session['user_id']).get_streak(session['current_streak'], increment=True)
    
    return {'success':True}

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
    
    db = Database()
    rows = list(reversed(db.get_images(session['user_id'])))
    image_dicts = []
    for row in rows:
        _, creator_user_id, match_user_id, img_path, img_date_published = row
        img_creator_name = Database().get_user_row(creator_user_id)[1]
        img_match_name = Database().get_user_row(match_user_id)[1]
        formatted_date_published = str(img_date_published)
        
        image_dicts.append({'creator_user_id':creator_user_id, 'creator_name':img_creator_name, 'match_user_id':match_user_id,
                            'match_name':img_match_name, 'img_path':img_path, 'formatted_date_published':formatted_date_published})
    
    return render_template('profile.html', paths=image_dicts)

@app.route('/user/<user_id>')
def user_page(user_id):
    if not session.get('user_id'):
        return redirect('/auth/login')
    
    if not session.get('current_streak') or not session.get('user_id'):
        session['current_streak'] = 0
    else:
        session['current_streak'] = Streak(session['user_id']).get_streak(session['current_streak'], increment=False)
    
    db = Database()
    
    current_viewer_followers = db.get_following(session['user_id'])
    user_row = db.get_user_row(user_id)
    _, name, username, _, major, year = user_row
    followers = []
    for id_ in db.get_followers(user_id):
        user_row = db.get_user_row(id_)
        followers.append((id_, user_row[1], user_row[2]))
    following = []
    for id_ in db.get_following(user_id):
        user_row = db.get_user_row(id_)
        following.append((id_, user_row[1], user_row[2]))
    
    rows = list(reversed(db.get_images(user_id)))
    image_dicts = []
    for row in rows:
        _, creator_user_id, match_user_id, img_path, img_date_published = row
        img_creator_name = Database().get_user_row(creator_user_id)[1]
        img_match_name = Database().get_user_row(match_user_id)[1]
        formatted_date_published = str(img_date_published)
        
        image_dicts.append({'creator_user_id':creator_user_id, 'creator_name':img_creator_name, 'match_user_id':match_user_id,
                            'match_name':img_match_name, 'img_path':'/'+img_path, 'formatted_date_published':formatted_date_published})
    
    return render_template('user.html', name=name, username=username, major=major, year=year, paths=image_dicts,
                           streak=session['current_streak'], followers=followers, following=following, user_id=int(user_id),
                           viewer_user_id=session['user_id'], is_following=session['user_id'] in followers, 
                           viewer_followers=current_viewer_followers)
    
@app.route('/follow', methods=['POST'])
def follow():
    db = Database()
    follower_id = request.json['followerID']
    following_id = request.json['followingID']
    db.add_follower(follower_id, following_id)
    
    return {'success':True}
    
@app.route('/unfollow', methods=['POST'])
def unfollow():
    db = Database()
    follower_id = request.json['followerID']
    following_id = request.json['followingID']
    db.remove_follower(follower_id, following_id)
    
    return {'success':True}

if __name__ == '__main__':
    app.run(port=3000, debug=True)