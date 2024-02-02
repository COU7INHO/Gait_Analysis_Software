"""
InitialWindow GUI Module

This module defines a PyQt5-based graphical user interface (GUI) for the initial window of a Gait analysis application.
It provides options to search for existing amputee patients and add a new amputee to the database.

Dependencies:
- PyQt5.QtWidgets: For creating the graphical user interface.
- gui.ListOfPatients: Module providing the ListOfPatients class for displaying a list of patients.
- gui.NewPatient: Module providing the NewPatient class for adding a new patient.

Classes:
- InitialWindow: A QMainWindow class for the initial window of the Gait analysis application.

Usage:
- Instantiate the InitialWindow class to display the initial GUI.
- Users can click the "Search Amputee" button to access a list of existing patients (ListOfPatients).
- Clicking the "Add Amputee" button opens a dialog for adding a new patient (NewPatient).
- The script sets up the main window layout with buttons and connects them to corresponding functions.

Note: Ensure the necessary dependencies are installed before running the script.
"""

import sys

from gui.ListOfPatients import ListOfPatients
from gui.NewPatient import NewPatient
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class InitialWindow(QMainWindow):
    def __init__(self):
        """
        Initialize InitialWindow GUI.
        """
        super().__init__()

        self.setWindowTitle("Welcome - Gait analysis")
        self.setFixedSize(300, 100)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()

        search_button = QPushButton("Search Amputee", self)
        search_button.clicked.connect(self.access_patients)

        add_button = QPushButton("Add Amputee", self)
        add_button.clicked.connect(self.add_patient)

        top_layout.addWidget(search_button)
        top_layout.addWidget(add_button)

        main_layout.addLayout(top_layout)

    def add_patient(self):
        """
        Open the NewPatient dialog for adding a new patient.
        """
        dialog = NewPatient()
        dialog.exec_()

    def access_patients(self):
        """
        Open the ListOfPatients dialog for accessing existing patients.
        """
        dialog = ListOfPatients()
        dialog.exec_()


def main():
    """
    Entry point for the Gait analysis application.
    """
    app = QApplication(sys.argv)
    ex = InitialWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
