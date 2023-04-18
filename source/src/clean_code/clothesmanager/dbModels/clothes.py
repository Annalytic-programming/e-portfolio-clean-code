from random import choice
from uuid import uuid4

from clothesmanager import db
from clothesmanager.enums.clothesStylesEnum import ClothesStylesEnum
from clothesmanager.mapper.styleToCategoriesMapper import StyleToCategoriesMapper


class Clothes(db.Model):

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    color = db.Column(db.Text)
    path_to_img = db.Column(db.Text, unique=True, default="default.png")

    def __repr__(self) -> str:
        return f"Clothes: {self.name} for category {self.category}"

    @staticmethod
    def add_clothing(name: str, category: str, color: str, path_to_img: str):
        clothing = Clothes(id=str(uuid4()), name=name, category=category, color=color, path_to_img=path_to_img)
        db.session.add(clothing)
        db.session.commit()
        return True

    @staticmethod
    def get_random_outfit():
        style_str = Clothes._get_random_style_string()
        category_list = Clothes._map_style_to_category_list(style_str)
        return Clothes._get_random_outfit_from_categories(category_list)

    @staticmethod
    def _get_random_outfit_from_categories(category_list) -> list[str]:
        final_outfit = []
        for category in category_list:
            clothes = Clothes.query.filter_by(category=category).all()
            clothing = choice(clothes)
            final_outfit.append(clothing)
        return final_outfit

    @staticmethod
    def _map_style_to_category_list(style: str):
        style_list = StyleToCategoriesMapper.map_style_string_to_categories(style)
        return Clothes._map_styles_to_category_string_list(style_list)
    
    @staticmethod
    def _map_styles_to_category_string_list(style_list):
        return [style.value for style in style_list]

    @staticmethod
    def _get_random_style_string():
        style = ClothesStylesEnum.get_random_style()
        return style.value
