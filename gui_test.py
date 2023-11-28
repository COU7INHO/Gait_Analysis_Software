from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class PatientDetails(QDialog):
    def __init__(
        self,
        name,
        age,
        amputation_level,
        amputated_limb,
        phone,
        address,
        zip_code,
        district,
    ):
        super().__init__()

        self.setWindowTitle("Details")
        self.setMinimumSize(300, 100)

        layout = QVBoxLayout()

        name_level_layout = QHBoxLayout()

        name_label = QLabel(f"Name: {name}")
        level_label = QLabel(f"Level of Amputation: {amputation_level}")
        name_level_layout.addWidget(name_label)
        name_level_layout.addWidget(level_label)

        details_groupbox = QGroupBox("See More Details")
        details_layout = QVBoxLayout()

        age_label = QLabel(f"Age: {age}")
        amputated_limb_label = QLabel(f"Amputated Limb: {amputated_limb}")
        phone_label = QLabel(f"Phone Number: {phone}")
        address_label = QLabel(f"Address: {address}")
        zip_code_label = QLabel(f"Zip Code: {zip_code}")
        district_label = QLabel(f"District: {district}")

        # Initially hide the additional details
        age_label.hide()
        amputated_limb_label.hide()
        phone_label.hide()
        address_label.hide()
        zip_code_label.hide()
        district_label.hide()

        # Toggle button to show/hide additional details
        toggle_button = QPushButton("Show More")
        toggle_button.setCheckable(True)
        toggle_button.clicked.connect(
            lambda: self.toggle_details(
                toggle_button,
                [
                    age_label,
                    amputated_limb_label,
                    phone_label,
                    address_label,
                    zip_code_label,
                    district_label,
                ],
            )
        )

        details_layout.addLayout(name_level_layout)
        details_layout.addWidget(age_label)
        details_layout.addWidget(amputated_limb_label)
        details_layout.addWidget(phone_label)
        details_layout.addWidget(address_label)
        details_layout.addWidget(zip_code_label)
        details_layout.addWidget(district_label)
        details_layout.addWidget(toggle_button)

        details_groupbox.setLayout(details_layout)
        layout.addWidget(details_groupbox)
        self.setLayout(layout)

    def toggle_details(self, button, labels):
        if button.isChecked():
            button.setText("Show Less")
            for label in labels:
                label.show()
        else:
            button.setText("Show More")
            for label in labels:
                label.hide()


# Example usage:
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    details_dialog = PatientDetails(
        "John Doe",
        35,
        "Below Knee",
        "Left Leg",
        "1234567890",
        "123 Main St",
        "12345",
        "Sample District",
    )
    details_dialog.show()
    sys.exit(app.exec_())
