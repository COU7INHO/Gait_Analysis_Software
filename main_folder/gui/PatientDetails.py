import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from conn_to_db import connect_to_database
from EditPatient import EditPatientInfo

# from EditPatient import EditPatientInfo
from main2 import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout


class PatientDetails(QDialog):
    def __init__(self, patient_details):
        super().__init__()

        self.patient_details = patient_details
        self.details_gui()

    def details_gui(self):
        self.conn, self.cur = connect_to_database()

        self.setWindowTitle("Details")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        labels = {
            "name": self.patient_details.get("name", "N/A"),
            "age": self.patient_details.get("age", "N/A"),
            "amputation_level": self.patient_details.get("amputation_level", "N/A"),
            "amputated_limb": self.patient_details.get("amputated_limb", "N/A"),
            "phone": self.patient_details.get("phone_number", "N/A"),
            "address": self.patient_details.get("address", "N/A"),
            "zip_code": self.patient_details.get("zip_code", "N/A"),
            "district": self.patient_details.get("district", "N/A"),
        }

        self.patient_id = self.patient_details.get("id", "N/A")
        self.patient_info = []
        self.patient_info_all = []
        self.patient_info_all.append(("id", self.patient_id))

        for label, value in labels.items():
            label_widget = QLabel(f"<b>{label}:</b> {value}")
            self.patient_info_all.append((label, value))

            if label == "name":
                label_widget = QLabel(f"{value}")
                label_widget.setAlignment(Qt.AlignCenter)
                label_widget.setStyleSheet("font-size: 18px")
                name = value
                self.patient_info.append(name)
            elif label == "amputation_level":
                amputation_level = value
                self.patient_info.append(amputation_level)
            elif label == "amputated_limb":
                amputated_limb = value
                self.patient_info.append(amputated_limb)
            layout.addWidget(label_widget)

        self.init_analysis_btn = QPushButton("Start analysis")
        self.init_analysis_btn.clicked.connect(self.start_main_window)
        layout.addWidget(self.init_analysis_btn)

        self.edit_information_btn = QPushButton("Edit information")
        self.edit_information_btn.clicked.connect(self.edit_information)
        layout.addWidget(self.edit_information_btn)

        self.delete_patient_btn = QPushButton("Delete patient")
        self.delete_patient_btn.clicked.connect(self.delete_patient)
        layout.addWidget(self.delete_patient_btn)

        self.setLayout(layout)

    def start_main_window(self):
        self.main_window = MainWindow(self.patient_info)
        self.main_window.on_submit()
        self.close()

    def edit_information(self):
        edit_window = EditPatientInfo(self.patient_info_all)
        edit_window.exec_()
        self.close()

    def delete_patient(self):
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this patient?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            try:
                query = "DELETE FROM patient WHERE id = %s"

                self.cur.execute(query, (self.patient_id,))
                self.conn.commit()
            except psycopg2.Error as e:
                QMessageBox.warning(None, "Error", str(e))
            finally:
                self.cur.close()
                self.conn.close()
        else:
            print("Deletion cancelled")
        self.close()
