from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):

    s_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return (
            f"{self.s_no} --- {self.title}---{self.description}---{self.date_created}"
        )


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title_var = request.form["title"]
        description_var = request.form["description"]

        todo = Todo(title=title_var, description=description_var)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("home.html", allTodo=allTodo)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/delete/<int:s_no>")
def delete(s_no):
    todo = Todo.query.filter_by(s_no=s_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/home")


@app.route("/update/<int:s_no>", methods=["GET", "POST"])
def update(s_no):
    if request.method == "POST":
        title_var = request.form["title"]
        description_var = request.form["description"]
        todo = Todo.query.filter_by(s_no=s_no).first()
        todo.title = title_var
        todo.description = description_var
        db.session.add(todo)
        db.session.commit()
        return redirect("/home")

    todo = Todo.query.filter_by(s_no=s_no).first()

    return render_template("update.html", todo=todo)


if __name__ == "__main__":
    app.run(debug=True, port=8001)


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]

#         todo = Todo(email=email, password=password)
#         db.session.add(todo)
#         db.session.commit()
#     allData = Todo.query.all()
#     return render_template("home.html", allData=allData)
