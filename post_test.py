import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView

class CitizenInputWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New citizen")
        self.setGeometry(700, 300, 250, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()

        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()

        self.insert_button = QPushButton("Insert")
        self.view_button = QPushButton("View Citizens")  # Add the view button

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.city_label)
        self.layout.addWidget(self.city_input)
        self.layout.addWidget(self.insert_button)
        self.layout.addWidget(self.view_button)  # Add the view button to the layout

        self.insert_button.clicked.connect(self.insert_data)
        self.view_button.clicked.connect(self.view_citizen_data)  # Connect the view button

        self.central_widget.setLayout(self.layout)

    def insert_data(self):
        name = self.name_input.text()
        age = self.age_input.text()
        city = self.city_input.text()

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="admin",
        )

        cur = conn.cursor()

        insert_query = """
        INSERT INTO citizen (name, age, city)
        VALUES (%s, %s, %s)
        """

        citizen_data = (name, age, city)

        try:
            cur.execute(insert_query, citizen_data)
            conn.commit()
            print("Citizen added successfully.")
            
            self.name_input.clear()
            self.age_input.clear()
            self.city_input.clear()

        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")

        cur.close()
        conn.close()

    def view_citizen_data(self):
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="admin",
        )

        cur = conn.cursor()

        select_query = "SELECT * FROM citizen"

        try:
            cur.execute(select_query)
            results = cur.fetchall()

            if len(results) == 0:
                print("No data found in the 'citizen' table.")
            else:
                data_str = "Index, Name, Age, City\n"
                for row in results:
                    data_str += ", ".join(map(str, row)) + "\n"

                # Create and show the CitizenDataWindow with the data
                self.citizen_data_window = CitizenDataWindow(data_str)
                self.citizen_data_window.show()

        except Exception as e:
            print(f"Error: {e}")

        cur.close()
        conn.close()

class CitizenDataWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Citizen Data")
        self.setGeometry(700, 300, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.data_label = QLabel("Citizen Data:")
        self.search_label = QLabel("Search by Name:")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.table_widget = QTableWidget()

        self.layout.addWidget(self.data_label)
        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.table_widget)

        self.central_widget.setLayout(self.layout)

        # Connect the search button to the search function
        self.search_button.clicked.connect(self.search_by_name)

        # Display the data
        self.display_data(data)

    def display_data(self, data):
        rows = data.strip().split("\n")
        headers = ["Index", "Name", "Age", "City"]  # Column headers
        self.data_rows = [row.strip().split(", ") for row in rows[1:]]  # Exclude header row

        self.table_widget.setRowCount(len(self.data_rows))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(self.data_rows):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                self.table_widget.setItem(row_index, col_index, item)

        # Automatically adjust column widths to fit content
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def search_by_name(self):
        search_name = self.search_input.text()
        if not search_name:
            return  # Don't perform a search if the search input is empty

        # Filter the data based on the search_name
        filtered_data = [row for row in self.data_rows if search_name in row[1]]  # row[1]] - 2nd element of column, name

        # Update the table with the filtered data
        self.display_data("Index, Name, Age, City\n" + "\n".join([", ".join(row) for row in filtered_data]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CitizenInputWindow()
    window.show()
    sys.exit(app.exec_())
