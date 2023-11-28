from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class PatientDetails(QDialog):
    def __init__(self, name):
        super().__init__()

        self.setWindowTitle("Details")
        self.setFixedSize(300, 100)

        layout = QVBoxLayout()

        name_label = QLabel(f"Name: {name}")
        layout.addWidget(name_label)

        self.setLayout(layout)
