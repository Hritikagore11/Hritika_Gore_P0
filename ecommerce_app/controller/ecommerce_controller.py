from service.product_service import ProductService
from service.user_service import UserService
from service.cart_service import CartService
from service.order_service import OrderService
from service.category_service import CategoryService


class EcommerceController:
    def __init__(self):
        self.product_service = ProductService()
        self.user_service = UserService()
        self.cart_service = CartService()
        self.order_service = OrderService()
        self.category_service = CategoryService()

    def view_products(self):
        page = 1
        page_size = 5
        while True:
            try:
                products = self.product_service.get_products_paginated(page,page_size)

                print("\n------- PRODUCTS -------")
                print("Page:", page)

                if not products:
                    if page == 1:
                        print("No products available")
                    else:
                        print("No more products")
                    return

                for product in products:
                    print(product.product_id, "|", product.product_name, "| Rs.", f"{product.price:.2f}","| Stock:",product.stock)

                print("\n1. Next Page")
                print("2. Previous Page")
                print("3. Exit")

                choice = input("Enter choice: ")
                if choice == "1":
                    page += 1
                elif choice == "2":
                    if page > 1:
                        page -= 1
                    else:
                        print("Already on first page")
                elif choice == "3":
                    break
                else:
                    print("Invalid choice")

            except Exception as e:
                print("Unable to load products:", e)
                break

    def search_products(self):
        print("\n------- SEARCH PRODUCTS -------")

        keyword = input("Enter product name: ")
        if not keyword.strip():
            print("Search keyword cannot be empty")
            return

        try:
            products = self.product_service.search_products(keyword)
            if not products:
                print("No products found")
                return

            print("\n------- SEARCH RESULTS -------")
            for product in products:
                print(product.product_id, "|", product.product_name,"| Rs.", f"{product.price:.2f}","| Stock:",product.stock)

        except Exception as e:
            print("Search failed:", e)


    def register(self):
        print("\n------- REGISTER -------")

        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            success, message = self.user_service.register_user(
                name,
                email,
                password
            )
            print(message)

        except Exception as e:
            print("Registration failed")
            print(e)


    def login(self):
        print("\n----- LOGIN --------")

        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            user, message = self.user_service.login(email,password)
            print(message)

            if user is None:
                return

            print("\nWelcome,", user.name)
            print("Role:", user.role)

            if user.role == "CUSTOMER":
                self.customer_menu(user)
            elif user.role == "ADMIN":
                self.admin_menu(user)
            else:
                print("Unknown user role.")

        except Exception as e:
            print("Login failed:", e)


    def customer_menu(self, user):
        while True:
            print("\n------- CUSTOMER MENU -------")
            print("1. View Products")
            print("2. Search Products")
            print("3. Add to Cart")
            print("4. View Cart")
            print("5. Remove from Cart")
            print("6. Place Order")
            print("7. Order History")
            print("8. Generate Invoice")
            print("9. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_products()
            elif choice == "2":
                self.search_products()
            elif choice == "3":
                self.add_to_cart(user)
            elif choice == "4":
                self.view_cart(user)
            elif choice == "5":
                self.remove_from_cart(user)
            elif choice == "6":
                self.place_order(user)
            elif choice == "7":
                self.order_history(user)
            elif choice == "8":
                self.generate_invoice(user)
            elif choice == "9":
                print("Log out successful.")
                break
            else:
                print("Invalid choice")


    def add_to_cart(self, user):
        print("\n-------- ADD TO CART --------")
        try:
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity: "))

            if quantity <= 0:
                print("Quantity must be greater than 0")
                return

        except ValueError:
            print("Product ID and quantity must be numbers.")
            return

        try:
            success, message = self.cart_service.add_to_cart(
                user.user_id,
                product_id,
                quantity
            )

            print(message)

        except Exception as e:
            print("Unable to add product to cart")
            print(e)


    def view_cart(self, user):
        print("\n--------- MY CART ----------")

        try:
            cart_items = self.cart_service.view_cart(user.user_id)

            if not cart_items:
                print("Your cart is empty")
                return

            print(f"\n{'Product':<25}{'Price':>12}{'Quantity':>12}{'Total':>15}")
            print("-" * 64)

            total_amount = 0

            for item in cart_items:
                quantity = item[3]
                product_name = item[4]
                price = item[5]

                total = price * quantity
                total_amount += total

                print(
                    f"{product_name:<25}"
                    f"{price:>12.2f}"
                    f"{quantity:>12}"
                    f"{total:>15.2f}"
                )

            print("-" * 64)
            print(f"{'Total Amount:':<49}{total_amount:>15.2f}")

        except Exception as e:
            print("Unable to fetch cart:", e)

    def remove_from_cart(self, user):
        print("\n-------- REMOVE FROM CART --------")
        try:
            cart_id = int(input("Enter cart ID: "))

        except ValueError:
            print("Cart ID must be a number.")
            return

        try:
            success, message = self.cart_service.remove_from_cart(
                cart_id,
                user.user_id
            )

            print(message)

        except Exception as e:
            print("Unable to remove item from cart.")
            print("Error:", e)


    def place_order(self, user):
        print("\n-------- PLACE ORDER --------")

        try:
            success, message = self.order_service.place_order(
                user.user_id
            )
            print(message)

        except Exception as e:
            print("Unable to place order:", e)


    def order_history(self, user):
        print("\n--------- ORDER HISTORY -------")

        try:
            orders = self.order_service.get_order_history(user.user_id)

            if not orders:
                print("No orders found")
                return

            current_order_id = None
            for order in orders:
                order_id = order[0]

                if order_id != current_order_id:

                    print(f"\nOrder ID: {order[0]}")
                    print(
                        f"Date: {order[1]} | "
                        f"Total: Rs. {order[2]:.2f} | "
                        f"Status: {order[3]}"
                    )

                    print("\nItems:")
                    current_order_id = order_id

                print(
                    f"{order[4]} | "
                    f"Quantity: {order[5]} | "
                    f"Price: Rs. {order[6]:.2f}"
                )

        except Exception as e:
            print("Couldn't load order history")
            print(e)


    def generate_invoice(self, user):
        print("\n------- GENERATE INVOICE -------")
        try:
            order_id = int(input("Enter order ID: "))

        except ValueError:
            print("Order ID must be a number.")
            return

        try:
            success, result = self.order_service.generate_invoice(
                order_id,
                user.user_id
            )

            if success:
                print("Invoice generated successfully")
                print("File:", result)
            else:
                print(result)

        except Exception as e:
            print("Unable to generate invoice:", e)


    def admin_menu(self, user):
        while True:
            print("\n------- ADMIN MENU -------")
            print("1. View Products")
            print("2. Search Products")
            print("3. Add Product")
            print("4. Update Product")
            print("5. Delete Product")
            print("6. Add Category")
            print("7. View Categories")
            print("8. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_products()
            elif choice == "2":
                self.search_products()
            elif choice == "3":
                self.add_product()
            elif choice == "4":
                self.update_product()
            elif choice == "5":
                self.delete_product()
            elif choice == "6":
                self.add_category()
            elif choice == "7":
                self.view_categories()
            elif choice == "8":
                print("Log out successful.")
                break
            else:
                print("Invalid choice")


    def add_product(self):
        print("\n------- ADD PRODUCT -------")
        product_name = input("Enter product name: ")

        try:
            price = float(input("Enter price: "))
            stock = int(input("Enter stock: "))
            supplier_id = int(input("Enter supplier ID: "))
            category_id = int(input("Enter category ID: "))

        except ValueError:
            print("Price, stock, supplier ID and category ID must be numbers.")
            return

        try:
            success, message = self.product_service.add_product(
                product_name,
                price,
                stock,
                supplier_id,
                category_id
            )

            print(message)

        except Exception as e:
            print("Unable to add product:", e)


    def update_product(self):
        print("\n------- UPDATE PRODUCT -------")

        try:
            product_id = int(input("Enter product ID: "))
            product_name = input("Enter product name: ")
            price = float(input("Enter price: "))
            stock = int(input("Enter stock: "))
            supplier_id = int(input("Enter supplier ID: "))
            category_id = int(input("Enter category ID: "))

        except ValueError:
            print("Invalid input.")
            return

        try:
            success, message = self.product_service.update_product(
                product_id,
                product_name,
                price,
                stock,
                supplier_id,
                category_id
            )

            print(message)

        except Exception as e:
            print("Unable to update product:", e)


    def delete_product(self):
        print("\n------- DELETE PRODUCT -------")

        try:
            product_id = int(input("Enter product ID: "))

        except ValueError:
            print("Product ID must be a number.")
            return

        try:
            success, message = self.product_service.delete_product(
                product_id
            )
            print(message)

        except Exception as e:
            print("Unable to delete product:", e)


    def add_category(self):
        print("\n------- ADD CATEGORY -------")
        category_name = input("Enter category name: ")

        if not category_name.strip():
            print("Category name cannot be empty")
            return

        try:
            success, message = self.category_service.add_category(
                category_name
            )
            print(message)

        except Exception as e:
            print("Adding category failed:", e)


    def view_categories(self):
        try:
            categories = self.category_service.get_all_categories()

            if not categories:
                print("No categories found")
                return

            print("\n------- CATEGORIES -------")

            for category in categories:
                print(category.category_id, "-", category.category_name)

        except Exception as e:
            print("Unable to load categories:", e)