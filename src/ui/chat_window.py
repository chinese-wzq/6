import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import (
    Qt, QUrl, QObject, pyqtSlot, 
    QPropertyAnimation, pyqtProperty, QThread, pyqtSignal
)
from PyQt5.QtGui import QFont

from src.components.circle_button import CircleButton

class MessageWorker(QThread):
    finished = pyqtSignal(str, str, str)  # 信号：消息、模型、响应

    def __init__(self, message, model):
        super().__init__()
        self.message = message
        self.model = model

    def run(self):
        import time
        time.sleep(0.2)  # 模拟耗时操作
        response = f"# 这是来自{self.model}的回复: {self.message}"
        self.finished.emit(self.message, self.model, response)

class WebBridge(QObject):
    def __init__(self, web_view):
        super().__init__()
        self.web_view = web_view
        self.workers = []  # 保持对worker的引用

    @pyqtSlot(str, str)
    def handle_message(self, message, model):
        worker = MessageWorker(message, model)
        worker.finished.connect(self._handle_response)
        self.workers.append(worker)
        worker.start()

    def _handle_response(self, message, model, response):
        # 通过JavaScript回调发送响应
        self.web_view.page().runJavaScript(f'receiveResponse("{model}", "{response}");')
        # 清理完成的worker
        worker = self.sender()
        if worker in self.workers:
            self.workers.remove(worker)

class ChatWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setGeometry(0, 0, main_window.width(), main_window.height())
        
        # 添加opacity属性
        self._opacity = 0.0
        
        self._setup_ui()
        self._setup_bridge()
        self._setup_open_animation()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view = QWebEngineView(self)
        self.web_view.setAttribute(Qt.WA_TranslucentBackground, True)
        self.web_view.page().setBackgroundColor(Qt.transparent)
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chat_html_path = os.path.join(current_dir, '..', '..', 'src', 'web','chat.html')
        self.web_view.setUrl(QUrl.fromLocalFile(chat_html_path))
        
        self._configure_web_view_settings()
        
        layout.addWidget(self.web_view)
        
        self.icon = CircleButton(1, "6", 40, QFont.Medium, 
                                 movable=True, 
                                 parent=self, 
                                 main_window=self.main_window)
        self.icon.move(0, self.main_window.height() - 6 - 80)

    def _configure_web_view_settings(self):
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

    def _setup_bridge(self):
        self.channel = QWebChannel()
        self.bridge = WebBridge(self.web_view)
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        # 直接设置页面的背景透明度
        script = f"document.body.style.opacity = {value};"
        self.web_view.page().runJavaScript(script)

    def _setup_open_animation(self):
        self.opacity_animation = QPropertyAnimation(self, b"opacity")
        self.opacity_animation.setDuration(300)  # 300毫秒的动画时长
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)

    def start_open_animation(self):
        self.opacity = 0.0
        self.opacity_animation.start()

