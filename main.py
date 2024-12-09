from PyQt6.QtWidgets import QApplication, QLabel, QListWidget, QComboBox, QScrollArea, QGridLayout, QListWidgetItem, QLineEdit, QMessageBox, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QDate, QLocale, QTimer

from settings import ResizableWidget, Settings
import sys
import asyncio
from qasync import QEventLoop, asyncSlot


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
            button.setEnabled(True)
        sender = self.sender()  # Получаем кнопку, которая вызвала сигнал
        if sender:
            sender.setChecked(True)
            sender.setEnabled(False)

        page_mapping = {
            "Главная": MainPage,
            "Курсанты": CadTeachPayCarPage,
            "Инструкторы": CadTeachPayCarPage,
            "Автомобили": CadTeachPayCarPage,
            "Занятия": LessonsPage,
            "Платежи": CadTeachPayCarPage,
            "Отчет": ReportsPage
        }

        page_class = page_mapping.get(sender.text())
        if page_class:
            page_instance = page_class(self.stack, self.buttons)
            self.stack.addWidget(page_instance)
            self.stack.setCurrentWidget(page_instance)


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

    @asyncSlot()
    async def vhod(self):
        self.button_vhod.setText("Подождите...")
        self.button_vhod.setEnabled(False)
        self.login_input.returnPressed.disconnect()
        self.passwd_input.returnPressed.disconnect()

        self.login = self.login_input.text()
        self.passwd = self.passwd_input.text()

        global user
        user = await self.check_passwd()
        if user:
            main_widget = MainPage(self.stack, self.buttons)
            self.stack.addWidget(main_widget)
            self.stack.setCurrentWidget(main_widget)

        else:
            self.show_error_message("Ошибка", "Неверный логин или пароль")
            self.button_vhod.setText("Войти")
            self.login_input.clear()
            self.passwd_input.clear()
            self.button_vhod.setEnabled(True)
            self.login_input.returnPressed.connect(self.vhod)
            self.passwd_input.returnPressed.connect(self.vhod)


class MainPage(QWidget, Settings):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        self.count_instructors = 0
        self.count_students = 0
        for button in self.buttons[1:]:
            button.setEnabled(True)
        if user['role'] == "Admin":
            self.create_page_admin()
        else:
            self.create_page_manager()

    def create_page_admin(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(5000)

        self.menu_v_layout = QVBoxLayout()
        self.menu_h_layout = QHBoxLayout()

        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        spacerItem2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.menu_h_layout2 = QHBoxLayout()
        self.menu_v_layout2 = QVBoxLayout()

        self.list_with_label = QVBoxLayout()

        self.menu_v_layout3 = QVBoxLayout()

        self.label_vhod = QLabel(user['name'] + " " + user['patronymic'])

        self.menu_h_layout.addItem(spacerItem1)
        self.menu_h_layout.addWidget(self.label_vhod)
        self.menu_v_layout.addLayout(self.menu_h_layout)

        self.list_widget = QListWidget()

        self.button_add = QPushButton("Добавить")
        self.button_add.setCursor(Qt.CursorShape.PointingHandCursor)

        self.label_list = QLabel("Менеджеры")

        self.label_information1 = QLabel(f"""Количество 
инструкторов: 
{self.count_instructors}""")
        self.label_information1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_information1.setObjectName("label_info1")
        self.label_information2 = QLabel(f"""Количество
курсантов:
1""")
        self.label_information2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_information2.setObjectName("label_info2")
        self.menu_v_layout3.addItem(spacerItem2)
        self.menu_v_layout3.addWidget(self.button_add)
        self.menu_v_layout3.addItem(spacerItem2)
        self.menu_v_layout3.addWidget(self.label_information1)
        self.menu_v_layout3.addItem(spacerItem2)
        self.menu_v_layout3.addWidget(self.label_information2)
        self.menu_v_layout3.addItem(spacerItem2)

        self.menu_h_layout2.addLayout(self.menu_v_layout3)
        self.list_with_label.addWidget(self.label_list)
        self.list_with_label.addWidget(self.list_widget)
        self.menu_h_layout2.addLayout(self.list_with_label)

        self.menu_v_layout.addLayout(self.menu_h_layout2)

        self.setLayout(self.menu_v_layout)

        self.update_info()

        self.button_add.clicked.connect(self.add_manager)

    def add_manager(self):
        main_widget = ChangePage(self.stack, 'Менеджеры', self.buttons)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    def create_page_manager(self):

        self.menu_v_layout = QVBoxLayout()
        self.menu_h_layout = QHBoxLayout()

        self.menu_h_layout2 = QHBoxLayout()

        spacerItem = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        spacerItem2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.label_vhod = QLabel(user['name'] + " " + user['patronymic'])

        self.menu_h_layout.addItem(spacerItem1)
        self.menu_h_layout.addWidget(self.label_vhod)
        self.menu_v_layout.addLayout(self.menu_h_layout)

        self.label_information1 = QLabel(f"""
                                         Количество инструкторов: 
                                         {self.count_instructors}""")
        self.label_information1.setObjectName("label_info1")
        self.label_information2 = QLabel("Информация2")
        self.label_information2.setObjectName("label_info2")

        self.menu_h_layout2.addItem(spacerItem)
        self.menu_h_layout2.addWidget(self.label_information1)
        self.menu_h_layout2.addItem(spacerItem2)
        self.menu_h_layout2.addWidget(self.label_information2)
        self.menu_h_layout2.addItem(spacerItem)

        self.menu_v_layout.addLayout(self.menu_h_layout2)
        self.menu_v_layout.addItem(spacerItem)

        self.setLayout(self.menu_v_layout)

    @asyncSlot()
    async def update_info(self):
        current_items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(
                item).layout().itemAt(0).widget().text()
            current_items.append(widget)

        self.managers = await self.get_managers()

        self.count_instructors = len(self.managers)
        self.label_information1.setText(f"""Количество 
инструкторов: 
{self.count_instructors}"""
                                        )
        self.label_information1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        manager_names = [item["name"] for item in self.managers]
        items_to_add = [
            name for name in manager_names if name not in current_items]
        items_to_remove = [
            name for name in current_items if name not in manager_names]

        for item in items_to_add:
            item_widget = QWidget()
            layout = QHBoxLayout()

            spacer = QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            # Добавляем текст
            name_label = QLabel(f"{item}")
            layout.addWidget(name_label)

            # Создаем кнопку редактирования
            edit_button = QPushButton()
            edit_button.setIcon(QIcon("./src/img/pencil.svg"))
            edit_button.setIconSize(QSize(24, 24))
            edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_button.clicked.connect(lambda _, m=item: self.edit_manager(m))

            # Создаем кнопку удаления
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("./src/img/trash.svg"))
            delete_button.setIconSize(QSize(24, 24))
            delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_button.clicked.connect(
                lambda _, m=item: self.delete_manager(m))

            layout.addWidget(name_label)
            layout.addItem(spacer)
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)

            item_widget.setLayout(layout)

            # Добавляем виджет в QListWidget
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

        # Проходим с конца, чтобы индексы не смещались
        for i in range(self.list_widget.count() - 1, -1, -1):
            item = self.list_widget.item(i)  # Получаем QListWidgetItem
            widget = self.list_widget.itemWidget(
                item).layout().itemAt(0).widget().text()

            if widget in items_to_remove:
                self.list_widget.takeItem(i)

    def edit_manager(self, manager):
        print(
            f"Edit manager: {manager}")

    @asyncSlot()
    async def delete_manager(self, manager):
        await self.drop_manager(manager)
        print(f"Удалён {manager}")


class CadTeachPayCarPage(QWidget):
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

        spacerItem2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.button_add = QPushButton("Добавить")
        self.button_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_add.clicked.connect(self.add_object)

        self.list_widget = QListWidget()

        self.menu_v_layout.addWidget(self.button_add)
        self.menu_v_layout.addItem(spacerItem)

        self.menu_h_layout.addLayout(self.menu_v_layout)

        self.menu_h_layout.addWidget(self.list_widget)

        self.setLayout(self.menu_h_layout)

        self.update_info()

    def add_object(self):
        for button in self.buttons:
            if button.isChecked():
                self.type_object = button.text()
        main_widget = ChangePage(self.stack, self.type_object, self.buttons)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    @asyncSlot()
    async def update_info(self):
        current_items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(
                item).layout().itemAt(0).widget().text()
            current_items.append(widget)

        manager_names = [item["name"] for item in self.managers]
        items_to_add = [
            name for name in manager_names if name not in current_items]
        items_to_remove = [
            name for name in current_items if name not in manager_names]

        for item in items_to_add:
            item_widget = QWidget()
            layout = QHBoxLayout()

            spacer = QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            # Добавляем текст
            name_label = QLabel(f"{item}")
            layout.addWidget(name_label)

            # Создаем кнопку редактирования
            edit_button = QPushButton()
            edit_button.setIcon(QIcon("./src/img/pencil.svg"))
            edit_button.setIconSize(QSize(24, 24))
            edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_button.clicked.connect(lambda _, m=item: self.edit_manager(m))

            # Создаем кнопку удаления
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("./src/img/trash.svg"))
            delete_button.setIconSize(QSize(24, 24))
            delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_button.clicked.connect(
                lambda _, m=item: self.delete_manager(m))

            layout.addWidget(name_label)
            layout.addItem(spacer)
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)

            # Устанавливаем макет на виджет
            item_widget.setLayout(layout)

            # Добавляем виджет в QListWidget
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

        # Проходим с конца, чтобы индексы не смещались
        for i in range(self.list_widget.count() - 1, -1, -1):
            item = self.list_widget.item(i)  # Получаем QListWidgetItem
            widget = self.list_widget.itemWidget(
                item).layout().itemAt(0).widget().text()

            if widget in items_to_remove:
                self.list_widget.takeItem(i)

    def edit_manager(self, manager):
        print(
            f"Edit manager: {manager}")

    @asyncSlot()
    async def delete_manager(self, manager):
        pass


class LessonsPage(QWidget):
    def __init__(self, stack, buttons):
        super().__init__()
        self.current_date = QDate.currentDate()
        self.year = self.current_date.year()
        self.month = self.current_date.month()
        self.start_date = self.current_date.addDays(
            -self.current_date.dayOfWeek() + 1)

        QLocale.setDefault(
            QLocale(QLocale.Language.Russian, QLocale.Country.Russia))
        self.locale = QLocale()

        self.stack = stack
        self.buttons = buttons
        self.create_page()

    def create_page(self):
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        spacerItem2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.main_h_layout = QHBoxLayout()

        self.main_layout = QVBoxLayout()

        self.teach_list = QListWidget()

        self.navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("Предыдущая неделя")
        self.prev_button.clicked.connect(self.show_previous_week)
        self.next_button = QPushButton("Следующая неделя")
        self.next_button.clicked.connect(self.show_next_week)

        self.week_label = QLabel()
        self.update_week_label()

        self.navigation_layout.addWidget(self.prev_button)
        self.navigation_layout.addWidget(
            self.week_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.navigation_layout.addWidget(self.next_button)

        self.week_layout = QVBoxLayout()
        self.week_layout.setSpacing(10)

        self.main_layout.addLayout(self.navigation_layout)
        self.main_layout.addLayout(self.week_layout)

        self.main_h_layout.addWidget(self.teach_list)
        self.main_h_layout.addItem(spacerItem2)
        self.main_h_layout.addLayout(self.main_layout)

        self.display_week()
        self.setLayout(self.main_h_layout)

    def display_week(self):
        # Очистка предыдущего содержимого
        for i in reversed(range(self.week_layout.count())):
            widget = self.week_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Генерация дней недели строками
        date = self.start_date
        cell_style = "QWidget { border: 1px solid gray; }"

        for i in range(7):  # 7 дней в неделе
            day_widget = QWidget()
            day_layout = QHBoxLayout(day_widget)
            # day_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_layout.setContentsMargins(2, 2, 2, 2)

            # День недели и дата
            short_day_name = self.locale.dayName(
                date.dayOfWeek(), QLocale.FormatType.ShortFormat)
            day_label = QLabel(f"{short_day_name}, {date.day()}")
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setStyleSheet("border: none;")
            day_layout.addWidget(day_label)

            # Кнопки для временных интервалов
            for hour in range(6, 22, 3):
                time_button = QPushButton(f"{hour}:00")
                time_button.setObjectName("time_button")
                day_layout.addWidget(time_button)
                time_button.clicked.connect(self.on_time_button_clicked)

            day_widget.setStyleSheet(cell_style)
            self.week_layout.addWidget(day_widget)
            date = date.addDays(1)

    def update_week_label(self):
        end_date = self.start_date.addDays(6)
        start_text = self.locale.toString(self.start_date, "d MMMM yyyy")
        end_text = self.locale.toString(end_date, "d MMMM yyyy")
        self.week_label.setText(f"{start_text} - {end_text}")

    def show_previous_week(self):
        self.start_date = self.start_date.addDays(-7)
        self.update_calendar()

    def show_next_week(self):
        self.start_date = self.start_date.addDays(7)
        self.update_calendar()

    def update_calendar(self):
        self.update_week_label()
        self.display_week()

    def on_time_button_clicked(self):
        main_widget = ChangePage(self.stack, "", self.buttons)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)


class ReportsPage(QWidget):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        self.create_page()

    def create_page(self):

        self.menu_h_layout = QHBoxLayout()
        self.menu_v_layout = QVBoxLayout()

        self.report = QListWidget()

        self.hour_st_label = QLabel("Часовая ставка")
        self.hour_st = QLineEdit()
        self.coefficient_label = QLabel(
            "Коэффициент за дополнительные занятия")
        self.coefficient = QLineEdit()

        self.get_report_button = QPushButton("Рассчитать")

        self.menu_v_layout.addWidget(self.hour_st_label)
        self.menu_v_layout.addWidget(self.hour_st)
        self.menu_v_layout.addWidget(self.coefficient_label)
        self.menu_v_layout.addWidget(self.coefficient)
        self.menu_v_layout.addWidget(self.get_report_button)

        self.menu_h_layout.addLayout(self.menu_v_layout)
        self.menu_h_layout.addWidget(self.report)

        self.setLayout(self.menu_h_layout)


class ChangePage(QWidget, Settings):
    def __init__(self, stack, type_change, buttons):
        super().__init__()
        self.stack = stack
        self.type_change = type_change
        self.buttons = buttons
        self.create_page()

    @asyncSlot()
    async def create_page(self):

        self.menu_h_layout = QHBoxLayout()
        self.menu_v_layout = QVBoxLayout()

        self.menu_h_layout2 = QHBoxLayout()

        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        spacerItem2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.back_button = QPushButton("Отменить")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.label_name_object = QLabel("Название объекта")
        self.label_name_object_input = QLineEdit()
        self.label_name_object_input.setPlaceholderText("Название объекта")
        self.menu_v_layout.addWidget(self.label_name_object)
        self.menu_v_layout.addWidget(self.label_name_object_input)

        for elem in self.types_change[self.type_change]:
            self.name_input_label = QLabel(elem)
            if elem in ['Инструктор','Статус','Машина']:
                if elem == 'Статус' and self.type_change == 'Курсанты':
                    self.combo_box_status = QComboBox()
                    self.statuses = ['Заявка','Обучается','Закончил обучение', 'Отказ']
                    for status in self.statuses:
                        self.combo_box_status.addItem(status)
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.combo_box_status)
                    self.combo_box_status.setStyleSheet("background-color: #81b7f7; padding: 10px;")
                
                if elem == 'Инструктор' and self.type_change == 'Курсанты':
                    self.combo_box_trainer = QComboBox()
                    self.trainers = await self.get_trainers()
                    for trainer in self.trainers:
                        self.combo_box_trainer.addItem(str(trainer['id_user']))
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.combo_box_trainer)
                    self.combo_box_trainer.setStyleSheet("background-color: #81b7f7; padding: 10px;")


            else:
                self.name_input = QLineEdit()
                self.name_input.setPlaceholderText(elem)

                self.scroll_layout.addWidget(self.name_input_label)
                self.scroll_layout.addWidget(self.name_input)
            self.name_input.setStyleSheet("background-color: #81b7f7")

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_content.setStyleSheet("background-color: #F0F4F8;")
        self.scroll_area.setWidget(self.scroll_content)
        self.menu_v_layout.addWidget(self.scroll_area)

        self.menu_v_layout.addItem(spacerItem2)
        self.menu_h_layout2.addWidget(self.save_button)
        self.menu_h_layout2.addWidget(self.back_button)
        self.menu_v_layout.addLayout(self.menu_h_layout2)
        self.menu_h_layout.addItem(spacerItem1)
        self.menu_h_layout.addLayout(self.menu_v_layout)
        self.menu_h_layout.addItem(spacerItem1)

        self.setLayout(self.menu_h_layout)

        self.back_button.clicked.connect(self.back_to_manager_page)

        self.save_button.clicked.connect(self.save_changes)

    def back_to_manager_page(self):
        main_widget = MainPage(self.stack, self.buttons)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    @asyncSlot()
    async def save_changes(self):
        arr_fields = []
        for child in self.scroll_content.children():
            if isinstance(child, QLineEdit):
                if child.text() == "" or child.text() == None:
                    self.show_error_message("Ошибка", "Заполните все поля")
                    return
                else:
                    arr_fields.append(child.text())

        try:
            await self.create_manager(*arr_fields)
        except:
            self.show_error_message(
                "Ошибка добавления объекта", "Возникла ошибка, объект не добавлен.")
            return

        main_widget = MainPage(self.stack, self.buttons)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()
