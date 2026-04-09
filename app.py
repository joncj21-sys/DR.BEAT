from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

# Base de datos (archivo local)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# MODELO USUARIO
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREAR DB
with app.app_context():
    db.create_all()

# PELÍCULAS
peliculas = [
    {"titulo": "Acción Extrema", "url": "https://www.w3schools.com/html/movie.mp4"}
]

# HOME (PROTEGIDO)
@app.route("/")
@login_required
def inicio():
    return render_template("index.html", peliculas=peliculas)

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect(url_for("inicio"))

    return render_template("login.html")

# REGISTRO
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        nuevo = User(username=username, password=password)
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("registro.html")

# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()
