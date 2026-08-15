from controller.ecommerce_controller import EcommerceController

def main():
    controller = EcommerceController()
    while True:
        print("\n------ E-COMMERCE APP -------")
        print("1. Register")
        print("2. Login")
        print("3. View Products")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            controller.register()
        elif choice == "2":
            controller.login()
        elif choice == "3":
            controller.view_products()
        elif choice == "4":
            print("Thank you for using the app!")
            break 
        else:
            print("invalid choice")

if __name__ == "__main__":
    main()
