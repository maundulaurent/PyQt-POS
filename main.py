import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import POSSystem

def main():
    app = QApplication(sys.argv)
    pos_system = POSSystem()
    pos_system.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
