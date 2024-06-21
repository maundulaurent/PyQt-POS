from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout

class WelcomePage(QWidget):
    def __init__(self, switch_to_admin_page, switch_to_user_signin_page):
        super().__init__()

        # Main horizontal layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Left column
        self.left_column = QVBoxLayout()
        self.left_label = QLabel("+POS Peter System")
        self.left_column.addWidget(self.left_label)
        self.layout.addLayout(self.left_column, 1)  # Add left column to the main layout

        # Right column
        self.right_column = QVBoxLayout()
        self.layout.addLayout(self.right_column, 3)  # Add right column to the main layout

        self.init_ui(switch_to_admin_page, switch_to_user_signin_page)

    def init_ui(self, switch_to_admin_page, switch_to_user_signin_page):
        self.welcome_label = QLabel("~|~Init Technologies~|~")
        self.right_column.addWidget(self.welcome_label)

        # Form layout for login inputs

        self.signin_label = QLabel("SignIn Page")
        self.layout.addWidget(self.signin_label)
        
        self.form_layout = QFormLayout()
        self.right_column.addLayout(self.form_layout)

        

        self.username_input = QLineEdit()
        self.form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addRow("Password:", self.password_input)

        # Login buttons
        self.login_admin = QPushButton("Login as Admin")
        self.login_admin.clicked.connect(switch_to_admin_page)
        self.right_column.addWidget(self.login_admin)

        self.login_user = QPushButton("Login as Guest")
        self.login_user.clicked.connect(switch_to_user_signin_page)
        self.right_column.addWidget(self.login_user)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(switch_to_user_signin_page)
        self.right_column.addWidget(self.start_button)
