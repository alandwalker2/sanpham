
import sys
from PyQt6.uic import loadUi
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication,QDialog
from PyQt6.QtWidgets import QApplication,QMainWindow,QPushButton,QMessageBox,QCheckBox
from PyQt6 import QtWidgets,QtGui, QtCore
import json
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("dangnhap.ui", self)
        self.btlogin_2.clicked.connect(self.login)
        self.btregister33.clicked.connect(self.showregister)

#Check login   
    def login(self):
        username=self.usernameLineEdit_2.text()
        email=self.emailLineEdit_3.text()
        password=self.passwordLineEdit_2.text()
        with open("user.json", "r") as f:
            acc=json.load(f)
        
        

        if username =="" or password=="":
            mesageBox = QMessageBox()
            messageBox = QMessageBox()
            mesageBox.setWindowTitle("Lỗi")
            messageBox.setText("Thiếu dữ liệu")
            messageBox.setIcon( QMessageBox.Icon.Warning)
            messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
            messageBox.exec()
            return
        for account in acc:
            if account["name"] == username and account["email"] == email and account["password"] == password and self.checkBox.isChecked():
                self.close()
                menu.show()
                return
    
            elif account["name"] != username and  account["email"] != email and account["password"] != password :
                messageBox = QMessageBox()
                messageBox.setWindowTitle("Lỗi")
                messageBox.setText("Chưa đúng tài khoản hoặc mật khẩu!")
                messageBox.setIcon( QMessageBox.Icon.Warning)
                messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
                messageBox.exec()
                return
        if not  self.checkBox.isChecked() :
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Lỗi")
            messageBox.setText("Hãy đồng ý các điều khoản!")
            messageBox.setIcon( QMessageBox.Icon.Warning)
            messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
            messageBox.exec()
            return
    def showMainWindow(self):
        menu.show()
        self.close()
    def showregister(self):
        dangki.show()
        self.close()
#Trang dang ki
class Register3(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("dangki.ui", self)
        self.name = ""
        self.btlogin.clicked.connect(self.showlogin)
        self.btRegister.clicked.connect(self.Register)    
    def Register(self):
        self.name = self.fullname.text()
        self.email = self.emails.text()
        self.password = self.passwords.text()
        
        hoso= { 
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        
            
       # Read JSON file
        with open("user.json") as fp:
            listObj = json.load(fp)
        
        # Verify existing list
        print(listObj)
        print(type(listObj))
        
        listObj.append(hoso)
        
        # Verify updated list
        print(listObj)
        
        with open("user.json", 'w') as json_file:
            json.dump(listObj, json_file, 
                                indent=2,  
                                separators=(',',': '))
        
        print('Successfully appended to the JSON file')
        

        
            
    #Check dang ki
        if not self.name:
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Lỗi")
            messageBox.setText("Vui lòng nhập tên!")
            messageBox.setqIcon( QMessageBox.Icon.Warning)
            messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
            messageBox.exec()
            return
        if not self.email: 
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Lỗi")
            messageBox.setText("Vui lòng nhập email!")
            messageBox.setIcon( QMessageBox.Icon.Warning)
            messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
            messageBox.exec()
            return
        if not self.password:
            
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Lỗi")
            messageBox.setText("Vui lòng nhập mật khẩu!")
            messageBox.setIcon( QMessageBox.Icon.Warning)
            messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
            messageBox.exec()
            return
        if not self.checkBox.isChecked():
            
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Lỗi")
            messageBox.setText("Vui lòng đồng ý các điều khoản!")
            messageBox.setIcon( QMessageBox.Icon.Warning)
            messageBox.setStyleSheet("background-color:#f8f8f8;color:blue")
            messageBox.exec()
            return
        
        menu.show()
        self.close()
    
    def showlogin(self):
        dangnhap.show()
        self.close()
    def showMainWindow(self):
        menu.show()
        self.close()
#trang main
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)

     #menu

            
        self.logout1.clicked.connect(lambda:self.close())
        self.logout2.clicked.connect(lambda:self.close())

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
   
    


    #inventory
        self.addbt.clicked.connect(self.add)
        
    def to_table(self, table_widget, file_path):
        # Load data from JSON
        with open(file_path, "r") as f:
            data = json.load(f)

        #lOix

        
        
    
        for row, item in enumerate(data):
            for col, (key, value) in enumerate(item.items()):
                table_widget.setItem(row, col, QTableWidgetItem(str(value)))
        
    def add(Self):
        add.show()
class ADD(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add.ui', self)

# # Define the main function
def main():
    # Create an instance of the QApplication
    app = QApplication(sys.argv)

    # Create an instance of the LoginSignUpWindow and show it
    window = Login()
    window.show()

    

# Call the main function
if __name__== '__main__':
    app=QApplication(sys.argv) 
    dangnhap =Login()
    dangnhap.show()
    dangki=Register3()
    menu=Main()
    add=ADD()
    sys.exit(app.exec())


