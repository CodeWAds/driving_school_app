from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
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
        self.user_data = {
            'surname': None,
            'name': None,
            'patronymic': None,
            'login': None,
            'password': None,
            'role': None
        }

        self.student_data = {
            'id_user': None,
            'number_phone': None,
            'trainer_id': None,
            'status_student': None,
            'desc_object': None
        }

        self.trainer_data = {
            'id_user': None,
            'car_id': None,
            'desc_object': None
        }

        self.payment_data = {
            'id_payment': None,
            'student_id': None,
            'amount': None,
            'date_payment': None,
            'status_payment': None,
            'desc_object': None
        }

        self.manager_data = {
            'id_user': None,
            'desc_object': None
        }

        self.lesson_data = {
            'id_lesson': None,
            'student_id': None,
            'trainer_id': None,
            'date_lesson': None,
            'status_lesson': None,
            'desc_object': None
        }

        self.car_data = {
            'id_car': None,
            'brand': None,
            'number': None,
            'desc_object': None
        }

        self.admin_data = {
            'id_user': None,
            'desc_object': None
        }

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
                sql = "SELECT * FROM Users where role = 'Manager'"
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
                sql = "SELECT * FROM Users where role = 'Manager'"
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
                sql = "SELECT * FROM Users where role = 'Manager'"
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