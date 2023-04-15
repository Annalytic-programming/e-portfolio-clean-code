from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "MySecretKey"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = "login"


from application import controller