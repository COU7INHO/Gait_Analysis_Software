"""
NewPatient GUI Module

This module defines a PyQt5-based graphical user interface (GUI) for adding new patient information.
It includes input fields for name, age, amputation level, amputated limb, phone number, address, zip code, and district.

Dependencies:
- PyQt5.QtWidgets: For creating the graphical user interface.
- gui.conn_to_db: Module providing a function for connecting to a database.

Classes:
- NewPatient: A QDialog class for entering and adding new patient information.

Usage:
- Instantiate the NewPatient class to display the GUI for adding a new patient.
- Users can input the patient's information and click the "Add patient" button to add the information to the database.
- The script connects to a PostgreSQL database using the connect_to_database function from gui.conn_to_db module.
- Successfully added patients result in an information QMessageBox, while errors are shown in a critical QMessageBox.

Note: Ensure the necessary dependencies are installed before running the script.
"""

from gui.conn_to_db import connect_to_database
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)


class NewPatient(QDialog):
    def __init__(self):
        """
        Initialize NewPatient GUI.
        """
        super().__init__()

        self.conn, self.cursor = connect_to_database()
        self.initUI()

    def initUI(self):
        """
        Set up the GUI layout and components.
        """
        self.setWindowTitle("Patient Information")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()

        age_label = QLabel("Age:")
        self.age_spinbox = QSpinBox()

        amputation_level_label = QLabel("Amputation Level:")
        self.amputation_level_combo = QComboBox()
        self.amputation_level_combo.addItem("Transtibial")
        self.amputation_level_combo.addItem("Transfemoral")

        amputated_limb_label = QLabel("Amputated Limb:")
        self.amputated_limb_combo = QComboBox()
        self.amputated_limb_combo.addItem("Right")
        self.amputated_limb_combo.addItem("Left")

        phone_label = QLabel("Phone Number:")
        self.phone_edit = QLineEdit()

        address_label = QLabel("Address:")
        self.address_edit = QLineEdit()

        zip_code_label = QLabel("Zip Code:")
        self.zip_code_edit = QLineEdit()

        district_label = QLabel("District:")
        self.district_edit = QComboBox()
        self.portugal_districts = [
            "Aveiro",
            "Beja",
            "Braga",
            "Bragança",
            "Castelo Branco",
            "Coimbra",
            "Evora",
            "Faro",
            "Guarda",
            "Leiria",
            "Lisboa",
            "Portalegre",
            "Porto",
            "Santarém",
            "Setúbal",
            "Viana do Castelo",
            "Vila Real",
            "Viseu",
            "Açores",
            "Madeira",
        ]

        for district in sorted(self.portugal_districts):
            self.district_edit.addItem(district)

        self.add_patient_button = QPushButton("Add patient")
        self.add_patient_button.clicked.connect(self.info_to_db)

        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(age_label)
        layout.addWidget(self.age_spinbox)
        layout.addWidget(amputation_level_label)
        layout.addWidget(self.amputation_level_combo)
        layout.addWidget(amputated_limb_label)
        layout.addWidget(self.amputated_limb_combo)
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_edit)
        layout.addWidget(address_label)
        layout.addWidget(self.address_edit)
        layout.addWidget(zip_code_label)
        layout.addWidget(self.zip_code_edit)
        layout.addWidget(district_label)
        layout.addWidget(self.district_edit)
        layout.addWidget(self.add_patient_button)

        self.setLayout(layout)

    def info_to_db(self):
        """
        Add the entered patient information to the database.
        """
        try:
            insert_query = "INSERT INTO patient \
                            (name, age, amputation_level, amputated_limb, phone, address, zip_code, district) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            data_to_insert = (
                self.name_edit.text(),
                self.age_spinbox.value(),
                self.amputation_level_combo.currentText(),
                self.amputated_limb_combo.currentText(),
                self.phone_edit.text(),
                self.address_edit.text(),
                self.zip_code_edit.text(),
                self.district_edit.currentText(),
            )

            self.cursor.execute(insert_query, data_to_insert)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(self, "Success", "Person added to the database!")
            self.accept()
        except Exception:
            QMessageBox.critical(self, "Error")
