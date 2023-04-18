from enum import Enum
from random import choice


class ClothesStylesEnum(Enum):
    
    
    TOP_AND_BOTTOM_CLOTHES = "top and bottom"
    DRESS_ONLY = "dress only"
    ONSIE_ONLY = "onsie only"

    @staticmethod
    def get_random_style():
        all_styles = [style for style in ClothesStylesEnum]
        return choice(all_styles)
