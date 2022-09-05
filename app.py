from flask import request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from objects import *


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        return "EH"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = request.form.get("name")
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


@app.route("/logout", methods=["POST"])
def logout():
    pass


@app.route("/")
@login_required
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)