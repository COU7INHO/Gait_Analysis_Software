import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFrame, \
    QDialog, QLabel, QLineEdit, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem
import psycopg2


class AmputeeAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Amputee Analyzer')
        self.setFixedSize(300, 150)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()

        search_button = QPushButton('Search Amputee', self)
        search_button.clicked.connect(self.access_patients)

        add_button = QPushButton('Add Amputee', self)
        add_button.clicked.connect(self.add_patient)

        top_layout.addWidget(search_button)
        top_layout.addWidget(add_button)

        main_layout.addLayout(top_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        analysis_layout = QHBoxLayout()
        start_analysis_button = QPushButton('Start Analysis', self)
        analysis_layout.addWidget(start_analysis_button)
        main_layout.addLayout(analysis_layout)

    def add_patient(self):
        dialog = PatientInfoDialog()
        dialog.exec_()

    def access_patients(self):
        dialog = AccessPatients()
        dialog.exec()

class PatientInfoDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Patient Information')
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        name_label = QLabel('Name:')
        self.name_edit = QLineEdit()

        age_label = QLabel('Age:')
        self.age_spinbox = QSpinBox()

        amputation_level_label = QLabel('Amputation Level:')
        self.amputation_level_combo = QComboBox()
        self.amputation_level_combo.addItem('Transtibial')
        self.amputation_level_combo.addItem('Transfemoral')

        amputated_limb_label = QLabel('Amputated Limb:')
        self.amputated_limb_combo = QComboBox()
        self.amputated_limb_combo.addItem('Right')
        self.amputated_limb_combo.addItem('Left')

        phone_label = QLabel('Phone Number:')
        self.phone_edit = QLineEdit()

        address_label = QLabel('Address:')
        self.address_edit = QLineEdit()

        zip_code_label = QLabel('Zip Code:')
        self.zip_code_edit = QLineEdit()

        district_label = QLabel('District:')
        self.district_edit = QComboBox()
        portugal_districts = [
            'Aveiro', 'Beja', 'Braga', 'Bragança', 'Castelo Branco', 'Coimbra', 'Evora', 'Faro',
            'Guarda', 'Leiria', 'Lisboa', 'Portalegre', 'Porto', 'Santarém', 'Setúbal', 'Viana do Castelo',
            'Vila Real', 'Viseu', 'Açores', 'Madeira'
        ]

        for district in sorted(portugal_districts):
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

        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="admin"
            )

            cursor = conn.cursor()

            insert_query = ("INSERT INTO patient \
                            (name, age, amputation_level, amputated_limb, phone, address, zip_code, district) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            data_to_insert = (
                self.name_edit.text(),
                self.age_spinbox.value(),
                self.amputation_level_combo.currentText(),
                self.amputated_limb_combo.currentText(),
                self.phone_edit.text(),
                self.address_edit.text(),
                self.zip_code_edit.text(),
                self.district_edit.currentText()
            )

            cursor.execute(insert_query, data_to_insert)
            conn.commit()
            cursor.close()
            conn.close()
            self.accept()
        except Exception:
            print("Error")

class AccessPatients(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Patient Information')
        self.setFixedSize(1000, 400)

        layout = QVBoxLayout()

        self.tableWidget = QTableWidget(self)
        layout.addWidget(self.tableWidget)

        self.display_data()
        self.setLayout(layout)

        self.display_data()

    def display_data(self):
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="admin"
            )
            
            cursor = conn.cursor()

            query = "SELECT * FROM patient;"
            cursor.execute(query)

            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(len(cursor.description))
            headers = [desc[0] for desc in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(headers)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()

        except Exception as e:
            print("Error:", str(e))


def main():
    app = QApplication(sys.argv)
    ex = AmputeeAnalyzer()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
