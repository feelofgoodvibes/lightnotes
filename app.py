from flask import request, flash, jsonify
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
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def index():
    user_notes = Note.query.filter(Note.author==current_user.id).all()

    return render_template("index.html", notes=user_notes)


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

        if len(title) > 100:
            title = title[:100]

        new_note = Note(title=title, text=text, author=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        return redirect("/note/"+str(new_note.id))


@app.route("/note/<int:note_id>", methods=["GET", "PUT", "DETETE"])
@login_required
def note(note_id):
    note_query = Note.query.filter(Note.id==note_id)
    note = note_query.first()

    if request.method == "GET":
        if not note or note.author != current_user.id:
            return redirect("/")

        return render_template("note.html", note=note)
    
    elif request.method == "DELETE":
        if not note:
            return jsonify({"error": "Note does not exists"}), 404

        if note.author != current_user.id:
            return ({"error": "Access denied"}), 403

        note_query.delete()
        db.session.commit()

        return ({"status": "OK"}), 204

    elif request.method == "PUT":
        if not note:
            return jsonify({"error": "Note does not exists"}), 404

        if note.author != current_user.id:
            return ({"error": "Access denied"}), 403

        title = request.form.get("title")
        text = request.form.get("text")

        print(f"Title: [{title}]", flush=True)
        print("Text:", text, flush=True)

        if not text:
            return ({"error": "Text field is empty"}), 400

        if len(title) > 100:
            return ({"error": "Maximum length of title field is 100"}), 400

        if not title:
            title = text[:100]

        note.title = title
        note.text = text
        note.edited = datetime.datetime.now()

        db.session.commit()

        return ({"status": "OK"}), 204

if __name__ == "__main__":
    app.run(debug=True)