from flask import request, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from objects import *


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            flash("Name and password fields are required!")
            return redirect("/signup")

        user = User.query.filter(User.login==login).first()

        if user:
            flash("User already exists")
            return redirect("/signup")

        new_user = User(login=login, password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            flash("Name and password fields are required!")
            return redirect("/login")

        user = User.query.filter(User.login==login).first()

        if not user:
            flash("This user does not exists!")
            return redirect("/login")

        if not check_password_hash(user.password, password):
            flash("Wrong password")
            return redirect("/login")

        login_user(user, remember=True)

        return redirect("/")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create.html")
    
    else:
        title = request.form.get("title")
        text = request.form.get("text")

        if not text:
            flash("Cannot create empty note")
            return redirect("/create")

        if not title:
            title = text[:20] + "..."

        new_note = Note(title=title, text=text, author=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        return redirect("/note/"+str(new_note.id))


if __name__ == "__main__":
    app.run(debug=True)