import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from conn_to_db import connect_to_database
from main2 import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout


class PatientDetails(QDialog):
    def __init__(self, patient_details):
        super().__init__()

        self.conn, self.cur = connect_to_database()

        self.setWindowTitle("Details")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        labels = {
            "Name": patient_details.get("name", "N/A"),
            "Age": patient_details.get("age", "N/A"),
            "Amputation Level": patient_details.get("amputation_level", "N/A"),
            "Amputated Limb": patient_details.get("amputated_limb", "N/A"),
            "Phone Number": patient_details.get("phone_number", "N/A"),
            "Address": patient_details.get("address", "N/A"),
            "Zip Code": patient_details.get("zip_code", "N/A"),
            "District": patient_details.get("district", "N/A"),
        }

        self.patient_info = []

        for label, value in labels.items():
            label_widget = QLabel(f"<b>{label}:</b> {value}")

            if label == "Name":
                label_widget = QLabel(f"{value}")
                label_widget.setAlignment(Qt.AlignCenter)
                label_widget.setStyleSheet("font-size: 18px")
                name = value
                self.patient_info.append(name)
            elif label == "Amputation Level":
                amputation_level = value
                self.patient_info.append(amputation_level)
            elif label == "Amputated Limb":
                amputated_limb = value
                self.patient_info.append(amputated_limb)
            layout.addWidget(label_widget)

        self.init_analysis_btn = QPushButton("Start analysis")
        self.init_analysis_btn.clicked.connect(self.start_main_window)
        layout.addWidget(self.init_analysis_btn)

        self.delete_patient_btn = QPushButton("Delete patient")
        self.delete_patient_btn.clicked.connect(self.delete_patient)
        layout.addWidget(self.delete_patient_btn)

        self.setLayout(layout)

    def start_main_window(self):
        self.main_window = MainWindow(self.patient_info)
        self.main_window.on_submit()
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
                query = "DELETE FROM patient WHERE name = %s"
                name = self.patient_info[
                    0
                ]  # Assuming name is the first element in patient_info
                self.cur.execute(query, (name,))
                self.conn.commit()
            except psycopg2.Error as e:
                QMessageBox.warning(None, "Error", str(e))
            finally:
                self.cur.close()
                self.conn.close()
        else:
            print("Deletion cancelled")
        self.close()
