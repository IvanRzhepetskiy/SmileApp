
"""import sys
from PyQt5 import QtWidgets, QtGui


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    l1 = QtWidgets.QLabel(w)
    l2 = QtWidgets.QLabel(w)
    l1.setText('Hello World')
    l2.setPixmap(QtGui.QPixmap(''))
    w.setWindowTitle('PYQt5 lesson 1')
    w.setGeometry(100, 100, 300, 200)
    l1.move(130, 20)
    w.show()
    sys.exit(app.exec_())

window()
"""
import cv2

import time


import threading

def gfg():
    font = cv2.FONT_HERSHEY_SIMPLEX

    facePath = "haarcascade_frontalface_default.xml"
    smilePath = "haarcascade_smile.xml"
    faceCascade = cv2.CascadeClassifier(facePath)
    smileCascade = cv2.CascadeClassifier(smilePath)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    sF = 1.05
    while (cap.isOpened()):
        print('SMILE')
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
                print("Found" + str(len(smile)) + "smiles!")
                cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(roi_color, 'SMILE', (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                time.sleep(3)
                cap.release()
                cv2.destroyAllWindows()

                break
                #time.sleep(20)
        cv2.imshow('Smile Detector', frame)
        c = cv2.waitKey(7) % 0x100
        if c == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    """
        Объявление чекбокса и иконки системного трея.
        Инициализироваться будут в конструкторе.
    """
    check_box = None
    tray_icon = None

    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))  # Устанавливаем размеры
        self.setWindowTitle("System Tray Application")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout(self)  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет
        grid_layout.addWidget(QLabel("Application, which can minimize to Tray", self), 0, 0)

        # Добавляем чекбокс, от которого будет зависеть поведение программы при закрытии окна
        self.check_box = QCheckBox('Minimize to Tray')
        grid_layout.addWidget(self.check_box, 1, 0)
        grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0)

        # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        '''
            Объявим и добавим действия для работы с иконкой системного трея
            show - показать окно
            hide - скрыть окно
            exit - выход из программы
        '''
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    # Окно будет закрываться только в том случае, если нет галочки в чекбоксе
    def closeEvent(self, event):
        if self.check_box.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )
            timer.start()

def start():
    while True:
        print('Working')
        time.sleep(1)
        flag = gfg()
        print("found")
        time.sleep(10)

timer = threading.Timer(2.0, start)




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())