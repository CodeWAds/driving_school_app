from PyQt6.QtWidgets import QApplication, QMessageBox, QLabel, QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt
import sys
# import pymysql
import bcrypt
from contextlib import asynccontextmanager
import aiomysql


class ResizableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def updateStyles(self):
        width = self.width()
        font_size = max(10, min(width // 50, 20))
        font_size2 = max(7, min(width // 100, 20))

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
                }}

            QPushButton:hover {{
                background-color: #2767f2;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 0px;
            }}

            QScrollArea#scroll_area {{
                background-color: #81b7f7;
            }}

            QLineEdit {{
                font-size: {font_size}px;
                padding: 10px;
                font-weight: bold;
                background-color: #81b7f7;
                border: none; border-radius: 15px;
                color: #FFFFFF;
            }}

            QLabel#label_info1 {{
                background-color: #81b7f7;
            }}

            QLabel#label_info2 {{
                background-color: #81b7f7;
            }}

            QListWidget {{
                background-color: #81b7f7;
            }}

            QPushButton#time_button {{
                font-size: {font_size}px;
            }}

            QListWidget {{
                font-size: {font_size}px;
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
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        last_button = self.buttons[-1]
        last_button.setStyleSheet(last_button.styleSheet().replace(
            "border-right: 1px solid white;", ""))

    def resizeEvent(self, event):
        """Обработчик события изменения размера окна."""
        self.updateStyles()
        super().resizeEvent(event)


class Settings():
    def __init__(self):
        self.manager_data = ['Фамилия', 'Имя', 'Отчество', 'Логин', 'Пароль',]
        self.student_data = ['Фамилия', 'Имя', 'Отчество', 'Логин',
                             'Пароль', 'Номер телефона', 'Инструктор', 'Статус']
        self.trainer_data = ['Фамилия', 'Имя',
                             'Отчество', 'Логин', 'Пароль', 'Машина']
        self.payment_data = ['Курсант', 'Сумма', 'Дата', 'Статус']
        self.lesson_data = ['Курсант', 'Инструктор', 'Дата',
                            'Время', 'Статус', 'Дополнительное занятие']
        self.car_data = ['Марка', 'Номер']

        self.types_change = {
            'Менеджеры': self.manager_data,
            'Курсанты': self.student_data,
            'Инструкторы': self.trainer_data,
            'Платежи': self.payment_data,
            'Занятия': self.lesson_data,
            'Автомобили': self.car_data,
        }

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def show_error_message(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    @asynccontextmanager
    async def get_connection(self):
        connection = None
        try:
            connection = await aiomysql.connect(
                host='150.241.90.210',
                user='mainuser',
                password='VeCrk135NeN!',
                db='driving_school',
                cursorclass=aiomysql.DictCursor
            )
            yield connection
        finally:
            if connection:
                connection.close()

    async def execute_query(self, query, params=None):
        async with self.get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchall()

    async def execute_single_query(self, query, params=None):
        async with self.get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchone()

    async def commit_query(self, query, params=None):
        async with self.get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params or ())
                await connection.commit()

    async def find_user_by_login(self, login):
        sql = "SELECT * FROM Users WHERE login = %s"
        return await self.execute_single_query(sql, (login,))

    async def check_passwd(self):
        user_data = await self.find_user_by_login(self.login)
        if user_data and bcrypt.checkpw(self.passwd.encode('utf-8'), user_data['password'].encode('utf-8')):
            return user_data
        return None


### GET ###


    async def get_managers(self):
        sql = """
            SELECT Managers.id_user, Managers.desc_object FROM Users
            INNER JOIN Managers ON Users.id_user = Managers.id_user
            WHERE role = 'Manager'
        """
        return await self.execute_query(sql)

    async def get_students(self):
        sql = """
            SELECT Users.id_user as id, Students.desc_object FROM Users
            INNER JOIN Students ON Users.id_user = Students.id_user
            WHERE role = 'Student'
        """
        return await self.execute_query(sql)

    async def get_trainers(self):
        sql = """
            SELECT Users.id_user as id, Trainers.desc_object FROM Users
            INNER JOIN Trainers ON Users.id_user = Trainers.id_user
            WHERE role = 'Trainer'
        """
        return await self.execute_query(sql)

    async def get_payments(self):
        sql = "SELECT Payments.id_payment as id, Payments.student_id, Payments.amount, Payments.date_payment, Payments.status_payment, Payments.desc_object FROM Payments"
        return await self.execute_query(sql)

    async def get_cars(self):
        sql = "SELECT Cars.id_car as id, Cars.brand, Cars.number, Cars.desc_object FROM Cars"
        return await self.execute_query(sql)

    async def get_lessons(self):
        sql = "SELECT * FROM Lessons"
        return await self.execute_query(sql)

    async def get_data_week(self, start_text, end_text):

        sql = "SELECT * FROM Lessons WHERE date_lesson BETWEEN %s AND %s"

        return await self.execute_query(sql, (start_text, end_text))

    async def get_count_students(self):

        sql = "SELECT COUNT(*) as count_student FROM Users WHERE role = 'Student'"

        return await self.execute_query(sql)

    async def get_count_trainers(self):

        sql = "SELECT COUNT(*) as count_trainer FROM Users WHERE role = 'Trainer'"

        return await self.execute_query(sql)

    async def get_lessons_by_trainer(self, start_text, end_text, trainer_id):

        sql = """SELECT * FROM Lessons
                WHERE date_lesson BETWEEN %s AND %s
                AND trainer_id = %s"""

        return await self.execute_query(sql, (start_text, end_text, trainer_id))

    async def get_count_lessons(self, start_text, end_text):

        sql = """SELECT 
            Trainers.desc_object,
            COUNT(CASE WHEN Lessons.status_lesson = 'Проведено' AND Lessons.additional = 0 THEN 1 END) AS count_main,
            COUNT(CASE WHEN Lessons.status_lesson = 'Проведено' AND Lessons.additional = 1 THEN 1 END) AS count_add
            
            FROM Lessons
            INNER JOIN Trainers ON Trainers.id_user = Lessons.trainer_id
            WHERE Lessons.date_lesson BETWEEN %s AND %s
            GROUP BY Trainers.desc_object;
            """

        return await self.execute_query(sql, (start_text, end_text))

    async def get_student_by_id(self, id_user):

        sql = """SELECT Users.id_user, Users.surname, Users.name, Users.patronymic, Users.login,Students.number_phone,Students.trainer_id, 
        Students.status_student, Students.desc_object FROM Users INNER JOIN Students 
        ON Users.id_user = Students.id_user WHERE role = 'Student' AND Users.id_user = %s"""

        return await self.execute_query(sql, (id_user,))

    async def get_manager_by_id(self, id_user):

        sql = """SELECT Users.id_user, Users.surname, Users.name, Users.patronymic, Users.login, 
       Managers.desc_object FROM Users INNER JOIN Managers
        ON Users.id_user = Managers.id_user WHERE role = 'Manager' AND Users.id_user = %s"""

        return await self.execute_query(sql, (id_user))

    async def get_trainer_by_id(self, id_user):

        sql = """SELECT Users.id_user, Users.surname, Users.name, Users.patronymic, Users.login, Trainers.car_id, 
       Trainers.desc_object FROM Users INNER JOIN Trainers
        ON Users.id_user = Trainers.id_user WHERE role = 'Trainer' AND Users.id_user = %s"""

        return await self.execute_query(sql, (id_user,))

    async def get_car_by_id(self, id_object):

        sql = """SELECT Cars.id_car, Cars.brand, Cars.number, Cars.desc_object FROM Cars WHERE Cars.id_car = %s"""

        return await self.execute_query(sql, (id_object,))

    async def get_lesson_by_trainer_date_time(self, trainer_id, date, time):

        sql = """SELECT Lessons.id_lesson, Lessons.student_id, Lessons.trainer_id, Lessons.status_lesson, Lessons.additional, Lessons.desc_object FROM Lessons WHERE Lessons.trainer_id = %s AND Lessons.date_lesson = %s AND Lessons.time_lesson = %s"""

        return await self.execute_query(sql, (trainer_id, date, time))

    async def get_payment_by_id(self, id_object):

        sql = """SELECT Payments.id_payment as id, Payments.student_id, Payments.amount, Payments.date_payment, Payments.status_payment, Payments.desc_object FROM Payments WHERE Payments.id_payment = %s"""

        return await self.execute_query(sql, (id_object,))

### CREATE ###

    async def create_manager(self, surname, name, patronymic, login, password, desc_object):

        password = self.hash_password(password)

        sql_users = """INSERT INTO Users (surname, name, patronymic, login, password, role) VALUES (%s, %s, %s, %s, %s, 'Manager');
        INSERT INTO Managers (id_user, desc_object) VALUES (LAST_INSERT_ID(), %s)"""

        await self.commit_query(sql_users, (surname, name, patronymic, login, password, desc_object))

    async def create_trainer(self, surname, name, patronymic, login, password, car, desc_object):

        password = self.hash_password(password)

        password = self.hash_password(password)

        sql_users = """INSERT INTO Users (surname, name, patronymic, login, password, role) 
                        VALUES (%s, %s, %s, %s, %s, 'Trainer'); 
                        INSERT INTO Trainers (id_user, car_id, desc_object) 
                        VALUES (LAST_INSERT_ID(), %s, %s)"""

        await self.commit_query(sql_users, (surname, name, patronymic, login, password, car, desc_object))

    async def create_car(self, brand, number, desc_object):

        sql = "INSERT INTO Cars (brand, number, desc_object) VALUES (%s, %s, %s)"

        await self.commit_query(sql, (brand, number, desc_object))

    async def create_student(self, surname, name, patronymic, login, password, num_phone, trainer, status, desc_object):

        password = self.hash_password(password)

        sql_users = """INSERT INTO Users (surname, name, patronymic, login, password, role) 
                        VALUES (%s, %s, %s, %s, %s, 'Student'); 
                        INSERT INTO Students (id_user, number_phone, trainer_id, status_student, desc_object) 
                        VALUES (LAST_INSERT_ID(), %s, %s, %s, %s)"""

        await self.commit_query(sql_users, (surname, name, patronymic, login, password, num_phone, trainer, status, desc_object))

    async def create_lesson(self, student_id, trainer_id, date, time, status, additional, desc_object):

        sql = "INSERT INTO Lessons (student_id, trainer_id, date_lesson, time_lesson, status_lesson, additional, desc_object) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        await self.commit_query(sql, (student_id, trainer_id, date, time, status, additional, desc_object))

    async def create_payment(self, student_id, amount, date_payment, status_payment, desc_object):

        sql = "INSERT INTO Payments (student_id, amount, date_payment, status_payment, desc_object) VALUES (%s, %s, %s, %s, %s)"

        await self.commit_query(sql, (student_id, amount, date_payment, status_payment, desc_object))


### DELETE ###

    async def delete_manager(self, id_manager):

        sql = "DELETE Users FROM Users WHERE Users.id_user = %s"

        await self.commit_query(sql, (id_manager))

    async def delete_student(self, id_user):

        sql = "DELETE Users FROM Users INNER JOIN Students ON Users.id_user = Students.id_user WHERE Users.id_user = %s"

        await self.commit_query(sql, (id_user))

    async def delete_trainer(self, id_user):

        sql = "DELETE Users FROM Users INNER JOIN Trainers ON Users.id_user = Trainers.id_user WHERE Users.id_user = %s"

        await self.commit_query(sql, (id_user))

    async def delete_car(self, id_object):

        sql = "DELETE FROM Cars WHERE id_car = %s"

        await self.commit_query(sql, (id_object))

    async def delete_payment(self, id_object):

        sql = "DELETE FROM Payments WHERE id_payment = %s"

        await self.commit_query(sql, (id_object))

### UPDATE ###

    async def update_manager(self, surname, name, patronymic, login, password, desc_object, id_user):

        password = self.hash_password(password)

        sql = """UPDATE Users SET surname = %s, name = %s, patronymic = %s, login = %s, password = %s WHERE id_user = %s;
                UPDATE Managers SET desc_object = %s WHERE id_user = %s"""

        await self.commit_query(sql, (surname, name, patronymic, login, password, id_user, desc_object, id_user))

    async def update_student(self, surname, name, patronymic, login, password, num_phone, trainer, status, desc_object, id_user):

        password = self.hash_password(password)

        sql = """UPDATE Users SET surname = %s, name = %s, patronymic = %s, login = %s, password = %s WHERE id_user = %s;
                UPDATE Students SET number_phone = %s, trainer_id = %s, status_student = %s, desc_object = %s WHERE id_user = %s"""

        await self.commit_query(sql, (surname, name, patronymic, login, password, id_user, num_phone, trainer, status, desc_object, id_user))

    async def update_trainer(self, surname, name, patronymic, login, password, car, desc_object, id_user):

        password = self.hash_password(password)

        sql = """UPDATE Users SET surname = %s, name = %s, patronymic = %s, login = %s, password = %s WHERE id_user = %s;
                UPDATE Trainers SET car_id = %s, desc_object = %s WHERE id_user = %s"""

        await self.commit_query(sql, (surname, name, patronymic, login, password, id_user, car, desc_object, id_user))

    async def update_car(self, desc_object, brand, number, id_object):

        sql = "UPDATE Cars SET brand = %s, number = %s, desc_object = %s WHERE id_car = %s"

        await self.commit_query(sql, (brand, number, desc_object, id_object))

    async def update_payment(self, student_id, amount, date_payment, status_payment, desc_object, id_object):

        sql = "UPDATE Payments SET student_id = %s, amount = %s, date_payment = %s, status_payment = %s, desc_object = %s WHERE id_payment = %s"

        await self.commit_query(sql, (student_id, amount, date_payment, status_payment, desc_object, id_object))

    async def update_lesson(self, student_id, trainer_id, date, time, status, additional, desc_object, id_object):

        sql = "UPDATE Lessons SET student_id = %s, trainer_id = %s, date_lesson = %s, time_lesson = %s, status_lesson = %s, additional = %s, desc_object = %s WHERE id_lesson = %s"

        await self.commit_query(sql, (student_id, trainer_id, date, time, status, additional, desc_object, id_object))
