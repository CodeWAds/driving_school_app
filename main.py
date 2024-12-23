from PyQt6.QtWidgets import QApplication, QLabel, QCheckBox, QListWidget, QComboBox, QScrollArea, QGridLayout, QListWidgetItem, QLineEdit, QMessageBox, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QDate, QLocale, QTimer
from datetime import date, datetime, timedelta
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

        self.login_input.returnPressed.connect(self.start_login_process)
        self.passwd_input.returnPressed.connect(self.start_login_process)
        self.button_vhod.clicked.connect(self.start_login_process)

        self.updateStyles()

    def start_login_process(self):
        # Таймер для повторных попыток
        self.retry_timer = QTimer()
        self.retry_timer.setInterval(5000)  # Интервал в 5 секунд
        # Связываем таймер с методом входа
        self.retry_timer.timeout.connect(self.vhod)
        self.retry_timer.start()
        self.vhod()

    def stop_login_process(self):
        self.retry_timer.stop()

    @asyncSlot()
    async def vhod(self):

        self.button_vhod.setText("Подождите...")
        self.button_vhod.setEnabled(False)
        try:
            self.login_input.returnPressed.disconnect(self.vhod)
        except TypeError:
            pass

        try:
            self.passwd_input.returnPressed.disconnect(self.vhod)
        except TypeError:
            pass

        self.login = self.login_input.text()
        self.passwd = self.passwd_input.text()

        global user
        user = await self.check_passwd()  # Проверка учетных данных

        if user and user['role'] in ['Admin', "Manager"]:
            self.retry_timer.stop()  # Останавливаем таймер при успехе
            main_widget = MainPage(self.stack, self.buttons)
            self.stack.addWidget(main_widget)
            self.stack.setCurrentWidget(main_widget)
        else:
            self.show_error_message("Ошибка", "Неверный логин или пароль")
            self.retry_timer.stop()
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
        elif user['role'] == "Manager":
            self.create_page_manager()

    def create_page_admin(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info_admin)
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
{self.count_students}""")
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

        self.update_info_admin()

        self.button_add.clicked.connect(self.add_manager)

    def create_page_manager(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info_manager)
        self.timer.start(5000)

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

        self.label_information1 = QLabel(
            f"Количество\nинструкторов:\n{self.count_instructors}")
        self.label_information1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_information1.setObjectName("label_info1")
        self.label_information2 = QLabel(
            f"Количество\nкурсантов:\n{self.count_students}")
        self.label_information2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_information2.setObjectName("label_info2")

        self.menu_h_layout2.addItem(spacerItem)
        self.menu_h_layout2.addWidget(self.label_information1)
        self.menu_h_layout2.addItem(spacerItem2)
        self.menu_h_layout2.addWidget(self.label_information2)
        self.menu_h_layout2.addItem(spacerItem)

        self.menu_v_layout.addLayout(self.menu_h_layout2)
        self.menu_v_layout.addItem(spacerItem)

        self.setLayout(self.menu_v_layout)

        self.update_info_manager()

    @asyncSlot()
    async def update_info_manager(self):
        self.instructors = await self.get_count_trainers()
        self.students = await self.get_count_students()

        self.count_instructors = self.instructors[0]['count_trainer']
        self.count_students = self.students[0]['count_student']
        self.label_information1.setText(
            f"Количество\nинструкторов:\n{self.count_instructors}")
        self.label_information2.setText(
            f"Количество\nкурсантов:\n{self.count_students}")
        self.label_information1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_information2.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @asyncSlot()
    async def update_info_admin(self):
        # Получаем текущие элементы списка
        current_items = [self.list_widget.item(i).data(
            Qt.ItemDataRole.UserRole) for i in range(self.list_widget.count())]

        # Получаем актуальные данные
        self.managers = await self.get_managers()
        self.instructors = await self.get_count_trainers()
        self.students = await self.get_count_students()
        self.count_instructors = self.instructors[0]['count_trainer']
        self.count_students = self.students[0]['count_student']
        self.label_information1.setText(
            f"Количество\nинструкторов:\n{self.count_instructors}")
        self.label_information2.setText(
            f"Количество\nкурсантов:\n{self.count_students}")

        manager_ids = [manager["id_user"] for manager in self.managers]

        items_to_add = [
            manager for manager in self.managers if manager["id_user"] not in current_items]
        items_to_remove = [i for i, item in enumerate(
            current_items) if item not in manager_ids]

        # Удаляем старые элементы
        for index in sorted(items_to_remove, reverse=True):
            self.list_widget.takeItem(index)

        # Добавляем новые элементы
        for manager in items_to_add:
            manager_id = manager["id_user"]
            manager_name = manager["desc_object"]

            item_widget = QWidget()
            layout = QHBoxLayout()
            name_label = QLabel(manager_name)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("./src/img/pencil.svg"))
            edit_button.setIconSize(QSize(24, 24))
            edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_button.clicked.connect(
                lambda _, m=manager_id: self.edit_manager(m))

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("./src/img/trash.svg"))
            delete_button.setIconSize(QSize(24, 24))
            delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_button.clicked.connect(
                lambda _, m=manager_id: self.drop_manager(m))

            layout.addWidget(name_label)
            layout.addStretch()
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)
            item_widget.setLayout(layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            list_item.setData(Qt.ItemDataRole.UserRole, manager_id)

            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

    def add_manager(self):
        date = None
        time = None
        trainer = None
        manager = None
        for button in self.buttons:
            if button.isChecked():
                self.type_object = button.text()
        main_widget = ChangePage(
            self.stack, 'Менеджеры', self.buttons, date, time, trainer, manager)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    def edit_manager(self, manager):
        date = None
        time = None
        trainer = None
        for button in self.buttons:
            if button.isChecked():
                self.type_object = button.text()
        main_widget = ChangePage(
            self.stack, 'Менеджеры', self.buttons, date, time, trainer, manager)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    @asyncSlot()
    async def drop_manager(self, manager):
        await self.delete_manager(manager)


class CadTeachPayCarPage(QWidget, Settings):
    def __init__(self, stack, buttons):
        super().__init__()
        self.stack = stack
        self.buttons = buttons
        self.create_page()

        self.data_loaders = {
            "Курсанты": self.get_students,
            "Инструкторы": self.get_trainers,
            "Автомобили": self.get_cars,
            "Занятия": self.get_lessons,
            "Платежи": self.get_payments,
        }

    def create_page(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(3000)

        self.menu_v_layout = QVBoxLayout()
        self.menu_h_layout = QHBoxLayout()

        spacer_vertical = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_horizontal = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.button_add = QPushButton("Добавить")
        self.button_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_add.clicked.connect(self.add_object)

        self.list_widget = QListWidget()

        self.menu_v_layout.addWidget(self.button_add)
        self.menu_v_layout.addItem(spacer_vertical)

        self.menu_h_layout.addLayout(self.menu_v_layout)
        self.menu_h_layout.addWidget(self.list_widget)

        self.setLayout(self.menu_h_layout)

        self.update_info()

    @asyncSlot()
    async def update_info(self):
        current_page = None
        for button in self.buttons:
            if button.isChecked():
                current_page = button.text()
                break

        if not current_page or current_page not in self.data_loaders:
            return

        loader_function = self.data_loaders[current_page]
        self.object = await loader_function()

        self.populate_list_widget()

    def populate_list_widget(self):
        # Получаем текущие элементы из списка
        current_items = [
            self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.list_widget.count())
        ]

        # Подготовка данных для добавления и удаления
        manager_ids = [item['id'] for item in self.object]
        items_to_add = [
            item for item in self.object if item['id'] not in current_items]
        items_to_remove = [
            item_id for item_id in current_items if item_id not in manager_ids]

        # Добавляем новые элементы
        for item in items_to_add:
            item_widget = self.create_list_widget_item(item)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            list_item.setData(Qt.ItemDataRole.UserRole, item['id'])
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

        # Удаляем старые элементы
        for i in range(self.list_widget.count() - 1, -1, -1):
            list_item = self.list_widget.item(i)
            item_id = list_item.data(Qt.ItemDataRole.UserRole)
            if item_id in items_to_remove:
                self.list_widget.takeItem(i)

    def create_list_widget_item(self, item):
        item_name = item['desc_object']
        item_id = item['id']

        item_widget = QWidget()
        layout = QHBoxLayout()
        spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        name_label = QLabel(item_name)
        layout.addWidget(name_label)

        edit_button = QPushButton()
        edit_button.setIcon(QIcon("./src/img/pencil.svg"))
        edit_button.setIconSize(QSize(24, 24))
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_button.clicked.connect(lambda: self.edit_object(item_id))

        delete_button = QPushButton()
        delete_button.setIcon(QIcon("./src/img/trash.svg"))
        delete_button.setIconSize(QSize(24, 24))
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.clicked.connect(lambda: self.delete_object(item_id))

        layout.addWidget(name_label)
        layout.addItem(spacer)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)

        item_widget.setLayout(layout)
        return item_widget

    def add_object(self):
        date = None
        time = None
        trainer = None
        for button in self.buttons:
            if button.isChecked():
                self.type_object = button.text()
        main_widget = ChangePage(
            self.stack, self.type_object, self.buttons, date, time, trainer, None)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    @asyncSlot()
    async def edit_object(self, item_id):
        date = None
        time = None
        trainer = None
        for button in self.buttons:
            if button.isChecked():
                self.type_object = button.text()
        main_widget = ChangePage(
            self.stack, self.type_object, self.buttons, date, time, trainer, item_id)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)

    @asyncSlot()
    async def delete_object(self, item_id):
        self.delete_data = {
            "Курсанты": self.delete_student,
            "Инструкторы": self.delete_trainer,
            "Автомобили": self.delete_car,
            "Платежи": self.delete_payment
        }

        try:
            for button in self.buttons:
                if button.isChecked():
                    current_button = button.text()

            delete_func = self.delete_data.get(current_button)

            await delete_func(item_id)

        except Exception as e:
            self.show_error_message(
                "Ошибка удаления объекта", f"Возникла ошибка, объект не удален: {str(e)}")


class LessonsPage(QWidget, Settings):
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
        self.data_week = []
        self.selected_instructor = None  # Выбранный инструктор
        self.create_page()

    def create_page(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_calendar)
        self.timer.timeout.connect(self.load_instructors)
        self.timer.start(3000)

        spacerItem2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.main_h_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()

        # Список инструкторов
        self.teach_list = QListWidget()
        self.teach_list.itemClicked.connect(self.on_instructor_selected)
        self.load_instructors()

        # Навигация по неделям
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

        # Сетка календаря
        self.week_layout = QVBoxLayout()
        self.week_layout.setSpacing(10)

        self.main_layout.addLayout(self.navigation_layout)
        self.main_layout.addLayout(self.week_layout)

        self.main_h_layout.addWidget(self.teach_list)
        self.main_h_layout.addItem(spacerItem2)
        self.main_h_layout.addLayout(self.main_layout)

        self.display_week()
        self.setLayout(self.main_h_layout)

    @asyncSlot()
    async def load_instructors(self):
        instructors = await self.get_trainers()
        self.teach_list.clear()
        for instructor in instructors:
            item = QListWidgetItem(instructor['desc_object'])
            item.setData(Qt.ItemDataRole.UserRole, instructor['id'])
            self.teach_list.addItem(item)

    def on_instructor_selected(self, item):
        self.selected_instructor = item.data(Qt.ItemDataRole.UserRole)
        self.update_calendar()

    @asyncSlot()
    async def update_week_label(self):
        end_date = self.start_date.addDays(6)
        start_text = self.locale.toString(self.start_date, "d MMMM yyyy")
        end_text = self.locale.toString(end_date, "d MMMM yyyy")
        self.week_label.setText(f"{start_text} - {end_text}")

        start_text = self.start_date.toString("yyyy-MM-dd")
        end_text = end_date.toString("yyyy-MM-dd")
        if self.selected_instructor:
            self.data_week = await self.get_lessons_by_trainer(
                str(start_text), str(end_text), self.selected_instructor)
        else:
            self.data_week = []

    def display_week(self):
        for i in reversed(range(self.week_layout.count())):
            widget = self.week_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        date = self.start_date
        cell_style = "QWidget { border: 1px solid gray; }"

        for i in range(7):
            day_widget = QWidget()
            day_layout = QHBoxLayout(day_widget)
            day_layout.setContentsMargins(2, 2, 2, 2)

            short_day_name = self.locale.dayName(
                date.dayOfWeek(), QLocale.FormatType.ShortFormat)
            day_label = QLabel(f"{short_day_name}, {date.day()}")
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setStyleSheet("border: none;")
            day_layout.addWidget(day_label)

            for hour in range(6, 22, 3):
                time_button = QPushButton(f"{hour}:00")
                time_button.setObjectName("time_button")

                date_str = date.toString("yyyy-MM-dd")
                today_date = QDate.currentDate()

                if date < today_date:
                    time_button.setStyleSheet("background-color: blue;")
                else:
                    time_button.setStyleSheet("background-color: green;")

                for lesson in self.data_week:
                    lesson_date_str = lesson['date_lesson'].strftime(
                        '%Y-%m-%d')
                    lesson_time = lesson['time_lesson']

                    if lesson_date_str == date_str and lesson_time == f"{hour}:00":
                        status = lesson['status_lesson']
                        if status == "Запланировано":
                            time_button.setStyleSheet("background-color: red;")
                        elif status == "Свободно":
                            time_button.setStyleSheet(
                                "background-color: green;")

                        break

                day_layout.addWidget(time_button)
                time_button.clicked.connect(self.on_time_button_clicked)

            day_widget.setStyleSheet(cell_style)
            self.week_layout.addWidget(day_widget)
            date = date.addDays(1)

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
        button = self.sender()
        if button is None:
            return

        # Извлекаем дату и время из кнопки
        button_time = button.text()  # Время в формате "HH:00"
        button_date = button.parentWidget().findChild(
            QLabel).text()  # Дата из QLabel в формате "день, DD"

        # Конвертируем дату из текста
        short_day_name, day = button_date.split(', ')
        day = int(day)
        current_month = self.start_date.month()
        current_year = self.start_date.year()
        button_date = QDate(current_year, current_month, day)

        self.date = button_date.toString("yyyy-MM-dd")
        self.time = button_time

        main_widget = ChangePage(
            self.stack, "Занятия", self.buttons, self.date, self.time, self.selected_instructor)
        self.stack.addWidget(main_widget)
        self.stack.setCurrentWidget(main_widget)


class ReportsPage(QWidget, Settings):
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
        self.get_report_button.clicked.connect(self.get_report)

        self.menu_v_layout.addWidget(self.hour_st_label)
        self.menu_v_layout.addWidget(self.hour_st)
        self.menu_v_layout.addWidget(self.coefficient_label)
        self.menu_v_layout.addWidget(self.coefficient)
        self.menu_v_layout.addWidget(self.get_report_button)

        self.menu_h_layout.addLayout(self.menu_v_layout)
        self.menu_h_layout.addWidget(self.report)

        self.setLayout(self.menu_h_layout)

    @asyncSlot()
    async def get_report(self):
        if self.hour_st.text() == "" or self.coefficient.text() == "":
            self.show_error_message("Ошибка", "Заполните все поля")
            return

        self.report.clear()

        now = datetime.now()

        start_of_month = datetime(now.year, now.month, 1)

        if now.month == 12:
            end_of_month = datetime(now.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_of_month = datetime(
                now.year, now.month + 1, 1) - timedelta(days=1)

        start_text = start_of_month.strftime("%Y-%m-%d")
        end_text = end_of_month.strftime("%Y-%m-%d")

        report = await self.get_count_lessons(start_text, end_text)

        for item in report:
            trainer_id = item['desc_object']
            lesson_count_main = item['count_main']
            lesson_count_add = item['count_add']
            summ = lesson_count_main * float(self.hour_st.text()) + lesson_count_add * float(
                self.hour_st.text()) * float(self.coefficient.text())

            item_widget = self.create_list_widget_item_with_data(
                trainer_id, summ)

            list_item = QListWidgetItem(self.report)
            list_item.setSizeHint(item_widget.sizeHint())
            self.report.addItem(list_item)
            self.report.setItemWidget(list_item, item_widget)

    def create_list_widget_item_with_data(self, trainer_id, summ):
        item_widget = QWidget()
        layout = QHBoxLayout()
        spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        id_label = QLabel(f"Инструктор: {trainer_id}")
        count_label = QLabel(f"Сумма: {summ}")
        layout.addWidget(id_label)
        layout.addWidget(count_label)

        item_widget.setLayout(layout)
        return item_widget


class ChangePage(QWidget, Settings):
    def __init__(self, stack, type_change, buttons, date, time, trainer, item=None):
        super().__init__()
        self.date = date
        self.time = time
        self.item = item
        self.trainer = trainer
        self.stack = stack
        self.type_change = type_change
        self.buttons = buttons

        self.arr_data = {"Курсанты": ['surname', 'name', 'patronymic', 'login', 'number_phone'],
                         "Менеджеры": ['surname', 'name', 'patronymic', 'login'],
                         "Инструкторы": ['surname', 'name', 'patronymic', 'login'],
                         "Автомобили": ['brand', 'number'],
                         "Занятия": [],
                         "Платежи": ['amount', 'date_payment']}

        self.data_loaders = {
            "Менеджеры": self.get_manager_by_id,
            "Курсанты": self.get_student_by_id,
            "Инструкторы": self.get_trainer_by_id,
            "Автомобили": self.get_car_by_id,
            "Занятия": self.get_lesson_by_trainer_date_time,
            "Платежи": self.get_payment_by_id
        }

        self.page_mapping = {
            "Главная": MainPage,
            "Курсанты": CadTeachPayCarPage,
            "Инструкторы": CadTeachPayCarPage,
            "Автомобили": CadTeachPayCarPage,
            "Занятия": LessonsPage,
            "Платежи": CadTeachPayCarPage,
            "Отчет": ReportsPage
        }

        self.create_page()

    @asyncSlot()
    async def create_page(self):
        if self.item:
            load_fun = self.data_loaders[self.type_change]
            self.item = await load_fun(self.item)
            if self.item:
                self.item = self.item[0]

        elif self.type_change == "Занятия":
            load_fun = self.data_loaders[self.type_change]
            self.item = await load_fun(self.trainer, self.date, self.time)
            if self.item:
                self.item = self.item[0]

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
        if self.item:
            self.label_name_object_input.setText(self.item['desc_object'])
        self.label_name_object_input.setPlaceholderText("Название объекта")
        self.menu_v_layout.addWidget(self.label_name_object)
        self.menu_v_layout.addWidget(self.label_name_object_input)

        i = 0
        for elem in self.types_change[self.type_change]:
            self.name_input_label = QLabel(elem)
            if elem in ['Инструктор', 'Курсант', 'Статус', 'Машина', 'Дата', 'Время', 'Дополнительное занятие']:
                if elem == 'Дополнительное занятие' and self.type_change == 'Занятия':
                    self.name_input = QCheckBox()
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.name_input)
                    if self.item:
                        self.name_input.setChecked(self.item['additional'])
                    self.name_input.setStyleSheet(
                        "background-color: #81b7f7; padding: 10px;")
                if (elem == 'Дата' or elem == 'Время') and self.type_change == 'Занятия':
                    self.name_input = QLineEdit()
                    if elem == 'Дата':
                        self.name_input.setText(self.date)
                    if elem == 'Время':
                        self.name_input.setText(self.time)
                    self.name_input.setEnabled(False)
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.name_input)
                    self.name_input.setStyleSheet(
                        "background-color: #81b7f7; padding: 10px;")
                if elem == 'Дата' and self.type_change == 'Платежи':
                    self.current_date = date.today().strftime("%Y-%m-%d")
                    self.name_input = QLineEdit()
                    self.name_input.setText(self.current_date)
                    self.name_input.setEnabled(False)
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.name_input)
                    self.name_input.setStyleSheet(
                        "background-color: #81b7f7; padding: 10px;")

                if elem == 'Статус' and (self.type_change == 'Курсанты' or self.type_change == 'Занятия' or self.type_change == 'Платежи'):
                    self.combo_box_status = QComboBox()
                    self.statuses_stud = ['Заявка', 'Обучается',
                                          'Закончил обучение', 'Отказ']
                    self.future_statuses_lesson = [
                        'Свободно', 'Запланировано']
                    self.past_statuses_lesson = [
                        'Проведено', 'Отменено']
                    self.payment_statuses = ['Оплачено', 'Не оплачено']
                    if self.type_change == 'Курсанты':
                        for status in self.statuses_stud:
                            self.combo_box_status.addItem(status)
                        if self.item:
                            self.combo_box_status.setCurrentText(
                                self.item['status_student'])
                    if self.type_change == 'Занятия':
                        if self.date >= date.today().strftime("%Y-%m-%d"):
                            for status in self.future_statuses_lesson:
                                self.combo_box_status.addItem(status)
                        if self.date < date.today().strftime("%Y-%m-%d"):
                            for status in self.past_statuses_lesson:
                                self.combo_box_status.addItem(status)
                    if self.type_change == 'Платежи':
                        for status in self.payment_statuses:
                            self.combo_box_status.addItem(status)
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.combo_box_status)
                    self.combo_box_status.setStyleSheet(
                        "background-color: #81b7f7; padding: 10px;")

                if elem == 'Инструктор' and (self.type_change == 'Курсанты' or self.type_change == 'Занятия'):
                    if self.type_change == 'Занятия':
                        self.name_input = QLineEdit()
                        self.name_input.setText(str(self.trainer))
                        self.name_input.setEnabled(False)
                        self.scroll_layout.addWidget(self.name_input_label)
                        self.scroll_layout.addWidget(self.name_input)
                        self.name_input.setStyleSheet(
                            "background-color: #81b7f7; padding: 10px;")
                        if self.item:
                            self.name_input.setText(
                                str(self.item['trainer_id']))
                    else:
                        self.combo_box_trainer = QComboBox()
                        self.trainers = await self.get_trainers()
                        for trainer in self.trainers:
                            # Добавляем пару (ID и desc_object)
                            self.combo_box_trainer.addItem(
                                f"{trainer['id']} - {trainer['desc_object']}")
                        if self.item:
                            self.combo_box_trainer.setCurrentText(
                                f"{self.item['trainer_id']} - {self.item['desc_object']}")
                        self.scroll_layout.addWidget(self.name_input_label)
                        self.scroll_layout.addWidget(self.combo_box_trainer)
                        self.combo_box_trainer.setStyleSheet(
                            "background-color: #81b7f7; padding: 10px;")

                if elem == 'Машина' and self.type_change == 'Инструкторы':
                    self.combo_box_car = QComboBox()
                    self.cars = await self.get_cars()
                    for car in self.cars:
                        # Добавляем пару (ID и desc_object)
                        self.combo_box_car.addItem(
                            f"{car['id']} - {car['desc_object']}")
                    if self.item:
                        self.combo_box_car.setCurrentText(
                            f"{self.item['car_id']} - {self.item['desc_object']}")
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.combo_box_car)
                    self.combo_box_car.setStyleSheet(
                        "background-color: #81b7f7; padding: 10px;")

                if elem == 'Курсант' and (self.type_change == 'Занятия' or self.type_change == 'Платежи'):
                    self.combo_box_student = QComboBox()
                    self.students = await self.get_students()
                    for student in self.students:
                        self.combo_box_student.addItem(
                            f"{student['id']} - {student['desc_object']}")
                    if self.item:
                        self.combo_box_student.setCurrentText(
                            f"{self.item['student_id']} - {self.item['desc_object']}")
                    self.scroll_layout.addWidget(self.name_input_label)
                    self.scroll_layout.addWidget(self.combo_box_student)
                    self.combo_box_student.setStyleSheet(
                        "background-color: #81b7f7; padding: 10px;"
                    )

            else:
                self.name_input = QLineEdit()
                self.name_input.setPlaceholderText(elem)
                if self.item:
                    if elem == 'Пароль':
                        pass
                    else:
                        self.name_input.setText(
                            str(self.item[self.arr_data[self.type_change][i]]))
                        i += 1
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

    def on_selection_change(self):
        selected_index = self.combo_box_car.currentIndex()
        selected_item = self.combo_box_car.itemText(selected_index)
        car_id = selected_item.split(" - ")[0]  # Берем только ID
        self.combo_box_car.setCurrentText(car_id)

    def back_to_manager_page(self):

        for button in self.buttons:
            if button.isChecked():
                current_button = button.text()

        page_class = self.page_mapping.get(current_button)
        if page_class:
            page_instance = page_class(self.stack, self.buttons)
            self.stack.addWidget(page_instance)
            self.stack.setCurrentWidget(page_instance)

    @asyncSlot()
    async def save_changes(self):
        self.create_data = {
            "Главная": self.create_manager,
            "Курсанты": self.create_student,
            "Инструкторы": self.create_trainer,
            "Автомобили": self.create_car,
            "Занятия": self.create_lesson,
            "Платежи": self.create_payment,
        }

        self.data_updates = {
            "Менеджеры": self.update_manager,
            "Курсанты": self.update_student,
            "Инструкторы": self.update_trainer,
            "Автомобили": self.update_car,
            "Занятия": self.update_lesson,
            "Платежи": self.update_payment
        }

        arr_fields = []
        for child in self.scroll_content.children():
            if isinstance(child, QLineEdit):
                text = child.text()
                if not text:
                    self.show_error_message("Ошибка", "Заполните все поля")
                    return
                arr_fields.append(text)
            if isinstance(child, QComboBox):
                text = child.currentText().split(" - ")[0]
                if not text:
                    self.show_error_message("Ошибка", "Заполните все поля")
                    return
                arr_fields.append(text)
            if isinstance(child, QCheckBox):
                text = child.isChecked()
                arr_fields.append(int(text))

        arr_fields.append(self.label_name_object_input.text())

        data_id = {
            'Главная': 'id_user',
            'Курсанты': 'id_user',
            'Инструкторы': 'id_user',
            'Автомобили': 'id_car',
            'Занятия': 'id_lesson',
            'Платежи': 'id'
        }

        try:
            for button in self.buttons:
                if button.isChecked():
                    current_button = button.text()
            if self.item:
                arr_fields.append(self.item[data_id[self.type_change]])
                update_func = self.data_updates.get(self.type_change)
                await update_func(*arr_fields)
            else:
                create_func = self.create_data.get(current_button)

                await create_func(*arr_fields)

        except Exception as e:
            if self.item:
                self.show_error_message(
                    "Ошибка обновления объекта", f"Возникла ошибка, объект не обновлен: {str(e)}")
            else:
                self.show_error_message(
                    "Ошибка добавления объекта", f"Возникла ошибка, объект не добавлен: {str(e)}")

        for button in self.buttons:
            if button.isChecked():
                current_button = button.text()

        page_class = self.page_mapping.get(current_button)
        if page_class:
            page_instance = page_class(self.stack, self.buttons)
            self.stack.addWidget(page_instance)
            self.stack.setCurrentWidget(page_instance)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()
