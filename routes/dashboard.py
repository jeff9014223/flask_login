from flask import *
from main import *

from middleware import login_required

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard.route("/", methods=["GET", "POST"])
@login_required
def index():
    error = None
    if request.method == "POST":
        pass
    
    return render_template("dashboard/index.html", error=error)

@dashboard.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    error = None
    if request.method == "POST":
        update_type = request.args.get("update")
        user = User.query.filter(User.id == session["user"]).first()
        
        if update_type == "username":
            new_username = request.form.get("new_username")
            curr_password = request.form.get("curr_password")
            
            if not new_username or not curr_password:
                error = "Please fill out all fields."
            
            elif not bcrypt.check_password_hash(user.password, curr_password):
                error = "Password incorrect."
            
            elif User.query.filter(User.username == new_username).first():
                error = "Username already in use."
                
            else:
                user.username = new_username
                db.session.commit()
            
        elif update_type == "password":
            new_password = request.form.get("new_password")
            curr_password = request.form.get("curr_password")
            
            if not new_password or not curr_password:
                error = "Please fill out all fields."
                
            elif not bcrypt.check_password_hash(user.password, curr_password):
                error = "Password incorrect."
                
            else:
                new_password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
                user.password = new_password_hash
                db.session.commit()

    return render_template("dashboard/profile.html", error=error)
    