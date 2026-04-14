from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# CONFIG
app.secret_key = "secreto123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

UPLOAD_FOLDER = "static/videos"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"mp4", "webm", "ogg"}

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- MODELO ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- FUNCION VIDEO ----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- HOME ----------------
@app.route("/")
def home():
    videos = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", videos=videos)


# ---------------- SUBIR VIDEO ----------------
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "video" not in request.files:
        return redirect("/admin")

    file = request.files["video"]

    if file.filename == "":
        return redirect("/admin")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return redirect("/admin")


# ---------------- REGISTRO ----------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("registro.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect("/admin")

    return render_template("login.html")


# ---------------- ADMIN ----------------
@app.route("/admin")
@login_required
def admin():
    users = User.query.all()
    videos = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("admin.html", users=users, videos=videos)


# ---------------- ELIMINAR ----------------
@app.route("/delete_user/<int:id>")
@login_required
def delete_user(id):
    user = User.query.get(id)

    if user and user.username != "admin":
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin")


# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# ---------------- CREAR DB ----------------
with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin_user = User(username="admin", password="admin", role="admin")
        db.session.add(admin_user)
        db.session.commit()


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
