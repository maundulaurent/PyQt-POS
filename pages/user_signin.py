import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class UserSignin(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize database connection and create table if not exists
        self.init_db()
        self.init_ui()



    def init_db(self):
        # Connect to database and create 'user' table if not exists
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                username TEXT NOT NULL UNIQUE, 
                                password TEXT NOT NULL)''')
        self.conn.commit()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)


    
        self.reports_label = QLabel("Login as a Guest")
        self.main_layout.addWidget(self.reports_label)