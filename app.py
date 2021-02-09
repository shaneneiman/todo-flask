from flask import Flask, redirect, url_for, render_template, request
from models import db, User
from flask_user import login_required, UserManager

import os

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['DEBUG'] = os.environ.get("DEBUG")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.environ.get("DEBUG")
app.config['MAIL_DEBUG'] = 0
db.init_app(app)

# Flask-Mail SMTP server settings
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get("GMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("GMAIL_PASSWORD")

# Flask-User Settings
app.config['USER_APP_NAME'] = "Flask To-Do"
app.config['USER_ENABLE_EMAIL'] = False      # Disable email authentication
app.config['USER_ENABLE_USERNAME'] = True    # Enable username authentication
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True
app.config['USER_EMAIL_SENDER_EMAIL'] = os.environ.get("GMAIL_USERNAME")
app.config['USER_EMAIL_SENDER_NAME'] = "Flask To-Do"

# Creat Database
db.create_all()

# Setup Flask-User and specify User data-model
user_manager = UserManager(app, db, User)

@app.route("/")
def index():
    '''
    Home page
    '''
    return render_template("index.html")



if __name__ == "__main__":
    app.run(port=3000)
