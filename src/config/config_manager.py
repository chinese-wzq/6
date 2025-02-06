import atexit

import yaml
from PyQt5.QtCore import QObject, pyqtSignal
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

config = []


class ConfigReloadHandler(FileSystemEventHandler):
    """自定义事件处理器，用于监听文件修改事件"""

    def __init__(self, config_path, signal_emitter):
        self.config_path = config_path
        self.signal_emitter = signal_emitter

    def on_modified(self, event):
        """当文件被修改时触发"""
        if event.src_path.endswith(self.config_path):
            self.signal_emitter.signal.emit()


class SignalEmitter(QObject):
    signal = pyqtSignal()


class ConfigManager:
    """配置管理器，负责加载和打印配置"""

    def __init__(self, config_path="config.yaml"):
        self.signal_emitter = SignalEmitter()
        self.config_path = config_path
        self.config = {}
        self.callbacks = []

        self.load_config()
        self.observer = self.start_file_watcher()

        atexit.register(self.cleanup)

    def load_config(self):
        """加载配置文件"""
        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        if self.config is None:
            return
        global config
        config = self.config
        self.notify_callbacks()

    def save_config(self):
        """保存配置文件"""
        with open(self.config_path, "w", encoding="utf-8") as file:
            yaml.dump(self.config, file, encoding="utf-8", allow_unicode=True)

    def start_file_watcher(self):
        """启动文件观察者"""
        self.signal_emitter.signal.connect(self.load_config)

        event_handler = ConfigReloadHandler(self.config_path, self.signal_emitter)
        observer = Observer()
        observer.schedule(event_handler, path=".", recursive=False)
        observer.start()
        return observer

    def cleanup(self):
        """对象销毁时停止观察者，并保存配置文件"""
        self.observer.stop()
        self.observer.join()
        self.save_config()

    def register_callback(self, callback):
        """作为装饰器，注册回调函数"""
        self.callbacks.append(callback)
        return callback

    def notify_callbacks(self):
        """调用/通知所有回调函数"""
        for callback in self.callbacks:
            callback()

    def output_callbacks(self):
        """打印所有回调函数"""
        print("以下是所有回调函数来自的类：")
        for callback in self.callbacks:
            print(callback.__self__.__class__.__name__)


config_manager = ConfigManager('config.yaml')
register_callback = config_manager.register_callback
