from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "cambia_esto_en_produccion"

# BASE DE DATOS
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# MODELO USUARIO
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREAR BASE DE DATOS
with app.app_context():
    db.create_all()

# PELÍCULAS
peliculas = [
    {"titulo": "Acción Extrema", "url": "https://www.w3schools.com/html/movie.mp4"},
    {"titulo": "Comedia Divertida", "url": "https://www.w3schools.com/html/movie.mp4"}
]

# HOME (SIN ERROR)
@app.route("/")
def inicio():
    return render_template("index.html", peliculas=peliculas, user=current_user)

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("inicio"))

        return "❌ Usuario o contraseña incorrectos"

    return render_template("login.html")

# REGISTRO
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existe = User.query.filter_by(username=username).first()
        if existe:
            return "⚠️ Ese usuario ya existe"

        nuevo_usuario = User(username=username, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("registro.html")

# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# RUN LOCAL (Render usa gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
