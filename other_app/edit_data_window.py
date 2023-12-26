import pycountry
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class EditJobApplicationWindow(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Edit Job Application")
        self.setFixedSize(400, 300)

        self.data = data
        self.updated_data = None

        layout = QVBoxLayout(self)

        # Country field
        self.country_input = QComboBox()
        countries = list(map(lambda x: x.name, list(pycountry.countries)))
        self.country_input.addItems(countries)
        self.country_input.setCurrentText(self.data.get("country"))
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country_input)

        # Application Status field with predefined options
        self.status_input = QComboBox()
        self.status_input.addItems(["No Response", "Rejected", "Interview"])
        self.status_input.setCurrentText(self.data.get("application_status"))
        layout.addWidget(QLabel("Application Status:"))
        layout.addWidget(self.status_input)

        # Other input fields
        self.company_input = QLineEdit()
        self.company_input.setText(self.data.get("company"))
        layout.addWidget(QLabel("Company:"))
        layout.addWidget(self.company_input)

        self.role_input = QLineEdit()
        self.role_input.setText(self.data.get("job_role"))
        layout.addWidget(QLabel("Job Role:"))
        layout.addWidget(self.role_input)

        self.link_input = QLineEdit()
        self.link_input.setText(self.data.get("application_link"))
        layout.addWidget(QLabel("Application Link:"))
        layout.addWidget(self.link_input)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_data)
        layout.addWidget(update_button)

    def update_data(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to update this application?")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.No)

        response = confirm_dialog.exec_()

        if response == QMessageBox.Yes:
            self.updated_data = {
                "country": self.country_input.currentText(),
                "application_status": self.status_input.currentText(),
                "company": self.company_input.text(),
                "job_role": self.role_input.text(),
                "application_link": self.link_input.text(),
                "application_id": self.data.get("application_id"),
            }

            self.accept()

    def get_updated_data(self):
        return self.updated_data
