import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
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
        self.logout1.clicked.connect(self.close)
        self.logout2.clicked.connect(self.close)

        # Navigation Buttons
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

    def load_table_data(self):
        try:
            with open("products.json", "r") as f:
                data = json.load(f)
                self.products = data.get("data", [])
            self.populate_table()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.show_message("Error", f"Failed to load products: {e}", QMessageBox.Icon.Critical)

    def populate_table(self):
        self.tableWidget.setRowCount(len(self.products))
        for row, product in enumerate(self.products):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(product["name"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(product["price"]))

    def open_add_window(self):
        self.add_window = ADD()
        self.add_window.data_added.connect(self.load_table_data)
        self.add_window.show()

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
        product_data = {
            "name": self.name.text(),
            "import": self.import_2.text(),
            "inventory": self.quantity.text(),
            "HSD": self.HSD.text(),
            "NSX": self.NSX.text(),
            "price": self.Price.text()
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
