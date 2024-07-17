
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("#lowerpane {\n"
"    background-color:#29c9d9;\n"
"}\n"
"\n"
"#upperright {\n"
"    background-color:#2731f2;\n"
"}\n"
"\n"
"#uleft2 {\n"
"    background-color:#58ecfc;\n"
"}\n"
"\n"
"#uleft1 {\n"
"    background-color:#4c8187;\n"
"}\n"
"#uleft3 {\n"
"    background-color:#0f2b2e;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.upperpane = QtWidgets.QWidget(self.centralwidget)
        self.upperpane.setObjectName("upperpane")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.upperpane)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.upperleft = QtWidgets.QWidget(self.upperpane)
        self.upperleft.setObjectName("upperleft")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.upperleft)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.upperleft)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uleft1 = QtWidgets.QWidget(self.widget_2)
        self.uleft1.setObjectName("uleft1")
        self.horizontalLayout_2.addWidget(self.uleft1)
        self.uleft2 = QtWidgets.QWidget(self.widget_2)
        self.uleft2.setObjectName("uleft2")
        self.horizontalLayout_2.addWidget(self.uleft2)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.upperleft)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(2, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_6 = QtWidgets.QWidget(self.widget)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_3.addWidget(self.widget_6)
        self.uleft3 = QtWidgets.QWidget(self.widget)
        self.uleft3.setObjectName("uleft3")
        self.horizontalLayout_3.addWidget(self.uleft3)
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout.addWidget(self.upperleft)
        self.upperright = QtWidgets.QWidget(self.upperpane)
        self.upperright.setObjectName("upperright")
        self.label_3 = QtWidgets.QLabel(self.upperright)
        self.label_3.setGeometry(QtCore.QRect(40, 20, 241, 101))
        font = QtGui.QFont()
        font.setFamily("Colonna MT")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("\n"
"font: 48pt \"Colonna MT\";\n"
"color:rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.upperright)
        self.label_4.setGeometry(QtCore.QRect(30, 120, 211, 51))
        self.label_4.setStyleSheet("color:rgb(255, 255, 255);\n"
"font: 26pt \"Bradley Hand ITC\";")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.upperright)
        self.verticalLayout.addWidget(self.upperpane)
        self.lowerpane = QtWidgets.QWidget(self.centralwidget)
        self.lowerpane.setObjectName("lowerpane")
        self.label = QtWidgets.QLabel(self.lowerpane)
        self.label.setGeometry(QtCore.QRect(160, 80, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.lowerpane)
        self.label_2.setGeometry(QtCore.QRect(160, 110, 47, 13))
        self.label_2.setObjectName("label_2")
        self.user_login_input = QtWidgets.QLineEdit(self.lowerpane)
        self.user_login_input.setGeometry(QtCore.QRect(300, 70, 141, 20))
        self.user_login_input.setObjectName("user_login_input")
        self.password_login_input = QtWidgets.QLineEdit(self.lowerpane)
        self.password_login_input.setGeometry(QtCore.QRect(300, 100, 141, 20))
        self.password_login_input.setObjectName("password_login_input")
        self.password_login_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton(self.lowerpane)
        self.login_button.setGeometry(QtCore.QRect(300, 140, 75, 23))
        self.login_button.setObjectName("login_button")
        # self.admin_login_label = QtWidgets.QLabel(self.lowerpane)
        self.admin_login_label = ClickableLabel(MainWindow)
        self.admin_login_label.setGeometry(QtCore.QRect(320, 530, 81, 16))
        self.admin_login_label.setObjectName("admin_login_label")
        self.verticalLayout.addWidget(self.lowerpane)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Peter"))
        self.label_4.setText(_translate("MainWindow", "Point of Stock System"))
        self.label.setText(_translate("MainWindow", "Username"))
        self.label_2.setText(_translate("MainWindow", "Password"))
        self.login_button.setText(_translate("MainWindow", "Login"))
        self.admin_login_label.setText(_translate("MainWindow", "Login as Admin"))

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()
