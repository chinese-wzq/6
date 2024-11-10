from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from src.ui.main_menu import MainMenu
from src.ui.chat_window import ChatWindow
from src.ui.organize_menu import OrganizeMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 800, 800)
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self)
        self.chat_window = ChatWindow(self)
        self.organize_menu = OrganizeMenu(self)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.chat_window)
        self.stacked_widget.addWidget(self.organize_menu)

    def open_ai_chat(self):
        self.stacked_widget.setCurrentIndex(1)
        self.stacked_widget.currentWidget().start_open_animation()

    def open_organize_menu(self):
        self.stacked_widget.setCurrentIndex(2)
        self.stacked_widget.currentWidget().start_open_animation()
