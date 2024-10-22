from flask import Flask, render_template, request,redirect
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


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title_var = request.form["title"]
        description_var = request.form["description"]
        # title_var=request.form['title']
        todo = Todo(title=title_var, description=description_var)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("home.html", allTodo=allTodo)


@app.route("/delete/<int:s_no>")
def delete(s_no):
    todo=Todo.query.filter_by(s_no=s_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:s_no>")
def update(s_no):
    todo=Todo.query.filter_by(s_no=s_no).first()
    db.session.update(todo)
    db.session.commit()
    return redirect("/")




    
if __name__ == "__main__":
    app.run(debug=True, port=8001)
