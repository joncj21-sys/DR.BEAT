from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "cambia_esto_en_produccion"

# =========================
# BASE DE DATOS
# =========================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# LOGIN MANAGER
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# MODELO USUARIO
# =========================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
# CREAR TABLAS
# =========================
with app.app_context():
    db.create_all()

# =========================
# PELÍCULAS
# =========================
peliculas = [
    {"titulo": "Acción Extrema", "url": "https://www.w3schools.com/html/movie.mp4"},
    {"titulo": "Comedia Divertida", "url": "https://www.w3schools.com/html/movie.mp4"},
]

# =========================
# HOME
# =========================
@app.route("/")
@login_required
def inicio():
    return render_template("index.html", peliculas=peliculas, user=current_user)

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("inicio"))

        return "❌ Usuario o contraseña incorrectos"

    return render_template("login.html")

# =========================
# REGISTRO
# =========================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return "⚠️ Llena todos los campos"

        existe = User.query.filter_by(username=username).first()
        if existe:
            return "⚠️ Ese usuario ya existe"

        password_hash = generate_password_hash(password)

        nuevo = User(username=username, password=password_hash)
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("registro.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
