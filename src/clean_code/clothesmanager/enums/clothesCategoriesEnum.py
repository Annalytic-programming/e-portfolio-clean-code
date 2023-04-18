from enum import Enum
from random import choice


class ClothesCategoriesEnum(Enum):
    
    
    TOP_CLOTHING = "top clothing"
    BOTTOM_CLOTHING = "bottom clothing"
    ONSIE = "onsie"
    DRESS = "dress"
    SHOES = "shoes"

    @staticmethod
    def get_random_clothing_category():
        categories = list[ClothesCategoriesEnum]
        return choice(categories)

    @staticmethod
    def get_all_clothing_categories():
        return list[ClothesCategoriesEnum]

    @staticmethod
    def get_all_clothing_category_values() -> list[str]:
        return [category.value for category in ClothesCategoriesEnum]
