import os
from dotenv import load_dotenv
from flask import Flask, render_template


load_dotenv('config.env')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(os.environ['HOST'], int(os.environ['PORT']), debug=True)