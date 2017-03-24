# Hat Tip to https://blog.pythonanywhere.com/121/
from flask import Flask, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import secrets,datetime,hashlib
from flask_recaptcha import ReCaptcha

#Initialize app
app = Flask(__name__)
app.config["DEBUG"] = True

#Enable ReCaptcha
app.config["RECAPTCHA_ENABLED"] = True
app.config["RECAPTCHA_SITE_KEY"] = secrets.RECAPTCHA_SITE_KEY
app.config["RECAPTCHA_SECRET_KEY"] = secrets.RECAPTCHA_SECRET_KEY
recaptcha = ReCaptcha(app=app)

#Enable mySQL
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=secrets.username,
    password=secrets.password,
    hostname=secrets.hostname,
    databasename=secrets.databasename,
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
db = SQLAlchemy(app)

#Model
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    pid = db.Column(db.String(40))
    name = db.Column(db.String(9))
    timestamp = db.Column(db.DateTime)

#View
@app.route("/<hexval>/", methods=["GET", "POST"])
def index(hexval):
    error = None
    hash_object = hashlib.sha1(hexval.encode())
    hashedval = hash_object.hexdigest()
    if request.method == "POST":
        if recaptcha.verify():
            #Insert to DB
            comment = Comment(content=request.form["contents"],
                pid=hashedval,
                name=request.form["name"],
                timestamp=datetime.datetime.now(),
            )
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('index',hexval=hexval))
        else:
            error = "Please prove you are human by solving the recaptcha box!"
    return render_template("main_page.html", comments=Comment.query.filter_by(pid=hashedval).all(), error = error)

