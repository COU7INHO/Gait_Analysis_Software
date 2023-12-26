import psycopg2
from conn_to_db import connect_to_database
from NewPatient import NewPatient
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


class EditPatientInfo(QDialog):
    def __init__(self, patient_info):
        super().__init__()
        self.conn, self.cur = connect_to_database()

        self.patient_info = patient_info
        self.patient_id = self.patient_info[0][1]
        self.setWindowTitle("Edit Information")
        self.setFixedSize(400, 500)
        new_patient = NewPatient()

        layout = QVBoxLayout()
        self.widgets = {}  # Store created widgets for later use

        # Define widget types for each field
        field_types = {
            "name": QLineEdit,
            "age": QSpinBox,
            "amputation_level": QComboBox,
            "amputated_limb": QComboBox,
            "phone": QLineEdit,
            "address": QLineEdit,
            "zip_code": QLineEdit,
            "district": QComboBox,
        }

        for field, value in self.patient_info:
            label = QLabel(field + ":")
            layout.addWidget(label)

            if field in field_types:
                widget_type = field_types[field]
                widget = widget_type()

                if field == "district":
                    widget.addItems(new_patient.portugal_districts)
                else:
                    if field == "amputation_level":
                        widget.addItems(["Transfemoral", "Transtibial"])
                    elif field == "amputated_limb":
                        widget.addItems(["Right", "Left"])

                    if isinstance(widget, QComboBox):
                        index = widget.findText(str(value))
                        if index != -1:  # Check if the text exists in the combobox
                            widget.setCurrentIndex(index)
                    elif isinstance(widget, QSpinBox):
                        widget.setValue(int(value))
                    else:
                        widget.setText(str(value))

                layout.addWidget(widget)
                self.widgets[field] = widget  # Store the widget for later use

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_information)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_information(self):
        updated_values = {}
        for field, widget in self.widgets.items():
            if isinstance(widget, QLineEdit):
                updated_values[field] = widget.text()
            elif isinstance(widget, QSpinBox):
                updated_values[field] = widget.value()
            elif isinstance(widget, QComboBox):
                updated_values[field] = widget.currentText()

        try:
            confirmation = QMessageBox.question(
                self,
                "Confirmation",
                "Save changes?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if confirmation:
                set_clause_parts = [f"{key} = %s" for key in updated_values.keys()]
                set_clause = ", ".join(set_clause_parts)
                query = f"UPDATE patient SET {set_clause} WHERE id = %s"

                # Construct the parameter list for the query
                params = list(updated_values.values())
                params.append(self.patient_id)

                self.conn, self.cur = connect_to_database()
                self.cur.execute(query, params)

                self.conn.commit()

        except psycopg2.Error as e:
            print("Database Error:", e)
            QMessageBox.warning(None, "Error", str(e))
        finally:
            self.cur.close()
            self.conn.close()
            self.close()
