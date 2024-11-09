import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QWidget, QLabel, QStackedWidget
)

from src import ChatWindow, Menu


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(500, 500, 800, 800)

        # 设置窗口透明度
        self.setWindowOpacity(1)
        # 设置窗口为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 确保窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.stacked_widget = QStackedWidget()  # 将在菜单、设置、AI聊天、整理等窗口之间切换
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(Menu(self))
        self.stacked_widget.addWidget(ChatWindow(self))

    def open_ai_chat(self):
        self.stacked_widget.setCurrentIndex(1)
        self.stacked_widget.currentWidget().start_open_animation()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
