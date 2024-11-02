from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
import sys


def set_current(new_widget):
    previous_widget = Stack.currentWidget()
    if previous_widget:
        previous_widget.deleteLater()

    Stack.addWidget(new_widget)
    Stack.setCurrentWidget(new_widget)

# Главное окно


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_window()

    def create_window(self):
        menu_widget = QWidget()
        self.menu_v_layout = QVBoxLayout(menu_widget)
        self.menu_h_layout = QHBoxLayout()

        self.setObjectName("MainWindow")
        self.setMinimumSize(720, 480)
        self.setStyleSheet("MainWindow {background-color: #F0F4F8};")

        # Инициализация Stack
        global Stack
        Stack = QStackedWidget()
        self.setCentralWidget(Stack)

        icon = QIcon("src/img/icon.svg")
        self.setWindowIcon(icon)
        self.setWindowTitle("Информационная система для автошколы")

        self.titles_buttons = [
            "Главная", "Курсанты", "Инструкторы", "Автомобили", "Занятия", "Платежи", "Отчет"]

        self.buttons = []
        self.selected_button = None  # Для хранения выбранной кнопки

        for name in self.titles_buttons:
            button = QPushButton(self)
            button.setText(f"{name}")
            button.setCheckable(True)  # Делаем кнопку переключаемой
            button.clicked.connect(
                lambda _, b=button: self.on_button_clicked(b))
            self.menu_h_layout.addWidget(button)
            self.buttons.append(button)

        self.menu_h_layout.setSpacing(0)
        self.menu_v_layout.setContentsMargins(0, 0, 0, 0)
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.menu_v_layout.addLayout(self.menu_h_layout)
        self.menu_v_layout.addItem(spacerItem)
        self.label_vhod = QLabel("Вход")
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

        menu_widget.setLayout(self.menu_v_layout)
        Stack.addWidget(menu_widget)

        self.updateFont()

        self.button_vhod.clicked.connect(self.clck)
        
    def clck(self):
        login = self.login_input.text()
        passwd = self.passwd_input.text()

        if login == "admin" and passwd == "admin":
            for button in self.buttons:
                button.setEnabled(True)
        # Здесь будет обработчик проверки логина и пароля пользователя
    def resizeEvent(self, event):
        self.updateFont()
        super().resizeEvent(event)

    def updateFont(self):
        width = self.width()
        font_size = max(10, min(width // 50, 20))

        self.label_vhod.setStyleSheet(
            f"font-size: {font_size * 2}px; font-weight: bold; color: black;")
        self.login_label.setStyleSheet(
            f"font-size: {font_size}px; font-weight: bold; color: black;")
        self.passwd_label.setStyleSheet(
            f"font-size: {font_size}px; font-weight: bold; color: black;")

        self.login_input.setStyleSheet(
            f"font-size: {font_size}px; color: black; padding: 10px; background-color: #4A90E2; border: none; border-radius: 15px; color: #FFFFFF;")
        self.passwd_input.setStyleSheet(
            f"font-size: {font_size}px; color: black; padding: 10px; background-color:#4A90E2; border: none; border-radius: 15px; color: #FFFFFF;")

        self.button_vhod.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    padding: 10px; 
                    border-radius: 0px;
                    font-size: {font_size}px;
                    border-right: 1px solid white; 
                }}
                QPushButton:hover {{
                    background-color: #357ABD;
                    color: #FFFFFF; 
                    padding: 10px; 
                    border-radius: 0px;
                }}"""
        )
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
                    background-color: #357ABD;
                    color: #FFFFFF; 
                    padding: 10px; 
                    border-radius: 0px;
                }}
                QPushButton:checked {{
                    background-color: #357ABD;  /* Цвет для нажатой кнопки */
                    color: #FFFFFF; 
                }}
                QPushButton:disabled {{
                    background-color: #B0BEC5;  /* Цвет для неактивной кнопки */
                    color: #FFFFFF; 
                    border: none;  /* Убираем границу для неактивной кнопки */
                }}
            """)
            button.setEnabled(False)

        self.buttons[-1].setStyleSheet(button.styleSheet().replace(
            "border-right: 1px solid white;", ""))

    def on_button_clicked(self, button):
        # Снимаем выделение с предыдущей кнопки
        if self.selected_button and self.selected_button != button:
            self.selected_button.setChecked(False)

        # Устанавливаем текущую кнопку как выбранную
        self.selected_button = button


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Stack = QStackedWidget()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
