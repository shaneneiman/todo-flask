from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    username = db.Column(db.String(100, collation="NOCASE"), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.func.current_timestamp())
    name = db.Column(db.String(200, collation="NOCASE"), nullable=False, server_default="")


class Todo(db.Model):
    __tablename__ = "todos"
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, server_default=False)
    date_created = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTIme, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())
