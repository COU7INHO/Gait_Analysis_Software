import sys
import cv2
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WebcamWidget(QLabel):
    def __init__(self):
        super(WebcamWidget, self).__init__()
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def update_frame(self):
        ret, frame = self.webcam.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = frame.shape
            q_image = QImage(frame.data, width, height, channels * width, QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(q_image))


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.webcam_widget = WebcamWidget()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Webcam Viewer")
        self.setGeometry(100, 100, 1280, 480)

        # Create layout for the main window
        main_layout = QHBoxLayout()

        # Create frame1 for the plot
        plot_frame = QFrame()
        plot_frame.setFrameShape(QFrame.StyledPanel)

        # Create a Figure object for the plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Add the canvas to frame1
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.canvas)
        plot_frame.setLayout(v_layout)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Real-Time Plot')
        self.line, = self.ax.plot([], [])

        main_layout.addWidget(plot_frame)
        main_layout.addWidget(self.webcam_widget)

        self.setLayout(main_layout)

        # Call function to update the plot with real-time data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(500)

    def update_plot(self):
        # Generate random data for the plot
        x = list(range(10))
        y = [random.randint(0, 10) for _ in range(10)]

        # Update the plot with the new data
        self.line.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

