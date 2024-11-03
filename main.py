from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys


class ResizableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def updateFont(self):
        width = self.width()
        font_size = max(10, min(width // 50, 20))

        self.setStyleSheet(f"""
            QMainWindow {{background-color: #F0F4F8;}}               
            
            QLabel {{
                font-size: {font_size*1.1}px;
                color: black;
            }}

            QLabel#label_vhod {{
                font-weight: bold;
                font-size: {font_size * 2}px; 
            }}

            QPushButton {{
                background-color: #4A90E2;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 0px;
                font-size: {font_size}px;
                border-right: 1px solid white;
                }}
            QPushButton:hover {{
                background-color: #2767f2;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 0px;
            }}

            QLineEdit {{
                font-size: {font_size}px;
                padding: 10px;
                font-weight: bold;
                background-color: #81b7f7;
                border: none; border-radius: 15px;
                color: #FFFFFF;
            }}          
        """)

        for button in self.buttons:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    padding: 10px; 
                    border-radius: 0px;
                    font-size: {font_size}px;
                    border-right: 1px solid white; 
                }}
                QPushButton:hover {{
                    background-color: #2767f2;
                    color: #FFFFFF; 
                    padding: 10px; 
                    border-radius: 0px;
                }}
                QPushButton:checked {{
                    background-color: #2767f2;
                    color: #FFFFFF; 
                }}
            """)
            button.setEnabled(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        if self.buttons:
            # Убираем правую границу у последней кнопки
            self.buttons[-1].setStyleSheet(self.buttons[-1].styleSheet().replace(
                "border-right: 1px solid white;", ""))

    def resizeEvent(self, event):
        """Обработчик события изменения размера окна."""
        self.updateFont()
        super().resizeEvent(event)


class MainWindow(QMainWindow, ResizableWidget):
    def __init__(self):
        QMainWindow.__init__(self)  # Вызов конструктора QMainWindow
        ResizableWidget.__init__(self)  # Вызов конструктора ResizableWidget
        self.stack = QStackedWidget()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.menu_v_layout = QVBoxLayout()
        self.menu_h_layout = QHBoxLayout()

        self.create_window()

    def create_window(self):
        self.setObjectName("MainWindow")
        self.setMinimumSize(720, 480)

        icon = QIcon("src/img/icon.svg")
        self.setWindowIcon(icon)
        self.setWindowTitle("Информационная система для автошколы")

        self.titles_buttons = [
            "Главная", "Курсанты", "Инструкторы", "Автомобили", "Занятия", "Платежи", "Отчет"]

        for name in self.titles_buttons:
            button = QPushButton(self)
            button.setText(f"{name}")
            button.setCheckable(True)  # Делаем кнопку переключаемой
            self.menu_h_layout.addWidget(button)
            self.buttons.append(button)

        self.menu_h_layout.setSpacing(0)
        self.menu_v_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_v_layout.addLayout(self.menu_h_layout)

        self.stack.addWidget(LoginPage())
        self.menu_v_layout.addWidget(self.stack)

        self.central_widget.setLayout(self.menu_v_layout)

        self.updateFont()  # Обновляем шрифты при загрузке окна


class LoginPage(ResizableWidget):
    def __init__(self):
        super().__init__()
        self.create_page()

    def create_page(self):
        self.menu_v_layout = QVBoxLayout()
        self.menu_h_layout = QHBoxLayout()

        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.menu_v_layout.addLayout(self.menu_h_layout)
        self.menu_v_layout.addItem(spacerItem)
        self.label_vhod = QLabel("Вход")
        self.label_vhod.setObjectName("label_vhod")
        self.login_label = QLabel("Логин")
        self.passwd_label = QLabel("Пароль")
        self.login_input = QLineEdit()
        self.passwd_input = QLineEdit()
        self.button_vhod = QPushButton("Войти")
        self.passwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.vhod_layout = QHBoxLayout()
        self.vhod_layout.addItem(spacerItem1)
        self.vhod_layout.addWidget(self.label_vhod)
        self.inputs_h_layout = QHBoxLayout()
        self.inputs_v_layout = QVBoxLayout()
        self.menu_v_layout.addLayout(self.vhod_layout)
        self.inputs_v_layout.addWidget(self.login_label)
        self.inputs_v_layout.addWidget(self.login_input)
        self.inputs_v_layout.addWidget(self.passwd_label)
        self.inputs_v_layout.addWidget(self.passwd_input)
        self.inputs_v_layout.addItem(spacerItem)
        self.inputs_v_layout.addWidget(self.button_vhod)
        self.inputs_h_layout.addItem(spacerItem1)
        self.inputs_h_layout.addLayout(self.inputs_v_layout)
        self.inputs_h_layout.addItem(spacerItem1)
        self.menu_v_layout.addLayout(self.inputs_h_layout)
        self.menu_v_layout.addItem(spacerItem)
        self.menu_v_layout.addItem(spacerItem)
        self.menu_v_layout.addItem(spacerItem)
        self.vhod_layout.addItem(spacerItem1)
        self.setLayout(self.menu_v_layout)

        self.updateFont()


class MainPage(QWidget):
    def __init__(self):
        super().__init__()


class CadTeachPayCarPage(QWidget):
    def __init__(self):
        super().__init__()


class LessonsPage(QWidget):
    def __init__(self):
        super().__init__()


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
