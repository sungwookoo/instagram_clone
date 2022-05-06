import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt
import hashlib
from werkzeug.utils import secure_filename
import config
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# DB
# client = config.DbConfig().client
# db = client.dbinsta
client = MongoClient('localhost', 27017)
db = client.dbinsta

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
        return redirect(url_for('login'))
    except jwt.exceptions.DecodeError:
        return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('login.html')


@app.route('/api/register', methods=['POST'])
def sign_up():
    user = db.users.find_one({'user_id': request.form['id_give']})
    if user is not None:
        return jsonify({'result': 'duplication', 'msg': '이미 존재하는 사용자이름입니다.'})

    else:
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

    user = db.users.find_one({'user_id': user_id, 'password': hashed_pw})

    if user is not None:
        payload = {'id': user_id,
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}

        return jsonify({
            'result': 'success',
            # 검증된 경우, access 토큰 반환
            'token': jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        })
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/main')
def main():
    return render_template('main.html')


# 보니까 이 두개 합쳐야함.. ㄷㄷ..
# 파일 전송하기(POST)
@app.route('/api/upload', methods=['get', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        content = request.form['content']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static', 'uploads', filename))
        feed_img_src = os.path.join('static', 'uploads', filename)
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        doc = {
            'user_id': 'testId0',
            'feed_img_src': feed_img_src,
            'content': content,
            'created_at': created_at
        }

        db.feed.insert_one(doc)
        return redirect(url_for('main'))


# id를 문자열로 바꾸는 함수
def objectIdToString(find_list):
    results = []
    for i in find_list:
        i['_id'] = str(i['_id'])
        results.append(i)
    return results


@app.route('/api/feed', methods=['GET'])
def get_feed():
    users = list(db.users.find({}))
    feeds = list(db.feed.find({}))
    comments = list(db.comment.find({}))
    feeds = objectIdToString(feeds)
    users = objectIdToString(users)
    comments = objectIdToString(comments)
    return jsonify({'all_users': users,
                    'all_feeds': feeds,
                    'all_comments': comments
                    })


# 댓글 작성(POST) API
@app.route('/api/comment', methods=['POST'])
def save_comment():
    # id는 로그인기능받아오면 하고
    content_receive = request.form['content']
    feed_idx = request.form['feed_idx']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    doc = {
        'writer_id': 'testId0',
        'feed_idx': feed_idx,
        'content': content_receive,
        'created_at': created_at
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '댓글이 작성되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
