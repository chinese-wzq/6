from PyQt5.QtCore import (
    QRect, pyqtProperty, QEasingCurve, 
    QPropertyAnimation, Qt, QTimer, QPoint
)
from PyQt5.QtGui import (
    QPainter, QBrush, QColor, QPen, QFont
)
from PyQt5.QtWidgets import QWidget

from src.config.config_manager import config_manager

class CircleButton(QWidget):
    def __init__(
        self, 
        number, 
        text, 
        text_size, 
        font_weight, 
        movable=False, 
        parent=None, 
        main_window=None, 
        moving_callback=None
    ):
        super().__init__(parent)
        self._animation_alpha = 255
        self.number = number
        self.text = text
        self.text_size = text_size
        self.font_weight = font_weight
        
        self.movable = movable
        self.mouse_drag_pos = None
        self.is_moving = False
        
        self.press_callback = None
        self.main_window = main_window
        self.moving_callback = moving_callback

        self.unfolded = False

        self._load_config_and_setup_variables()
        
        self._setup_move_timer()
        
    def _setup_move_timer(self):
        '''
        设置移动定时器
        '''
        self.move_timer = QTimer()
        try:
            screen = self.screen()
            refresh_rate = screen.refreshRate()
            refresh_rate = max(refresh_rate, 60)
            interval = int(1000 / refresh_rate)
        except:
            interval = 16
        
        self.move_timer.setInterval(interval)
        self.move_timer.timeout.connect(self._do_delayed_move)
        self.pending_move = None
        
    def paintEvent(self, event):
        """
        绘制数字6标识的核心部分，这里的魔法数字几乎无法向你解释，因为这涉及到复杂的数学运算，请见谅o(╥﹏╥)o。
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        brush = QBrush(QColor(*self._background_color, self._animation_alpha))
        pen = QPen(QColor(*self._border_color, self._animation_alpha))
        pen.setWidth(self._border_width)
        
        painter.setPen(pen)
        painter.setBrush(brush)
        
        #绘制圆形背景底部
        painter.drawEllipse(*self._paint_bottom_parameters)
        
        # 计算常用的局部变量
        self._bottom_minus_animation_height = self._bottom - self._animation_height

        # 绘制圆形背景底部
        painter.drawEllipse(*self._paint_bottom_parameters)
        
        # 绘制圆形背景顶部
        painter.drawEllipse(self._half_border_width,
                            self._bottom_minus_animation_height - self._half_border_width,
                            self._border_radius_times_2,
                            self._border_radius_times_2)
        
        # 绘制中间连接部分
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(self._half_border_width,
                         self._bottom_minus_half_border_width - self._animation_height + self._border_radius,
                         self._half_border_width,
                         self._bottom_minus_half_border_width - self._border_radius)
        painter.drawLine(self._border_radius_times_2 + self._half_border_width,
                         self._bottom_minus_half_border_width - self._animation_height + self._border_radius,
                         self._border_radius_times_2 + self._half_border_width,
                         self._bottom_minus_half_border_width - self._border_radius)
        
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self._border_width,
                         self._bottom_minus_half_border_width - self._animation_height + self._border_radius,
                         self._border_radius_times_2 - self._border_width,
                         self._animation_height - self._border_radius_times_2)
        
        # 绘制文本
        painter.setFont(self._QFont)
        painter.setPen(QColor(*self._QFont_color, self._animation_alpha))
        painter.drawText(QRect(self._border_width,
                               self._bottom_minus_animation_height - self._half_border_width,
                               self._border_radius_times_2 - self._border_width,
                               self._border_radius_times_2), Qt.AlignCenter, self.text)
    
    @pyqtProperty(int)
    def animation_height(self):
        return self._animation_height
    
    @animation_height.setter
    def animation_height(self, value):
        self._animation_height = value
        self.update()
    
    def _do_delayed_move(self):
        if self.pending_move and self.main_window:
            self.main_window.move(self.pending_move)
            if self.moving_callback:
                self.moving_callback(self.pending_move)
            self.pending_move = None
    
    def mousePressEvent(self, event):
        if self.movable and event.button() == Qt.LeftButton:
            self.mouse_drag_pos = event.globalPos() - self.main_window.frameGeometry().topLeft()
            self.is_moving = False
    
    def mouseMoveEvent(self, event):
        if self.movable and event.buttons() == Qt.LeftButton and self.mouse_drag_pos is not None:
            new_pos = event.globalPos() - self.mouse_drag_pos
            self.pending_move = new_pos
            if not self.move_timer.isActive():
                self.move_timer.start()
            self.is_moving = True
    
    def mouseReleaseEvent(self, event):
        if self.movable and event.button() == Qt.LeftButton:
            self.mouse_drag_pos = None
        if not self.is_moving and self.press_callback:
            self.press_callback()

    def get_animation_height(self):
        return self._animation_height

    def _load_config_and_setup_variables(self):
        """
        加载配置文件，并为paintEvent准备需要用到的所有变量
        有点太复杂了？不要慌，我也跟你一样慌
        但是，我必须告诉你一个残酷的事实，那就是这里的计算已经是最精简的了
        """
        self._border_radius = config_manager.config["主题"]["圆角半径"]
        self._border_width = config_manager.config["主题"]["数字6标识"]["描边宽度"]
        self._animation_height = self._border_radius * 2
        self.setFixedSize(self._border_radius * 2 + self._border_width,
                          self._border_radius * 2 * self.number + self._border_width)

        self._background_color = list(map(int, config_manager.config["主题"]["数字6标识"]["背景颜色"].split(',')))
        self._border_color = list(map(int, config_manager.config["主题"]["数字6标识"]["描边颜色"].split(',')))
        self._bottom = self._border_radius * 2 * self.number + self._border_width
        self._half_border_width = int(self._border_width / 2)
        self._bottom_minus_half_border_width = self._bottom - self._half_border_width
        self._border_radius_times_2 = self._border_radius * 2
        self._paint_bottom_parameters = (self._half_border_width,
                                         self._bottom_minus_half_border_width - self._border_radius_times_2,
                                         self._border_radius_times_2,
                                         self._border_radius_times_2)
        self._QFont = QFont(config_manager.config["主题"]["字体"], self.text_size, self.font_weight)
        self._QFont_color = list(map(int, config_manager.config["主题"]["数字6标识"]["字体颜色"].split(',')))

        self.update()