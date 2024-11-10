from PyQt5.QtCore import (
    QRect, pyqtProperty, QEasingCurve, 
    QPropertyAnimation, Qt, QTimer, QPoint
)
from PyQt5.QtGui import (
    QPainter, QBrush, QColor, QPen, QFont
)
from PyQt5.QtWidgets import QWidget

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
        self._animation_height = 80
        
        self.number = number
        self.setFixedSize(86, 80 * self.number + 6)
        
        self.text = text
        self.text_size = text_size
        self.font_weight = font_weight
        
        self.movable = movable
        self.mouse_drag_pos = None
        self.is_moving = False
        
        self.press_callback = None
        self.main_window = main_window
        self.moving_callback = moving_callback
        
        self._setup_move_timer()
        
    def _setup_move_timer(self):
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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bottom = 80 * self.number + 6
        
        # 绘制背景
        brush = QBrush(QColor(42, 130, 228, self._animation_alpha))
        pen = QPen(QColor(72, 143, 224, self._animation_alpha))
        pen.setWidth(6)
        
        painter.setPen(pen)
        painter.setBrush(brush)
        
        # 绘制圆形背景底部
        # painter.drawEllipse(3, bottom-80-3, 80, 80)
        # 绘制圆形背景顶部
        painter.drawEllipse(3, bottom - self._animation_height - 3, 80, 80)
        
        # 绘制中间连接部分
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(3, bottom - 3 - self._animation_height + 40, 3, bottom - 3 - 40)
        painter.drawLine(80 + 3, bottom - 3 - self._animation_height + 40, 83, bottom - 3 - 40)
        
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(6, bottom - 3 - self._animation_height + 40, 80 - 6, self._animation_height - 80)
        
        # 绘制文本
        painter.setFont(QFont("HarmonyOS Sans SC", self.text_size, self.font_weight))
        painter.setPen(QColor(255, 255, 255, self._animation_alpha))
        painter.drawText(QRect(6, bottom - self._animation_height - 3, 80 - 6, 80), Qt.AlignCenter, self.text)
    
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
