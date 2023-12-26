from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
import matplotlib.pyplot as plt

class StatisticsWindow(QDialog):
    def __init__(self, conn, cur):
        super().__init__()
        self.setWindowTitle("Statistics")
        self.setFixedSize(500, 400)
        self.conn = conn
        self.cur = cur

        layout = QVBoxLayout(self)

        # Fetch statistics
        self.total_apps = self.get_total_applications()
        self.no_response = self.get_application_count("No Response")
        self.rejected = self.get_application_count("Rejected")
        self.interviews = self.get_application_count("Interview")

        # Calculate percentages
        self.no_response_percentage = (self.no_response / self.total_apps) * 100 if self.total_apps > 0 else 0
        self.rejected_percentage = (self.rejected / self.total_apps) * 100 if self.total_apps > 0 else 0
        self.interviews_percentage = (self.interviews / self.total_apps) * 100 if self.total_apps > 0 else 0

        # Display statistics
        layout.addWidget(QLabel(f"<b>Total applications:</b> {self.total_apps}"))
        layout.addWidget(QLabel(f"<b>No Response:</b> {self.no_response} ({self.no_response_percentage:.2f}%)"))
        layout.addWidget(QLabel(f"<b>Rejected:</b> {self.rejected} ({self.rejected_percentage:.2f}%)"))
        layout.addWidget(QLabel(f"<b>Interviews:</b> {self.interviews} ({self.interviews_percentage:.2f}%)"))

        # Create pie chart
        self.create_pie_chart(layout)

    def get_total_applications(self):
        # Fetch and return the total number of applications
        query = "SELECT COUNT(*) FROM Job_Application"
        self.cur.execute(query)
        total_apps = self.cur.fetchone()[0] if self.cur.rowcount > 0 else 0
        return total_apps

    def get_application_count(self, status):
        # Fetch and return the count of applications by status
        query = f"SELECT COUNT(*) FROM Job_Application WHERE application_status = '{status}'"
        self.cur.execute(query)
        count = self.cur.fetchone()[0] if self.cur.rowcount > 0 else 0
        return count

    def create_pie_chart(self, layout):
        # Create pie chart
        labels = ['No Response', 'Rejected', 'Interviews']
        sizes = [self.no_response, self.rejected, self.interviews]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        explode = (0.1, 0.1, 0.1)  

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Set background color to transparent
        fig.patch.set_facecolor('#ECECEC')
        ax.set_facecolor('#ECECEC')

        layout.addWidget(fig.canvas)
