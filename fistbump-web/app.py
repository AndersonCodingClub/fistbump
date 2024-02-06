import os
from database import Database
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request


load_dotenv('config.env')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-waitlist-entry', methods=['POST'])
def save_waitlist_entry():
    data = request.json
    name, email = data['name'], data['email']
    Database().add_waitlist_user(name=name, email=email)
    
    return jsonify()

if __name__ == '__main__':
    app.run(os.environ['HOST'], int(os.environ['PORT']), debug=True)