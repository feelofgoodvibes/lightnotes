from objects import *


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    pass


@app.route("/")
def index():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)