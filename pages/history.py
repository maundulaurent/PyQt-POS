import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout


class HistoryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        self.setLayout(layout)

    def update_history(self, history_entries):
        self.history_list.clear()
        for entry in history_entries:
            item_text = f"{entry[0]} - {entry[1]}: {entry[2]}"
            item = QListWidgetItem(item_text)
            self.history_list.addItem(item)


class HistoryManager(QWidget):
    def __init__(self, parent=None, db_path='products.db'):
        super().__init__(parent)
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_db()

        self.history_widget = HistoryWidget(self)

    def init_db(self):
        # Create history table if it does not exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        event_type TEXT NOT NULL,
                        details TEXT)''')
        self.conn.commit()

    def record_history(self, event_type, details):
        self.cursor.execute("INSERT INTO history (event_type, details) VALUES (?, ?)", (event_type, details))
        self.conn.commit()

    def fetch_history(self):
        self.cursor.execute("SELECT timestamp, event_type, details FROM history ORDER BY timestamp DESC")
        history_entries = self.cursor.fetchall()
        return history_entries

    def close_connection(self):
        self.conn.close()
