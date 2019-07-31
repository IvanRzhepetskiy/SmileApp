import json
import sys
import threading
import time

import cv2
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.uic.properties import QtGui
import requests
from datetime import datetime
global threads
threads = []
global_token = 0

def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(t))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class ResumableTimer:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = threading.Timer(timeout, callback)
        self.startTime = time.time()


    def start(self):
        self.timer.start()

    def pause(self):
        self.timer.cancel()
        self.pauseTime = time.time()

    def resume(self):
        self.timer = threading.Timer(
            self.timeout - (self.pauseTime - self.startTime),
            self.callback)

        self.timer.start()

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
        #self.setGeometry(self.top, self.left, self.width, self.height)
        layoutMain = QVBoxLayout()
        layoutHLogin = QHBoxLayout()
        layoutHPassword = QHBoxLayout()
        layoutHButtons = QHBoxLayout()
        layoutMain.addLayout(layoutHLogin)
        layoutMain.addLayout(layoutHPassword)
        layoutMain.addLayout(layoutHButtons)
        login_label = QLabel('Login', self)
        login_label.move(100, 100)
        layoutHLogin.addWidget(login_label)

        buttonLogin = QPushButton('Login', self)
        buttonLogin.move(150, 300)
        buttonLogin.clicked.connect(self.buttonWindow1_onClick)
        layoutHButtons.addWidget(buttonLogin)

        self.lineEdit_Login = QLineEdit(self)
        self.lineEdit_Login.setGeometry(250, 100, 400, 30)
        layoutHLogin.addWidget(self.lineEdit_Login)

        password_label = QLabel('Password', self)
        password_label.move(100, 200)
        layoutHPassword.addWidget(password_label)

        self.lineEdit_Password = QLineEdit( self)
        self.lineEdit_Password.setEchoMode(QLineEdit.Password)
        self.lineEdit_Password.setGeometry(250, 200, 400, 30)
        layoutHPassword.addWidget(self.lineEdit_Password)

        buttonRegister = QPushButton('Register', self)
        buttonRegister.move(300, 300)
        buttonRegister.clicked.connect(self.buttonRegister_onClick)
        layoutHButtons.addWidget(buttonRegister)

        self.setLayout(layoutMain)
        self.show()



    @pyqtSlot()
    def buttonWindow1_onClick(self):
        global global_token
        self.statusBar().showMessage("Switched to window 1")
        # importing the requests library

        # defining the api-endpoint
        API_ENDPOINT = "http://127.0.0.1:8000/login_with_token/"

        # your API key here
        #API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api
        login = self.lineEdit_Login.text()
        password = self.lineEdit_Password.text()
        data = {
                "username": login,
                "password": password}

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=data)
        data = r.json()
        token = data['token']
        print(token)
        global_token = token
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s" % pastebin_url)
        if data['success']:
            self.cams = MainWindow()
            self.cams.show()
            self.close()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText('Логин неверный')


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

        self.line_edit_username = QLineEdit()
        layoutV2.addWidget(self.line_edit_username)

        self.line_edit_login = QLineEdit()
        layoutV2.addWidget(self.line_edit_login)

        self.line_edit_password = QLineEdit()
        layoutV2.addWidget(self.line_edit_password)

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
        API_ENDPOINT = "http://127.0.0.1:8000/register/"

        # your API key here
        # API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api
        data = {
            "username":  self.line_edit_username.text(),
            "login": self.line_edit_login.text(),
            "password": self.line_edit_password.text()
        }

        r = requests.post(url=API_ENDPOINT, data=data)
        #data = r.json()
        pastebin_url = r.text
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(pastebin_url)
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        print("The pastebin URL is:%s" % pastebin_url)
        self.cams = Window()
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonRegisterNewUser_onClick(self):
        print('Registered')
        pass

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Smile')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        self.timer_was_on = False
        self.timer_on_now = False
        self.start_recognizing = False
        self.recognising_started = False
        self.last_recognition_time = time.time()
        self.t = ResumableTimer(3, self.detection_thread)
        layoutMain = QVBoxLayout()
        layoutH1 = QHBoxLayout()
        layoutH2 = QHBoxLayout()
        layoutMain.addLayout(layoutH1)
        layoutMain.addLayout(layoutH2)

        button_start = QPushButton('Start')
        button_start.clicked.connect(self.onClick_start)
        layoutH1.addWidget(button_start)

        button_getStats = QPushButton('Get Statistics')
        button_getStats.clicked.connect(self.onClick_getStats)
        layoutH1.addWidget(button_getStats)

        self.label_smile = QLabel('Smile found: -')
        layoutH2.addWidget(self.label_smile)

        button_goMainWindow = QPushButton('<-')
        button_goMainWindow.clicked.connect(self.goMainWindow)
        layoutH1.addWidget(button_goMainWindow)

        self.setLayout(layoutMain)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def onClick_getStats(self):

        self.cams = StatisticsWindow()
        self.cams.show()
        self.close()


    def onClick_start(self):
        global global_token
        print(threading.currentThread().getName())
        if not self.recognising_started:
            self.t.start()
            self.recognising_started = True
        if not self.start_recognizing:
            self.start_recognizing = True
        else:
            self.start_recognizing = False
        if not self.timer_was_on:
            threads.append(self.t)

            self.timer_was_on = True

        else:
            self.timer_on_now = True
            self.label_smile.setText("hola")


            #self.t.resume()


        pass

    def detection_thread(self):

        while True:
            print(time.time() - self.last_recognition_time)
            if time.time() - self.last_recognition_time > 20:

                self.start_recognizing = True
            if not self.start_recognizing:
                print('Not recogn')
            else:
                font = cv2.FONT_HERSHEY_SIMPLEX

                facePath = "haarcascade_frontalface_default.xml"
                smilePath = "haarcascade_smile.xml"
                faceCascade = cv2.CascadeClassifier(facePath)
                smileCascade = cv2.CascadeClassifier(smilePath)

                cap = cv2.VideoCapture(0)
                cap.set(3, 640)
                cap.set(4, 480)

                sF = 1.05

                #while (cap.isOpened()):
                while (cap.isOpened() and self.start_recognizing):
                    #print(threading.currentThread().getName())
                    ret, frame = cap.read()  # Capture frame-by-frame
                    img = frame
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=sF,
                        minNeighbors=15,
                        minSize=(55, 55),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )
                    # ---- Draw a rectangle around the faces

                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        roi_gray = gray[y:y + h, x:x + w]
                        roi_color = frame[y:y + h, x:x + w]

                        smile = smileCascade.detectMultiScale(
                            roi_gray,
                            scaleFactor=1.7,
                            minNeighbors=9,
                            minSize=(25, 25),
                            flags=cv2.CASCADE_SCALE_IMAGE
                        )

                        for (x, y, w, h) in smile:
                            print("Found " + str(len(smile)) + " smiles!")
                            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 0, 0), 1)
                            cv2.putText(roi_color, 'SMILE', (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                            API_ENDPOINT = "http://127.0.0.1:8000/add_recognition/"
                            headers = {'Content-Type': 'application/json',
                                       'Authorization': "Token " + global_token}
                            data = {"Token": global_token, "time": format(datetime.now())}
                            print(global_token)
                            r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)
                            pastebin_url = r.text
                            print("The pastebin URL is:%s" % pastebin_url)
                            #time.sleep(3)
                            #cap.release()
                            #cv2.destroyAllWindows()
                            self.last_recognition_time = time.time()
                            self.start_recognizing = False
                            break
                        break
                            # time.sleep(20)
                    cv2.imshow('Smile Detector', frame)
                    c = cv2.waitKey(7) % 0x100

                    if c == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class StatisticsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        global global_token
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)


        API_ENDPOINT = "http://127.0.0.1:8000/get_recognition_stats/"

        # your API key here
        # API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api



        headers = {'Content-Type': 'application/json',
                   'Authorization': "Token " + global_token}
        data = {"Token": global_token}

        r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)
        # sending post request and saving response as response object
        data = r.json()
        print(data)
        list_of_dates = data['time_list']
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is!!!!!!!!!!!!!!!!!:%s" % pastebin_url)
        if data['success']:
            print('Success')
            self.plot(list_of_times=list_of_dates)

    def plot(self, list_of_times):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]
        data = list_of_times
        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
def main():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
    raise RuntimeError


if __name__ == '__main__':
    main()

