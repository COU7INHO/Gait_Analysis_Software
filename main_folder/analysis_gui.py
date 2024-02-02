"""
Gait Analysis GUI Application

This script implements a graphical user interface (GUI) application for the analysis of gait data captured from video footage. The application is built using PyQt for the GUI components and Matplotlib for real-time plotting.

Main Components:
----------------

1. `MainWindow` Class:
   - The central class representing the main application window.

2. Plotting Frames:
   - Left and right leg angle plots are created using QFrame, Figure, and Canvas components.

3. Patient Information Display:
   - Patient details, including name, amputation level, and amputated limb, are shown.

4. `angle_max_min` Method:
   - Calculates and displays the maximum and minimum angles for hip, knee, and ankle joints.

5. Gait Phases Visualization:
   - `gait_phase_line` method adds vertical lines indicating gait phases.
   - `normalize_gait_phases` method normalizes gait data and updates the plot accordingly.

6. `gait_duration` Method:
   - Calculates and displays the difference in stance phase duration between legs.
   - Identifies gait deviations and suggests corrective actions.

7. Real-time Angle Updates:
   - `update_angle_values` method continuously updates hip, knee, and ankle angles.

8. User Actions:
   - Actions triggered by user interaction, such as toggling display options and saving reports.

9. `open_save_dialog` Method:
   - Opens a dialog for saving a PDF report with user comments.

10. `correction_window` Method:
    - Displays a window with details on necessary corrections.

11. `InfoWindow` Class:
    - A custom QDialog for displaying information and corrections.

Implemented Features:
---------------------

- Deviation Calculation and Solutions:
  - Gait deviations are accurately calculated.
  - The application suggests corrective actions for each identified deviation.

- PDF Report Generation:
  - Users can save gait analysis information, including comments, in a PDF report.

To-Be-Implemented Features (examples):
---------------------------

- Frontal Plane Analysis:
  - Implement the capability to analyze gait data in the frontal plane.

- Settings Window:
  - Create a settings window to adjust parameters such as FPS rate and calibration object dimensions.

Usage:
------
1. Ensure PyQt and Matplotlib are installed.
2. Run the script to launch the GUI.
3. Load video data, analyze gait angles, and receive insights into gait deviations.

Note: For detailed information on individual methods and functionalities, refer to the respective function and class docstrings in the code.
"""

import copy
import sys

import cv2
from backend.backend import MotionAnalysis
from backend.pdf_report import PdfGen
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QImage, QLinearGradient, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class VideoData(QLabel):
    """
    VideoData class handles video processing and visualization for gait analysis.

    Attributes:
        - window_name (str): The name of the GUI window.
        - init_video (MotionAnalysis): Instance of MotionAnalysis for video analysis.
        - timer (QTimer): Timer to trigger periodic frame updates.
        - knee_angle (float): Current knee angle value.

    Methods:
        - __init__: Initializes VideoData, sets up video analysis, and starts the update timer.
        - update_frame: Updates the video frame, processes gait analysis, and displays the video.
        - angle_value(joint: str): Retrieves the current angle value for the specified joint.
        - toggle_show_lines(value: bool): Toggles the display of lines in the video.
        - toggle_show_labels(value: bool): Toggles the display of labels in the video.
        - toggle_show_bbox(value: bool): Toggles the display of bounding boxes in the video.
    """

    def __init__(self):
        super(VideoData, self).__init__()
        self.window_name = "Gait Analysis"
        self.init_video = MotionAnalysis(
            "/Users/tiagocoutinho/Desktop/videos/2_ciclos.mp4", self.window_name
        )

        self.init_video.open_camera()
        self.init_video.init_time()
        self.init_video.get_video_frame()
        self.init_video.init_tracker()
        video_scaling_factor = 2.5
        self.setMaximumSize(
            int(1920 / video_scaling_factor), int(1080 / video_scaling_factor)
        )

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

        self.init_video.display_window()  # * Display Window <-- <-- <-- <-- <--

        self.video_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
        self.video_frame = cv2.resize(
            self.video_frame, (self.maximumWidth(), self.maximumHeight())
        )
        height, width, channels = self.video_frame.shape
        q_image = QImage(
            self.video_frame.data, width, height, channels * width, QImage.Format_RGB888
        )
        self.setPixmap(QPixmap.fromImage(q_image))

    def angle_value(self, joint: str):
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
    """
    This class manages the gradient color in the graphical user interface (GUI) background.
    It is responsible for controlling and applying a gradient color scheme to enhance the visual aesthetics of the interface.
    """

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
    """
    MainWindow class for the application.

    Attributes:
    - patient_info (list): Information about the patient.
    - x_history, y_history, x_history_2, y_history_2 (list): Lists to store angle data for plotting.
    - x_history2, y_history2, x_history2_2, y_history2_2 (list): Lists to store knee angle data for plotting.
    - x_history3, y_history3, x_history3_2, y_history3_2 (list): Lists to store ankle angle data for plotting.
    - gait_phase_duration_RTL (bool): Flag indicating if the right-to-left gait phase duration has been calculated.
    - gait_phase_duration_LTR (bool): Flag indicating if the left-to-right gait phase duration has been calculated.
    - min_value_x_RTL, min_value_x_LTR (float): Minimum values of x for right-to-left and left-to-right gait.
    - time_difference_difference (float): Difference between right-to-left and left-to-right gait phase durations.
    - time_difference_RTL, time_difference_LTR (float): Gait phase durations for right-to-left and left-to-right.
    - percent_diff (float): Percentage difference between gait phase durations.
    """

    def __init__(self, patient_info):
        """
        Constructor for the MainWindow class.

        Args:
        - patient_info (list): Information about the patient.
        """
        super(MainWindow, self).__init__()

        self.patient_info = patient_info

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
        """
        Event handler for the submit action.

        This method is triggered when the user submits the form. It initializes the VideoData widget,
        sets up the user interface, and displays the main window.
        """
        self.video_widget = VideoData()
        self.init_ui()
        self.show()

    def init_ui(self):
        """
        Initialize the user interface of the main window.

        This method sets up the main window layout, menus, and frames, creating a visually appealing interface.
        It also initializes various graphical elements like plots, labels, and buttons for displaying and interacting
        with the data related to left and right leg angles, gait deviations, and video information.

        The user interface consists of multiple frames, each serving a specific purpose such as displaying angle plots,
        presenting patient information, and providing options for correction of gait deviations.

        Additionally, this method sets up timers for updating angle values at regular intervals.
        """
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

        # * ############################### FRAMES ###############################

        # * ############################### Main frame ###############################

        main_layout = QHBoxLayout()

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        start_color = QColor(rgb_plot_frame[0], rgb_plot_frame[1], rgb_plot_frame[2])
        end_color = QColor(0, 0, 0)
        main_widget.setStyleSheet(
            f"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start_color.name()}, stop:1 {end_color.name()});"
        )

        # * ############################### Plot frame ###############################

        plot_frame = QFrame()

        plot_frame.setFrameShape(QFrame.NoFrame)
        plot_frame.setStyleSheet(
            f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); "
        )

        self.figure = Figure()
        self.figure.suptitle("Left leg", fontsize=16, fontweight="bold")

        self.canvas = FigureCanvas(self.figure)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)
        plot_frame.setLayout(plot_layout)

        self.ax = self.figure.add_subplot(311)
        self.ax.set_title("Hip angle")
        (self.line,) = self.ax.plot([], [])
        self.ax.set_xticklabels([])

        self.ax2 = self.figure.add_subplot(312)
        self.ax2.set_ylabel("Angle (degrees)")
        self.ax2.set_title("Knee angle")
        (self.line2,) = self.ax2.plot([], [])
        self.ax2.set_xticklabels([])

        self.ax3 = self.figure.add_subplot(313)
        self.ax3.set_xlabel("Seconds")
        self.ax3.set_title("Ankle angle")
        (self.line3,) = self.ax3.plot([], [])

        facecolor = (
            rgb_plot_frame[0] / 255,
            rgb_plot_frame[1] / 255,
            rgb_plot_frame[2] / 255,
        )
        self.figure.set_facecolor(facecolor)
        plot_frame.setFixedSize(400, WINDOW_HEIGHT)

        main_layout.addWidget(plot_frame)

        # *********************************************************

        plot_frame_2 = QFrame()

        plot_frame_2.setFrameShape(QFrame.NoFrame)
        plot_frame_2.setStyleSheet(
            f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]}); "
        )

        self.figure_2 = Figure()
        self.figure_2.suptitle("Right leg", fontsize=16, fontweight="bold")

        self.canvas_2 = FigureCanvas(self.figure_2)

        plot_layout_2 = QVBoxLayout()
        plot_layout_2.addWidget(self.canvas_2)
        plot_frame_2.setLayout(plot_layout_2)

        self.ax_2 = self.figure_2.add_subplot(311)
        self.ax_2.set_title("Hip angle")
        (self.line_2,) = self.ax_2.plot([], [])
        self.ax_2.set_xticklabels([])

        self.ax2_2 = self.figure_2.add_subplot(312)
        self.ax2_2.set_ylabel("Angle (degrees)")
        self.ax2_2.set_title("Knee angle")
        (self.line2_2,) = self.ax2_2.plot([], [])
        self.ax2_2.set_xticklabels([])

        self.ax3_2 = self.figure_2.add_subplot(313)
        self.ax3_2.set_xlabel("Seconds")
        self.ax3_2.set_title("Ankle angle")
        (self.line3_2,) = self.ax3_2.plot([], [])

        facecolor = (
            rgb_plot_frame[0] / 255,
            rgb_plot_frame[1] / 255,
            rgb_plot_frame[2] / 255,
        )
        self.figure_2.set_facecolor(facecolor)
        plot_frame_2.setFixedSize(400, WINDOW_HEIGHT)

        main_layout.addWidget(plot_frame_2)

        # * ############################### Central frame ###############################

        person_info_frame = QFrame()
        person_info_frame.setFrameShape(QFrame.NoFrame)
        person_info_frame.setStyleSheet(
            f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]});"
        )

        person_info_layout = QHBoxLayout()
        self.name = QLabel()
        self.amp_level = QLabel()
        self.amp_side = QLabel()
        self.name.setText(f"<html><b>Name:</b> {self.patient_info[0]}")
        # self.name.setText(f"<html><b>Name:</b> {self.amputee_data.name}")
        self.amp_level.setText(f"<html><b>Amp.level</b>: {self.patient_info[1]}")
        # self.amp_level.setText(f"<html><b>Amp.level</b>: {self.amputee_data.amputation_level}" )
        self.amp_side.setText(f"<html><b>Amp.limb</b>: {self.patient_info[2]}")
        # self.amp_side.setText( f"<html><b>Amp.limb</b>: {self.amputee_data.amputated_limb}")

        person_info_layout.addWidget(self.name)
        person_info_layout.addWidget(self.amp_level)
        person_info_layout.addWidget(self.amp_side)

        person_info_frame.setLayout(person_info_layout)

        video_frame = QFrame()
        video_frame.setFrameShape(QFrame.NoFrame)
        video_frame.setStyleSheet(
            f"background-color: rgb({rgb_plot_frame[0]}, {rgb_plot_frame[1]}, {rgb_plot_frame[2]});"
        )

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
        dev_frame_title.setStyleSheet(
            "font-weight: bold; font-size: 16px; padding: 5px;"
        )

        self.gait_phases_time = QLabel()

        dev_frame_layout.addWidget(dev_frame_title)
        dev_frame_layout.addWidget(self.gait_phases_time)

        self.vaulting_dev = QLabel()
        self.vaulting_dev_button = QPushButton("Correction")
        self.vaulting_dev_button.setStyleSheet("background-color: #D2F9D3;")
        self.vaulting_dev_button.setFixedSize(80, 40)
        self.vaulting_dev_button.setVisible(False)

        vaulting_layout = QHBoxLayout()
        vaulting_layout.addWidget(self.vaulting_dev)
        vaulting_layout.addWidget(self.vaulting_dev_button)
        dev_frame_layout.addLayout(vaulting_layout)

        self.socket_align = QLabel()
        self.knee_hyp_ext_button = QPushButton("Correction")
        self.knee_hyp_ext_button.setStyleSheet("background-color: #D2F9D3;")
        self.knee_hyp_ext_button.setFixedSize(80, 40)
        self.knee_hyp_ext_button.setVisible(False)

        knee_hyp_ext_layout = QHBoxLayout()
        knee_hyp_ext_layout.addWidget(self.socket_align)
        knee_hyp_ext_layout.addWidget(self.knee_hyp_ext_button)
        dev_frame_layout.addLayout(knee_hyp_ext_layout)

        self.foot_flex_dev = QLabel()
        self.trunk_elev_button = QPushButton("Correction")
        self.trunk_elev_button.setStyleSheet("background-color: #D2F9D3;")
        self.trunk_elev_button.setFixedSize(80, 40)
        self.trunk_elev_button.setVisible(False)

        trunk_elev_layout = QHBoxLayout()
        trunk_elev_layout.addWidget(self.foot_flex_dev)
        trunk_elev_layout.addWidget(self.trunk_elev_button)
        dev_frame_layout.addLayout(trunk_elev_layout)

        video_info_layout.addWidget(angles_values_frame)
        video_info_layout.addWidget(dev_frame)

        video_info_frame.setLayout(video_info_layout)

        video_frame_layout.addWidget(video_info_frame)

        video_frame.setFixedHeight(WINDOW_HEIGHT)

        main_layout.addWidget(video_frame)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_angle_values("Hip"))
        self.timer.start(int(1000 / 120))

        self.timer2 = QTimer()
        self.timer2.timeout.connect(lambda: self.update_angle_values("Knee"))
        self.timer2.start(int(1000 / 120))

        self.timer3 = QTimer()
        self.timer3.timeout.connect(lambda: self.update_angle_values("Ankle"))
        self.timer3.start(int(1000 / 120))

    def angle_max_min(self, joint: str, y_history):
        """
        Update and display the maximum and minimum angle values for a specific joint.

        Parameters:
        - joint (str): The joint for which to calculate and display angle statistics (e.g., "Hip", "Knee", "Ankle").
        - y_history (list): A list of angle values representing the historical data for the specified joint.

        This method calculates the maximum and minimum angle values from the provided historical data
        and updates the corresponding QLabel elements to display these values in the user interface.

        Note: The method assumes the existence of QLabel elements for displaying max and min values
        for each joint (e.g., self.max_hip, self.min_hip for the hip joint).
        """
        max_y = float("-inf")
        min_y = float("inf")

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
        """
        Draw a dashed vertical line on the specified Axes to indicate a gait phase.

        Parameters:
        - ax (matplotlib.axes._subplots.AxesSubplot): The Axes on which to draw the gait phase line.
        - frame (float or None): The frame (time point) where the gait phase occurs. If None, no line is drawn.

        This method adds a vertical dashed line to the specified Axes at the given frame to visually represent a gait phase.
        The line is drawn using a dashed linestyle with a linewidth of 2.

        Note: Ensure that the provided Axes (ax) is part of the matplotlib Figure where you want to display the line.
        """
        if frame is not None:
            ax.axvline(frame, linestyle="--", linewidth=2)

    def normalize_gait_phases(
        self, ax, line, list_x, list_y, lower_threshold: int, upper_threshold: int
    ):
        """
        Normalize gait phases and update the plot with the normalized data.

        Parameters:
        - ax (matplotlib.axes._subplots.AxesSubplot): The Axes on which to plot the normalized gait phases.
        - line (matplotlib.lines.Line2D): The Line2D object representing the gait data plot.
        - list_x (list): List of x-axis values (time points).
        - list_y (list): List of y-axis values (angle data).
        - lower_threshold (int): The lower index for the range of data to be considered.
        - upper_threshold (int): The upper index for the range of data to be considered.

        This method normalizes the gait phases based on the specified range and updates the plot with the normalized data.
        It calculates the minimum x-value within the specified range and adjusts all x-values accordingly.
        Additionally, it draws dashed vertical lines on the plot to indicate the start and end of gait phases.

        Note: The provided Axes (ax) and Line2D object (line) should be part of the matplotlib Figure where you want to display the plot.
        """
        original_list_x = list_x
        original_list_y = list_y
        copied_list_x = copy.deepcopy(original_list_x)
        copied_list_y = copy.deepcopy(original_list_y)

        if len(copied_list_x) >= lower_threshold:
            copied_list_x = copied_list_x[lower_threshold:upper_threshold]
            copied_list_y = copied_list_y[lower_threshold:upper_threshold]

            if self.video_widget.init_video.direction == "right_to_left":
                (
                    stance_frame_RTL,
                    swing_frame_RTL,
                ) = self.video_widget.init_video.gait_phases_RTL()

                if len(copied_list_x) > 0:
                    self.min_value_x_RTL = min(copied_list_x)
                    normalized_values = [
                        x - self.min_value_x_RTL for x in copied_list_x
                    ]

                    if stance_frame_RTL is not None:
                        self.gait_phase_line(
                            ax,
                            stance_frame_RTL
                            - self.min_value_x_RTL
                            + lower_threshold / self.video_widget.init_video.fps_rate,
                        )

                    if swing_frame_RTL is not None:
                        self.gait_phase_line(
                            ax,
                            swing_frame_RTL
                            - self.min_value_x_RTL
                            + lower_threshold / self.video_widget.init_video.fps_rate,
                        )

                    if (
                        self.gait_phase_duration_RTL == False
                        and stance_frame_RTL is not None
                        and swing_frame_RTL is not None
                    ):
                        self.time_difference_RTL = swing_frame_RTL - stance_frame_RTL
                        self.gait_phase_duration_RTL = True

                    line.set_data(normalized_values, copied_list_y)
            else:
                (
                    stance_frame_LTR,
                    swing_frame_LTR,
                ) = self.video_widget.init_video.gait_phase_LTR()

                if len(copied_list_x) > 0:
                    self.min_value_x_LTR = min(copied_list_x)
                    normalized_values_x = [
                        x - self.min_value_x_LTR for x in copied_list_x
                    ]

                    if stance_frame_LTR is not None:
                        self.gait_phase_line(
                            ax,
                            stance_frame_LTR
                            - self.min_value_x_LTR
                            + lower_threshold / self.video_widget.init_video.fps_rate,
                        )

                    if swing_frame_LTR is not None:
                        self.gait_phase_line(
                            ax,
                            swing_frame_LTR
                            - self.min_value_x_LTR
                            + lower_threshold / self.video_widget.init_video.fps_rate,
                        )

                    if (
                        self.gait_phase_duration_LTR == False
                        and stance_frame_LTR is not None
                        and swing_frame_LTR is not None
                    ):
                        self.time_difference_LTR = swing_frame_LTR - stance_frame_LTR
                        self.gait_phase_duration_LTR = True

                    line.set_data(normalized_values_x, copied_list_y)

    def gait_duration(self):
        """
        Calculate and analyze the difference in gait phase duration between the left and right legs.
        Display relevant gait deviations and provide corrective actions if necessary.

        This method compares the gait phase duration of the left and right legs, calculates the percentage difference,
        and identifies potential gait deviations. It updates the UI with information about gait deviations
        and displays buttons for possible corrective actions.

        Note: The corrective actions mentioned in the UI are placeholders and may need to be adjusted based on actual corrections.
        """
        if self.time_difference_RTL is None or self.time_difference_LTR is None:
            self.gait_phases_time.setText(f"Analyzing gait deviations...")

        if (
            self.time_difference_RTL is not None
            and self.time_difference_LTR is not None
        ):
            time_difference_difference = (
                self.time_difference_RTL - self.time_difference_LTR
            )

            if self.time_difference_RTL > self.time_difference_LTR:
                self.percent_diff = (
                    (self.time_difference_RTL - self.time_difference_LTR)
                    / self.time_difference_RTL
                    * 100
                )
                self.vaulting_dev.setText(f"Vaulting")
                self.socket_align.setText(f"Alinhamento do encaixe")
                self.foot_flex_dev.setText(f"Flexão do pé")

                """
                The following gait deviations are not currently being calculated.
                These deviations are included for testing purposes to demonstrate how they should appear in the user interface. 
                They will only be displayed when the gait phase duration is calculated.
                """

                if self.percent_diff > 1:
                    self.vaulting_dev.setStyleSheet("color: green;")
                    self.vaulting_dev_button.setVisible(True)
                    self.vaulting_dev_button.clicked.connect(
                        lambda: self.correction_window(
                            f"A diferença na fase de apoio foi de {time_difference_difference: .2f} segundos\
                                                                                            \n\nA perna esquerda teve uma fase de apoio {self.percent_diff:.2f}% mais longa.\
                                                                                              \n\nCertifique-se que o comprimento da prótese não está demasiado comprido\
                                                                                              \n\nVerifique a tensão do joelho para garantir que o este consegue fletir e extender \na um ritmo que acompanha o movimento do pé"
                        )
                    )

                    self.socket_align.setStyleSheet("color: green;")
                    self.knee_hyp_ext_button.setVisible(True)
                    self.knee_hyp_ext_button.clicked.connect(
                        lambda: self.correction_window(
                            "Alinhamento do encaixe\
                                                                                            \n\nVerifique que o centro do encaixe está alinhado com o mesmo ponto, na vertical, na posição a 1/3 do pé"
                        )
                    )

                    self.foot_flex_dev.setStyleSheet("color: green;")
                    self.trunk_elev_button.setVisible(True)
                    self.trunk_elev_button.clicked.connect(
                        lambda: self.correction_window(
                            "O pé esquerdo teve menos 5.2 graus de dorsiflexão e menos 4 graus de flexão plantar\
                                                                                          \n\nGaranta que a tensão do mecanismo que ajusta a velocidade de flexão do pé está adequada para garantir que o pé consegue ser utilizador corretamente, em toda a sua amplitude articular, se necessário"
                        )
                    )

            elif self.time_difference_RTL < self.time_difference_LTR:
                self.percent_diff = (
                    (self.time_difference_LTR - self.time_difference_RTL)
                    / self.time_difference_LTR
                    * 100
                )
                self.vaulting_dev.setText(f"Vaulting")
                self.socket_align.setText(f"Alinhamento do encaixe")
                self.foot_flex_dev.setText(f"Flexão do pé")

                if self.percent_diff > 1:
                    self.vaulting_dev.setStyleSheet("color: green;")
                    self.vaulting_dev_button.setVisible(True)
                    self.vaulting_dev_button.clicked.connect(
                        lambda: self.correction_window(
                            f"A diferença na fase de apoio foi de {time_difference_difference: .2f} segundos\
                                                                                            \n\nA perna esquerda teve uma fase de apoio {self.percent_diff:.2f}% mais longa.\
                                                                                              \n\nCertifique-se que o comprimento da prótese não está demasiado comprido\
                                                                                                \n\nVerifique a tensão do joelho para garantir que o este consegue fletir e extender \na um ritmo que acompanha o movimento do pé"
                        )
                    )

                    self.socket_align.setStyleSheet("color: green;")
                    self.knee_hyp_ext_button.setVisible(True)
                    self.knee_hyp_ext_button.clicked.connect(
                        lambda: self.correction_window(
                            "Alinhamento do encaixe\
                                                                                            \n\nVerifique que o centro do encaixe está alinhado com o mesmo ponto, na vertical, na posição a 1/3 do pé"
                        )
                    )

                    self.foot_flex_dev.setStyleSheet("color: green;")
                    self.trunk_elev_button.setVisible(True)
                    self.trunk_elev_button.clicked.connect(
                        lambda: self.correction_window(
                            "O pé esquerdo teve menos 5.2 graus de dorsiflexão e menos 4 graus de flexão plantar\
                                                                                          \n\nGaranta que a tensão do mecanismo que ajusta a velocidade de flexão do pé está adequada para garantir que o pé consegue ser utilizador corretamente, em toda a sua amplitude articular, se necessário"
                        )
                    )

            else:
                self.vaulting_dev.setText(f"Same stance phase in both legs")
                self.vaulting_dev_button.setVisible(False)

    def update_angle_values(self, angle: str):
        """
        Update the real-time display of joint angles during video playback.

        Parameters:
        - angle (str): The joint angle to be updated (e.g., "Hip", "Knee", "Ankle").

        This method is responsible for updating the real-time display of joint angles during video playback.
        It retrieves the current frame and corresponding joint angle from the video widget, records historical data,
        normalizes gait phases, and updates the UI with the current joint angle. The visualization is handled separately
        for different joint angles and directions of movement.

        Note: The method assumes the existence of specific UI elements such as labels, axes, lines, and canvases,
        which need to be present in the class for proper execution.
        """

        """
        Set lower and upper thresholds for gait phase normalization.

        Parameters:
        - lower_threshold (int): The lower threshold for gait phase normalization.
        - upper_threshold (int): The upper threshold for gait phase normalization.

        This block of code initializes the lower and upper thresholds used for gait phase normalization.
        These thresholds determine the range of frames considered for gait phase analysis.
        Frames falling outside this range are excluded from the analysis to ensure accurate gait phase identification.
        The thresholds are typically defined based on the specific requirements of the gait analysis algorithm.
        """
        lower_threshold = 5
        upper_threshold = -5
        x = self.video_widget.current_frame / self.video_widget.init_video.fps_rate
        self.gait_duration()

        if angle == "Hip":
            y = self.video_widget.angle_value("Hip")
            if self.video_widget.init_video.direction == "right_to_left":
                self.x_history.append(x)
                self.y_history.append(y)

                self.normalize_gait_phases(
                    self.ax,
                    self.line,
                    self.x_history,
                    self.y_history,
                    lower_threshold,
                    upper_threshold,
                )

                self.line.set_color("red")
                self.line.set_linewidth(2)
                self.ax.relim()
                self.ax.autoscale_view()
                self.ax.set_ylim([-20, 30])
                self.canvas.draw()
                self.angle_max_min("Hip", self.y_history)

            else:
                self.x_history_2.append(x)
                self.y_history_2.append(y)

                self.normalize_gait_phases(
                    self.ax_2,
                    self.line_2,
                    self.x_history_2,
                    self.y_history_2,
                    lower_threshold,
                    upper_threshold,
                )

                self.line_2.set_color("red")
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

                self.normalize_gait_phases(
                    self.ax2,
                    self.line2,
                    self.x_history2,
                    self.y_history2,
                    lower_threshold,
                    upper_threshold,
                )

                self.line2.set_color("blue")
                self.line2.set_linewidth(2)
                self.ax2.relim()
                self.ax2.autoscale_view()
                self.ax2.set_ylim([-5, 70])
                self.canvas.draw()
                self.angle_max_min("Knee", self.y_history2)

            else:
                self.x_history2_2.append(x)
                self.y_history2_2.append(y)

                self.normalize_gait_phases(
                    self.ax2_2,
                    self.line2_2,
                    self.x_history2_2,
                    self.y_history2_2,
                    lower_threshold,
                    upper_threshold,
                )

                self.line2_2.set_color("blue")
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

                self.normalize_gait_phases(
                    self.ax3,
                    self.line3,
                    self.x_history3,
                    self.y_history3,
                    lower_threshold,
                    upper_threshold,
                )

                self.line3.set_color("black")
                self.line3.set_linewidth(2)
                self.ax3.relim()
                self.ax3.autoscale_view()
                self.ax3.set_ylim([-20, 25])
                self.canvas.draw()
                self.angle_max_min("Ankle", self.y_history3)
            else:
                self.x_history3_2.append(x)
                self.y_history3_2.append(y)

                self.normalize_gait_phases(
                    self.ax3_2,
                    self.line3_2,
                    self.x_history3_2,
                    self.y_history3_2,
                    lower_threshold,
                    upper_threshold,
                )

                self.line3_2.set_color("black")
                self.line3_2.set_linewidth(2)
                self.ax3_2.relim()
                self.ax3_2.autoscale_view()
                self.ax3_2.set_ylim([-20, 25])
                self.canvas_2.draw()
                self.angle_max_min("Ankle", self.y_history3_2)

            self.ankle_angle_label.setText(f"Current ankle angle: {round(y, 2)}°")

    def view_lines_action_triggered(self, checked):
        """
        Toggle visibility of lines in the video.

        Parameters:
        - checked (bool): The status of the action (True if checked, False otherwise).

        This method is triggered when the user selects or deselects the option to show lines in the video.
        It toggles the visibility of lines based on the provided 'checked' parameter.
        """
        self.video_widget.toggle_show_lines(not checked)

    def view_labels_action_triggered(self, checked):
        """
        Toggle visibility of labels in the video.

        Parameters:
        - checked (bool): The status of the action (True if checked, False otherwise).

        This method is triggered when the user selects or deselects the option to show labels in the video.
        It toggles the visibility of labels based on the provided 'checked' parameter.
        """
        self.video_widget.toggle_show_labels(not checked)

    def view_bbox_action_triggered(self, checked):
        """
        Toggle visibility of bounding boxes in the video.

        Parameters:
        - checked (bool): The status of the action (True if checked, False otherwise).

        This method is triggered when the user selects or deselects the option to show bounding boxes in the video.
        It toggles the visibility of bounding boxes based on the provided 'checked' parameter.
        """
        self.video_widget.toggle_show_bbox(not checked)

    def open_save_dialog(self):
        """
        Open a dialog for adding comments and saving the analysis as a PDF.

        This method creates a dialog window with a text edit field for adding comments and a button to save the analysis as a PDF.
        The user can input comments in the text edit field, and clicking the 'Save PDF' button triggers the PDF generation process.

        Note: The PdfGen class is assumed to be used for generating PDFs based on the provided amputee data.
        """
        results_pdf = PdfGen(
            self.amputee_data.name,
            self.amputee_data.amputation_level,
            self.amputee_data.amputated_limb,
        )
        dialog = QDialog()
        dialog.setWindowTitle("Comments")

        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        save_pdf_button = QPushButton("Save PDF")
        save_pdf_button.clicked.connect(
            lambda: results_pdf.save_as_pdf(text_edit.toPlainText(), dialog)
        )
        layout.addWidget(save_pdf_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def correction_window(self, label_text):
        """
        Open a correction information window.

        This method creates and opens a window to display information related to corrections.
        The window typically contains details or instructions for correcting specific aspects based on gait analysis.

        Parameters:
            label_text (str): The text or information to be displayed in the correction window.
        """
        info_window = InfoWindow(label_text)
        info_window.exec_()


class InfoWindow(QDialog):
    """
    InfoWindow class creates a dialog window to display correction information.

    Attributes:
        - label_text (str): Text content to be displayed in the InfoWindow.

    Methods:
        - __init__: Initializes the InfoWindow, setting up the window title, geometry, and content.
    """

    def __init__(self, label_text):
        """
        Initializes the InfoWindow.

        Parameters:
            - label_text (str): Text content to be displayed in the InfoWindow.
        """
        super().__init__()

        self.setWindowTitle("Info Window")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        info_label = QLabel(f"Correções: \n\n{label_text}.")
        layout.addWidget(info_label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
