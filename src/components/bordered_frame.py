from PyQt5.QtCore import QRect, QParallelAnimationGroup, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsOpacityEffect


class AnimatedFrame(QWidget):
    def __init__(self):
        super().__init__()
        self._animation_alpha = 0
        self.open_time = 0
        self.close_time = 0
        self._setup_animation()

    def _setup_animation(self):
        self.open_animation_group = QParallelAnimationGroup(self)

    def add_to_animation_group__by_effect(self, targets: list):
        for target in targets:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0)
            target.setGraphicsEffect(opacity_effect)

            animation = QPropertyAnimation(opacity_effect, b'opacity')
            self.open_animation_group.addAnimation(animation)

    def add_to_animation_group__by_property(self, targets: list, property_name: bytes):
        for target in targets:
            animation = QPropertyAnimation(target, property_name)
            self.open_animation_group.addAnimation(animation)

    def _close_open_animation(self, open_or_close: bool, duration: int):
        """根据close_or_open的值，实际执行展开或收起菜单的操作"""
        self.open_animation_group.stop()
        for i in range(self.open_animation_group.animationCount()):
            animation = self.open_animation_group.animationAt(i)
            if open_or_close:
                animation.setStartValue(0.0)
                animation.setEndValue(1.0)
            else:
                animation.setStartValue(1.0)
                animation.setEndValue(0.0)
            animation.setDuration(duration)
        self.open_animation_group.start()

    def open(self):
        self._close_open_animation(True, self.open_time)

    def close(self):
        self._close_open_animation(False, self.close_time)

class BorderedFrame(AnimatedFrame):
    def __init__(self, wrapped_class,*args, **kwargs):
        super().__init__()
        self.child = wrapped_class(*args, **kwargs)
        self.child.parent_frame = self
        self.real_width, self.real_height = 0, 0
        self.border_width = 0
        self.half_border_width = 0
        self.border_radius = 0
        self.background_color = [0,0,0]
        self.border_color = [0,0,0]
        self.window_height = 0
        # 设置布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.child)

        _animation_alpha = 0.0
        self.add_to_animation_group__by_property([self],b"animation_alpha")

    @pyqtProperty(float)
    def animation_alpha(self):
        return self._animation_alpha

    @animation_alpha.setter
    def animation_alpha(self, value):
        self._animation_alpha = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置边框和背景颜色
        brush = QBrush(QColor(*self.background_color, int(self._animation_alpha*255)))
        painter.setBrush(brush)

        pen = QPen(QColor(*self.border_color, int(self._animation_alpha*255)))
        pen.setWidth(self.border_width)
        painter.setPen(pen)

        # 绘制圆角矩形
        rect = QRect(0, 0, self.real_width, self.real_height)
        rect.moveTo(self.half_border_width, self.window_height - self.real_height - self.half_border_width)
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

    def start_open_animation(self):
        self.open()

def bordered_frame(cls):
    """为传入的类添加边框，并管理透明度动画"""
    def wrapper(*args, **kwargs):
        return BorderedFrame(cls, *args, **kwargs)
    return wrapper