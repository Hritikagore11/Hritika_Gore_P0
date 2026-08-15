from dao.category_dao import CategoryDAO
from model.category import Category

class CategoryService:
    def __init__(self):
        self.category_dao = CategoryDAO()

    def add_category(self, category_name):
        if not category_name:
            raise ValueError("Category name cannot be empty")

        category = Category(None, category_name)
        self.category_dao.add_category(category)

    def get_all_categories(self):
        return self.category_dao.get_all_categories()

    def get_category_by_id(self, category_id):
        return self.category_dao.get_category_by_id(category_id)