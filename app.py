import datetime

from flask import Flask, render_template, jsonify, request, redirect, url_for
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
def home():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'user_id': payload['id']})
        return render_template('main.html', user_id=user["user_id"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='로그인이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return render_template('login.html')


@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/api/register', methods=['POST'])
def sign_up():
    password = request.form['pw_give']
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {'user_id': request.form['id_give'],
           'password': hashed_pw,
           'name': request.form['name_give'],
           'phone': request.form['phone_give'],
           'email': request.form['email_give'],
           'profile_img_src': ''
           }
    db.users.insert_one(doc)

    return jsonify({'msg': '회원가입이 완료되었습니다.'})


# 로그인 API
@app.route("/api/login", methods=['POST'])
def login_proc():
    user_id = request.form['id_give']
    password = request.form['pw_give']
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user = db.user.find_one({'id': user_id, 'pw': hashed_pw})

    if user is None:
        payload = {'id': user_id,
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)}

        return jsonify({
            'result': 'success',
            # 검증된 경우, access 토큰 반환
            'token': jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        })
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
