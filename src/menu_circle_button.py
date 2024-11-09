from PyQt5.QtCore import QRect, pyqtProperty, QEasingCurve, QPropertyAnimation, Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
from PyQt5.QtWidgets import QWidget

# 定义字体常量
FONT = "HarmonyOS Sans SC"

class CircleButton(QWidget):
    def __init__(self, number, text, text_size, font_weight, movable=False, parent=None, main_window=None, moving_callback=None):
        """
        初始化圆形按钮
        :param number: 按钮的编号，用于计算位置
        :param text: 按钮的文本
        :param text_size: 文本大小
        :param font_weight: 文本粗细
        :param movable: 是否可以拖动
        :param parent: 父窗口
        :param main_window: 主窗口，只在需要移动窗口时使用
        :param moving_callback: 移动时的将调用该回调函数
        """
        super().__init__(parent)
        self._animation_alpha = 255  # 动画透明度初始值
        self._animation_height = 80  # 动画高度初始值
        self.number = number  # 按钮编号
        self.setFixedSize(86, 80*self.number+6)  # 设置固定大小
        self.text = text  # 按钮文本
        self.text_size = text_size  # 文本大小
        self.font_weight = font_weight  # 文本粗细
        self.QAnimation_height = self.setup_animation_height()  # 设置高度动画
        self.QAnimation_alpha = self.setup_animation_alpha()  # 设置透明度动画

        self.movable = movable  # 是否可拖动
        self.mouse_drag_pos = None  # 记录鼠标按下的位置
        self.is_moving = False  # 标记窗口是否被移动过
        self.press_callback = None  # 按钮按下回调函数
        self.main_window = main_window  # 主窗口
        self.moving_callback = moving_callback  # 移动回调函数

        self.move_timer = QTimer()  # 限制页面刷新刷新率，提升性能
        try:
            screen = self.screen()
            refresh_rate = screen.refreshRate()
            if refresh_rate <= 0:
                refresh_rate = 60  # 使用默认值
            interval = int(1000 / refresh_rate)
        except:
            interval = 16  # 出错时使用60fps的间隔
        self.move_timer.setInterval(interval)
        self.move_timer.timeout.connect(self.do_delayed_move)
        self.pending_move = None

        self.is_dragging = False  # 添加拖动状态标记

    def paintEvent(self, event):
        """
        绘制事件处理函数
        """
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(self.font())
        painter.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿

        # 这是中心部分的rect
        bottom = 80*self.number+6

        # 绘制圆形背景底部
        brush = QBrush(QColor(42, 130, 228, self._animation_alpha))
        pen = QPen(QColor(72, 143, 224, self._animation_alpha))
        pen.setWidth(6)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(3, bottom-80-3, 80, 80)
        # 绘制圆形背景顶部
        painter.drawEllipse(3, bottom - self._animation_height - 3, 80, 80)

        # 绘制圆形背景中部
        painter.setBrush(Qt.NoBrush)
        painter.setPen(pen)
        painter.drawLine(3, bottom - 3 - self._animation_height + 40, 3, bottom - 3 - 40)
        painter.drawLine(80 + 3, bottom - 3 - self._animation_height + 40, 83, bottom - 3 - 40)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(6, bottom - 3 - self._animation_height + 40, 80 - 6, self._animation_height - 80)

        # 绘制文本
        painter.setFont(QFont(FONT, self.text_size, self.font_weight))
        painter.setPen(QColor(255, 255, 255, self._animation_alpha))
        painter.drawText(QRect(6, bottom - self._animation_height - 3, 80 - 6, 80), Qt.AlignCenter, self.text)

    @pyqtProperty(int)
    def animation_height(self):
        """
        获取动画高度
        """
        return self._animation_height

    @animation_height.setter
    def animation_height(self, value):
        """
        设置动画高度
        """
        self._animation_height = value
        self.update()  # 更新绘制

    def get_animation_height(self):
        """
        获取动画高度
        """
        return self._animation_height

    def setup_animation_height(self):
        """
        设置高度动画
        """
        animation = QPropertyAnimation(self, b'animation_height')
        animation.setEasingCurve(QEasingCurve.OutQuint)
        return animation

    def prepare_animation_height(self, start_value: int, end_value: int, duration: int = 1000):
        """
        准备高度动画
        :param start_value: 动画起始值
        :param end_value: 动画结束值
        :param duration: 动画持续时间
        """
        self.QAnimation_height.setStartValue(start_value)
        self.QAnimation_height.setEndValue(end_value)
        self.QAnimation_height.setDuration(duration)

    def mousePressEvent(self, event):
        """
        鼠标按下事件处理函数
        """
        if self.movable:
            if event.button() == Qt.LeftButton:
                # 记录鼠标按下的位置
                self.mouse_drag_pos = event.globalPos()-self.main_window.frameGeometry().topLeft()
                self.is_moving = False  # 重置移动标记
                self.is_dragging = True
                self.setUpdatesEnabled(False)  # 拖动开始时禁用更新
                if self.main_window:
                    self.main_window.setUpdatesEnabled(False)  # 主窗口也禁用更新
                event.accept()

    def mouseMoveEvent(self, event):
        if self.movable:
            if event.buttons() == Qt.LeftButton and self.mouse_drag_pos is not None:
                new_pos = event.globalPos()-self.mouse_drag_pos
                self.pending_move = new_pos
                if not self.move_timer.isActive():
                    self.move_timer.start()
                self.is_moving = True
                event.accept()

    def do_delayed_move(self):
        if self.pending_move:
            if not self.is_dragging:
                self.setUpdatesEnabled(True)
                if self.main_window:
                    self.main_window.setUpdatesEnabled(True)
            self.main_window.move(self.pending_move)
            if self.moving_callback:
                self.moving_callback(self.pending_move)
            self.pending_move = None

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理函数
        """
        if self.movable:
            if event.button() == Qt.LeftButton:
                # 判断是否为单击操作（没有移动）
                if not self.is_moving and self.press_callback:
                    self.press_callback()
                self.mouse_drag_pos = None
                self.is_dragging = False
                self.setUpdatesEnabled(True)  # 拖动结束时恢复更新
                if self.main_window:
                    self.main_window.setUpdatesEnabled(True)  # 主窗口恢复更新
                    self.main_window.update()  # 强制更新一次
                self.update()  # 强制更新按钮
                event.accept()
        else:
            if self.press_callback:
                self.press_callback()
            event.accept()

    def setup_animation_alpha(self):
        """
        设置透明度动画
        """
        animation = QPropertyAnimation(self, b'animation_alpha')
        animation.setEasingCurve(QEasingCurve.OutQuint)
        return animation

    def prepare_animation_alpha(self, start_value: int, end_value: int, duration: int = 1000):
        """
        准备透明度动画
        :param start_value: 动画起始值
        :param end_value: 动画结束值
        :param duration: 动画持续时间
        """
        self.QAnimation_alpha.setStartValue(start_value)
        self.QAnimation_alpha.setEndValue(end_value)
        self.QAnimation_alpha.setDuration(duration)

    @pyqtProperty(int)
    def animation_alpha(self):
        """
        获取动画透明度
        """
        return self._animation_alpha

    @animation_alpha.setter
    def animation_alpha(self, value):
        """
        设置动画透明度
        """
        self._animation_alpha = value
        self.update()  # 更新绘制

    def get_animation_alpha(self):
        """
        获取动画透明度
        """
        return self._animation_alpha