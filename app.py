import os

from bson import ObjectId
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


def check_token(html):
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'user_id': payload['id']})
        if user is not None:
            if html == 'login.html' or html == 'signup.html':
                return redirect(url_for('main'))

            return render_template(html, user_id=user['user_id'])
    except jwt.ExpiredSignatureError:
        return render_template('login.html', msg='로그인 만료')
    except jwt.exceptions.DecodeError:
        if html == 'signup.html':
            return render_template('signup.html')
        return render_template('login.html')


@app.route('/')
def home():
    return check_token('main.html')


@app.route('/main')
def main():
    return check_token('main.html')


@app.route('/signup')
def signup():
    return check_token('signup.html')


@app.route('/login')
def login():
    return check_token('login.html')


@app.route('/profile')
def profile():
    return check_token('profile.html')


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
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}

        return jsonify({
            'result': 'success',
            # 검증된 경우, access 토큰 반환
            'token': jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        })
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


# 로그아웃 API
@app.route("/api/logout", methods=['GET'])
def logout_proc():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({
            'result': 'success',
            'token': jwt.encode(payload, SECRET_KEY, algorithm='HS256'),
            'msg': '로그아웃 성공'
        })
    except jwt.ExpiredSignatureError or jwt.exceptions.DecodeError:
        return jsonify({
            'result': 'fail',
            'msg': '로그아웃 실패'
        })


# 파일 전송하기(POST)
@app.route('/api/upload', methods=['get', 'POST'])
def upload_file():
    if request.files['file']:
        if request.method == 'POST':
            file = request.files['file']
            content = request.form['content']
            user_id = request.form['user_id']
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', 'uploads', filename))
            feed_img_src = os.path.join('static', 'uploads', filename)
            created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

            doc = {
                'user_id': user_id,
                'feed_img_src': feed_img_src,
                'content': content,
                'created_at': created_at
            }

            db.feed.insert_one(doc)
            return redirect(url_for('login'))


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
    likes = list(db.like.find({}))
    feeds = objectIdToString(feeds)
    users = objectIdToString(users)
    likes = objectIdToString(likes)
    return jsonify({'all_users': users,
                    'all_feeds': feeds,
                    'all_likes': likes
                    })


@app.route('/api/comment', methods=['GET'])
def get_comment():
    comments = list(db.comment.find({}))
    comments = objectIdToString(comments)
    return jsonify({
        'all_comments': comments
    })


# 댓글 작성(POST) API
@app.route('/api/comment', methods=['POST'])
def save_comment():
    content_receive = request.form['content']
    feed_idx = request.form['feed_idx']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    user_id = request.form['user_id']
    doc = {
        'writer_id': user_id,
        'feed_idx': feed_idx,
        'content': content_receive,
        'created_at': created_at
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '댓글이 작성되었습니다.'})


# 좋아요(POST) API
@app.route('/api/like', methods=['POST'])
def like():
    user_id = request.form['user_id']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    likes = list(db.like.find({}))
    feed_idx = request.form['feed_idx']
    count = 0
    for i in range(len(likes)):
        if likes[i]['feed_idx'] == feed_idx:
            if likes[i]['user_id'] == user_id:
                count += 1
    if count == 1:
        db.like.delete_one({'user_id': user_id})
    else:
        doc = {
            'user_id': user_id,
            'feed_idx': feed_idx,
            'created_at': created_at
        }

        db.like.insert_one(doc)

    return jsonify({'msg': '좋아요.'})

# 리포스트
@app.route('/api/repost', methods=['POST'])
def save_repost():
    user_id = request.form['user_id']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    feed_idx = request.form['feed_idx']
    feeds = list(db.feed.find({}))
    feeds = objectIdToString(feeds)
    for i in range(len(feeds)):
        if feed_idx == feeds[i]['_id']:
            feed_img_src=feeds[i]['feed_img_src']
            content=feeds[i]['content']
            doc = {
                'user_id': user_id,
                'feed_img_src': feed_img_src,
                'content': content,
                'created_at': created_at
            }

            db.feed.insert_one(doc)
    return jsonify({'msg': '리포스트 완료.'})

@app.route('/api/removefeed', methods=['POST'])
def remove_feed():
    feed_idx = request.form['feed_idx']
    db.feed.delete_one({'_id': ObjectId(feed_idx)})

    return jsonify({'msg': '게시물이 삭제 되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
