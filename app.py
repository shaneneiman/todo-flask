from flask import Flask, redirect, url_for, render_template, request
from sqlalchemy.pool import QueuePool
from models import db, User, Todo
from flask_user import login_required, UserManager
from flask_login import current_user

import os

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['DEBUG'] = os.environ.get("DEBUG")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_size": 10, "poolclass": QueuePool, "pool_pre_ping": True}
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

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        todo_input = request.form["todo_input"]
        due_date = request.form["due_date"]
        todo = Todo(text=todo_input, user=current_user, due_date=due_date)

        try:
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding the task"

    else:
        user = current_user
        todos = None
        if user.is_authenticated:
            todos = Todo.query.filter(Todo.user == user, Todo.completed == False).all()
        return render_template("index.html", todos=todos)

@app.route("/<int:todo_pk>/delete/")
def todo_delete(todo_pk):
    todo = Todo.query.get_or_404(todo_pk)

    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting the todo"

@app.route("/<int:todo_pk>/update/", methods=["POST", "GET"])
def todo_update(todo_pk):
    todo = Todo.query.get_or_404(todo_pk)

    if request.method == "POST":
        todo.text = request.form["todo_input"]
        todo.due_date = request.form["due_date"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            "There was a problem updating the todo"

    else:
        return render_template("todo_update.html", todo=todo)

@app.route("/<int:todo_pk>/complete/")
def todo_mark_completed(todo_pk):
    todo = Todo.query.get_or_404(todo_pk)

    if todo.completed == False:
        todo.completed = True
    else:
        todo.completed = False
    
    try:
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem updating the todo"

@app.route("/todos/completed/", methods=["GET"])
def todos_completed():
    user = current_user
    if user.is_authenticated:
        todos = Todo.query.filter(Todo.user == user, Todo.completed == True).all()
    return render_template("todos_completed.html", todos=todos)

if __name__ == "__main__":
    app.run(port=3000)
