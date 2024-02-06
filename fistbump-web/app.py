import os
from flask import Flask
from dotenv import load_dotenv


load_dotenv('config.env')

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(os.environ['HOST'], int(os.environ['PORT']))