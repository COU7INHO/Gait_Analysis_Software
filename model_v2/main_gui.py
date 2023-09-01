import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QMenu, QAction, QMainWindow, QPushButton, QDialog, QTextEdit
from PyQt5.QtGui import QImage, QPixmap, QIcon, QLinearGradient, QColor, QPainter

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from motionAnalysis_class import MotionAnalysis
from info_gui import AmputeeDataInput
from pdf_report import PdfGen

import copy



class VideoData(QLabel):
    def __init__(self):
        super(VideoData, self).__init__()
        self.window_name = "Gait Analysis"
        self.init_video = MotionAnalysis("/Users/tiagocoutinho/Desktop/videos/2_ciclos.mp4", self.window_name)

        self.init_video.open_camera()
        self.init_video.init_time()
        self.init_video.get_video_frame()
        self.init_video.init_tracker() 
        video_scaling_factor = 2.5
        self.setMaximumSize(int(1920/video_scaling_factor), int(1080/video_scaling_factor))

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        self.knee_angle = 0
        
    def update_frame(self):

        self.init_video.get_video_frame()
        self.current_frame = int(self.init_video.camera.get(cv2.CAP_PROP_POS_FRAMES))
        self.init_video.remove_empty_boxes()
        self.init_video.check_markers()
        self.init_video.markers_centers()  
        self.init_video.gait_direction()
        self.init_video.get_filtered_angles()

        self.init_video.lines()
        self.init_video.labels()
        self.init_video.end_time()
        self.video_frame = self.init_video.new_frame

        self.init_video.display_window()  #* Display Window <-- <-- <-- <-- <-- 

        self.video_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
        self.video_frame = cv2.resize(self.video_frame, (self.maximumWidth(), self.maximumHeight()))
        height, width, channels = self.video_frame.shape
        q_image = QImage(self.video_frame.data, width, height, channels * width, QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(q_image))
    
    def angle_value(self, joint:str):
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
            
        
    def toggle_show_lines(self, value):
        self.init_video.showLines = value

    def toggle_show_labels(self, value):
        self.init_video.showLabels = value

    def toggle_show_bbox(self, value):
        self.init_video.showbbox = value
        
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

        # GUI to input amputee data
        self.amputee_data = AmputeeDataInput()
        self.amputee_data.submit_signal.connect(self.on_submit) 
        self.amputee_data.show()

        # Hip angle
        self.x_history = []
        self.y_history = []
        self.x_history_2 = []
        self.y_history_2 = []

        # Knee angle
        self.x_history2 = []
        self.y_history2 = []
        self.x_history2_2 = []
        self.y_history2_2 = []
        
        # Ankle angle
        self.x_history3 = []
        self.y_history3 = []
        self.x_history3_2 = []
        self.y_history3_2 = []

        self.gait_phase_duration_RTL = False
        self.gait_phase_duration_LTR = False
        
        self.min_value_x_RTL = None
        self.min_value_x_LTR = None

        self.time_difference_difference = None

        self.time_difference_RTL = None
        self.time_difference_LTR = None

        self.percent_diff = None

        
    def on_submit(self):

        self.video_widget = VideoData()
        self.init_ui()
        self.show()

    def init_ui(self):
        WINDOW_HEIGHT = 800
        WINDOW_WIDTH = 1500

        rgb_plot_frame = [156, 255, 80]

        self.setWindowTitle(self.video_widget.window_name)
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

        view_labels_action = QAction("Hide labels", self)
        view_labels_action.setCheckable(True)
        view_labels_action.setChecked(False)
        view_labels_action.triggered.connect(self.view_labels_action_triggered)
        view_menu.addAction(view_labels_action)

        view_bboxes_action = QAction("Hide bounding boxes", self)
        view_bboxes_action.setCheckable(True)
        view_bboxes_action.setChecked(False)
        view_bboxes_action.triggered.connect(self.view_bbox_action_triggered)
        view_menu.addAction(view_bboxes_action)

        view_lines_action = QAction("Hide lines", self)
        view_lines_action.setCheckable(True)
        view_lines_action.setChecked(False)
        view_lines_action.triggered.connect(self.view_lines_action_triggered)
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
        
        plot_frame.setFrameShape(QFrame.NoFrame)
        plot_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        self.figure = Figure()
        self.figure.suptitle("Left leg", fontsize=16, fontweight='bold')

        self.canvas = FigureCanvas(self.figure)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)
        plot_frame.setLayout(plot_layout)

        self.ax = self.figure.add_subplot(311)
        self.ax.set_title("Hip angle")
        self.line, = self.ax.plot([], [])
        self.ax.set_xticklabels([]) 

        self.ax2 = self.figure.add_subplot(312)
        self.ax2.set_ylabel("Angle (degrees)")
        self.ax2.set_title("Knee angle")
        self.line2, = self.ax2.plot([], [])
        self.ax2.set_xticklabels([]) 

        self.ax3 = self.figure.add_subplot(313)
        self.ax3.set_xlabel("Seconds")
        self.ax3.set_title("Ankle angle")
        self.line3, = self.ax3.plot([], [])

        facecolor = (rgb_plot_frame[0] / 255, rgb_plot_frame[1] / 255, rgb_plot_frame[2] / 255)
        self.figure.set_facecolor(facecolor)
        plot_frame.setFixedSize(400, WINDOW_HEIGHT)

        main_layout.addWidget(plot_frame)

#*********************************************************


        plot_frame_2 = QFrame()
        
        plot_frame_2.setFrameShape(QFrame.NoFrame)
        plot_frame_2.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        self.figure_2 = Figure()
        self.figure_2.suptitle("Right leg", fontsize=16, fontweight='bold')

        self.canvas_2 = FigureCanvas(self.figure_2)

        plot_layout_2 = QVBoxLayout()
        plot_layout_2.addWidget(self.canvas_2)
        plot_frame_2.setLayout(plot_layout_2)

        self.ax_2 = self.figure_2.add_subplot(311)
        self.ax_2.set_title("Hip angle")
        self.line_2, = self.ax_2.plot([], [])
        self.ax_2.set_xticklabels([]) 

        self.ax2_2 = self.figure_2.add_subplot(312)
        self.ax2_2.set_ylabel("Angle (degrees)")
        self.ax2_2.set_title("Knee angle")
        self.line2_2, = self.ax2_2.plot([], [])
        self.ax2_2.set_xticklabels([]) 

        self.ax3_2 = self.figure_2.add_subplot(313)
        self.ax3_2.set_xlabel("Seconds")
        self.ax3_2.set_title("Ankle angle")
        self.line3_2, = self.ax3_2.plot([], [])

        facecolor = (rgb_plot_frame[0] / 255, rgb_plot_frame[1] / 255, rgb_plot_frame[2] / 255)
        self.figure_2.set_facecolor(facecolor)
        plot_frame_2.setFixedSize(400, WINDOW_HEIGHT)

        main_layout.addWidget(plot_frame_2)

#* ############################### Central frame ###############################

        person_info_frame = QFrame()
        person_info_frame.setFrameShape(QFrame.NoFrame)
        person_info_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]});")  
        
        person_info_layout = QHBoxLayout()
        self.name = QLabel()
        self.amp_level = QLabel()
        self.amp_side = QLabel()
        self.name.setText(f"<html><b>Name:</b> {self.amputee_data.name}")
        self.amp_level.setText(f"<html><b>Amp.level</b>: {self.amputee_data.amputation_level}")
        self.amp_side.setText(f"<html><b>Amp.limb</b>: {self.amputee_data.amputated_limb}")

        person_info_layout.addWidget(self.name)
        person_info_layout.addWidget(self.amp_level)
        person_info_layout.addWidget(self.amp_side)

        person_info_frame.setLayout(person_info_layout)

        video_frame = QFrame()
        video_frame.setFrameShape(QFrame.NoFrame)
        video_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]});")  

        video_frame_layout = QVBoxLayout()
        video_frame_layout.addWidget(person_info_frame)
        video_frame_layout.addWidget(self.video_widget)
        video_frame_layout.setAlignment(Qt.AlignCenter) 
        video_frame.setLayout(video_frame_layout)

        video_info_frame = QFrame()
        video_info_frame.setFrameShape(QFrame.StyledPanel)
        start_color = QColor(156, 255, 80)
        end_color = QColor(255, 255, 255)
        video_info_frame = GradientFrame(start_color, end_color)
        video_info_frame.setFrameShape(QFrame.StyledPanel)
    
        video_info_layout = QHBoxLayout()

        # Create the left_leg_frame
        angles_values_frame = QFrame()
        angles_values_frame_layout = QVBoxLayout()
        angles_values_frame.setLayout(angles_values_frame_layout)

        self.hip_angle_label = QLabel()
        self.knee_angle_label = QLabel()
        self.ankle_angle_label = QLabel()
        
        self.max_hip = QLabel()
        self.min_hip = QLabel()
        self.max_knee = QLabel()
        self.min_knee = QLabel()
        self.max_ankle = QLabel()
        self.min_ankle = QLabel()

        # Add labels to the left_leg_frame
        angles_values_frame_layout.addWidget(self.hip_angle_label)
        angles_values_frame_layout.addWidget(self.max_hip)
        angles_values_frame_layout.addWidget(self.min_hip)
        angles_values_frame_layout.addWidget(self.knee_angle_label)
        angles_values_frame_layout.addWidget(self.max_knee)
        angles_values_frame_layout.addWidget(self.min_knee)
        angles_values_frame_layout.addWidget(self.ankle_angle_label)
        angles_values_frame_layout.addWidget(self.max_ankle)
        angles_values_frame_layout.addWidget(self.min_ankle)

        # Set stylesheet for labels inside left_leg_frame
        self.hip_angle_label.setStyleSheet("background-color: transparent;")
        self.knee_angle_label.setStyleSheet("background-color: transparent;")
        self.ankle_angle_label.setStyleSheet("background-color: transparent;")
        self.max_hip.setStyleSheet("background-color: transparent;")
        self.min_hip.setStyleSheet("background-color: transparent;")
        self.max_knee.setStyleSheet("background-color: transparent;")
        self.min_knee.setStyleSheet("background-color: transparent;")
        self.max_ankle.setStyleSheet("background-color: transparent;")
        self.min_ankle.setStyleSheet("background-color: transparent;")

        dev_frame = QFrame()
        dev_frame_layout = QVBoxLayout()
        dev_frame.setLayout(dev_frame_layout)

        dev_frame_title = QLabel("Gait deviations")
        dev_frame_title.setStyleSheet("font-weight: bold; font-size: 16px; padding: 5px;")

        self.gait_phases_time = QLabel()         
        self.phases_summary = QLabel()

        dev_frame_layout.addWidget(dev_frame_title)
        dev_frame_layout.addWidget(self.gait_phases_time)
        dev_frame_layout.addWidget(self.phases_summary)


        
        '''
        corrections_frame = QFrame()
        corrections_frame_layout = QVBoxLayout()
        corrections_frame.setLayout(corrections_frame_layout)

        corrections_frame_title = QLabel("Corrections")
        corrections_frame_title.setStyleSheet("font-weight: bold; font-size: 16px; padding: 5px;")

        corrections_frame_layout.addWidget(corrections_frame_title)
        video_info_layout.addWidget(corrections_frame)
        '''

        video_info_layout.addWidget(angles_values_frame)
        video_info_layout.addWidget(dev_frame)

        video_info_frame.setLayout(video_info_layout)
        
        video_frame_layout.addWidget(video_info_frame)

        video_frame.setFixedHeight(WINDOW_HEIGHT)

        main_layout.addWidget(video_frame)

        ''' 
#* ############################### devi_info_frame ###############################
        devi_info_frame = QFrame()
        devi_info_frame.setFrameShape(QFrame.NoFrame)
        devi_info_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  

        devi_info_layout = QVBoxLayout()
        devi_info_frame.setLayout(devi_info_layout)

        # Actions frame
        actions_frame = QFrame()

        actions_frame.setFrameShape(QFrame.NoFrame)
        actions_frame.setStyleSheet(f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); ")  
        actions_frame.setFixedSize(374, 140)

        save_button = QPushButton("Save results")
        save_button.setStyleSheet("background-color: white; border-radius: 7px; padding: 10px; border: 2px solid black;")
        save_button.clicked.connect(self.open_save_dialog)

        new_analysis_button = QPushButton("Start a new analysis")
        new_analysis_button.setStyleSheet("background-color: white; border-radius: 7px; padding: 10px; border: 2px solid black;")

        actions_layout = QVBoxLayout()
        actions_frame.setLayout(actions_layout)
        actions_layout.setAlignment(Qt.AlignHCenter)
        actions_layout.addWidget(save_button)
        actions_layout.addWidget(new_analysis_button)

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
        '''
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_angle_values("Hip"))
        self.timer.start(int(1000/120))

        self.timer2 = QTimer()
        self.timer2.timeout.connect(lambda: self.update_angle_values("Knee"))
        self.timer2.start(int(1000/120))

        self.timer3 = QTimer()
        self.timer3.timeout.connect(lambda: self.update_angle_values("Ankle"))
        self.timer3.start(int(1000/120))
    
    def angle_max_min(self, joint:str, y_history):
        max_y = float('-inf')
        min_y = float('inf')
        
        if joint == "Hip":
            y_history = y_history
        elif joint == "Knee":
            y_history = y_history
        elif joint == "Ankle":
            y_history = y_history

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

    def gait_phase_line(self, ax, frame):
        if frame is not None:
            ax.axvline(frame, linestyle='--', linewidth=2)

    def normalize_gait_phases(self, ax, line, list_x, list_y, lower_threshold: int, upper_threshold: int):

        original_list_x = list_x
        original_list_y = list_y
        copied_list_x = copy.deepcopy(original_list_x)
        copied_list_y = copy.deepcopy(original_list_y)

        if len(copied_list_x) >= lower_threshold:
            copied_list_x = copied_list_x[lower_threshold:upper_threshold]
            copied_list_y = copied_list_y[lower_threshold:upper_threshold]

            if self.video_widget.init_video.direction == "right_to_left":
                stance_frame_RTL, swing_frame_RTL = self.video_widget.init_video.gait_phases_RTL()

                if len(copied_list_x) > 0: 
                    self.min_value_x_RTL = min(copied_list_x)
                    normalized_values = [x - self.min_value_x_RTL for x in copied_list_x]

                    if stance_frame_RTL is not None:
                        self.gait_phase_line(ax, stance_frame_RTL - self.min_value_x_RTL + lower_threshold / self.video_widget.init_video.fps_rate)

                    if swing_frame_RTL is not None:
                        self.gait_phase_line(ax, swing_frame_RTL - self.min_value_x_RTL + lower_threshold / self.video_widget.init_video.fps_rate)

                    if self.gait_phase_duration_RTL == False and stance_frame_RTL is not None and swing_frame_RTL is not None:
                        self.time_difference_RTL = swing_frame_RTL - stance_frame_RTL
                        self.gait_phase_duration_RTL = True

                    line.set_data(normalized_values, copied_list_y)
            else:
                stance_frame_LTR, swing_frame_LTR = self.video_widget.init_video.gait_phase_LTR()

                if len(copied_list_x) > 0: 
                    self.min_value_x_LTR = min(copied_list_x)
                    normalized_values_x = [x - self.min_value_x_LTR for x in copied_list_x]

                    if stance_frame_LTR is not None:
                        self.gait_phase_line(ax, stance_frame_LTR - self.min_value_x_LTR + lower_threshold / self.video_widget.init_video.fps_rate)

                    if swing_frame_LTR is not None:
                        self.gait_phase_line(ax, swing_frame_LTR - self.min_value_x_LTR + lower_threshold / self.video_widget.init_video.fps_rate)

                    if self.gait_phase_duration_LTR == False and stance_frame_LTR is not None and swing_frame_LTR is not None:
                        self.time_difference_LTR = swing_frame_LTR - stance_frame_LTR
                        self.gait_phase_duration_LTR = True

                    line.set_data(normalized_values_x, copied_list_y)


    def gait_duration(self):
        if self.time_difference_RTL is None or self.time_difference_LTR is None:
            self.gait_phases_time.setText(f"Stance phase diff: calculating...")
        
        if self.time_difference_RTL is not None and self.time_difference_LTR is not None:
            time_difference_difference = self.time_difference_RTL - self.time_difference_LTR
            self.gait_phases_time.setText(f"Stance phase diff: {time_difference_difference: .2f} seconds")

            if self.time_difference_RTL > self.time_difference_LTR:
                self.percent_diff = (self.time_difference_RTL - self.time_difference_LTR) / self.time_difference_RTL * 100
                self.phases_summary.setText(f"The left leg had a {self.percent_diff:.2f}% stance phase longer")
                if self.percent_diff > 15:
                    self.phases_summary.setStyleSheet("color: red;")

            elif self.time_difference_RTL < self.time_difference_LTR:
                self.percent_diff = (self.time_difference_LTR - self.time_difference_RTL) / self.time_difference_LTR * 100
                self.phases_summary.setText(f"The right leg had a {self.percent_diff:.2f}% stance phase longer")
                if self.percent_diff > 15:
                    self.phases_summary.setStyleSheet("color: red;")
                
            else:
                self.phases_summary.setText(f"Same stance phase in both legs")


    def update_angle_values(self, angle:str):
        lower_threshold = 5
        upper_threshold = -5
        #? x = current_frame / fps (fps in this case is 120)
        x = self.video_widget.current_frame / self.video_widget.init_video.fps_rate
        self.gait_duration()

        if angle == "Hip":
            y = self.video_widget.angle_value("Hip")
            if self.video_widget.init_video.direction == "right_to_left":
                self.x_history.append(x)
                self.y_history.append(y)   

                self.normalize_gait_phases(self.ax, self.line, self.x_history, self.y_history, lower_threshold, upper_threshold)
                
                self.line.set_color('red')
                self.line.set_linewidth(2)
                self.ax.relim()
                self.ax.autoscale_view()
                self.ax.set_ylim([-20, 30])
                self.canvas.draw()
                self.angle_max_min("Hip", self.y_history)

            else:

                self.x_history_2.append(x)
                self.y_history_2.append(y)

                self.normalize_gait_phases(self.ax_2, self.line_2, self.x_history_2, self.y_history_2, lower_threshold, upper_threshold)

                self.line_2.set_color('red')
                self.line_2.set_linewidth(2)    
                self.ax_2.relim()
                self.ax_2.autoscale_view()
                self.ax_2.set_ylim([-20, 30])
                self.canvas_2.draw()
                self.angle_max_min("Hip", self.y_history_2)

            self.hip_angle_label.setText(f"Current hip angle: {round(y, 2)}°")

        elif angle == "Knee":
            y = self.video_widget.angle_value("Knee")
            if self.video_widget.init_video.direction == "right_to_left":
                self.x_history2.append(x)  
                self.y_history2.append(y)  

                self.normalize_gait_phases(self.ax2, self.line2, self.x_history2, self.y_history2, lower_threshold, upper_threshold)

                self.line2.set_color('blue')
                self.line2.set_linewidth(2)
                self.ax2.relim() 
                self.ax2.autoscale_view()  
                self.ax2.set_ylim([-5, 70])
                self.canvas.draw()
                self.angle_max_min("Knee", self.y_history2)

            else:
                self.x_history2_2.append(x)  
                self.y_history2_2.append(y)  

                self.normalize_gait_phases(self.ax2_2, self.line2_2, self.x_history2_2, self.y_history2_2, lower_threshold, upper_threshold)
                
                self.line2_2.set_color('blue')
                self.line2_2.set_linewidth(2)
                self.ax2_2.relim() 
                self.ax2_2.autoscale_view()  
                self.ax2_2.set_ylim([-5, 70])
                self.canvas_2.draw()
                self.angle_max_min("Knee", self.y_history2_2)

            self.knee_angle_label.setText(f"Current knee angle: {round(y, 2)}°")

        elif angle == "Ankle":
            y = self.video_widget.angle_value("Ankle")
            if self.video_widget.init_video.direction == "right_to_left":
                self.x_history3.append(x)  
                self.y_history3.append(y)  
                
                self.normalize_gait_phases(self.ax3, self.line3, self.x_history3, self.y_history3, lower_threshold, upper_threshold)

                self.line3.set_color('black')
                self.line3.set_linewidth(2)
                self.ax3.relim() 
                self.ax3.autoscale_view()  
                self.ax3.set_ylim([-20, 25])
                self.canvas.draw()
                self.angle_max_min("Ankle", self.y_history3)
            else:
                self.x_history3_2.append(x)  
                self.y_history3_2.append(y)  

                self.normalize_gait_phases(self.ax3_2, self.line3_2, self.x_history3_2, self.y_history3_2, lower_threshold, upper_threshold)
                
                self.line3_2.set_color('black')
                self.line3_2.set_linewidth(2)
                self.ax3_2.relim() 
                self.ax3_2.autoscale_view()  
                self.ax3_2.set_ylim([-20, 25])
                self.canvas_2.draw()
                self.angle_max_min("Ankle", self.y_history3_2)

            self.ankle_angle_label.setText(f"Current ankle angle: {round(y, 2)}°")

    def view_lines_action_triggered(self, checked):
        self.video_widget.toggle_show_lines(not checked)

    def view_labels_action_triggered(self, checked):
        self.video_widget.toggle_show_labels(not checked)

    def view_bbox_action_triggered(self, checked):
        self.video_widget.toggle_show_bbox(not checked)

    def open_save_dialog(self):

        results_pdf = PdfGen(self.amputee_data.name, self.amputee_data.amputation_level, self.amputee_data.amputated_limb)
        dialog = QDialog()
        dialog.setWindowTitle("Comments")

        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        save_pdf_button = QPushButton("Save PDF")
        save_pdf_button.clicked.connect(lambda: results_pdf.save_as_pdf(text_edit.toPlainText(), dialog))
        layout.addWidget(save_pdf_button)

        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())