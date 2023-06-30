
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

app = Flask(__name__)
if os.environ.get("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    completed = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_task = Task(
            name=request.form.get("name"),
            completed=0
        )
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.all()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<task_id>")
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get(task_id)
    if request.method == "POST":
        task.name = request.form.get("name")
        if request.form.get("completed"):
            task.completed = 1
        else:
            task.completed = 0
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run()
