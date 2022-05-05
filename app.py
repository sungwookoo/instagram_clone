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

# 파일 전송하기(POST)
@app.route('/api/upload', methods=['get', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static','uploads',filename))
        return 'success'

# 댓글 작성(POST) API
@app.route('/api/comment', methods=['POST'])
def save_comment():
    writer_receive = request.form['writer_id']
    content_receive = request.form['content']
    feed_idx = request.form['feed_idx']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    doc = {
        'writer_id': writer_receive,
        'feed_idx': feed_idx,
        'content': content_receive,
        'created_at': created_at
    }

    db.comments.insert_one(doc)

    return jsonify({'msg': '댓글이 작성되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
