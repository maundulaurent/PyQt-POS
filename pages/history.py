from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pages.dialogs import (
    TransactionsDialog,
    OrdersHistoryDialog,
    StocksHistoryDialog,
    InventoryHistoryDialog,
    AlertsHistoryDialog,
    SalesHistoryDialog
)
import sqlite3
from datetime import datetime

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

        # Get today's transaction count
        transaction_count = self.get_today_transaction_count()

        self.add_card_to_layout(quick_stats_layout, "Transactions", f"{transaction_count} Transactions Today", "click for more..", self.show_transactions)
        self.add_card_to_layout(quick_stats_layout, "Sales", "Items sold", "Details..", self.show_sales_history_dialog)
        self.add_card_to_layout(quick_stats_layout, "Orders History", "Recent Orders", "see all orders...", self.show_orders_history_dialog)
        self.add_card_to_layout(quick_stats_layout, "Stocks History", "Products' activities", "check your stocks...", self.show_stocks_history_dialog)

        # Quick Statistics Bar2
        quick_stats_layout2 = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout2)
        self.add_card_to_layout(quick_stats_layout2, "Inventory", "Check categories", "Actions..", self.show_inventory_history_dialog)
        self.add_card_to_layout(quick_stats_layout2, "Top Selling Category", " ", "See order", self.show_modal)
        self.add_card_to_layout(quick_stats_layout2, " ", "Alerts", " ", self.show_alerts_history_dialog)
        self.add_card_to_layout(quick_stats_layout2, " ", "", " ", self.show_modal)

        # Quick link to Dashboard
        quick_stats_layout4 = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout4)
        self.add_card_to_layout(quick_stats_layout4, "", "Dashboard", "click here", self.switch_to_dashboard_page)

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
                padding: 15px;
                margin: 5px;
                min-width: 100px;
                max-width: 200px;
                height: 100px;
            }
        """)

        # Title as QLabel
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size:16px; color: #A8A8A8; background-color: #4e5052;")
        card_layout.addWidget(title_label)

        # Main text as QLabel
        main_text_label = QLabel(main_text)
        main_text_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff; background-color: #4e5052;")
        card_layout.addWidget(main_text_label)

        # Subtext as QPushButton if function is provided
        if function:
            sub_text_button = QPushButton(sub_text)
            sub_text_button.setStyleSheet("font-size: 14px; color: #A8A8A8; background-color: #4e5052; border: none; text-align: left;")
            sub_text_button.clicked.connect(function)
            card_layout.addWidget(sub_text_button)
        else:
            sub_text_label = QLabel(sub_text)
            sub_text_label.setStyleSheet("font-size: 14px; color: #A8A8A8; background-color: #4e5052;")
            card_layout.addWidget(sub_text_label)

        layout.addWidget(card, alignment=Qt.AlignTop)

    def get_today_transaction_count(self):
        today_date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM sales_history
            WHERE date_of_sale LIKE ?
        """, (f"{today_date}%",))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def show_modal(self):
        QMessageBox.information(self, "Peter POS", "Please check later.")

    def show_transactions(self):
        dialog = TransactionsDialog(self)
        dialog.exec_()

    def show_orders_history_dialog(self):
        dialog = OrdersHistoryDialog(self)
        dialog.exec_()

    def show_stocks_history_dialog(self):
        dialog = StocksHistoryDialog(self)
        dialog.exec_()

    def show_inventory_history_dialog(self):
        dialog = InventoryHistoryDialog(self)
        dialog.exec_()

    def show_alerts_history_dialog(self):
        dialog = AlertsHistoryDialog(self)
        dialog.exec_()

    def show_sales_history_dialog(self):
        dialog = SalesHistoryDialog(self)
        dialog.exec_()
