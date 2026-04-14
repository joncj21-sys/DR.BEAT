from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "secreto123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# 🔹 MODELO USUARIO
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 🔹 HOME
@app.route("/")
def home():
    return render_template("index.html")


# 🔹 REGISTRO
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username=username, password=password, role="user")
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("registro.html")


# 🔹 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect("/admin")

    return render_template("login.html")


# 🔹 ADMIN
@app.route("/admin")
@login_required
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)


# 🔹 ELIMINAR USUARIO
@app.route("/delete_user/<int:id>")
@login_required
def delete_user(id):
    user = User.query.get(id)

    if user.username != "admin":
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin")


# 🔹 LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# 🔹 CREAR DB
with app.app_context():
    db.create_all()

    # Crear admin si no existe
    if not User.query.filter_by(username="admin").first():
        admin_user = User(username="admin", password="admin", role="admin")
        db.session.add(admin_user)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
