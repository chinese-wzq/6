from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow, QStackedLayout, QSizePolicy
from PyQt5.QtCore import Qt, QUrl, QRect, pyqtProperty, QPropertyAnimation, QParallelAnimationGroup, QTimer, QSize, QPoint
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot, QVariant
import sys
import os


os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '16324'

from menu_circle_button import CircleButton

FONT = "HarmonyOS Sans SC"

class Bridge(QObject):
    def __init__(self):
        super().__init__()
    
    @pyqtSlot(str, str, result=str)  # 定义与网页通讯的槽函数，接收消息和模型作为参数并返回回复
    def handleMessage(self, message, model):
        response = f"这是来自{model}的回复: {message}"
        print(response)
        return response

class ChatWindow(QWidget):
    def __init__(self,main_window: QMainWindow):
        super().__init__()
        self.setWindowTitle("AI")  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口初始位置和大小
        self._animation_alpha = 0  # 初始化动画透明度属性
        self.main_window = main_window  # 保存主窗口引用
        self.setup_ui()  # 设置用户界面
        self.setup_open_animation()  # 设置打开动画
        self.setup_bridge()

        self.update_timer = QTimer()   # 限制页面刷新刷新率，提升性能
        try:
            screen = self.screen()
            refresh_rate = screen.refreshRate()
            if refresh_rate <= 0:
                refresh_rate = 60  # 使用默认值
            interval = int(1000 / refresh_rate)
        except:
            interval = 16  # 出错时使用60fps的间隔
        self.update_timer.setInterval(interval)
        self.update_timer.timeout.connect(self.do_delayed_update)
        self.pending_update = None


    def setup_ui(self):
        # 创建主部件
        self.main_widget = QWidget(self)
        self.setLayout(QVBoxLayout())  # 设置主布局为垂直布局
        self.layout().setContentsMargins(0, 0, 0, 0)  # 移除边距
        self.layout().setSpacing(0)  # 移除间距
        self.layout().addWidget(self.main_widget)  # 将主部件添加到布局中

        # 为主部件创建布局
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        layout.setSpacing(0)  # 移除间距

        # 创建用于聊天界面的 WebEngineView
        self.web_view = QWebEngineView(self.main_widget)
        self.web_view.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置背景透明
        self.web_view.page().setBackgroundColor(Qt.transparent)  # 设置页面背景透明
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 确保其扩展以填充空间

        current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录
        chat_html_path = os.path.join(current_dir, 'chat.html')  # 构建聊天 HTML 文件路径
        self.web_view.setUrl(QUrl.fromLocalFile(chat_html_path))  # 设置 WebEngineView 加载的 URL

        # 基础设置
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        # 优化性能（虽然还是很狗屎）
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # 将 WebEngineView 添加到布局中
        layout.addWidget(self.web_view)

        # 创建并设置 CircleButton
        self.icon = CircleButton(1, "6", 40, QFont.Medium, movable=True, main_window=self.main_window, moving_callback=self.moving_callback)
        self.icon.setParent(self.main_widget)  # 设置按钮的父部件
        self.icon.setGeometry(0, 0, 40, 40)  # 设置初始位置
        self.icon.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)  # 使其保持在顶部
        self.icon.setAttribute(Qt.WA_TranslucentBackground, True)  # 使按钮背景透明
        self.icon.show()  # 确保按钮显示

        self.show()  # 确保窗口显示

        # 相对于 WebEngineView 定位按钮
        self.update_icon_position()

    def setup_bridge(self):
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

    def resizeEvent(self, event):
        super(ChatWindow, self).resizeEvent(event)
        self.update_icon_position()  # 在窗口大小改变时更新按钮位置

    def update_icon_position(self):
        main_window_geometry = self.main_window.geometry()  # 获取主窗口几何信息
        self.icon.move(main_window_geometry.x(), main_window_geometry.y() + main_window_geometry.height()-80-6)  # 更新按钮位置

    @pyqtProperty(int)
    def animation_alpha(self):
        return self._animation_alpha  # 返回动画透明度属性

    @animation_alpha.setter
    def animation_alpha(self, value):
        self._animation_alpha = value  # 设置动画透明度属性
        self.update()  # 更新窗口

    def setup_open_animation(self):
        self.open_animation_group = QParallelAnimationGroup(self)  # 创建并行动画组

        self.chat_window_open_animation = QPropertyAnimation(self, b"animation_alpha")
        self.chat_window_open_animation.setDuration(500)  # 设置动画持续时间
        self.chat_window_open_animation.setStartValue(0)  # 设置动画起始值
        self.chat_window_open_animation.setEndValue(255)  # 设置动画结束值
        self.open_animation_group.addAnimation(self.chat_window_open_animation)  # 将动画添加到动画组

    def start_open_animation(self):
        self.open_animation_group.start()  # 开始动画

    def moving_callback(self, a0: QPoint):
        self.pending_update = QPoint(a0.x(), a0.y()+self.height()-80-6)
        if not self.update_timer.isActive():
            self.update_timer.start()

    def do_delayed_update(self): # 降低页面刷新频率，提高性能
        if self.pending_update:
            self.icon.move(self.pending_update.x(), self.pending_update.y())
            self.pending_update = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(500, 500, 800, 800)  # 设置主窗口位置和大小

    # 设置窗口属性
    window.setWindowOpacity(1)  # 设置窗口不透明度
    window.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口无边框
    window.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    chat_window = ChatWindow(window)  # 创建 ChatWindow 实例
    window.setCentralWidget(chat_window)  # 将 ChatWindow 设置为主窗口的中央部件
    chat_window.start_open_animation()  # 开始打开动画
    window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 进入应用程序主循环