from os import path

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "MySecretKey"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config["UPLOAD_FOLDER"] = path.join(path.dirname(__file__), "static", "pictures")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///annalytic.db"

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "render_index_view"

# Here is a break of the import pattern because of the import order.
# The Python interpreter doesn't know the Controller since it is part
# of the clothemanager module. So DO NOT change the import position.
from clothesmanager import clean_code_controller
