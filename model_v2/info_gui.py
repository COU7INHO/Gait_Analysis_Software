
import sys
from PyQt5.QtWidgets import QApplication, QWidget,QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class SearchAmputeeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Amputee')
        self.setFixedSize(300, 150)

        self.name_input = QLineEdit()

        search_button = QPushButton('Search')
        search_button.clicked.connect(self.searchAmputee)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Enter the name of the amputee:'))
        layout.addWidget(self.name_input)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def searchAmputee(self):
        name = self.name_input.text()
        # Add your search logic here using the provided name input
        print('There are no available results', name)


from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal

class AmputeeDataInput(QWidget):
    submit_signal = pyqtSignal()  # Custom signal for submit button

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Amputee Information')
        self.setFixedSize(300, 500)

        # Create labels
        name_label = QLabel('Full Name:')
        amputation_level_label = QLabel('Amputation Level:')
        amputated_limb_label = QLabel('Amputated Limb:')
        weight_label = QLabel('Horizontal measurement (mm):')
        height_label = QLabel('Vertical measurement (mm):')

        # Create input fields
        self.name_input = QLineEdit()
        self.amputation_level_combo = QComboBox()
        self.amputation_level_combo.addItems(['Transfemoral', 'Transtibial'])
        self.amputated_limb_combo = QComboBox()
        self.amputated_limb_combo.addItems(['Right', 'Left'])

        # Create number input boxes
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setDecimals(2)
        self.weight_input.setSingleStep(0.01)
        self.height_input = QDoubleSpinBox()
        self.height_input.setDecimals(2)
        self.height_input.setSingleStep(0.01)

        # Create submit button
        start_button = QPushButton('Start Gait Analysis')
        search_button = QPushButton('Search amputee')
        search_button.clicked.connect(self.searchAmputee)
        start_button.clicked.connect(self.submitData)

        # Create layout
        info_box_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel('<h1>Amputee Information</h1>'))
        info_box_layout.addLayout(title_layout)
        info_box_layout.addWidget(name_label)
        info_box_layout.addWidget(self.name_input)
        info_box_layout.addWidget(amputation_level_label)
        info_box_layout.addWidget(self.amputation_level_combo)
        info_box_layout.addWidget(amputated_limb_label)
        info_box_layout.addWidget(self.amputated_limb_combo)
        info_box_layout.addWidget(weight_label)
        info_box_layout.addWidget(self.weight_input)
        info_box_layout.addWidget(height_label)
        info_box_layout.addWidget(self.height_input)
        info_box_layout.addWidget(search_button)
        info_box_layout.addWidget(start_button)

        self.setLayout(info_box_layout)

    def submitData(self):
        self.name = self.name_input.text()
        self.amputation_level = self.amputation_level_combo.currentText()
        self.amputated_limb = self.amputated_limb_combo.currentText()
        self.h_calibration = self.weight_input.value()
        self.v_calibration = self.height_input.value()

        self.submit_signal.emit() 
        self.close()
    
    def searchAmputee(self):
        search_window = SearchAmputeeWindow()
        search_window.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AmputeeDataInput()
    window.show()
    sys.exit(app.exec_())