from flask import *
from main import *

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter(User.email == email).first()
    
        if not email or not password:
            error = "Please fill out all fields."
            
        elif not user:
            error = "Email not found."
            
        elif not bcrypt.check_password_hash(user.password, password):
            error = "Password incorrect."
            
        else:
            session["user"] = user.id
            return redirect("/dashboard")
        
    return render_template("auth/login.html", error=error)

@auth.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        
        if not username or not password or not email:
            error = "Please fill out all fields."
            
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            error = "Username or email already in use."
            
        else:
            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            user = User(username=username, password=password_hash, email=email)
            db.session.add(user)
            db.session.commit()
            
            session["user"] = user.id
            return redirect("/dashboard")
            
    return render_template("auth/register.html", error=error)

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/auth/login")