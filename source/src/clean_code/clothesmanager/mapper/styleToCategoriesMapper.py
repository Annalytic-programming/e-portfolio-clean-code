from clothesmanager.enums.clothesCategoriesEnum import ClothesCategoriesEnum


class StyleToCategoriesMapper():
    
    @staticmethod
    def map_style_string_to_categories(style) -> list[ClothesCategoriesEnum]:
        styles = []
        if "top" in style:
            styles.append(ClothesCategoriesEnum.TOP_CLOTHING)
        if "bottom" in style:
            styles.append(ClothesCategoriesEnum.BOTTOM_CLOTHING)
        if "dress" in style:
            styles.append(ClothesCategoriesEnum.DRESS)
        if "onsie" in style:
            styles.append(ClothesCategoriesEnum.ONSIE)
        styles.append(ClothesCategoriesEnum.SHOES)
        return styles
        