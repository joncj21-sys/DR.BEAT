from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "drbeat_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ================= MODELO =================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # 👈 ADMIN / USER

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= DB INIT =================
with app.app_context():
    db.create_all()

    # 👑 ADMIN AUTOMÁTICO
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("1234"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

# ================= DECORADOR ADMIN =================
def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return "🚫 Acceso denegado (solo admin)"
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ================= HOME =================
@app.route("/")
@login_required
def home():
    return render_template("index.html", user=current_user)

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))

        return render_template("login.html", error="❌ Error login")

    return render_template("login.html")

# ================= REGISTRO =================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "Usuario existe"

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("registro.html")

# ================= ADMIN PANEL =================
@app.route("/admin")
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

# ================= DELETE USER =================
@app.route("/delete_user/<int:id>")
@login_required
@admin_required
def delete_user(id):
    user = User.query.get(id)

    if user.username == "admin":
        return "No puedes borrar admin"

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin"))

# ================= LOGOUT =================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
