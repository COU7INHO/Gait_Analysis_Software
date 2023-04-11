import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import cv2
from motionAnalysis_class import MotionAnalysis



class VideoData(QLabel):
    def __init__(self):
        super(VideoData, self).__init__()
        '''self.video = cv2.VideoCapture('/Users/tiagocoutinho/Desktop/videos/espelho.mov')
        '''
        self.init_video = MotionAnalysis("/Users/tiagocoutinho/Desktop/videos/espelho.mov", "Motion Analysis")

        self.init_video.openCamera()
        self.init_video.timeInit()
        self.init_video.getFrame()
        self.init_video.trackerInit() 

        self.setMaximumSize(800, 480)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        self.knee_angle = 0
        

    def update_frame(self):

        self.init_video.getFrame()
        self.current_frame = int(self.init_video.camera.get(cv2.CAP_PROP_POS_FRAMES))
        self.init_video.removeEmptyBoxes()
        self.init_video.checkMarkers()
        self.init_video.getCenters()  
        self.init_video.calcAngles()
        self.init_video.lines()
        self.init_video.writeLabels()
        self.init_video.timeStop()
        self.video_frame = self.init_video.frame
        self.video_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
        self.video_frame = cv2.resize(self.video_frame, (self.maximumWidth(), self.maximumHeight()))
        height, width, channels = self.video_frame.shape
        q_image = QImage(self.video_frame.data, width, height, channels * width, QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(q_image))
        
    def getAngles(self):
        for knee_ang in self.init_video.ankle_angles:
            self.knee_angle = knee_ang
        return self.knee_angle

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.webcam_widget = VideoData()
        self.init_ui()

        self.x_history = []
        self.y_history = []

    def init_ui(self):
        self.setWindowTitle("Webcam Viewer")
        self.setGeometry(100, 100, 1600, 480)

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
        self.ax.set_xlabel("Frame")
        self.ax.set_ylabel("Angle (degrees)")
        self.ax.set_title("Angle plot")
        self.line, = self.ax.plot([], [])

        main_layout.addWidget(plot_frame)

        # Create frame2 for the webcam widget
        webcam_frame = QFrame()
        webcam_frame.setFrameShape(QFrame.StyledPanel)

        # Create a QVBoxLayout for the webcam frame
        webcam_layout = QVBoxLayout()

        # Create the webcam widget and add it to the layout
        webcam_layout.addWidget(self.webcam_widget)

        webcam_frame.setLayout(webcam_layout)

        main_layout.addWidget(webcam_frame)

        self.setLayout(main_layout)

        # Call function to update the plot with real-time data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1)


    def update_plot(self):

        x = self.webcam_widget.current_frame
        y = self.webcam_widget.getAngles()
 
        self.x_history.append(x)
        self.y_history.append(y)

        self.line.set_data(self.x_history, self.y_history)
        self.ax.relim()
        self.line.set_color('blue')  
        self.line.set_linestyle('-') 
        self.ax.set_xlim([0, max(self.x_history)])  # Set the x-axis limit from zero to the maximum value in x_history
        self.ax.set_ylim([-10, 20])  # Replace y_min and y_max with your desired limits
        self.ax.autoscale_view()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())