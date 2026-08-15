from dao.product_dao import ProductDAO
from model.product import Product

class ProductService:
    def __init__(self):
        self.product_dao = ProductDAO()

    def get_all_products(self):
        return self.product_dao.get_all_product()

    def get_product_by_id(self, product_id):
        return self.product_dao.get_product_by_id(product_id)

    def search_products(self, keyword):
        if not keyword:
            raise ValueError("Search keyword cannot be empty")

        return self.product_dao.search_products(keyword)
    
    def get_products_paginated(self, page=1, page_size=5):
        if page < 1:
            raise ValueError("Invalid page number")

        return self.product_dao.get_products_paginated(
            page,
            page_size
        )

    def add_product(self, product_name, price, stock, supplier_id, category_id):
        try:
            self.product_dao.add_product(
                product_name,
                price,
                stock,
                supplier_id,
                category_id
            )

            return True, "Product added successfully"

        except Exception as e:
            return False, str(e)

    def update_product(self, product_id, product_name, price, stock, supplier_id, category_id):
        product = self.product_dao.get_product_by_id(product_id)

        if product is None:
            raise ValueError("Product not found")
        if not product_name:
            raise ValueError("Product name cannot be empty")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        product = Product(
            product_id,
            product_name,
            price,
            stock,
            supplier_id,
            category_id
        )

        self.product_dao.update_product(product)


    def delete_product(self, product_id):
        product = self.product_dao.get_product_by_id(product_id)

        if product is None:
            raise ValueError("Product not found")

        self.product_dao.delete_product(product_id)