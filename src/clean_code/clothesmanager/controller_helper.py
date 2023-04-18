from os import path

import flask_login
from flask import redirect, session
from flask import render_template
from flask import url_for

from clothesmanager import app
from clothesmanager.dbModels.clothes import Clothes
from clothesmanager.dbModels.user import User


class ControllerHelper():
    
    
    @staticmethod
    def add_clothing_to_db_and_save_image(request):
        category = request.form["category"]
        color = request.form["color"]
        name = request.form["name"]
        image = request.files["img"]
        return ControllerHelper.add_clothing_to_db(category, color, name, image)

    @staticmethod
    def add_clothing_to_db(category, color, name, image):
        path_to_db = path.join("static", "pictures", image.filename)
        return Clothes.add_clothing(name, category, color, path_to_db)
        
    @staticmethod
    def save_to_upload_folder(image):
        path_to_save = path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(path_to_save)
    
    @staticmethod
    def login_user_if_valid(request):
        username = request.form["username"]
        password = request.form["password"]
        if User.login_user(username, password):
            flask_login.login_user(User.get_user_by_username(username))
            return redirect(url_for("render_dashboard_view"))
        return render_template("index.html", msg="Login failed")
    
    @staticmethod
    def prepare_view_message(request):
        name = request.form["name"]
        return f"Clothing added: {name}"
    
    @staticmethod
    def logout_user_and_clear_session(session):
        flask_login.logout_user()
        session.clear()
        return redirect(url_for("render_index_view"))
    
    