# 🛒 E-Commerce Application

A console-based **E-Commerce Application developed using Python and MySQL**.  
The application supports separate **Customer and Admin roles** and follows a layered architecture for better organization and maintainability.

##  Features

### Customer Features
- User Registration
- User Login
- View Products
- Product Pagination
- Search Products
- Add Products to Cart
- View Cart
- Remove Products from Cart
- Place Orders
- View Order History
- Generate PDF Invoice
- Logout

### 👨‍💼 Admin Features
- Admin Login
- View Products
- Product Pagination
- Search Products
- Add Product
- Update Product
- Delete Product
- Add Category
- View Categories
- Logout

### Additional Features
- MySQL Database Integration
- Role-Based Access
- Input Validation
- Exception Handling
- File Management
- PDF Invoice Generation
- Unit Testing using `unittest`
- Mocking using `MagicMock`

---

## Project Structure

```text
ecommerce_app/
│
├── controller/
│   └── ecommerce_controller.py
│
├── service/
│   ├── user_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   ├── order_service.py
│   └── category_service.py
│
├── dao/
│   ├── user_dao.py
│   ├── product_dao.py
│   ├── cart_dao.py
│   ├── order_dao.py
│   └── category_dao.py
│
├── model/
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   └── ...
│
├── config/
│   └── database.py
│
├── invoice/
│   └── invoice_generator.py
│
├── utils/
│   └── file_handler.py
│
├── tests/
│   ├── test_user_service.py
│   ├── test_cart_service.py
│   └── test_order_service.py
│
├── invoices/
│
├── main.py
├── requirements.txt
└── README.md