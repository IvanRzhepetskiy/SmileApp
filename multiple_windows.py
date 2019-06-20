import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui
import requests

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        login_label = QLabel('Login', self)
        login_label.move(100, 100)
        buttonWindow1 = QPushButton('Window1', self)
        buttonWindow1.move(150, 300)
        buttonWindow1.clicked.connect(self.buttonWindow1_onClick)
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setGeometry(250, 100, 400, 30)

        password_label = QLabel('Password', self)
        password_label.move(100, 200)
        self.lineEdit2 = QLineEdit( self)
        self.lineEdit2.setEchoMode(QLineEdit.Password)
        self.lineEdit2.setGeometry(250, 200, 400, 30)
        buttonRegister = QPushButton('Register', self)
        buttonRegister.move(300, 300)
        buttonRegister.clicked.connect(self.buttonRegister_onClick)
        self.show()



    @pyqtSlot()
    def buttonWindow1_onClick(self):
        self.statusBar().showMessage("Switched to window 1")
        # importing the requests library

        # defining the api-endpoint
        API_ENDPOINT = "http://127.0.0.1:8000/login_with_token/"

        # your API key here
        #API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api
        login = self.lineEdit1.text()
        data = {
                "login": login,
                "password": "passasd" }

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=data)
        data = r.json()
        token = data['token']
        print(token)
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s" % pastebin_url)
        self.cams = Window1(self.lineEdit1.text())
        self.cams.show()
        self.close()


    @pyqtSlot()
    def buttonRegister_onClick(self):
        self.cams = WindowRegister()
        self.cams.show()
        self.close()


class Window1(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Window1')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        label1 = QLabel(value)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.button.setIconSize(QSize(200, 200))

        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Click me!')
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        layoutH = QHBoxLayout()
        layoutH.addWidget(label1)
        layoutH.addWidget(self.button)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()

class WindowRegister(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('RegisterScreen')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        layoutV2 = QVBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addLayout(layoutV2)

        label_username = QLabel('Username')
        layoutV.addWidget(label_username)

        label_login = QLabel('Login')
        layoutV.addWidget(label_login)

        label_password = QLabel('Password')
        layoutV.addWidget(label_password)

        line_edit_username = QLineEdit()
        layoutV2.addWidget(line_edit_username)

        line_edit_login = QLineEdit()
        layoutV2.addWidget(line_edit_login)

        line_edit_password = QLineEdit()
        layoutV2.addWidget(line_edit_password)

        button_register = QPushButton('Register')
        button_register.clicked.connect(self.register_onClick)
        layoutV.addWidget(button_register)

        button_goMainWindow = QPushButton('<-')
        button_goMainWindow.clicked.connect(self.goMainWindow)
        layoutV2.addWidget(button_goMainWindow)

        self.setLayout(layoutH)


    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def register_onClick(self):
        API_ENDPOINT = "http://127.0.0.1:8000/login_with_token/"

        # your API key here
        # API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api
        login = self.lineEdit1.text()
        data = {
            "username": self.line_edit_username.text ,
            "login": self.line_edit_login.text,
            "password": self.line_edit_password.text
        }

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=data)
        data = r.json()
        token = data['token']
        print(token)
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s" % pastebin_url)
        pass

    @pyqtSlot()
    def buttonRegisterNewUser_onClick(self):
        print('Registered')
        pass

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Window()
    sys.exit(app.exec_())