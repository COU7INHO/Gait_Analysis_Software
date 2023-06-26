import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QMenu, QAction, QMainWindow, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QImage, QPixmap, QIcon, QLinearGradient, QColor, QPainter, QPalette
from PyQt5.QtCore import pyqtSignal

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import cv2
from motionAnalysis_class import MotionAnalysis
from info_gui import AmputeeDataInput

class VideoData(QLabel):
    def __init__(self):
        super(VideoData, self).__init__()

        self.init_video = MotionAnalysis("/Users/tiagocoutinho/Desktop/videos/espelho.mov", "Motion Analysis")

        self.init_video.openCamera()
        self.init_video.timeInit()
        self.init_video.getFrame()
        self.init_video.trackerInit() 
        video_scaling_factor = 2.5
        self.setMaximumSize(1920/video_scaling_factor, 1080/video_scaling_factor)

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

        final_angle = 0
        for angle in angles:
             final_angle = angle
        return final_angle

class GradientFrame(QFrame):
    def __init__(self, start_color, end_color):
        super().__init__()
        self.start_color = start_color
        self.end_color = end_color

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0, self.start_color)
        gradient.setColorAt(1, self.end_color)
        painter.fillRect(rect, gradient)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.video_widget = VideoData()
        self.init_ui()

        self.x_history = []
        self.y_history = []
        self.x_history2 = []
        self.y_history2 = []
        self.x_history3 = []
        self.y_history3 = []

    def init_ui(self):
        WINDOW_HEIGHT = 800
        WINDOW_WIDTH = 1500

        rgb_plot_frame = [156, 255, 80]

        self.setWindowTitle("Gait analysis")
        self.setGeometry(30, 40, WINDOW_WIDTH, WINDOW_HEIGHT)
        menu_bar = self.menuBar()

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        new_analysis = QAction("New analysis", self)
        file_menu.addAction(new_analysis)

        adv_settings_action = QAction("Advanced settings", self)
        file_menu.addAction(adv_settings_action)

        view_menu = QMenu("View", self)
        menu_bar.addMenu(view_menu)

        view_labels_action = QAction("View labels", self)
        view_menu.addAction(view_labels_action)

        view_bboxes_action = QAction("View bounding boxes", self)
        view_menu.addAction(view_bboxes_action)

        view_lines_action = QAction("View lines", self)
        view_menu.addAction(view_lines_action)

        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

        docs_action = QAction("Documentation", self)
        help_menu.addAction(docs_action)


#* ############################### FRAMES ###############################
        
#* ############################### Main frame ###############################

        main_layout = QHBoxLayout()

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        start_color = QColor(rgb_plot_frame[0], rgb_plot_frame[1], rgb_plot_frame[2])
        end_color = QColor(0, 0, 0)
        main_widget.setStyleSheet(f"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start_color.name()}, stop:1 {end_color.name()});")

#* ############################### Plot frame ###############################

        plot_frame = QFrame()
        
        plot_frame.setFrameShape(QFrame.StyledPanel)
        plot_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        self.figure = Figure()
        self.figure.suptitle("Joint Angles", fontsize=16, fontweight='bold')

        self.canvas = FigureCanvas(self.figure)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)
        plot_frame.setLayout(plot_layout)

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
        self.ax3.set_title("Ankle angle")
        self.line3, = self.ax3.plot([], [])
        
        facecolor = (rgb_plot_frame[0] / 255, rgb_plot_frame[1] / 255, rgb_plot_frame[2] / 255)
        self.figure.set_facecolor(facecolor)
        plot_frame.setFixedSize(400, WINDOW_HEIGHT)

        main_layout.addWidget(plot_frame)

#* ############################### Central frame ###############################

        person_info_frame = QFrame()
        person_info_frame.setFrameShape(QFrame.StyledPanel)
        person_info_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]});")  
        
        person_info_layout = QHBoxLayout()
        self.name = QLabel()
        self.amp_level = QLabel()
        self.amp_side = QLabel()
        #self.name.setText(f"Name: {self.name}")
        #self.amp_level.setText(f"Amp.level: {self.amputation_level}")
        #self.amp_side.setText(f"Amp.limb: {self.amputated_limb}")

        person_info_layout.addWidget(self.name)
        person_info_layout.addWidget(self.amp_level)
        person_info_layout.addWidget(self.amp_side)

        person_info_frame.setLayout(person_info_layout)


        video_frame = QFrame()
        video_frame.setFrameShape(QFrame.StyledPanel)
        video_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]});")  

        video_frame_layout = QVBoxLayout()
        video_frame_layout.addWidget(person_info_frame)
        video_frame_layout.addWidget(self.video_widget)
        video_frame_layout.setAlignment(Qt.AlignCenter)  # Set the alignment of the layout to center the video widget
        video_frame.setLayout(video_frame_layout)

        video_info_frame = QFrame()
        video_info_frame.setFrameShape(QFrame.StyledPanel)
        start_color = QColor(156, 255, 80)
        end_color = QColor(255, 255, 255)
        video_info_frame = GradientFrame(start_color, end_color)
        video_info_frame.setFrameShape(QFrame.StyledPanel)

        video_info_layout = QVBoxLayout()

        self.hip_angle_label = QLabel()
        self.knee_angle_label = QLabel()
        self.ankle_angle_label = QLabel()
        
        self.max_hip = QLabel()
        self.min_hip = QLabel()
        self.max_knee = QLabel()
        self.min_knee = QLabel()
        self.max_ankle = QLabel()
        self.min_ankle = QLabel()

        video_info_layout.addWidget(self.hip_angle_label)
        video_info_layout.addWidget(self.max_hip)
        video_info_layout.addWidget(self.min_hip)
        video_info_layout.addWidget(self.knee_angle_label)
        video_info_layout.addWidget(self.max_knee)
        video_info_layout.addWidget(self.min_knee)
        video_info_layout.addWidget(self.ankle_angle_label)
        video_info_layout.addWidget(self.max_ankle)
        video_info_layout.addWidget(self.min_ankle)

        self.hip_angle_label.setStyleSheet("background-color: transparent;")
        self.knee_angle_label.setStyleSheet("background-color: transparent;")
        self.ankle_angle_label.setStyleSheet("background-color: transparent;")
        self.max_hip.setStyleSheet("background-color: transparent;")
        self.min_hip.setStyleSheet("background-color: transparent;")
        self.max_knee.setStyleSheet("background-color: transparent;")
        self.min_knee.setStyleSheet("background-color: transparent;")
        self.max_ankle.setStyleSheet("background-color: transparent;")
        self.min_ankle.setStyleSheet("background-color: transparent;")

        video_info_frame.setLayout(video_info_layout)
        
        video_frame_layout.addWidget(video_info_frame)

        video_frame.setFixedHeight(WINDOW_HEIGHT)

        main_layout.addWidget(video_frame)


#* ############################### devi_info_frame ###############################
        
        devi_info_frame = QFrame()
        devi_info_frame.setFrameShape(QFrame.StyledPanel)
        devi_info_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        devi_info_layout = QVBoxLayout()
        devi_info_frame.setLayout(devi_info_layout)

        # Actions frame
        actions_frame = QFrame()
        actions_frame.setFrameShape(QFrame.StyledPanel)
        actions_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        actions_label = QLabel("Actions")

        actions_layout = QVBoxLayout()
        actions_layout.addWidget(actions_label)
        actions_frame.setLayout(actions_layout)

        # Deviations frame
        deviations_frame = QFrame()
        deviations_frame.setFrameShape(QFrame.StyledPanel)
        deviations_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        deviations_label = QLabel("Deviations")

        deviations_layout = QVBoxLayout()
        deviations_layout.addWidget(deviations_label)
        deviations_frame.setLayout(deviations_layout)

        # Corrections frame
        corrections_frame = QFrame()
        corrections_frame.setFrameShape(QFrame.StyledPanel)
        corrections_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        corrections_label = QLabel("Corrections")

        corrections_layout = QVBoxLayout()
        corrections_layout.addWidget(corrections_label)
        corrections_frame.setLayout(corrections_layout)

        # Add frames to the vertical layout
        devi_info_layout.addWidget(actions_frame)
        devi_info_layout.addWidget(deviations_frame)
        devi_info_layout.addWidget(corrections_frame)

        devi_info_frame.setFixedSize(400, WINDOW_HEIGHT)

        main_layout.addWidget(devi_info_frame)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_values("Hip"))
        self.timer.start(int(1000/120))

        self.timer2 = QTimer()
        self.timer2.timeout.connect(lambda: self.update_values("Knee"))
        self.timer2.start(int(1000/120))

        self.timer3 = QTimer()
        self.timer3.timeout.connect(lambda: self.update_values("Ankle"))
        self.timer3.start(int(1000/120))
    
    def findMaxMin(self, joint:str):
        max_y = float('-inf')
        min_y = float('inf')
        
        if joint == "Hip":
            y_history = self.y_history
        elif joint == "Knee":
            y_history = self.y_history2
        elif joint == "Ankle":
            y_history = self.y_history3

        for y in y_history:
            if y > max_y:
                max_y = y  
            if y < min_y:
                min_y = y

        if joint == "Hip":
            self.max_hip.setText(f"Max: {round(max_y, 2)}°")
            self.min_hip.setText(f"Min: {round(min_y, 2)}°")
        elif joint == "Knee":
            self.max_knee.setText(f"Max: {round(max_y, 2)}°")
            self.min_knee.setText(f"Min: {round(min_y, 2)}°")
        elif joint == "Ankle":
            self.max_ankle.setText(f"Max: {round(max_y, 2)}°")
            self.min_ankle.setText(f"Min: {round(min_y, 2)}°")

    def update_values(self, angle:str):
            
        if angle == "Hip":
            x = self.video_widget.current_frame
            y = self.video_widget.getAngle("Hip")
            self.x_history.append(x)
            self.y_history.append(y)
            self.line.set_data(self.x_history, self.y_history)
            self.line.set_color('red')
            self.line.set_linewidth(2)
            self.ax.relim()
            self.ax.autoscale_view()
            self.ax.set_ylim([-20, 30])
            self.canvas.draw()

            self.hip_angle_label.setText(f"Current hip angle: {round(y, 2)}°")

            self.findMaxMin("Hip")

        elif angle == "Knee":
            x = self.video_widget.current_frame
            y = self.video_widget.getAngle("Knee")
            self.x_history2.append(x)  
            self.y_history2.append(y)  
            self.line2.set_data(self.x_history2, self.y_history2) 
            self.line2.set_color('blue')
            self.line2.set_linewidth(2)
            self.ax2.relim() 
            self.ax2.autoscale_view()  
            self.ax2.set_ylim([-5, 70])
            self.canvas.draw()

            self.knee_angle_label.setText(f"Current knee angle: {round(y, 2)}°")

            self.findMaxMin("Knee")

        elif angle == "Ankle":
            x = self.video_widget.current_frame
            y = self.video_widget.getAngle("Ankle")
            self.x_history3.append(x)  
            self.y_history3.append(y)  
            self.line3.set_data(self.x_history3, self.y_history3) 
            self.line3.set_color('black')
            self.line3.set_linewidth(2)
            self.ax3.relim() 
            self.ax3.autoscale_view()  
            self.ax3.set_ylim([-20, 25])
            self.canvas.draw()

            self.ankle_angle_label.setText(f"Current ankle angle: {round(y, 2)}°")

            self.findMaxMin("Ankle")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())