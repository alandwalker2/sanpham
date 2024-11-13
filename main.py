import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QPushButton
from PyQt6 import uic, QtCore

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dangnhap.ui", self)
        self.btlogin_2.clicked.connect(self.login)
        self.btregister33.clicked.connect(self.show_register)

    def login(self):
        username = self.usernameLineEdit_2.text()
        email = self.emailLineEdit_3.text()
        password = self.passwordLineEdit_2.text()

        if not username or not password:
            self.show_message("Lỗi", "Thiếu dữ liệu", QMessageBox.Icon.Warning)
            return

        with open("user.json", "r") as f:
            accounts = json.load(f)

        for account in accounts:
            if account["name"] == username and account["email"] == email and account["password"] == password:
                if not self.checkBox.isChecked():
                    self.show_message("Lỗi", "Hãy đồng ý các điều khoản!", QMessageBox.Icon.Warning)
                    return
                self.close()
                menu.show()
                return

        self.show_message("Lỗi", "Sai tài khoản hoặc mật khẩu!", QMessageBox.Icon.Warning)

    def show_register(self):
        self.close()
        register.show()

    @staticmethod
    def show_message(title, text, icon):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStyleSheet("background-color:#f8f8f8;color:blue")
        message_box.exec()


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dangki.ui", self)
        self.btlogin.clicked.connect(self.show_login)
        self.btRegister.clicked.connect(self.register_user)

    def register_user(self):
        name = self.fullname.text()
        email = self.emails.text()
        password = self.passwords.text()

        if not name:
            self.show_message("Lỗi", "Vui lòng nhập tên!", QMessageBox.Icon.Warning)
            return
        if not email:
            self.show_message("Lỗi", "Vui lòng nhập email!", QMessageBox.Icon.Warning)
            return
        if not password:
            self.show_message("Lỗi", "Vui lòng nhập mật khẩu!", QMessageBox.Icon.Warning)
            return
        if not self.checkBox.isChecked():
            self.show_message("Lỗi", "Vui lòng đồng ý các điều khoản!", QMessageBox.Icon.Warning)
            return

        user_data = {"name": name, "email": email, "password": password}

        with open("user.json", "r+") as f:
            users = json.load(f)
            users.append(user_data)
            f.seek(0)
            json.dump(users, f, indent=2)

        self.close()
        menu.show()

    def show_login(self):
        self.close()
        login.show()

    @staticmethod
    def show_message(title, text, icon):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStyleSheet("background-color:#f8f8f8;color:blue")
        message_box.exec()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("menu.ui", self)

        # Set columns to stretch when window resizes
        header = self.productTable_2.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.searchButton.clicked.connect(self.search_product)

        # Navigation Buttons
        self.logout1.clicked.connect(self.close)
        self.logout2.clicked.connect(self.close)
        self.home1.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(0))
        self.home2.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(0))
        self.sell1.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(1))
        self.sell2.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(1))
        self.product1.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(2))
        self.product2.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(2))
        self.stat1.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(3))
        self.stat2.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(3))
        self.cus1.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(4))
        self.cus2.clicked.connect(lambda: self.stackedWidget11.setCurrentIndex(4))

        # Add button to open ADD window
        self.addbt.clicked.connect(self.open_add_window)

        # Load initial table data
        self.load_table_data()
    def search_product(self):
        # Get the search text from the QLineEdit
        search_text = self.searchLineEdit.text().strip().lower()

        # Filter products by name
        filtered_products = [
            product for product in self.products if search_text in product["name"].lower()
        ]

        # Display filtered products in the table
        self.populate_table(filtered_products)


    def load_table_data(self):
        try:
            with open("products.json", "r") as f:
                data = json.load(f)
                self.products = data.get("data", [])
                for product in self.products:
                    product["id"] = int(product["id"])
                    product["price"] = float(product["price"])  # Ensure price is a float
                self.populate_table()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.show_message("Error", f"Failed to load products: {e}", QMessageBox.Icon.Critical)




    def populate_table(self, products=None):
        # Use the provided product list or default to all products
        products = products if products is not None else self.products

        # Disable sorting while populating the table to avoid re-sorting issues
        self.productTable_2.setSortingEnabled(False)
        self.productTable_2.setRowCount(len(products))

        for row, product in enumerate(products):
            # Populate table as before
            self.productTable_2.setItem(row, 0, QTableWidgetItem(str(product["id"])))
            self.productTable_2.setItem(row, 1, QTableWidgetItem(product["name"]))
            self.productTable_2.setItem(row, 2, QTableWidgetItem(product["supplier"]))
            self.productTable_2.setItem(row, 3, QTableWidgetItem(product["quantity"]))
            self.productTable_2.setItem(row, 4, QTableWidgetItem(product["expiry_date"]))
            self.productTable_2.setItem(row, 5, QTableWidgetItem(product["manufacture_date"]))
            self.productTable_2.setItem(row, 6, QTableWidgetItem(f"{product['price']:.1f}"))


            # Create and add "Edit" and "Delete" buttons as before
            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")
            edit_button.clicked.connect(lambda _, row=row: self.edit_product(row))
            delete_button.clicked.connect(lambda _, row=row: self.delete_product(row))
            
            self.productTable_2.setCellWidget(row, 7, edit_button)
            self.productTable_2.setCellWidget(row, 8, delete_button)

        # Enable sorting after populating the table
        self.productTable_2.setSortingEnabled(True)

        # Set column headers if needed
        headers = ["ID", "Name", "Supplier", "quantity", "Expiry Date", "Manufacture Date", "Price", "Edit", "Delete"]
        self.productTable_2.setHorizontalHeaderLabels(headers)



    def open_add_window(self):
        self.add_window = ADD()
        self.add_window.data_added.connect(self.load_table_data)
        self.add_window.show()

    def delete_product(self, row):
        # Get the product ID from the selected row
        product_name = self.products[row]["name"]

        # Confirm delete action
        reply = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete {product_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove the product from the list and update JSON
            self.products.pop(row)
            self.update_json_file()

            # Refresh the table view
            self.populate_table()
    def edit_product(self, row):
        # Retrieve product data from the selected row
        product = self.products[row]

        # Open the EDIT window and pass the selected product data
        self.edit_window = EDIT(product)
        self.edit_window.data_edited.connect(self.load_table_data)  # Refresh table on edit
        self.edit_window.show()

    def update_json_file(self):
        with open("products.json", "w") as f:
            json.dump({"data": self.products}, f, indent=4)

    @staticmethod
    def show_message(title, text, icon):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.exec()

class ADD(QMainWindow):
    data_added = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("add.ui", self)
        self.pushButton.clicked.connect(self.add_product)

    def add_product(self):
        try:
            with open("products.json", "r") as f:
                file_data = json.load(f)
                max_id = max(int(product["id"]) for product in file_data["data"]) if file_data["data"] else 0
        except (FileNotFoundError, json.JSONDecodeError):
            max_id = 0

        product_data = {
            "id": str(max_id + 1),
            "name": self.name.text(),
            "supplier": self.import_2.text(),
            "quantity": self.quantity.text(),
            "expiry_date": self.expiry_date.text(),
            "manufacture_date": self.manufacture_date.text(),
            "price": float(self.Price.text())  # Ensure price is a float
        }

        self.save_product(product_data)
        self.close()



    def save_product(self, product_data):
        try:
            with open("products.json", "r+") as f:
                file_data = json.load(f)
                file_data["data"].append(product_data)
                f.seek(0)
                json.dump(file_data, f, indent=4)
            self.data_added.emit()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.show_message("Error", f"Failed to save product: {e}", QMessageBox.Icon.Critical)

    @staticmethod
    def show_message(title, text, icon):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.exec()

class EDIT(QMainWindow):
    data_edited = QtCore.pyqtSignal()

    def __init__(self, product):
        super().__init__()
        uic.loadUi("edit.ui", self)

        # Populate fields with existing product data
        self.name.setText(product["name"])
        self.import_2.setText(product["supplier"])
        self.quantity.setText(product["quantity"])
        self.expiry_date.setText(product["expiry_date"])
        self.manufacture_date.setText(product["manufacture_date"])
        self.Price.setText(f"{product['price']:.1f}")

        # Save the product ID for reference
        self.product_id = product["id"]

        # Connect the save button to the editing function
        self.pushButton.clicked.connect(self.edit_product)

    def edit_product(self):
        updated_product = {
            "id": self.product_id,
            "name": self.name.text(),
            "supplier": self.import_2.text(),
            "quantity": self.quantity.text(),
            "expiry_date": self.expiry_date.text(),
            "manufacture_date": self.manufacture_date.text(),
            "price": float(self.Price.text())  # Ensure price is a float
        }
        self.save_edited_product(updated_product)
        self.close()


    def save_edited_product(self, updated_product):
        try:
            with open("products.json", "r+") as f:
                file_data = json.load(f)
                # Update the product data in the list
                for i, product in enumerate(file_data["data"]):
                    if product["id"] == updated_product["id"]:
                        file_data["data"][i] = updated_product
                        break
                f.seek(0)
                json.dump(file_data, f, indent=4)
            self.data_edited.emit()  # Signal that data was edited
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.show_message("Error", f"Failed to save edited product: {e}", QMessageBox.Icon.Critical)

    @staticmethod
    def show_message(title, text, icon):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.exec()

def main():
    app = QApplication(sys.argv)
    global login, register, menu
    login = Login()
    register = Register()
    menu = Main()
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
