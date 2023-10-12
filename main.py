import os

from flask import *
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32).hex()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy()
bcrypt = Bcrypt()

db.init_app(app)
bcrypt.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    
@app.get("/")
def index():
    return redirect("/dashboard")
    
with app.app_context():
    from routes.auth import auth
    from routes.dashboard import dashboard
     
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    db.create_all()
