from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QLabel

from src.components.bordered_frame import bordered_frame, BorderedFrame
from src.components.circle_button import CircleButton
from src.config.config_manager import register_callback


@bordered_frame
class OrganizeMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        print("OrganizeMenu: 整理菜单是未开发完成的功能，暂时不可用")
        self.parent_frame: BorderedFrame = None
        self.main_window = main_window
        self.setGeometry(0, 0, main_window.width(), main_window.height())

        self._setup_elements()

        register_callback(self._load_config_and_setup_variables)

    def initialize(self):
        self._load_config_and_setup_variables()
        self._setup_animation()

    def _setup_animation(self):
        self.parent_frame.add_to_animation_group__by_effect(
            [self.title_text, self.start_button, self.history_button, self.line1, self.line2])

    def _load_config_and_setup_variables(self):
        from src.config.config_manager import config
        self.parent_frame.open_time = config["动效"]["整理"]["进入时间"]
        self.parent_frame.close_time = config["动效"]["整理"]["退出时间"]
        self.parent_frame.real_width, self.parent_frame.real_height = config["主题"]["整理"]["窗口大小"]
        self.parent_frame.border_width = config["主题"]["数字6标识"]["描边宽度"]
        self.parent_frame.half_border_width = int(config["主题"]["数字6标识"]["描边宽度"] / 2)
        self.parent_frame.border_radius = config["主题"]["圆角半径"]
        self.parent_frame.background_color = list(map(int, config["主题"]["整理"]["背景颜色"].split(',')))
        self.parent_frame.border_color = list(map(int, config["主题"]["整理"]["描边颜色"].split(',')))
        self.parent_frame.window_height = self.main_window.height()

    def _setup_elements(self):
        self.icon = CircleButton(1, "6", 40, QFont.Medium,
                                 movable=True,
                                 parent=self,
                                 main_window=self.main_window)
        self.icon.move(0, self.main_window.height() - 6 - 80)

        self._create_title_label()
        self._create_start_organize_button()
        self._create_history_button()
        self._create_divider_lines()

    def _create_title_label(self):
        self.title_text = QLabel("整理", self)
        self._setup_label_style(self.title_text, 15, QFont.Normal,
                                color=QColor(255, 255, 255, 153))
        self.title_text.move(18, self.main_window.height() - 250 + 8)

    def _create_start_organize_button(self):
        self.start_button = QLabel("开始整理", self)
        self._setup_label_style(self.start_button, 20, QFont.Normal)
        self.start_button.move(18, self.main_window.height() - 250 + 55)

    def _create_history_button(self):
        self.history_button = QLabel("整理历史记录", self)
        self._setup_label_style(self.history_button, 20, QFont.Normal)
        self.history_button.move(18, self.main_window.height() - 250 + 110)

    def _create_divider_lines(self):
        self.line1 = self._create_divider(70, 18, self.main_window.height() - 250 + 50)
        self.line2 = self._create_divider(160, 18, self.main_window.height() - 250 + 107)

    def _create_divider(self, width, x, y):
        line = QLabel(self)
        line.setFixedSize(width, 4)
        line.move(x, y)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 153);")
        return line

    @staticmethod
    def _setup_label_style(label, font_size, font_weight, color=None):
        label.setFont(QFont("HarmonyOS Sans SC", font_size, font_weight))
        palette = label.palette()

        if color:
            palette.setColor(QPalette.WindowText, color)
        else:
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255, 255))

        label.setPalette(palette)
