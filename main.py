from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit,QMessageBox, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from settings import ResizableWidget, Settings
import sys


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
            button.setEnabled(False) 
            self.buttons.append(button)
            button.clicked.connect(self.on_button_clicked)
        
        
        self.buttons[0].setChecked(True)


        self.menu_h_layout.setSpacing(0)
        self.menu_v_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_v_layout.addLayout(self.menu_h_layout)

        self.stack.addWidget(LoginPage(self.stack, self.buttons))
        self.menu_v_layout.addWidget(self.stack)

        self.central_widget.setLayout(self.menu_v_layout)

        self.updateStyles()  # Обновляем стили при загрузке окна
        
    def on_button_clicked(self):
        for button in self.buttons:
            button.setChecked(False)
        sender = self.sender()  # Получаем кнопку, которая вызвала сигнал
        if sender:
            sender.setChecked(True)

class LoginPage(ResizableWidget, Settings):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
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
        self.button_vhod.setCursor(Qt.CursorShape.PointingHandCursor)
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

        self.login_input.returnPressed.connect(self.vhod)
        self.passwd_input.returnPressed.connect(self.vhod)
        self.button_vhod.clicked.connect(self.vhod)

        self.updateStyles()

    

    def vhod(self):
        self.login = self.login_input.text()
        self.passwd = self.passwd_input.text()

        # тут надо сделать проверку логина и пароля
        
        if self.login == "admin" and self.passwd == "admin":
            # Нужно будет сделать передачу значения role в классы  
            global role 
            role = "admin"
            main_widget = MainPage(self.stack, self.buttons)
            self.stack.addWidget(main_widget)
            self.stack.setCurrentWidget(main_widget)

            for button in self.buttons:
                button.setEnabled(True)
        else:
            self.show_error_message("Ошибка", "Неверный логин или пароль")

    def show_error_message(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()


class MainPage(QWidget):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        if role == "admin":
            self.create_page_admin()
        else:
            self.create_page_manager()
    
    def create_page_admin(self):
        self.menu_v_layout = QVBoxLayout()
        self.label_vhod = QLabel(role)
        self.menu_v_layout.addWidget(self.label_vhod)
        self.setLayout(self.menu_v_layout)

        pass

    def create_page_manager(self):
        pass
        
        

class CadTeachPayCarPage(QWidget):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        self.create_page()
    
    def create_page(self):
        pass


class LessonsPage(QWidget):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        self.create_page()
    
    def create_page(self):
        pass

class ReportsPage(QWidget):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        self.create_page()
    
    def create_page(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
