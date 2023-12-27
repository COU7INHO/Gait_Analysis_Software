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
        super().__init__()

        self.setWindowTitle("Amputee Analyzer")
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
        dialog = NewPatient()
        dialog.exec_()

    def access_patients(self):
        dialog = ListOfPatients()
        dialog.exec_()


def main():
    app = QApplication(sys.argv)
    ex = InitialWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
