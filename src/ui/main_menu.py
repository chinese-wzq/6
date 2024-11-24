from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from src.components.circle_button import CircleButton
from src.config.config_manager import config_manager

class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._button_created = False
        self.animation_group = QParallelAnimationGroup(self)
        self._load_config_and_setup_variables()
        self._create_buttons()
        self._setup_button_animations()

        global config_manager
        config_manager.register_callback(self._load_config_and_setup_variables)

    def _create_buttons(self):
        def create_and_move_button(number:int, text:str, font_pointSize:int,
                                   font_weight, movable: bool=False, parent=None,
                                   main_window=None, moving_callback: callable=None,press_callback: callable=None):
            button = CircleButton(number, text, font_pointSize, font_weight, movable, parent, main_window, moving_callback, press_callback)
            button.move(0, self._main_window_height - self._radius_width - self._radius_border * 2 * number)
            return button
        
        ( 
            self.advice,
            self.ai_chat,
            self.organize,
            self.settings,
            self.icon
        ) = [
            create_and_move_button(*config) 
            # 按钮配置格式: (序号, 文本, 字体大小, 字体粗细, 回调函数)
            for config in [
                (5, "建议", self._button_font_text["建议"], QFont.Medium, False, self, None, None, None),
                (4, "AI", self._button_font_text["AI"], QFont.Black, False, self, None, None, self._open_ai_chat),
                (3, "整理", self._button_font_text["整理"], QFont.Medium, False, self, None, None, self._open_organize_menu),
                (2, "设置", self._button_font_text["设置"], QFont.Medium, False, self, None, None, None),
                (1, "6", self._radius_border, QFont.Medium, True, self, self.main_window, self._update_icon_position, lambda:self.unfold(self._unfold_time))
            ]
        ] # 依次为各个按钮赋值，创建按钮的参数一一对应

        self._button_created = True

    def _setup_button_animations(self):
        for button in (self.advice, self.ai_chat, self.organize, self.settings):
            animation = QPropertyAnimation(button, b'animation_height')
            animation.setEasingCurve(QEasingCurve.OutQuint)
            button.QAnimation_height = animation
            self.animation_group.addAnimation(button.QAnimation_height)

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
        self.icon.press_callback = {True: lambda:self.fold(self._fold_time), False: lambda:self.unfold(self._unfold_time)}[unfold_or_fold]
        #需要注意的是，按钮的展开和收回时间不是立刻生效的设置，需要提醒用户。
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

    def unfold(self, duration: int):
        self._fold_unfold_animation(True, duration)

    def fold(self, duration: int):
        self._fold_unfold_animation(False, duration)

    def _open_ai_chat(self):
        self.fold(self._unfold_time)
        self.animation_group.finished.connect(self.main_window.open_ai_chat)

    def _open_organize_menu(self):
        self.fold(self._fold_time)
        self.animation_group.finished.connect(self.main_window.open_organize_menu)

    def _load_config_and_setup_variables(self):
        self._main_window_width = config_manager.config["主题"]["主窗口大小"]["宽度"]
        self._main_window_height = config_manager.config["主题"]["主窗口大小"]["高度"]
        self._radius_border = config_manager.config["主题"]["圆角半径"]
        self._radius_width = config_manager.config["主题"]["数字6标识"]["描边宽度"]
        self.setGeometry(0, 0, self._main_window_width, self._main_window_height)
        self._unfold_time = config_manager.config["动效"]["主菜单"]["展开时间"]
        self._fold_time = config_manager.config["动效"]["主菜单"]["收起时间"]
        self._button_font_text = config_manager.config["主题"]["主菜单按钮文字大小"]

        if self._button_created:
            self.icon.move(0, self._main_window_height - self._radius_width - self._radius_border * 2)
            for button in (self.advice, self.ai_chat, self.organize, self.settings):
                button.move(0, self._main_window_height - self._radius_width - self._radius_border * 2 * button.number)