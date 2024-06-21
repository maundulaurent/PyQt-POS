from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QAction, QLabel, QLineEdit, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

from pages.welcome_page import WelcomePage
from pages.dashboard_page import DashboardPage
from pages.product_management_page import ProductManagementPage
from pages.checkout_page import CheckoutPage
from pages.inventory_management_page import InventoryManagementPage
from pages.settings_page import SettingsPage
from pages.reports_page import ReportsPage
from pages.user_signin import UserSignin

class POSSystem(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Peter Mulwa POS")
        
        
        icon = QIcon('home.png')
        self.setWindowIcon(QIcon(icon))
        self.setGeometry(100, 50, 1000, 600)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.welcome_page = WelcomePage(self.switch_to_dashboard_page, self.show_user_signin_page)
        self.dashboard_page = DashboardPage()
        self.product_management_page = ProductManagementPage()
        self.checkout_page = CheckoutPage()
        self.inventory_management_page = InventoryManagementPage()
        self.settings_page = SettingsPage()
        self.reports_page = ReportsPage()
        self.user_signin = UserSignin()

        self.central_widget.addWidget(self.welcome_page)
        self.central_widget.addWidget(self.dashboard_page)
        self.central_widget.addWidget(self.product_management_page)
        self.central_widget.addWidget(self.checkout_page)
        self.central_widget.addWidget(self.inventory_management_page)
        self.central_widget.addWidget(self.settings_page)
        self.central_widget.addWidget(self.reports_page)
        self.central_widget.addWidget(self.user_signin)

        self.create_menu_bar()
        # self.create_top_bar()

    def switch_to_dashboard_page(self):
        self.central_widget.setCurrentWidget(self.dashboard_page)

    def show_user_signin_page(self):
        self.central_widget.setCurrentWidget(self.user_signin)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #000; color: #fff; padding: 8px;")

        navigate_menu = menu_bar.addMenu("Navigate")

        dashboard_action = QAction("Dashboard", self)
        dashboard_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.dashboard_page))
        navigate_menu.addAction(dashboard_action)

        product_management_action = QAction("Product Management", self)
        product_management_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.product_management_page))
        navigate_menu.addAction(product_management_action)

        checkout_action = QAction("Checkout", self)
        checkout_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.checkout_page))
        navigate_menu.addAction(checkout_action)

        inventory_management_action = QAction("Inventory Management", self)
        inventory_management_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.inventory_management_page))
        navigate_menu.addAction(inventory_management_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.settings_page))
        navigate_menu.addAction(settings_action)

        reports_action = QAction("Reports", self)
        reports_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.reports_page))
        navigate_menu.addAction(reports_action)

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        account_menu = menu_bar.addMenu("Account")
        logout_action = QAction("Signout", self)
        logout_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.welcome_page))
        account_menu.addAction(logout_action)

 
    def show_about_dialog(self):
        about_dialog = QLabel("This is a POS system For Managing a business.")
        about_dialog.setWindowTitle("About")
        about_dialog.setGeometry(100, 100, 200, 100)
        about_dialog.show()
