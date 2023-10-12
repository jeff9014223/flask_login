from main import *
from flask import *
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user")
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            if user:
                return f(*args, **kwargs)
            
        return redirect("/auth/login")
    
    return decorated_function