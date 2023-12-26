import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, Qt
from connect_to_db import connect_to_database
from edit_data_window import EditJobApplicationWindow

class JobDetailsWindow(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Job Application Details")
        self.setFixedSize(300, 250)
        layout = QVBoxLayout(self)
        self.data = data

        for column, value in self.data.items():
            if column == "application_link":
                link_label = QLabel(f'<b>Link</b>: <a href="{value}">Job Application Link</a>')
                link_label.setOpenExternalLinks(True)
                link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
                link_label.setWordWrap(True)
                link_label.linkActivated.connect(self.open_link)
                layout.addWidget(link_label)
            elif column == "application_id":
                pass
            else:
                label = QLabel(f"<b>{column}</b>: {value}")
                layout.addWidget(label)

        button_layout = QVBoxLayout()  # Changed from QHBoxLayout to QVBoxLayout

        edit_button = QPushButton("Edit")
        edit_button.setFocusPolicy(Qt.NoFocus)  
        edit_button.clicked.connect(self.edit_application)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setFocusPolicy(Qt.NoFocus)  
        delete_button.clicked.connect(self.delete_application)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

    def open_link(self, link):
        QDesktopServices.openUrl(QUrl(link))

    def edit_application(self):
        edit_window = EditJobApplicationWindow(self.data)  # Pass the current data to the edit window
        result = edit_window.exec_()

        if result == QDialog.Accepted:
            updated_data = edit_window.get_updated_data()  # Retrieve the updated data from the edit window
            if updated_data:  # Check if there are any changes
                # Update the database with the new data
                conn, cur = connect_to_database()

                application_id = updated_data.get('application_id')

                try:
                    # Update query for the specific application_id
                    update_query = "UPDATE Job_Application SET country = %s, application_status = %s, company = %s, job_role = %s, application_link = %s WHERE application_id = %s"
                    cur.execute(update_query, (updated_data['country'], updated_data['application_status'], updated_data['company'], updated_data['job_role'], updated_data['application_link'], application_id))

                    conn.commit()  # Commit changes to the database
                    QMessageBox.information(self, "Success", "Application updated successfully.")
                    
                    # Update the displayed data if the table is refreshed
                    self.fetch_data_and_display()
                except Exception as e:
                    print("Error occurred while updating application:", e)
                    conn.rollback()  # Roll back changes in case of an error

                cur.close()
                conn.close()
        
        self.close()

    def delete_application(self):
        conn, cur = connect_to_database()

        application_id = self.data.get('application_id')

        # Confirmation dialog before deletion
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to delete this application?")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.No)

        # Get user's response
        response = confirm_dialog.exec_()

        if response == QMessageBox.Yes:
            try:
                cur.execute ("DELETE FROM Job_Application WHERE application_id = %s",  (application_id,))
                conn.commit() 
                self.close()
            except Exception as e:
                QMessageBox.critical("Error occurred while deleting application:", e)
                conn.rollback()  

        cur.close()
        conn.close()
