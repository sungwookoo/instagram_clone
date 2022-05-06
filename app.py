import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename

import datetime

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

# 보니까 이 두개 합쳐야함.. ㄷㄷ..
# 파일 전송하기(POST)
@app.route('/api/upload', methods=['get', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        content = request.form['content']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static','uploads',filename))
        feed_img_src = os.path.join('static','uploads',filename)
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
