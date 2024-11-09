from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from .main_menu import MainMenu
from .organize_menu import OrganizeMenu

class Menu(QWidget):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        self.menus = QStackedWidget(self)  # 将在主菜单和整理菜单之间切换
        self.menus.setGeometry(0, 0, parent.width(), parent.height())
        self.main_menu = MainMenu(self.parent())
        self.organize_menu = OrganizeMenu(self.parent())
        self.menus.addWidget(self.main_menu)
        self.menus.addWidget(self.organize_menu)

    def open_organize_menu(self):
        self.menus.setCurrentIndex(1)
        self.organize_menu.start_open_animation()