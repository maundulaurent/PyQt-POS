from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class HistoryWidget(QWidget):
    def __init__(self, switch_to_dashboard_page):
        super().__init__()
        self.switch_to_dashboard_page = switch_to_dashboard_page      

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #fff;
                border-radius: 6px;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                background-color: #4e5052;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QTableWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 4px;
                border: 1px solid #ddd;
            }
        """)

        # Main content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_area)

        # Header Section
        header_layout = QHBoxLayout()
        self.content_layout.addLayout(header_layout)

        self.header = QLabel("System History")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        header_layout.addWidget(self.header)

        # Quick Statistics Bar
        quick_stats_layout = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout)

        self.add_card_to_layout(quick_stats_layout, "Transactions", "14 Transactions", "click for more..")
        self.add_card_to_layout(quick_stats_layout, "Account History", "Change in account..", "click..")
        self.add_card_to_layout(quick_stats_layout, "Orders History", "recent Orders", "see all orders...")
        self.add_card_to_layout(quick_stats_layout, "Stocks History", "loaded Products", "check your stocks...")

        # Quick Statistics Bar2
        quick_stats_layout2 = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout2)

        self.add_card_to_layout(quick_stats_layout2, "Inventory", "check categories", "Actions..")
        self.add_card_to_layout(quick_stats_layout2, "Top Selling category", "Clothes category", "see order")
        self.add_card_to_layout(quick_stats_layout2, " ", "Alerts", " ")
        self.add_card_to_layout(quick_stats_layout2, " ", "", " ")

        # Quick Statistics Bar3
        quick_stats_layout3 = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout3)

        self.add_card_to_layout(quick_stats_layout3, "Sales", "Items sold", "Details..")
        self.add_card_to_layout(quick_stats_layout3, "Total Sales Today", "New Americano Perfume", "30 units sold")
        self.add_card_to_layout(quick_stats_layout3, "Pending Orders", "5 Orders", "...")
        self.add_card_to_layout(quick_stats_layout3, "Stock Alerts", "3 Products", "...")

        # Quick link to Dashboard
        quick_stats_layout4 = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout4)
        self.add_card_to_layout(quick_stats_layout4, "Quick Link", "<<Dashboard", "", self.switch_to_dashboard_page)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card.setStyleSheet("""
            #card {
                background-color: #2b2b2b;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                min-width: 200px;
                max-width: 300px;
                height: 100px;
            }
        """)
        self.content_layout.addWidget(card, alignment=Qt.AlignTop)

    def add_card_to_layout(self, layout, title, main_text, sub_text="", function=None):
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card.setStyleSheet("""
            #card {
                background-color: #4e5052;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                min-width: 100px;
                max-width: 200px;
                height: 100px;
            }
        """)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size:16px; color: #A8A8A8; background-color: #4e5052;")
        card_layout.addWidget(title_label)

        main_text_label = QLabel(main_text)
        main_text_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff; background-color: #4e5052;")
        card_layout.addWidget(main_text_label)

        if sub_text:
            sub_text_label = QLabel(sub_text)
            sub_text_label.setStyleSheet("font-size: 14px; color: #A8A8A8; background-color: #4e5052;")
            card_layout.addWidget(sub_text_label)

        if function:
            button = QPushButton()
            button.setStyleSheet("background-color: transparent; border: none;")
            button.clicked.connect(function)
            card_layout.addWidget(button)
            button.setGeometry(card.rect())  # Ensure the button covers the card entirely
            button.lower()  # Ensure the button is behind other widgets

        layout.addWidget(card, alignment=Qt.AlignTop)
