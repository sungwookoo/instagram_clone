from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

# import db_config
app = Flask(__name__)

# DB
# db_cf = db_config.DbConfig()
# db = db_cf.client.dbmygame
client = MongoClient('localhost', 27017)
db = client.dbinsta


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
