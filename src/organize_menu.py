from PyQt5.QtCore import QRect, pyqtProperty, QPropertyAnimation, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QPalette, QColor, QBrush, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect

from .menu_circle_button import CircleButton

FONT = "HarmonyOS Sans SC"

class OrganizeMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setGeometry(0, 0, main_window.width(), main_window.height())

        self.line2_opacity_effect = None
        self.line2 = None
        self.button2_opacity_effect = None
        self.button2 = None
        self.line1_opacity_effect = None
        self.line1 = None
        self.button1_opacity_effect = None
        self.button1 = None
        self.up_text_opacity_effect1 = None
        self.up_text = None
        self.icon = None
        self.setup_elements()
        
        self.organize_menu_open_animation = None
        self.open_animation_group = None
        self._animation_alpha=0
        self.setup_open_animation()

    # 重写paintEvent来绘制圆角和边框
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置边框和背景颜色
        brush = QBrush(QColor(42, 130, 228,self._animation_alpha))
        painter.setBrush(brush)

        pen = QPen(QColor(72, 143, 224,self._animation_alpha))
        pen.setWidth(6)
        painter.setPen(pen)

        # 绘制圆角矩形
        rect = QRect(0, 0, 270, 250)
        rect.moveTo(3, self.main_window.height()-250-3)
        painter.drawRoundedRect(rect, 40, 40)

    @pyqtProperty(int)
    def animation_alpha(self):
        return self._animation_alpha

    @animation_alpha.setter
    def animation_alpha(self, value):
        self._animation_alpha = value
        self.update()

    def setup_open_animation(self):
        self.open_animation_group=QParallelAnimationGroup(self)

        self.organize_menu_open_animation=QPropertyAnimation(self, b"animation_alpha")
        self.organize_menu_open_animation.setDuration(500)
        self.organize_menu_open_animation.setStartValue(0)
        self.organize_menu_open_animation.setEndValue(255)
        self.open_animation_group.addAnimation(self.organize_menu_open_animation)

        #使文字和分割线透明度变化# 使文字和分割线透明度变化
        for opacity_effect in [self.up_text_opacity_effect1, self.button1_opacity_effect,
                               self.line1_opacity_effect, self.button2_opacity_effect,
                               self.line2_opacity_effect]:
            text_animation = QPropertyAnimation(opacity_effect, b"opacity")
            text_animation.setDuration(500)
            text_animation.setStartValue(0)
            text_animation.setEndValue(1)
            self.open_animation_group.addAnimation(text_animation)

    def start_open_animation(self):
        self.open_animation_group.start()
    
    def setup_elements(self):
        # 添加圆形按钮
        self.icon = CircleButton(1, "6", 40, QFont.Medium, movable=True, parent=self, main_window=self.main_window)
        self.icon.move(0, self.main_window.height() - 6 - 80)

        # 添加标题文字
        self.up_text = QLabel("整理", self)
        self.up_text.setFont(QFont(FONT, 15, QFont.Normal))  # 设置字体和字号
        palette = self.up_text.palette()
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255, 153))  # 设置文本颜色为白色
        self.up_text.setPalette(palette)
        self.up_text.move(18, self.main_window.height() - 250 + 8)
        self.up_text_opacity_effect1 = QGraphicsOpacityEffect()
        self.up_text_opacity_effect1.setOpacity(0)
        self.up_text.setGraphicsEffect(self.up_text_opacity_effect1)

        # 添加开始整理按钮
        self.button1 = QLabel("开始整理", self)
        self.button1.setFont(QFont(FONT, 20, QFont.Normal))
        palette = self.button1.palette()
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255, 255))
        self.button1.setPalette(palette)
        self.button1.move(18, self.main_window.height() - 250 + 55)
        self.button1_opacity_effect = QGraphicsOpacityEffect()
        self.button1_opacity_effect.setOpacity(0)
        self.button1.setGraphicsEffect(self.button1_opacity_effect)

        # 添加分割线1号
        self.line1 = QLabel(self)
        self.line1.setFixedSize(70, 4)
        self.line1.move(18, self.main_window.height() - 250 + 50)
        self.line1.setStyleSheet("background-color: rgba(255, 255, 255, 153);")
        self.line1_opacity_effect = QGraphicsOpacityEffect()
        self.line1_opacity_effect.setOpacity(0)
        self.line1.setGraphicsEffect(self.line1_opacity_effect)

        # 添加整理历史记录按钮
        self.button2 = QLabel("整理历史记录", self)
        self.button2.setFont(QFont(FONT, 20, QFont.Normal))
        palette = self.button2.palette()
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255, 255))
        self.button2.setPalette(palette)
        self.button2.move(18, self.main_window.height() - 250 + 110)
        self.button2_opacity_effect = QGraphicsOpacityEffect()
        self.button2_opacity_effect.setOpacity(0)
        self.button2.setGraphicsEffect(self.button2_opacity_effect)

        # 添加分割线2号
        self.line2 = QLabel(self)
        self.line2.setFixedSize(160, 4)
        self.line2.move(18, self.main_window.height() - 250 + 107)
        self.line2.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
        self.line2_opacity_effect = QGraphicsOpacityEffect()
        self.line2_opacity_effect.setOpacity(0)
        self.line2.setGraphicsEffect(self.line2_opacity_effect)