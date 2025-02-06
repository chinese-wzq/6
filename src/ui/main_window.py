from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from src.config.config_manager import register_callback
from src.ui.chat_window import ChatWindow
from src.ui.main_menu import MainMenu
from src.ui.organize_menu import OrganizeMenu
from src.ui.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._load_config_and_setup_variables()
        self.init_ui()

        register_callback(self._load_config_and_setup_variables)

    def _load_config_and_setup_variables(self):
        from src.config.config_manager import config
        self._main_window_width, self._main_window_height = config["主题"]["主窗口大小"]
        self._radius_border = config["主题"]["圆角半径"]
        self.setGeometry(0, 0, self._main_window_width, self._main_window_height)

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_menu = MainMenu(self)
        self.chat_window = ChatWindow(self)
        self.organize_menu = OrganizeMenu(self)
        self.organize_menu.child.initialize()
        self.settings_window = SettingsWindow(self)
        self.settings_window.child.initialize()

        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.chat_window)
        self.central_widget.addWidget(self.organize_menu)
        self.central_widget.addWidget(self.settings_window)

    def open_ai_chat(self):
        self.central_widget.setCurrentWidget(self.chat_window)
        self.chat_window.start_open_animation()

    def open_organize_menu(self):
        self.central_widget.setCurrentWidget(self.organize_menu)
        self.organize_menu.start_open_animation()

    def open_settings_window(self):
        self.central_widget.setCurrentWidget(self.settings_window)
        self.settings_window.start_open_animation()
