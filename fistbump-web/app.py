import os
from database import Database
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template, jsonify, request


load_dotenv('config.env')

app = Flask(__name__)
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

@app.route('/save-waitlist-entry', methods=['POST'])
def save_waitlist_entry():
    data = request.json
    name, email = data['name'], data['email']
    Database().add_waitlist_user(name=name, email=email)
    
    return jsonify()

if __name__ == '__main__':
    app.run(os.environ['HOST'], int(os.environ['PORT']), debug=True)