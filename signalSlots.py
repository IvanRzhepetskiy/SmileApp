"""


import sys
from PyQt5 import QtWidgets

import requests

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.b = QtWidgets.QPushButton('Push Me')
        self.l = QtWidgets.QLabel('I have not been clicked yet')

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.l)
        h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.b)
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('PyQt5 Lesson 5')

        self.b.clicked.connect(self.btn_click)

        self.show()

    def btn_click(self):
        userdata = {'heightdata': 20}
        r = requests.post("http://127.0.0.1:8000/idealweight/", json=userdata)
        print(r.status_code, r.reason)
        print(r.text)
        self.l.setText('I have been clicked')


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
"""

