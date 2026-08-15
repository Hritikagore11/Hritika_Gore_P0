import json
import os

class FileHandler:
    FILE_PATH = "data/order_backup.json"
    def save_order(self, order_data):
        os.makedirs("data", exist_ok=True)

        orders = []

        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as file:
                orders = json.load(file)

        orders.append(order_data)

        with open(self.FILE_PATH, "w") as file:
            json.dump(orders, file, indent=4)