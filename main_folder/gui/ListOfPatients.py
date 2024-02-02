"""
ListOfPatients GUI Module

This module defines a PyQt5-based graphical user interface (GUI) for displaying and filtering a list of patients.
It includes functionality for filtering patients based on name and district, displaying patient details, and updating the displayed data.

Dependencies:
- psycopg2: For PostgreSQL database interaction.
- PyQt5.QtCore: For Qt core functionality.
- PyQt5.QtWidgets: For creating the graphical user interface.

Classes:
- ListOfPatients: A QDialog class for displaying and filtering a list of patients.

Usage:
- Instantiate the ListOfPatients class to display the patient list GUI.
- Users can filter patients by entering text in the "Name" and "District" fields and clicking the "Filter" button.
- The GUI includes a table displaying patient information with a "Details" button for each patient.
- Clicking the "Details" button opens a PatientDetails window with additional patient information.
- The script connects to a PostgreSQL database using psycopg2 and updates the displayed data based on user interactions.

Note: Ensure the necessary dependencies are installed before running the script.
"""

import psycopg2
from gui.conn_to_db import connect_to_database
from gui.PatientDetails import PatientDetails
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class ListOfPatients(QDialog):
    def __init__(self):
        """
        Initialize ListOfPatients GUI.
        """
        super().__init__()

        self.setWindowTitle("Patient Information")
        self.setFixedSize(560, 450)

        self.conn, self.cur = connect_to_database()

        layout = QVBoxLayout()

        self.name_filter = QLineEdit()
        self.district_filter = QLineEdit()

        filter_patient = [
            ("Name:", self.name_filter),
            ("District:", self.district_filter),
        ]

        filter_layout = QHBoxLayout()

        for label, widget in filter_patient:
            label_widget = QLabel(label)
            filter_layout.addWidget(label_widget)
            filter_layout.addWidget(widget)

        filter_btn = QPushButton("Filter")
        filter_layout.addWidget(filter_btn)
        filter_btn.clicked.connect(self.filter_patient)

        layout.addLayout(filter_layout)

        self.tableWidget = QTableWidget(self)
        layout.addWidget(self.tableWidget)

        self.display_data()
        self.setLayout(layout)

    def filter_patient(self):
        """
        Filter patients based on user-entered criteria.
        """
        name_filter = self.name_filter.text()
        district_filter = self.district_filter.text()
        query = "SELECT name, amputation_level, district FROM patient WHERE name LIKE %s AND district LIKE %s ORDER by name;"

        try:
            self.cur.execute(
                query, ("%" + name_filter + "%", "%" + district_filter + "%")
            )
            rows = self.cur.fetchall()
            self.update_table_widget(rows)
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)

    def display_data(self):
        """
        Display patient information in the table.
        """
        query = "SELECT name, amputation_level, district FROM patient ORDER BY name;"

        self.cur.execute(query)

        rows = self.cur.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(
            len(self.cur.description) + 1
        )  # +1 for button column
        headers = [desc[0] for desc in self.cur.description]
        headers.append("Details")
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(
                    item.flags() ^ Qt.ItemIsEditable
                )  # Make the item non-editable
                self.tableWidget.setItem(i, j, item)

            self.tableWidget.setColumnWidth(len(headers) - 1, 100)
            self.tableWidget.setColumnWidth(0, 200)

            btn = QPushButton("Details", self)
            btn.clicked.connect(lambda _, index=i: self.show_details_window(index))
            self.tableWidget.setCellWidget(
                i, len(headers) - 1, btn
            )  # Set button in the last column
            btn.setFocusPolicy(Qt.NoFocus)

    def update_after_delete(self):
        """
        Update the table after deleting a patient.
        """
        self.tableWidget.clearContents()
        self.display_data()

    def update_table_widget(self, rows):
        """
        Update the table widget with new data.
        """
        self.tableWidget.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)

            btn = QPushButton("Details", self)
            btn.clicked.connect(lambda _, index=i: self.show_details_window(i))
            self.tableWidget.setCellWidget(i, len(row), btn)
            self.tableWidget.setColumnWidth(len(row), 100)  # Adjust button column width

    def show_details_window(self, index):
        """
        Show the details window for a selected patient.
        """
        self.close()

        name = self.tableWidget.item(index, 0).text()

        try:
            self.cur.execute(
                "SELECT age, amputation_level, amputated_limb, phone, address, zip_code, district, id FROM patient WHERE name = %s;",
                (name,),
            )
            patient_details = self.cur.fetchone()

            details_dict = {
                "name": name,
                "age": patient_details[0] if patient_details else "N/A",
                "amputation_level": patient_details[1] if patient_details else "N/A",
                "amputated_limb": patient_details[2] if patient_details else "N/A",
                "phone_number": patient_details[3] if patient_details else "N/A",
                "address": patient_details[4] if patient_details else "N/A",
                "zip_code": patient_details[5] if patient_details else "N/A",
                "district": patient_details[6] if patient_details else "N/A",
                "id": patient_details[7] if patient_details else "N/A",
            }

            details_window = PatientDetails(details_dict)
            details_window.exec_()

        except psycopg2.Error as e:
            QMessageBox.critical("Error fetching additional data:", e)
        self.update_after_delete()
