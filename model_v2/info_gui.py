import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
import cv2


class AmputeeDataInput(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Amputee Information')
        self.setFixedSize(300, 400)

        # Create labels
        name_label = QLabel('Full Name:')
        amputation_level_label = QLabel('Amputation Level:')
        amputated_limb_label = QLabel('Amputated Limb:')
        activity_level_label = QLabel('Activity Level:')

        # Create input fields
        self.name_input = QLineEdit()
        self.amputation_level_combo = QComboBox()
        self.amputation_level_combo.addItems(['Transfemoral', 'Transtibial'])
        self.amputated_limb_combo = QComboBox()
        self.amputated_limb_combo.addItems(['Right', 'Left'])
        self.activity_level_combo = QComboBox()
        self.activity_level_combo.addItems(['K0', 'K1', 'K2', 'K3', 'K4'])

        # Create submit button
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submitData)

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
        info_box_layout.addWidget(activity_level_label)
        info_box_layout.addWidget(self.activity_level_combo)
        info_box_layout.addWidget(submit_button)

        self.setLayout(info_box_layout)
        self.show()

    def submitData(self):
        name = self.name_input.text()
        amputation_level = self.amputation_level_combo.currentText()
        amputated_limb = self.amputated_limb_combo.currentText()
        activity_level = self.activity_level_combo.currentText()

        print('Name:', name)
        print('Amputation Level:', amputation_level)
        print('Amputated Limb:', amputated_limb)
        print('Activity Level:', activity_level)
        
        self.close()
        self.startWebcam()

    def startWebcam(self):
        cap = cv2.VideoCapture(0)  # 0 indicates the default webcam
        while True:
            ret, frame = cap.read()
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
                break
        cap.release()
        cv2.destroyAllWindows()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AmputeeDataInput()
    sys.exit(app.exec_())
