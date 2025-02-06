import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from src.ui.main_window import MainWindow


def handle_exception(exception_type, exception_value, exception_traceback):
    # 获取错误消息和回溯信息
    error_message = ''.join(traceback.format_exception(exception_type, exception_value, exception_traceback))

    # 显示错误消息框
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle("Error")
    error_box.setText("An error occurred:")
    error_box.setInformativeText(error_message)
    error_box.exec_()


# 创建应用程序类
class LoggedQApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sys.excepthook = handle_exception


def main():
    app = LoggedQApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        window.cleanup()


if __name__ == "__main__":
    main()
