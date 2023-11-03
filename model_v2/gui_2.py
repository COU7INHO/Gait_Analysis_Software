import sys

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.add_label_button_pair("Dynamic Label 1", "Info 1")
        self.add_label_button_pair("Dynamic Label 2", "Info 2")
        self.add_label_button_pair("Dynamic Label 3", "Info 3")

        self.setLayout(self.layout)

    def add_label_button_pair(self, label_text, button_text):
        label = QLabel(label_text)
        button = QPushButton(button_text)
        button.setFixedSize(100, 30)
        button.clicked.connect(lambda: self.open_info_window(label_text))

        pair_layout = QHBoxLayout()
        pair_layout.addWidget(label)
        pair_layout.addWidget(button)

        self.layout.addLayout(pair_layout)

    def open_info_window(self, label_text):
        info_window = InfoWindow(label_text)
        info_window.exec_()


class InfoWindow(QDialog):
    def __init__(self, label_text):
        super().__init__()

        self.setWindowTitle("Info Window")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        info_label = QLabel(f"This is additional information for {label_text}.")
        layout.addWidget(info_label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
