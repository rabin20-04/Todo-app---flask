from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_BINDS"] = {"users_data": "sqlite:///user.db"}
db = SQLAlchemy(app)


class user_data(db.Model):
    __bind_key__ = "users_data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        new_user = user_data(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = user_data.query.filter_by(email=email, password=password).first()
        if user:
            return redirect("/home")  
        else:
            return redirect("/error")  

    return render_template("login.html")


@app.route("/error", methods=["GET", "POST"])
def error_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = user_data.query.filter_by(email=email, password=password).first()
        if user:
            return redirect("/home")  
        else:
            return render_template("error.html")

    return render_template("error.html")


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
