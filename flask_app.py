# A very simple Flask Hello World app for you to get started with... https://blog.pythonanywhere.com/121/
from flask import Flask, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import secrets,datetime,hashlib
app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=secrets.username,
    password=secrets.password,
    hostname=secrets.hostname,
    databasename=secrets.databasename,
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    pid = db.Column(db.String(40))
    name = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime)

@app.route("/<hexval>/", methods=["GET", "POST"])
def index(hexval):
    hash_object = hashlib.sha1(hexval.encode())
    hashedval = hash_object.hexdigest()
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.filter_by(pid=hashedval).all())

    comment = Comment(content=request.form["contents"],
        pid=hashedval,
        name=request.form["name"],
        timestamp=datetime.datetime.now(),
    )
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index',hexval=hexval))

