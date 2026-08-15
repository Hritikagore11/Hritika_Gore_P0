class User:
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

class Customer(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, "CUSTOMER")

class Admin(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password,"ADMIN")

