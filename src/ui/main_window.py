from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from src.ui.main_menu import MainMenu
from src.ui.chat_window import ChatWindow
from src.ui.organize_menu import OrganizeMenu
from src.config.config_manager import config_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._load_config_and_setup_window()

        global config_manager
        config_manager.register_callback(self._load_config_and_setup_window)

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

    def cleanup(self):
        global config_manager
        del config_manager

    def closeEvent(self, a0):
        self.cleanup()
        return super().closeEvent(a0)
    
    def _load_config_and_setup_window(self):
        '''
        加载配置文件，并配置窗口大小和位置
        '''
        global config_manager
        screen_geometry = self.screen().availableGeometry()
        window_width = config_manager.config["主题"]["主窗口大小"]["宽度"]
        window_height = config_manager.config["主题"]["主窗口大小"]["高度"]
        x = int(screen_geometry.width()/5*4)
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

