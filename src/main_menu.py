from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from .menu_circle_button import CircleButton


class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        # 添加按钮、初始化动画、绑定跳转、设置按钮位置
        self.animation_group = QParallelAnimationGroup(self)

        self.advice = CircleButton(5, "建议", 18, QFont.Medium, parent=self)
        self.advice.move(0, main_window.height()-6-80*5)
        self.animation_group.addAnimation(self.advice.QAnimation_height)

        self.ai_chat = CircleButton(4, "AI", 30, QFont.Black, parent=self)
        self.ai_chat.move(0, main_window.height()-6-80*4)
        self.animation_group.addAnimation(self.ai_chat.QAnimation_height)
        self.ai_chat.press_callback = lambda: self.open_ai_chat()  # 单击后跳转到AI聊天

        self.organize = CircleButton(3, "整理", 18, QFont.Medium, parent=self)
        self.organize.move(0, main_window.height()-6-80*3)
        self.animation_group.addAnimation(self.organize.QAnimation_height)
        self.organize.press_callback = lambda: self.open_organize_menu()  # 单击后跳转到整理菜单

        self.settings = CircleButton(2, "设置", 18, QFont.Medium, parent=self)
        self.settings.move(0, main_window.height()-6-80*2)
        self.animation_group.addAnimation(self.settings.QAnimation_height)

        self.icon = CircleButton(1, "6", 40, QFont.Medium, movable=True, parent=self, main_window=self.main_window)
        self.icon.move(0, main_window.height()-6-80)
        self.icon.press_callback = self.unfold  # 单击后展开

    def unfold(self, duration: int = 1000):
        self.animation_group.stop()
        self.icon.press_callback = self.fold
        for i in range(self.animation_group.animationCount()):
            animation = self.animation_group.animationAt(i)
            animation.targetObject().prepare_animation_height(animation.targetObject().get_animation_height(),
                                                              80 * animation.targetObject().number, duration)
        self.animation_group.start()

    def fold(self, duration: int = 1000):
        if self.animation_group.state() == QPropertyAnimation.Running:
            self.animation_group.stop()
        self.icon.press_callback = self.unfold
        for i in range(self.animation_group.animationCount()):
            animation = self.animation_group.animationAt(i)
            animation.targetObject().prepare_animation_height(animation.targetObject().get_animation_height(), 80,
                                                              duration)
        self.animation_group.start()

    def open_ai_chat(self):
        self.fold(300)
        self.animation_group.finished.connect(self.main_window.open_ai_chat)

    def open_organize_menu(self):
        self.fold(300)
        self.animation_group.finished.connect(self.parent().parent().open_organize_menu)  # 在Menu类中继续
