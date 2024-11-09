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

            QLineEdit {{
                font-size: {font_size}px;
                padding: 10px;
                font-weight: bold;
                background-color: #81b7f7;
                border: none; border-radius: 15px;
                color: #FFFFFF;
            }}        

            QLabel#label_info1 {{
                padding: 2px;
                background-color: #81b7f7;
            }}  
            QLabel#label_info2 {{
                padding: 20px;
                background-color: #81b7f7;
            }}
            QListWidget {{
                background-color: #81b7f7;
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
        pass


    async def connect_to_db(self):
        try:
            # Установка асинхронного соединения с базой данных
            connection = await aiomysql.connect(
                host='150.241.90.210',
                user='mainuser',
                password='VeCrk135NeN!',
                db='f1030472_autoschool',
                cursorclass=aiomysql.DictCursor
            )
            return connection
        except Exception as ex:
            return None


    async def find_user_by_login(self, login):
        connection = await self.connect_to_db()
        if not connection:
            return None

        try:
            async with connection.cursor() as cursor:
                sql = "SELECT * FROM user WHERE login = %s"
                await cursor.execute(sql, (login,))
                user = await cursor.fetchone()
            return user
        except Exception as ex:
            return None
        finally:
            connection.close()


    async def check_passwd(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        user = await self.find_user_by_login(self.login)
        
        if user:
            stored_password = user['password']
            if bcrypt.checkpw(self.passwd.encode('utf-8'), stored_password.encode('utf-8')):
                QApplication.restoreOverrideCursor()
                return user
            else:
                QApplication.restoreOverrideCursor()
                return False
        else:
            QApplication.restoreOverrideCursor()
            return False

