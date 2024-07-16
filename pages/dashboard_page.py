from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

import sqlite3
from datetime import datetime
        
class DashboardPage(QWidget):
    def __init__(self,
                 show_products,
                 show_inventory,
                 show_orders,
                 show_history,
                 show_checkout
                 ):
        super().__init__()
        self.show_products = show_products
        self.show_inventory = show_inventory
        self.show_orders = show_orders
        self.show_history = show_history
        self.show_checkout = show_checkout
        

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)


        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #fff;
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
            .sidebar {
                background-color: #333;
                color: white;
                padding: 15px;
            }
            .sidebar QPushButton {
                background-color: #555;
                color: white;
                margin-bottom: 10px;
            }
            .sidebar QPushButton:hover {
                background-color: #777;
            }
        """)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar.setStyleSheet("background-color: #4e5052; border-radius: 6px;")
        self.sidebar.setFixedWidth(250)
        self.main_layout.addWidget(self.sidebar)

        # Adjust the margins and spacing here
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)  # Add some margin around the layout
        self.sidebar_layout.setSpacing(5)  # Adjust vertical spacing between buttons

        # Add sidebar buttons with callbacks
        self.add_sidebar_button("Dashboard")
        self.add_sidebar_button("Products", self.show_products)
        self.add_sidebar_button("Categories", self.show_inventory)
        self.add_sidebar_button("Orders", self.show_orders)
        # self.add_sidebar_button("Transactions")
        self.add_sidebar_button("POS History", self.show_history)

        # Main content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_area)
        # self.content_layout.setSpacing(0)  # Remove vertical spacing
        # self.content_layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins (left, top, right, bottom)



        # Header Section
        header_layout = QHBoxLayout()
        self.content_layout.addLayout(header_layout)

        self.header = QLabel("Dashboard")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        header_layout.addWidget(self.header)

        # Quick Statistics Bar
        quick_stats_layout = QHBoxLayout()
        self.content_layout.addLayout(quick_stats_layout)

         # Get today's transaction count
        transaction_count = self.get_today_transaction_count()
        pending_orders = self.get_pending_orders()
        low_stocks = self.get_low_stocks()

        self.add_card_to_layout(quick_stats_layout, "Transactions", f"{transaction_count} Transactions", "Today")
        self.add_card_to_layout(quick_stats_layout, "Top Selling Product", "New Americano Perfume", "30 units sold")
        self.add_card_to_layout(quick_stats_layout, "Pending Orders", f"{pending_orders} Orders", "...")
        self.add_card_to_layout(quick_stats_layout, "Low Stock Alerts", f"{low_stocks} Products", "...")

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
# ========================================  first   ================================================
        # Quick actions section
        self.quick_actions_layout = QGridLayout()
        self.content_layout.addLayout(self.quick_actions_layout)


        self.new_sale_frame = QFrame()
        self.new_sale_frame.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            padding: 20px;                                  
        """)
        self.new_sale_layout = QVBoxLayout()
        self.new_sale_frame.setLayout(self.new_sale_layout)

        self.new_sale_button = QPushButton("New Sale +")
        # self.new_sale_button.setAlignment(Qt.AlignCenter)
        self.new_sale_button.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            font-weight:bold;
            font-size: 20px;
        """)
        self.new_sale_button.clicked.connect(self.show_checkout)
        self.new_sale_layout.addWidget(self.new_sale_button)

        # Create the card-like frame for Add Product button
        self.add_product_frame = QFrame()
        self.add_product_frame.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            padding: 20px;
        """)
        self.add_product_layout = QVBoxLayout()
        self.add_product_frame.setLayout(self.add_product_layout)

        self.add_product_button = QPushButton("Add Product")
        # self.add_product_button.setAlignment(Qt.AlignCenter)
        self.add_product_button.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 20px;
        """)
        self.add_product_button.clicked.connect(self.show_products)
        self.add_product_layout.addWidget(self.add_product_button)


        # Add widgets to the grid layout
        self.quick_actions_layout.addWidget(self.new_sale_frame, 0, 0)  # Row 0, Column 0
        self.quick_actions_layout.addWidget(self.add_product_frame, 0, 1, 1, 2)  # Row 0, Column 1, Span 1 row, 2 columns
# ================================  TWO    ==========================================================
        # Quick actions section two
        self.quick_actions_layout = QGridLayout()
        self.content_layout.addLayout(self.quick_actions_layout)


        self.new_sale_frame = QFrame()
        self.new_sale_frame.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            padding: 20px;                                  
        """)
        self.new_sale_layout = QVBoxLayout()
        self.new_sale_frame.setLayout(self.new_sale_layout)

        self.new_sale_button = QPushButton("Categories")
        # self.new_sale_button.setAlignment(Qt.AlignCenter)
        self.new_sale_button.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            font-weight:bold;
            font-size: 20px;
        """)
        self.new_sale_button.clicked.connect(self.show_inventory)
        self.new_sale_layout.addWidget(self.new_sale_button)

        # Create the card-like frame for Add Product button
        self.add_product_frame = QFrame()
        self.add_product_frame.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            padding: 20px;
        """)
        self.add_product_layout = QVBoxLayout()
        self.add_product_frame.setLayout(self.add_product_layout)

        self.add_product_button = QPushButton("Inventory Alerts")
        # self.add_product_button.setAlignment(Qt.AlignCenter)
        self.add_product_button.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 20px;
        """)
        self.add_product_button.clicked.connect(self.show_history)
        self.add_product_layout.addWidget(self.add_product_button)


        # Add widgets to the grid layout
        self.quick_actions_layout.addWidget(self.new_sale_frame, 0, 0)  # Row 0, Column 0
        self.quick_actions_layout.addWidget(self.add_product_frame, 0, 1, 1, 2)  # Row 0, Column 1, Span 1 row, 2 columns

# ======================================    end tw0 =======================================================================


    def add_sidebar_button(self, text, callback=None):
        button = QPushButton()
        button_layout = QHBoxLayout()
        button.setLayout(button_layout)

        text_label = QLabel(text)
        button_layout.addWidget(text_label, alignment=Qt.AlignLeft)  # Align text to the left

        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)  # Adjust spacing between icon and text

        button.setStyleSheet("""
            text-align: left;
            padding: 8px 12px;
            margin: 0; 
            border: none;  
            font-size: 16px;        
        """)

        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sidebar_layout.addWidget(button)
        self.sidebar_layout.setAlignment(Qt.AlignTop)  # Align buttons at the top of the layout
        if callback:
            button.clicked.connect(callback)

    def add_card_to_layout(self, layout, title, main_text, sub_text=""):
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card.setStyleSheet("""
            #card {
                background-color: #4e5052;
                border-radius: 10px;
                padding: 4px;
                margin: 2px;
                min-width: 100px;
                max-width: 200px;
                height: 100px;
            }
        """)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size:16px; color: #A8A8A8; background-color: #4e5052;")#
        card_layout.addWidget(title_label)

        main_text_label = QLabel(main_text)
        main_text_label.setStyleSheet("font-size: 15px; font-weight: bold;color: #ffffff; background-color: #4e5052;")# 
        card_layout.addWidget(main_text_label)

        if sub_text:
            sub_text_label = QLabel(sub_text)
            sub_text_label.setStyleSheet("font-size: 14px; color: #A8A8A8; background-color: #4e5052;")#
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
    
    def get_pending_orders(self):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM orders_history
            WHERE amount_received IS NULL
        """)
        # pending_orders = cursor.fetchall()
        # conn.close()this is for chm
        # return pending_orders
        # change something
        count = cursor.fetchone()[0]
        conn.close()
        return count
    def get_low_stocks(self):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM alerts_history
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count