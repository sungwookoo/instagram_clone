import datetime

from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient
import jwt
import hashlib
import config

# import db_config
app = Flask(__name__)

# DB
client = MongoClient('localhost', 27017)
db = client.dbinsta

# client = config.DbConfig().client
# db = client.dbinsta


# JWT
SECRET_KEY = config.Config.SECRET_KEY


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def sign_up():
    password = request.form['pw_give']
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {'user_id': request.form['id_give'],
           'password': hashed_pw,
           'name': request.form['name_give'],
           'phone': request.form['phone_give'],
           'email': request.form['email_give']
           }
    db.users.insert_one(doc)

    return jsonify({'msg': '회원가입이 완료되었습니다.'})


@app.route("/login", methods=['POST'])
def login_proc():
    user_id = request.form['id_give']
    password = request.form['pw_give']
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    payload = {'id': user_id,
               'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)},
    user = db.users.find_one({'user_id': user_id})

    # 없는 ID
    if user is None:
        return jsonify({
            'result': 'none'
        })

    # 아이디, 암호 일치
    if user_id == user['user_id'] and password == hashed_pw:
        return jsonify({
            'result': 'success',
            # 검증된 경우, access 토큰 반환
            'token': jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        })

    # 아이디, 암호 불일치
    else:
        return jsonify({
            'result': 'wrong'
        })


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
