from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from connect_to_db import connect_to_database
import pycountry

class NewJobApplicationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Job Application")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        # Country Field
        country_layout = QHBoxLayout()
        country_label = QLabel("Country:")
        self.country_combobox = QComboBox()
        self.populate_countries()  # Populate the combo box with countries
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_combobox)
        layout.addLayout(country_layout)

        # Application Status Field (ComboBox)
        status_layout = QHBoxLayout()
        status_label = QLabel("Application Status:")
        self.status_combobox = QComboBox()
        self.status_combobox.addItems(["No Response", "Rejected", "Interview"])
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_combobox)
        layout.addLayout(status_layout)

        # Company Name Field
        company_layout = QHBoxLayout()
        company_label = QLabel("Company:")
        self.company_lineedit = QLineEdit()
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_lineedit)
        layout.addLayout(company_layout)

        # Job Role Field
        job_role_layout = QHBoxLayout()
        job_role_label = QLabel("Job Role:")
        self.job_role_lineedit = QLineEdit()
        job_role_layout.addWidget(job_role_label)
        job_role_layout.addWidget(self.job_role_lineedit)
        layout.addLayout(job_role_layout)

        # Application Link Field
        link_layout = QHBoxLayout()
        link_label = QLabel("Application Link:")
        self.link_lineedit = QLineEdit()
        link_layout.addWidget(link_label)
        link_layout.addWidget(self.link_lineedit)
        layout.addLayout(link_layout)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_application)
        layout.addWidget(submit_button)
    
    def populate_countries(self):
        # Fetch all country names using pycountry
        countries = list(pycountry.countries)
        country_names = [country.name for country in countries]

        # Add fetched countries to the combo box
        self.country_combobox.addItems(sorted(country_names))


    def submit_application(self):
        # Get values from fields
        country = self.country_combobox.currentText()
        application_status = self.status_combobox.currentText()
        company = self.company_lineedit.text()
        job_role = self.job_role_lineedit.text()
        link = self.link_lineedit.text()

        conn, cur = connect_to_database()

        try:
            cur.execute("INSERT INTO Job_Application (country, application_status, company, job_role, application_link) VALUES (%s, %s, %s, %s, %s)", (country, application_status, company, job_role, link))
            conn.commit()
        except Exception as e:
            # Handle exceptions (e.g., print error messages, log errors)
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        
        self.close()
