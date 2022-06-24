from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)



db_dv ='postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
    'user': 'shota',
    'password': '',
    'host': '127.0.0.1',
    'name': 'nenpassa2'
})
db_heroku = os.environ.get('DATABASE_URL')
#データベースのURIはデータベース名に合わせて適宜変更する
db_uri = db_heroku or db_dv

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Comment(db.Model):
    """[テーブルの定義を行うクラス]
    Arguments:
        db {[Class]} -- [ライブラリで用意されているクラス]
    """

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(20), nullable=False)
    twitter = db.Column(db.String(30), nullable=False)
    passdate = db.Column(db.DateTime, nullable=False)

    def __init__(self, pub_date, name, twitter, passdate):
        """[テーブルの各カラムを定義する]
        [Argument]
            id_ -- 投稿番号(プライマリキーなので、自動で挿入される)
            pub_date -- 投稿日時
            name -- 投稿者名
            comment -- 投稿内容
        """

        self.pub_date = pub_date
        self.name = name
        self.twitter = twitter
        self.passdate = passdate


@app.route("/")
def index():
    # テーブルから投稿データをSELECT文で引っ張ってくる
    text = Comment.query.all()
    return render_template("index.html", lines=text)


@app.route("/result", methods=["POST"])
def result():
    # 現在時刻　投稿者名　投稿内容を取得
    date = datetime.now()
    name = request.form["name"]
    twitter = request.form["twitter"]
    passdate = datetime.strptime(request.form['passdate'], '%Y-%m-%d')

    # テーブルに格納するデータを定義する
    comment_data = Comment(pub_date=date, name=name, twitter=twitter, passdate=passdate)
    # テーブルにINSERTする
    db.session.add(comment_data)
    # テーブルへの変更内容を保存
    db.session.commit()
    return render_template("result.html", twitter=twitter, passdate=passdate, name=name, now=date)

