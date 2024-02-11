import os
from database import Waitlist
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template, jsonify, request
from email_verification import handle_verification, check_verification_code, delete_verification_code


load_dotenv('config.env')

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send-verification', methods=['POST'])
def send_verification():
    data = request.json
    name, email = data['name'], data['email']
    if Waitlist().is_waitlist_user(email):
        return jsonify({'FAIL': 'DUPLICATE'}), 400
    
    handle_verification(email, name)
    return jsonify()
    
@app.route('/check-code', methods=['POST'])
def check_code():
    data = request.json
    name, email, code = data['name'], data['email'], data['verificationCode'].strip()
    is_correct_verification_code = check_verification_code(email, code)
    
    if is_correct_verification_code:
        Waitlist().add_waitlist_user(name, email)
        delete_verification_code(email)
        
    return jsonify({'isValid': is_correct_verification_code})

if __name__ == '__main__':
    app.run(os.environ['HOST'], int(os.environ['PORT']), debug=True)