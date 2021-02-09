from flask import Flask, redirect, url_for, render_template, request
from models import db
from flask_user import login_required, UserManager

import os

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['DEBUG'] = os.environ.get("DEBUG")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

# Flask-User Settings
USER_APP_NAME = "Flask To-Do"
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = True

# db.create_all()

# Setup Flask-User and specify User data-model
user_manager = UserManager(app, db, User)

@app.route("/")
def index():
    '''
    Home page
    '''
    return "Hello World"



if __name__ == "__main__":
    app.run(port=3000)
