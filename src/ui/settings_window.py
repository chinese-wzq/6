from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QCheckBox

from src.components.bordered_frame import bordered_frame, BorderedFrame
from src.config.config_manager import register_callback


@bordered_frame
class SettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.parent_frame: BorderedFrame = None
        self.setGeometry(0, 0, main_window.width(), main_window.height())

        self._setup_ui()

        register_callback(self._load_config_and_setup_variables)

    def _setup_ui(self):
        self.tab_widget = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab_widget.addTab(self.tab1, "常规")
        self.tab_widget.addTab(self.tab2, "AI")
        self.tab_widget.addTab(self.tab3, "整理")
        self.tab_widget.addTab(self.tab4, "关于")

        self.tab1_layout = QVBoxLayout(self.tab1)
        self.tab1_layout.setContentsMargins(15, 15, 15, 15)
        self.startup_checkbox = QCheckBox("开机时启动")
        self.startup_checkbox.toggled.connect(self.on_checkbox_toggled)
        self.startup_checkbox.installEventFilter(self)

        self.tab1_layout.addWidget(self.startup_checkbox)

    def _load_config_and_setup_variables(self):
        from src.config.config_manager import config
        lens = 4
        self.parent_frame.open_time = config["动效"]["设置"]["进入时间"]
        self.parent_frame.close_time = config["动效"]["设置"]["退出时间"]
        self.parent_frame.real_width, self.parent_frame.real_height = config["主题"]["设置"]["窗口大小"]
        self.parent_frame.border_width = config["主题"]["数字6标识"]["描边宽度"]
        self.parent_frame.half_border_width = int(config["主题"]["数字6标识"]["描边宽度"] / 2)
        self.parent_frame.border_radius = config["主题"]["圆角半径"]
        self.parent_frame.background_color = list(map(int, config["主题"]["设置"]["背景颜色"].split(',')))
        self.parent_frame.border_color = list(map(int, config["主题"]["设置"]["描边颜色"].split(',')))
        self.parent_frame.window_height = self.main_window.height()
        tab_bar_divider_width_half = config["主题"]["设置"]["选项卡"]["分割线半宽"]
        tab_width = self.parent_frame.real_width - self.parent_frame.border_width
        self.tab_widget.setGeometry(self.parent_frame.border_width,
                                    self.main_window.height() - self.parent_frame.real_height, tab_width,
                                    self.parent_frame.real_height)
        per_tab_base_width = (tab_width - tab_bar_divider_width_half * 2 * (1 + lens - 2)) / lens
        if per_tab_base_width % 1 != 0:
            print("警告： 设置的窗口大小计算得出的选项卡宽度不是整数，可能会导致显示异常")

        self.tab_widget.setStyleSheet(f"""
            QTabBar {{
                margin: 0;
                padding: 0;
            }}
            QTabBar::tab {{
                background: rgb({",".join(map(str, config["主题"]["设置"]["选项卡"]["背景颜色"].split(',')))});
                padding: 0;
                width: {per_tab_base_width}px;
                border-left: {tab_bar_divider_width_half}px solid rgb({",".join(map(str, config["主题"]["设置"]["描边颜色"].split(',')))});
                border-right: {tab_bar_divider_width_half}px solid rgb({",".join(map(str, config["主题"]["设置"]["描边颜色"].split(',')))});
                height: {config["主题"]["设置"]["选项卡"]["高度"]}px;

                color: rgb({",".join(map(str, config["主题"]["设置"]["选项卡"]["字体颜色"].split(',')))});
                font-family: {config["主题"]["字体"]};
                font-weight: bold;
                font-size: {int(config["主题"]["设置"]["选项卡"]["高度"] / 3 * 2)}px;
            }}
            QTabBar::tab:first {{
                border-top-left-radius: {self.parent_frame.border_radius}px;
                border-left: 0;
            }}
            QTabBar::tab:last {{
                border-top-right-radius: {self.parent_frame.border_radius}px;
                border-right: 0;
            }}
            QTabBar::tab:selected {{
                background: rgb({",".join(map(str, config["主题"]["设置"]["选项卡"]["被选中背景颜色"].split(',')))});
            }}
            QTabBar::tab:hover:!selected {{
                background: rgb({",".join(map(str, config["主题"]["设置"]["选项卡"]["鼠标悬停背景颜色"].split(',')))});
            }}
            QTabBar::scroller {{
                width: 0;
            }}
            QTabBar::tear {{
                width: 0;
            }}
            QTabWidget::pane {{
                border: 0;
                top: 0;
            }}
            QTabWidget::tab-bar {{
                left: 0;
            }}
        """)
        self.startup_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: white;
                font-size: 30px;
            }}
            QCheckBox::indicator {{
                width: 30px;
                height: 30px;
                background-color: rgb({",".join(map(str, config["主题"]["设置"]["勾选框"]["未选中"].split(',')))});
                border: 6px solid rgb({",".join(map(str, config["主题"]["设置"]["勾选框"]["描边颜色"].split(',')))});
                border-radius: 21px;
            }}
            QCheckBox::indicator:checked {{
                background-color: rgb({",".join(map(str, config["主题"]["设置"]["勾选框"]["选中"].split(',')))});
            }}
            QCheckBox::indicator:hover:!checked {{
                background-color: rgb({",".join(map(str, config["主题"]["设置"]["勾选框"]["鼠标悬停"].split(',')))});
            }}
            QCheckBox[hover_disabled="true"]::indicator:hover:!checked {{
                background-color: rgb({",".join(map(str, config["主题"]["设置"]["勾选框"]["未选中"].split(',')))});
            }}
        """)
        self.setStyleSheet(f"background-color: {config['主题']["设置"]['背景颜色']}")
        self.tab_widget.update()
        self.startup_checkbox.update()
        self.update()

    def initialize(self):
        self._load_config_and_setup_variables()

    def on_checkbox_toggled(self, checked):
        if not checked:
            self.startup_checkbox.setProperty("hover_disabled", True)
            self.startup_checkbox.style().polish(self.startup_checkbox)

    def eventFilter(self, source, event):
        if source == self.startup_checkbox and event.type() == QEvent.Leave:
            self.startup_checkbox.setProperty("hover_disabled", False)
            self.startup_checkbox.style().polish(self.startup_checkbox)
        return super().eventFilter(source, event)
