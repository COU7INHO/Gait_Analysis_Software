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
        
    def getAngle(self, joint):
        angles = None
        if joint == "Hip":
            angles = self.init_video.hip_angles
        elif joint == "Knee":
            angles = self.init_video.knee_angles
        elif joint == "Ankle":
            angles = self.init_video.ankle_angles
        else:
            raise ValueError("Invalid angle")

        for angle in angles:
             final_angle = angle
        return final_angle
    
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.webcam_widget = VideoData()
        self.init_ui()

        self.x_history = []
        self.y_history = []
        self.x_history2 = []
        self.y_history2 = []
        self.x_history3 = []
        self.y_history3 = []

    def init_ui(self):
        self.setWindowTitle("Gait analysis")
        self.setGeometry(100, 100, 1600, 480)

        main_layout = QHBoxLayout()

        plot_frame = QFrame()
        plot_frame.setFrameShape(QFrame.StyledPanel)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.canvas)
        plot_frame.setLayout(v_layout)

        self.ax = self.figure.add_subplot(311)
        self.ax.set_ylabel("Angle (degrees)")
        self.ax.set_title("Hip angle")
        self.line, = self.ax.plot([], [])
        self.ax.set_xticklabels([]) 

        self.ax2 = self.figure.add_subplot(312)
        self.ax2.set_ylabel("Angle (degrees)")
        self.ax2.set_title("Knee angle")
        self.line2, = self.ax2.plot([], [])
        self.ax2.set_xticklabels([]) 

        self.ax3 = self.figure.add_subplot(313)
        self.ax3.set_xlabel("Frame")
        self.ax3.set_ylabel("Angle (degrees)")
        self.ax3.set_title("Hip angle")
        self.line3, = self.ax3.plot([], [])

        main_layout.addWidget(plot_frame)

        webcam_frame = QFrame()
        webcam_frame.setFrameShape(QFrame.StyledPanel)

        webcam_layout = QVBoxLayout()

        webcam_layout.addWidget(self.webcam_widget)
        webcam_frame.setLayout(webcam_layout)
        main_layout.addWidget(webcam_frame)

        self.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_plot("Hip"))
        self.timer.start(1)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(lambda: self.update_plot("Knee"))
        self.timer2.start(1)

        self.timer3 = QTimer()
        self.timer3.timeout.connect(lambda: self.update_plot("Ankle"))
        self.timer3.start(1)
        
    def update_plot(self, angle:str):
            
        if angle == "Hip":
            x = self.webcam_widget.current_frame
            y = self.webcam_widget.getAngle("Hip")
            self.x_history.append(x)
            self.y_history.append(y)
            self.line.set_data(self.x_history, self.y_history)
            self.ax.relim()
            self.ax.autoscale_view()
            self.ax.set_ylim([-20, 30])
            self.canvas.draw()

        elif angle == "Knee":
            x = self.webcam_widget.current_frame
            y = self.webcam_widget.getAngle("Knee")
            self.x_history2.append(x)  
            self.y_history2.append(y)  
            self.line2.set_data(self.x_history2, self.y_history2) 
            self.ax2.relim() 
            self.ax2.autoscale_view()  
            self.ax2.set_ylim([-5, 70])
            self.canvas.draw()

        elif angle == "Ankle":
            x = self.webcam_widget.current_frame
            y = self.webcam_widget.getAngle("Ankle")
            self.x_history3.append(x)  
            self.y_history3.append(y)  
            self.line3.set_data(self.x_history3, self.y_history3) 
            self.ax3.relim() 
            self.ax3.autoscale_view()  
            self.ax3.set_ylim([-20, 25])
            self.canvas.draw()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())