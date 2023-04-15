from flask import Flask, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
import flask_login
from flask_login import LoginManager, UserMixin
import uuid
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)

app.config["SECRET_KEY"] = "MySecretKey"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'pictures')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///annalytic.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "index"

class Clothes(db.Model):
    
    # the id of the chlothing
    id = db.Column(db.Text, primary_key=True)
    
    # the name of the chlothing
    name = db.Column(db.Text)
    
    # the category of the chlothing -> see Enum ClothingCategory
    category = db.Column(db.Text)
    
    # the id of the clothing
    color = db.Column(db.Text)
    
    # the image file
    path_to_img = db.Column(db.Text, unique=True, default="default.png")
    
    styles = ["dress only", "onsie only", "top and bottom"]
    
    def __repr__(self) -> str:
        return f"Clothes: {self.name} for category {self.category}"
    
    def add_clothing(name, category, color, path_to_img):
        clothing = Clothes(id=str(uuid.uuid4()), name=name, category=category, color=color, path_to_img=path_to_img)
        db.session.add(clothing)
        db.session.commit()
        return True
    
    def outfit(self):
        outfit = random.choice(self.styles)
        outfit_fin = []
        if outfit == "dress only":
            dresses = Clothes.query.filter_by(category="dress").all()
            dress = random.choice(dresses)
            outfit_fin.append(dress)
            shoes = Clothes.query.filter_by(category="shoe").all()
            shoe = random.choice(shoes)
            outfit_fin.append(shoe)
        if outfit == "onsie only":
            dresses = Clothes.query.filter_by(category="onsie").all()
            dress = random.choice(dresses)
            outfit_fin.append(dress)
            shoes = Clothes.query.filter_by(category="shoe").all()
            shoe = random.choice(shoes)
            outfit_fin.append(shoe)
        if outfit == "top and bottom":
            tops = Clothes.query.filter_by(category="top clothing").all()
            top = random.choice(tops)
            outfit_fin.append(top)
            bottoms = Clothes.query.filter_by(category="bottom clothing").all()
            bottom = random.choice(bottoms)
            outfit_fin.append(bottom)
            shoes = Clothes.query.filter_by(category="shoe").all()
            shoe = random.choice(shoes)
            outfit_fin.append(shoe)
        return outfit_fin
            


class User(db.Model, UserMixin):
    
    id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    
    def __repr__(self) -> str:
        return f'User("{self.username}")'
    
    def register(username, password):
        user = User(id=str(uuid.uuid4()), username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return True
    
    @staticmethod
    def get_uid(id):
        user = User.query.filter_by(id=id).first()
        return user
    
    @staticmethod
    def get_user(username):
        user = User.query.filter_by(username=username).first()
        return user
    
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, password):
            return True
        else:
            return False


class ClothesCategory(Enum):
    
    TOP_CLOTHING = "top clothing"
    BOTTOM_CLOTHING = "bottom clothing"
    ONSIE = "onsie"
    DRESS = "dress"
    SHOE = "shoe"


class Controller():

    @lm.user_loader
    def load_user(user_id):
        print ("user loaded")
        return User.get_uid(user_id)

    @app.context_processor
    def inject_time():
        if flask_login.current_user.is_active:
            return {'cu': flask_login.current_user.username}
        return {}
        
    @app.route('/create_user')
    def create_user():
        User.register("Anna", bcrypt.generate_password_hash("Admin1!").decode("utf-8"))
        return redirect(url_for("index"))

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def index():
        if flask_login.current_user.is_active:
            flask_login.logout_user()
            session.clear()
        if request.method == "GET":
            return render_template("index.html")
        else:
            username = request.form["username"]
            password = request.form["password"]
            if User.login(username, password):
                user = User.get_user(username)
                print (flask_login.current_user.is_active)
                flask_login.login_user(user)
                return redirect(url_for("userdashboard"))
            else:
                return render_template("index.html")

    @app.route("/userdashboard", methods=["GET", "POST"])
    @flask_login.login_required
    def udb():
        return render_template("dashboard.html", user=flask_login.current_user.username)

    @app.route("/new_clothes", methods=["GET", "POST"])
    @flask_login.login_required
    def add_clothes():
        if request.method == "GET":
            categories = []
            for category in ClothesCategory:
                categories.append(category.value)
            return render_template("add_clothes.html", categories=categories)
        else:
            c = request.form["category"]
            col = request.form["color"]
            n = request.form["name"]
            img = request.files["img"]
            path = img.filename
            path_to_save = os.path.join(app.config["UPLOAD_FOLDER"], path)
            if Clothes.add_clothing(n, c, col, path_to_save):
                img.save(path_to_save)
                return render_template("add_clothes.html", mess="Clothing added")
            else:
                return redirect(url_for("udb"))

    @app.route("/new_outfit", methods=["GET", "POST"])
    def outfit():
        if flask_login.current_user.is_active:
            user = flask_login.current_user.username
            return render_template("outfit.html", user=user)
        else:
            user = flask_login.current_user.username
            outfit = Clothes.outfit()
            return render_template("outfit.html", clothes=outfit, user=user)
        
    @app.route("/easteregg")
    # TODO - implement easteregg method
    def easteregg():
        pass
        


    
if __name__ == "__main__":
    app.run(debug=False)
    
    
