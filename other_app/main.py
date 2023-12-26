import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QComboBox
)
from PyQt5.QtCore import Qt
from connect_to_db import connect_to_database
from details_window import JobDetailsWindow
from new_job_application_window import NewJobApplicationWindow
from statistics_window import StatisticsWindow


class JobApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Job Application Management")
        self.setFixedSize(820, 500)

        self.conn, self.cur = connect_to_database()

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Filter layout
        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        # Create filter widgets
        self.country_filter = self.create_filter("Country", "SELECT DISTINCT country FROM Job_Application ORDER BY country", filter_layout)
        self.company_filter = self.create_filter("Company", "SELECT DISTINCT company FROM Job_Application ORDER BY company", filter_layout)
        self.status_filter = self.create_filter("Application Status", "SELECT DISTINCT application_status FROM Job_Application", filter_layout)

        # Horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        # Button for "Statistics"
        btn_statistics = QPushButton("Statistics")
        btn_statistics.clicked.connect(self.show_statistics)
        buttons_layout.addWidget(btn_statistics)

        # Button for "New job application"
        btn_new_application = QPushButton("New job application")
        btn_new_application.clicked.connect(self.open_new_application_window)
        buttons_layout.addWidget(btn_new_application)

        # Table to display database rows
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Establish database connection and fetch initial data
        self.refresh_filters()  # Initial population of filters
        self.fetch_data_and_display()

    def create_filter(self, label_text, query, layout):
        label = QLabel(label_text + ":")
        combo_box = QComboBox()
        combo_box.addItem("All")
        combo_box.setCurrentIndex(0)

        self.cur.execute(query)
        data = self.cur.fetchall()
        for item in data:
            combo_box.addItem(item[0])

        combo_box.currentIndexChanged.connect(self.fetch_data_and_display)
        layout.addWidget(label)
        layout.addWidget(combo_box)
        return combo_box

    def fetch_data_and_display(self):
        country_filter = self.country_filter.currentText() if self.country_filter.currentIndex() != 0 else ""
        company_filter = self.company_filter.currentText() if self.company_filter.currentIndex() != 0 else ""
        status_filter = self.status_filter.currentText() if self.status_filter.currentIndex() != 0 else ""

        query = f"SELECT * FROM Job_Application WHERE country LIKE '%{country_filter}%' AND company LIKE '%{company_filter}%' AND application_status LIKE '%{status_filter}%'"

        self.cur.execute(query)
        rows = self.cur.fetchall()

        col_names = [desc[0] for desc in self.cur.description]

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(col_names) + 1)
        self.table_widget.setHorizontalHeaderLabels(col_names + ["Actions"])

        for i, row in enumerate(rows):
            self.table_widget.insertRow(i)
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                self.table_widget.setItem(i, j, item)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            btn_view = QPushButton("View Details")
            btn_view.clicked.connect(lambda checked, row=i: self.open_details_window(row, col_names, rows))
            self.table_widget.setCellWidget(i, len(col_names), btn_view)
        
        self.table_widget.setColumnHidden(0, True)
        self.table_widget.setColumnHidden(5, True)

        self.table_widget.setColumnWidth(1, 150)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 200)
        self.table_widget.setColumnWidth(4, 200)

    def show_statistics(self):
        stats_window = StatisticsWindow(self.conn, self.cur)
        stats_window.exec_()

    def open_new_application_window(self):
        new_job_application = NewJobApplicationWindow()
        new_job_application.exec_()
        self.refresh_filters()  # Refresh filters after adding a new job application
        self.refresh_window() 

    def open_details_window(self, row, col_names, rows):
        data = {}
        selected_row = rows[row]
        for i, value in enumerate(selected_row):
            data[col_names[i]] = value

        details_window = JobDetailsWindow(data)
        details_window.exec_()
        self.refresh_window()  

    def refresh_filters(self):
        # Clear and repopulate the Country, Company, and Application Status filters
        self.populate_filter(self.country_filter, "SELECT DISTINCT country FROM Job_Application ORDER BY country")
        self.populate_filter(self.company_filter, "SELECT DISTINCT company FROM Job_Application ORDER BY company")
        self.populate_filter(self.status_filter, "SELECT DISTINCT application_status FROM Job_Application")

    def populate_filter(self, filter_widget, query):
        filter_widget.clear()
        filter_widget.addItem("All")
        self.cur.execute(query)
        data = self.cur.fetchall()
        for item in data:
            filter_widget.addItem(item[0])

    def refresh_window(self):
        self.table_widget.clearContents()
        self.fetch_data_and_display()

    def closeEvent(self, event):
        self.cur.close()
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobApplicationWindow()
    window.show()
    sys.exit(app.exec_())
