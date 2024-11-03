from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys

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
        last_button.setStyleSheet(last_button.styleSheet().replace("border-right: 1px solid white;", ""))

    def resizeEvent(self, event):
        """Обработчик события изменения размера окна."""
        self.updateStyles()
        super().resizeEvent(event)


class CRUD():
    def __init__(self):
        self.username = "admin"
        self.password = "admin"
    
    def create():
        pass

    def read():
        pass

    def update():
        pass

    def delete():
        pass