from os import path

import flask_login
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from clothesmanager import app
from clothesmanager import bcrypt
from clothesmanager import login_manager
from clothesmanager.controller_helper import ControllerHelper as Helper
from clothesmanager.dbModels.clothes import Clothes
from clothesmanager.dbModels.user import User
from clothesmanager.enums.clothesCategoriesEnum import ClothesCategoriesEnum


class Controller():
    
    GET_AND_POST = ["GET", "POST"]

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_by_id(user_id)

    @staticmethod 
    @app.context_processor
    def inject_user():
        if flask_login.current_user.is_active:
            return {'current_user': flask_login.current_user.username}
        return {}

    @staticmethod 
    @app.route("/register")
    def register_user():
        User.register_user("Anna", bcrypt.generate_password_hash("Admin1!").decode("utf-8"))
        return redirect(url_for("index"))

    @app.route("/", methods=GET_AND_POST)
    @app.route("/login", methods=GET_AND_POST)
    def render_index_view():
        if request.method == "POST":
            return Helper.login_user_if_valid(request)
        return render_template("index.html")
    
    @staticmethod       
    @app.route("/logout")
    @flask_login.login_required
    def logout_user():
        return Helper.logout_user_and_clear_session(session)

    @staticmethod 
    @app.route("/dashboard", methods=GET_AND_POST)
    @flask_login.login_required
    def render_dashboard_view():
        return render_template("dashboard.html", user=flask_login.current_user.username)

    @staticmethod 
    @app.route("/add-clothes", methods=GET_AND_POST)
    @flask_login.login_required
    def render_add_clothes_view():
        categories = ClothesCategoriesEnum.get_all_clothing_category_values()
        if request.method == "POST":
            Helper.add_clothing_to_db_and_save_image(request, categories)
            msg = Helper.prepare_view_message(request)
            return render_template("add_clothes.html", msg=msg, categories=categories)
        return render_template("add_clothes.html", categories=categories)

    @staticmethod 
    @app.route("/generate-outfit")
    @flask_login.login_required
    def render_outfit_view():
        user = flask_login.current_user.username
        clothes = Clothes.get_random_outfit()
        return render_template("outfit.html", clothes=clothes, user=user)
    
    @staticmethod
    @app.route("/easteregg")
    @flask_login.login_required
    def render_easteregg_view():
        return render_template("easteregg.html")