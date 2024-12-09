from PyQt6.QtWidgets import QApplication,QMessageBox, QLabel, QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt
import sys
import pymysql
import bcrypt
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
        self.student_data = ['Фамилия', 'Имя', 'Отчество', 'Логин', 'Пароль', 'Номер телефона', 'Инструктор', 'Статус']
        self.trainer_data = ['Фамилия', 'Имя', 'Отчество', 'Логин', 'Пароль', 'Машина']
        self.payment_data = ['Сумма', 'Дата', 'Статус']
        self.lesson_data = ['Дата', 'Статус']
        self.car_data = ['Марка', 'Номер']

        self.types_change = {
            'Менеджеры': self.manager_data,
            'Курсанты': self.student_data,
            'Инструкторы': self.trainer_data,
            'Платежи': self.payment_data,
            'Уроки': self.lesson_data,
            'Автомобили': self.car_data,
        }

    def show_error_message(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    async def connect_to_db(self):
        try:
            connection = await aiomysql.connect(
                host='150.241.90.210',
                user='mainuser',
                password='VeCrk135NeN!',
                db='driving_school',
                cursorclass=aiomysql.DictCursor
            )
            return connection
        except Exception as ex:
            print(ex)

    async def find_user_by_login(self, login):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM Users WHERE login = %s"
                await cursor.execute(sql, (login,))
                user = await cursor.fetchone()
            return user
        except Exception as ex:
            return None
        finally:
            connection.close()

    async def check_passwd(self):
        user = await self.find_user_by_login(self.login)
        if user:
            stored_password = user['password']
            if bcrypt.checkpw(self.passwd.encode('utf-8'), stored_password.encode('utf-8')):
                return user
            else:
                return False
        else:
            return False

    async def get_managers(self):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM Users where role = 'Manager'"
                await cursor.execute(sql)
                manager = await cursor.fetchall()
            return manager
        except Exception as ex:
            return None

    async def get_students(self):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM Users where role = 'Student'"
                await cursor.execute(sql)
                manager = await cursor.fetchall()
            return manager
        except Exception as ex:
            return None

    async def get_trainers(self):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM Users where role = 'Manager'"
                await cursor.execute(sql)
                manager = await cursor.fetchall()
            return manager
        except Exception as ex:
            return None

    async def get_payments(self):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM Payments"
                await cursor.execute(sql)
                manager = await cursor.fetchall()
            return manager
        except Exception as ex:
            return None

    async def get_lessons(self):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM Lessons"
                await cursor.execute(sql)
                manager = await cursor.fetchall()
            return manager
        except Exception as ex:
            return None
        
    
    async def create_manager(self, surname, name, patronymic, login, password, role):
        connection = await self.connect_to_db()
        if not connection:
            return None
        
        try:
            async with connection.cursor() as cursor:
                sql = "INSERT INTO Users (surname, name, patronymic, login, password, role) VALUES (%s, %s, %s, %s, %s, %s)"
                await cursor.execute(sql, (surname, name, patronymic, login, password, role))
                sql = "INSERT INTO Managers (id_user, desc_object) VALUES (LAST_INSERT_ID(), %s)"
                await cursor.execute(sql, ("test"))
                await connection.commit()
            return True
        except Exception as ex:
            return None
        
    async def drop_manager(self, id_user):
        connection = await self.connect_to_db()
        if not connection:
            return None
        
        try:
            async with connection.cursor() as cursor:
                sql = "DELETE FROM Users WHERE name = %s"
                await cursor.execute(sql, (id_user,))
                await connection.commit()
            return True
        except Exception as ex:
            return None