from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from src.components.circle_button import CircleButton

class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setGeometry(0, 0, main_window.width(), main_window.height())
        
        self.animation_group = QParallelAnimationGroup(self)

        self._create_buttons()
        self._setup_button_animations()

    def _create_buttons(self):
        ( 
            self.advice,
            self.ai_chat,
            self.organize,
            self.settings
        ) = [
            self._create_circle_button(*config) 
            # 按钮配置格式: (序号, 文本, 字体大小, 字体粗细, 回调函数)
            for config in [
                (5, "建议", 18, QFont.Medium, None),
                (4, "AI", 30, QFont.Black, self._open_ai_chat),
                (3, "整理", 18, QFont.Medium, self._open_organize_menu),
                (2, "设置", 18, QFont.Medium, None)
            ]
        ] # 依次为各个按钮赋值，创建按钮的参数一一对应
        self.settings.move(0, self.main_window.height()- 6 -80*2)
        self.icon = CircleButton(1, "6", 40, QFont.Medium, 
                                 movable=True, 
                                 parent=self, 
                                 main_window=self.main_window, 
                                 moving_callback=self._update_icon_position)
        self.icon.move(0, self.main_window.height() - 6 - 80)
        self.icon.press_callback = self.unfold

    def _create_circle_button(self, number, text, text_size, font_weight, press_callback=None):
        button = CircleButton(number, text, text_size, font_weight, parent=self)
        button.move(0, self.main_window.height() - 6 - 80 * number)
        
        # 为按钮创建动画
        button.QAnimation_height = self._create_height_animation(button)
        self.animation_group.addAnimation(button.QAnimation_height)
        
        if press_callback:
            button.press_callback = press_callback
        
        return button

    def _setup_button_animations(self):
        self.icon.QAnimation_height = self._create_height_animation(self.icon)
        self.animation_group.addAnimation(self.icon.QAnimation_height)

    def _create_height_animation(self, target):
        animation = QPropertyAnimation(target, b'animation_height')
        animation.setEasingCurve(QEasingCurve.OutQuint)
        return animation

    def _update_icon_position(self, pos):
        # 可以在这里添加图标移动时的额外逻辑
        pass

    def _fold_unfold_animation(self, unfold_or_fold: bool, duration: int):
        """
        实际执行折叠或展开动画
        这个函数会停止之前的动画，然后根据传入的参数执行折叠或展开动画

        :param unfold_or_fold: True为展开，False为折叠
        :param duration: 动画持续时间
        """

        self.animation_group.stop()
        self.icon.press_callback = {True: self.fold, False: self.unfold}[unfold_or_fold]
        self.icon.unfolded = unfold_or_fold
        
        for i in range(self.animation_group.animationCount()):
            animation = self.animation_group.animationAt(i)
            target = animation.targetObject()
            target.unfolded = unfold_or_fold
            if unfold_or_fold:
                animation.setStartValue(target.get_animation_height())
                animation.setEndValue(80 * target.number)
            else:
                animation.setStartValue(target.get_animation_height())
                animation.setEndValue(80)
            animation.setDuration(duration)
        
        self.animation_group.start()

    def unfold(self, duration: int = 1000):
        self._fold_unfold_animation(True, duration)

    def fold(self, duration: int = 1000):
        self._fold_unfold_animation(False, duration)

    def _open_ai_chat(self):
        self.fold(500)
        self.animation_group.finished.connect(self.main_window.open_ai_chat)

    def _open_organize_menu(self):
        self.fold(500)
        self.animation_group.finished.connect(self.main_window.open_organize_menu)
