from PyQt5.QtCore import (
    QPropertyAnimation, QParallelAnimationGroup, 
    pyqtProperty, Qt, QRect
)
from PyQt5.QtGui import (
    QFont, QPalette, QColor, 
    QPainter, QPen, QBrush
)
from PyQt5.QtWidgets import (
    QWidget, QLabel, QGraphicsOpacityEffect
)

from src.components.circle_button import CircleButton

class OrganizeMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setGeometry(0, 0, main_window.width(), main_window.height())
        
        self._animation_alpha = 0
        
        self._setup_elements()
        self._setup_open_animation()

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
        self.up_text = QLabel("整理", self)
        self._setup_label_style(self.up_text, 15, QFont.Normal, 
                                color=QColor(255, 255, 255, 153))
        self.up_text.move(18, self.main_window.height() - 250 + 8)
        
        self.up_text_opacity_effect = QGraphicsOpacityEffect()
        self.up_text_opacity_effect.setOpacity(0)
        self.up_text.setGraphicsEffect(self.up_text_opacity_effect)

    def _create_start_organize_button(self):
        self.start_button = QLabel("开始整理", self)
        self._setup_label_style(self.start_button, 20, QFont.Normal)
        self.start_button.move(18, self.main_window.height() - 250 + 55)
        
        self.start_button_opacity_effect = QGraphicsOpacityEffect()
        self.start_button_opacity_effect.setOpacity(0)
        self.start_button.setGraphicsEffect(self.start_button_opacity_effect)

    def _create_history_button(self):
        self.history_button = QLabel("整理历史记录", self)
        self._setup_label_style(self.history_button, 20, QFont.Normal)
        self.history_button.move(18, self.main_window.height() - 250 + 110)
        
        self.history_button_opacity_effect = QGraphicsOpacityEffect()
        self.history_button_opacity_effect.setOpacity(0)
        self.history_button.setGraphicsEffect(self.history_button_opacity_effect)

    def _create_divider_lines(self):
        self.line1 = self._create_divider(70, 18, self.main_window.height() - 250 + 50)
        self.line2 = self._create_divider(160, 18, self.main_window.height() - 250 + 107)

    def _create_divider(self, width, x, y):
        line = QLabel(self)
        line.setFixedSize(width, 4)
        line.move(x, y)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 153);")
        
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0)
        line.setGraphicsEffect(opacity_effect)
        
        return line

    def _setup_label_style(self, label, font_size, font_weight, color=None):
        label.setFont(QFont("HarmonyOS Sans SC", font_size, font_weight))
        palette = label.palette()
        
        if color:
            palette.setColor(QPalette.WindowText, color)
        else:
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255, 255))
        
        label.setPalette(palette)

    def _setup_open_animation(self):
        self.open_animation_group = QParallelAnimationGroup(self)
        
        self.organize_menu_open_animation = QPropertyAnimation(self, b"animation_alpha")
        self.organize_menu_open_animation.setDuration(500)
        self.organize_menu_open_animation.setStartValue(0)
        self.organize_menu_open_animation.setEndValue(255)
        self.open_animation_group.addAnimation(self.organize_menu_open_animation)

        # 添加文字和分割线的透明度动画
        opacity_effects = [
            self.up_text_opacity_effect,
            self.start_button_opacity_effect,
            self.line1.graphicsEffect(),
            self.history_button_opacity_effect,
            self.line2.graphicsEffect()
        ]

        for effect in opacity_effects:
            text_animation = QPropertyAnimation(effect, b"opacity")
            text_animation.setDuration(500)
            text_animation.setStartValue(0)
            text_animation.setEndValue(1)
            self.open_animation_group.addAnimation(text_animation)

    def start_open_animation(self):
        self.open_animation_group.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置边框和背景颜色
        brush = QBrush(QColor(42, 130, 228, self._animation_alpha))
        painter.setBrush(brush)

        pen = QPen(QColor(72, 143, 224, self._animation_alpha))
        pen.setWidth(6)
        painter.setPen(pen)

        # 绘制圆角矩形
        rect = QRect(0, 0, 270, 250)
        rect.moveTo(3, self.main_window.height() - 250 - 3)
        painter.drawRoundedRect(rect, 40, 40)

    @pyqtProperty(int)
    def animation_alpha(self):
        return self._animation_alpha

    @animation_alpha.setter
    def animation_alpha(self, value):
        self._animation_alpha = value
        self.update()
