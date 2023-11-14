import math
from time import time

import cv2
import numpy as np
from backend.markers_detection import MarkerDetection


class MotionAnalysis:
    def __init__(self, cameraID, window_name, n_markers=5):
        self.cameraID = cameraID

        self.window_name = window_name
        self.names = ["Shoulder", "Trochanter", "Knee", "Ankle", "V_Metatarsal"]
        self.n_markers = n_markers
        self.first_ankle_angle = []
        self.angle_stored = False
        self.hip_angles = []
        self.knee_angles = []
        self.ankle_angles = []
        self.counting = 0
        self.counting_LTR = 0

        self.init_angle_ang = None
        self.filtered_ankle_angles = []
        self.direction = "left_to_right"
        self.showLines = True
        self.showLabels = True
        self.showbbox = True

        # *################################
        self.start_point_horizontal = None
        self.end_point_horizontal = None
        self.clicked_horizontal = False
        self.draw_horizontal_line = True

        self.start_point_vertical = None
        self.end_point_vertical = None
        self.clicked_vertical = False
        self.draw_vertical_line = True
        self.new_frame = None

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.handle_mouse_event)

        self.pixel_to_cm_horizontal = None
        self.pixel_to_cm_vertical = None

        self.min_y_vm_list = []
        self.vm_y_value = []
        self.init_stance_phase = False
        self.init_swing_phase = False
        self.stance_frame = None
        self.swing_frame = None

        self.vm_y_value_LTR = []
        self.init_stance_phase_LTR = False
        self.init_swing_phase_LTR = False
        self.stance_frame_LTR = None
        self.swing_frame_LTR = None

        self.fps_rate = 120

    # *######################################

    def draw_line_on_frame(
        self, frame, start_point, end_point, line_length, display=True
    ):
        if display:
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{line_length} cm",
                (start_point[0], start_point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    def handle_mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # Click left button
            if self.clicked_horizontal:
                self.end_point_horizontal = (x, y)
                self.clicked_horizontal = False
            else:
                self.start_point_horizontal = (x, y)
                self.clicked_horizontal = True

        elif event == cv2.EVENT_RBUTTONDOWN:  # Click right button
            if self.clicked_vertical:
                self.end_point_vertical = (x, y)
                self.clicked_vertical = False
            else:
                self.start_point_vertical = (x, y)
                self.clicked_vertical = True

    # *######################################

    def open_camera(self):
        self.camera = cv2.VideoCapture(self.cameraID)
        if not self.camera.isOpened():
            print("Error: Could not open video.")
            exit()

    def init_time(self):
        self.loop_time = time()

    def get_video_frame(self):
        self.success, self.frame = self.camera.read()

        if self.success:
            self.new_frame = self.frame.copy()
        else:
            self.new_frame = None
            print("\nFrame not available\n")

        # Calibrate horizontally
        if (
            self.start_point_horizontal is not None
            and self.end_point_horizontal is not None
            and self.draw_horizontal_line
        ):
            length_horizontal = math.sqrt(
                (self.end_point_horizontal[0] - self.start_point_horizontal[0]) ** 2
                + (self.end_point_horizontal[1] - self.start_point_horizontal[1]) ** 2
            )
            # Calculate the conversion factor from pixels to centimeters horizontally
            real_length_horizontal = 10.32
            self.pixel_to_cm_horizontal = real_length_horizontal / length_horizontal

            self.draw_line_on_frame(
                self.new_frame,
                self.start_point_horizontal,
                self.end_point_horizontal,
                real_length_horizontal,
                display=True,
            )

        # Calibrate vertically
        if (
            self.start_point_vertical is not None
            and self.end_point_vertical is not None
            and self.draw_vertical_line
        ):
            length_vertical = math.sqrt(
                (self.end_point_vertical[0] - self.start_point_vertical[0]) ** 2
                + (self.end_point_vertical[1] - self.start_point_vertical[1]) ** 2
            )

            # Calculate the conversion factor from pixels to centimeters vertically
            real_length_vertical = 4.21
            self.pixel_to_cm_vertical = real_length_vertical / length_vertical

            self.draw_line_on_frame(
                self.new_frame,
                self.start_point_vertical,
                self.end_point_vertical,
                real_length_vertical,
                display=True,
            )

    # *######################################

    def init_tracker(self):
        markerDDetection = MarkerDetection(self.new_frame)
        self.new_frame, self.boxes, self.indexes = markerDDetection.detect()

        self.multiTracker = cv2.legacy.MultiTracker_create()

        for box in self.boxes:
            self.multiTracker.add(cv2.legacy.TrackerCSRT_create(), self.new_frame, box)

    def remove_empty_boxes(self):
        self.boxes = [box for box in self.boxes if np.any(box != [0, 0, 0, 0])]

    def check_markers(self):
        if len(self.boxes) != self.n_markers:
            if self.n_markers - len(self.boxes) == 1:
                cv2.putText(
                    self.new_frame,
                    "1 marker missing",
                    (10, 110),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
            elif self.n_markers - len(self.boxes) == -1:
                cv2.putText(
                    self.new_frame,
                    "1 marker in excess",
                    (10, 110),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
            elif self.n_markers - len(self.boxes) > 1:
                cv2.putText(
                    self.new_frame,
                    f"{int(self.n_markers - len(self.boxes))} markers missing",
                    (10, 110),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
            elif self.n_markers - len(self.boxes) < -1:
                cv2.putText(
                    self.new_frame,
                    f"{abs(int(self.n_markers - len(self.boxes)))} markers in excess",
                    (10, 110),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

            markerDDetection = MarkerDetection(self.new_frame)
            self.new_frame, self.boxes, self.indexes = markerDDetection.detect()

            self.multiTracker = cv2.legacy.MultiTracker_create()

            for box in self.boxes:
                self.multiTracker.add(
                    cv2.legacy.TrackerCSRT_create(), self.new_frame, box
                )
        else:
            cv2.putText(
                self.new_frame,
                "Tracking",
                (10, 110),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (0, 255, 0),
                3,
            )

            self.tracking, self.boxes = self.multiTracker.update(self.new_frame)

    def markers_centers(self):
        self.sorted_centers = []
        self.centers = []

        for i, newbox in enumerate(self.boxes):
            x = int(newbox[0])
            y = int(newbox[1])
            w = int(newbox[2])
            h = int(newbox[3])

            center = (x + w // 2, y + h // 2)
            self.x_coord, self.y_coord = center[0], center[1]
            self.sorted_centers.append(((self.x_coord, self.y_coord), i))
            self.centers.append((center, i))
            if self.showbbox:
                cv2.rectangle(self.new_frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cv2.circle(self.new_frame, center, 6, (255, 0, 0), -1)

    def gait_direction(self):
        if not hasattr(self, "prev_frame"):
            self.prev_frame = self.new_frame.copy()
            return

        # Reduce frame size for better performance
        scale_factor = 0.15

        if self.success:
            resized_prev_frame = cv2.resize(
                self.prev_frame, None, fx=scale_factor, fy=scale_factor
            )
            resized_new_frame = cv2.resize(
                self.new_frame, None, fx=scale_factor, fy=scale_factor
            )

            prev_gray = cv2.cvtColor(resized_prev_frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(resized_new_frame, cv2.COLOR_BGR2GRAY)

            # Calculate optical flow using Farneback method
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray,
                gray,
                None,
                pyr_scale=0.5,
                levels=3,
                winsize=15,
                iterations=3,
                poly_n=5,
                poly_sigma=1.2,
                flags=0,
            )

            # Calculate the mean flow in the x-direction
            mean_flow_x = np.mean(flow[:, :, 0])

            # Set the direction based on the mean flow in the x-direction
            self.direction = "left_to_right" if mean_flow_x > 0 else "right_to_left"

            # Update the previous frame
            self.prev_frame = self.new_frame.copy()

    def get_raw_angles(self, joint1, joint2, joint3):
        # Calculate vectors between the points
        vec1 = (joint2[0] - joint1[0], joint2[1] - joint1[1])
        vec2 = (joint3[0] - joint2[0], joint3[1] - joint2[1])

        # Calculate the dot product of the two vectors
        dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]

        # Calculate the magnitude of the vectors
        magnitude_vec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
        magnitude_vec2 = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)

        if magnitude_vec1 == 0 or magnitude_vec2 == 0:
            return 0.00

        # Calculate the angle in radians
        angle_radians = math.acos(dot_product / (magnitude_vec1 * magnitude_vec2))

        # Convert angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

    def get_filtered_angles(self):
        self.gt_center = []
        self.sorted_centers = sorted(self.sorted_centers, key=lambda x: x[0][1])

        prev_x = 0
        prev_y = 0
        self.time_values = []  # Corresponding time values for each center

        for i, (_, _) in enumerate(self.sorted_centers):
            distance = (
                160  #! Colocar uma parte na GUI para inserir este valor em centímetros
            )
            if prev_x != 0 and prev_y != 0:
                x_gt = self.centers[1][0][0]
                y_gt = self.centers[1][0][1]
                x_le = self.centers[2][0][0]
                y_le = self.centers[2][0][1]
                alpha = np.arctan((x_gt - x_le) / (y_gt - y_le))
                new_x = int(-distance * np.sin(alpha) + x_gt)  #! Atualizar a distancia
                new_y = int(-distance * np.cos(alpha) + y_gt)  #! Atualizar a distancia
                if not self.gt_center:
                    self.gt_center.append((new_x, new_y))

                # * Markers coordinates
                a_marker = (self.centers[0][0][0], self.centers[0][0][1])
                gt_marker = (new_x, new_y)
                le_marker = (self.centers[2][0][0], self.centers[2][0][1])
                lm_marker = (self.centers[3][0][0], self.centers[3][0][1])
                v_m_marker = (self.centers[4][0][0], self.centers[4][0][1])

                hip_ang = self.get_raw_angles(a_marker, gt_marker, le_marker)
                knee_ang = self.get_raw_angles(gt_marker, le_marker, lm_marker)
                ankle_ang = self.get_raw_angles(le_marker, lm_marker, v_m_marker)

                if self.init_angle_ang == None:
                    self.init_angle_ang = ankle_ang

                ankle_ang -= self.init_angle_ang
                self.hip_angles.append(hip_ang)
                self.knee_angles.append(knee_ang)
                self.ankle_angles.append(ankle_ang)

                upper_threshold_hip = 40
                lower_threshold_hip = -20

                upper_threshold_knee = 80
                lower_threshold_knee = -10

                upper_threshold_ankle = 35
                lower_threshold_ankle = -30

                # For hip_angles
                filtered_hip_angles = []
                for angle in self.hip_angles:
                    if lower_threshold_hip <= angle <= upper_threshold_hip:
                        filtered_hip_angles.append(angle)
                self.hip_angles = filtered_hip_angles

                # For knee_angles
                filtered_knee_angles = []
                for angle in self.knee_angles:
                    if lower_threshold_knee <= angle <= upper_threshold_knee:
                        filtered_knee_angles.append(angle)
                self.knee_angles = filtered_knee_angles

                # For ankle_angles
                filtered_ankle_angles = []
                for angle in self.ankle_angles:
                    if lower_threshold_ankle <= angle <= upper_threshold_ankle:
                        filtered_ankle_angles.append(angle)
                self.ankle_angles = filtered_ankle_angles

                cv2.circle(self.new_frame, (new_x, new_y), 10, (0, 0, 255), -1)

            prev_x = self.centers[i][0][0]
            prev_y = self.centers[i][0][1]

        self.counting += 1

    def gait_phases_RTL(self):
        for value in self.sorted_centers:
            marker = value[1]
            if marker == 4:  # Consider the VM marker
                current_frame = int(self.camera.get(cv2.CAP_PROP_POS_FRAMES))
                current_vm_y = value[0][1]

                self.vm_y_value.append(current_vm_y)

                min_y = min(self.vm_y_value)
                max_y = max(self.vm_y_value)

                if not self.init_stance_phase and current_vm_y - min_y == 0:
                    self.init_stance_phase = True
                    if self.stance_frame == None:
                        self.stance_frame = current_frame / self.fps_rate

                if not self.init_swing_phase and max_y - current_vm_y >= 7:
                    self.init_swing_phase = True
                    if self.swing_frame == None:
                        self.swing_frame = current_frame / self.fps_rate

                # * Colocar uma nova variável para acabar a swing phase
                # * quando esta acabar então começa a stance phase outra vez

                self.counting += 1

        return self.stance_frame, self.swing_frame

    def gait_phase_LTR(self):
        for value in self.sorted_centers:
            marker = value[1]
            if marker == 4:  # Consider the VM marker
                current_frame = int(self.camera.get(cv2.CAP_PROP_POS_FRAMES))
                current_vm_y = value[0][1]

                self.vm_y_value_LTR.append(current_vm_y)

                min_y = min(self.vm_y_value_LTR)
                max_y = max(self.vm_y_value_LTR)

                if not self.init_stance_phase_LTR and current_vm_y - min_y == 0:
                    self.init_stance_phase_LTR = True
                    if self.stance_frame_LTR == None:
                        self.stance_frame_LTR = current_frame / self.fps_rate

                if not self.init_swing_phase_LTR and max_y - current_vm_y >= 7:
                    self.init_swing_phase_LTR = True
                    if self.swing_frame_LTR == None:
                        self.swing_frame_LTR = current_frame / self.fps_rate

                # * Colocar uma nova variável para acabar a swing phase
                # * quando esta acabar então começa a stance phase outra vez

                self.counting_LTR += 1

        return self.stance_frame_LTR, self.swing_frame_LTR

    def lines(self):
        if self.showLines:
            points = []
            for i in range(len(self.centers)):
                if i == 1:
                    continue
                x, y = self.centers[i][0][0], self.centers[i][0][1]
                points.append((x, y))

            for center in self.gt_center:
                points.append((center[0], center[1]))

            points.sort(key=lambda point: point[1])
            unique_points = {}
            for point in points:
                if point not in unique_points:
                    unique_points[point] = point

            self.unique_points_list = list(unique_points.values())

            for i in range(1, len(points)):
                cv2.line(self.new_frame, points[i], points[i - 1], (0, 255, 0), 3)

    def labels(self):
        if self.showLabels:
            for idx, point in enumerate(self.unique_points_list):
                if idx < len(self.names):
                    name = self.names[idx]

                x = point[0]
                y = point[1]
                cv2.putText(
                    self.new_frame,
                    f"{name}",
                    (x, y - 20),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

    def end_time(self):
        self.fps = 1 / (time() - self.loop_time)
        self.loop_time = time()
        cv2.putText(
            self.new_frame,
            f"FPS: {str(round(self.fps, 2))}",
            (10, 50),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (255, 0, 0),
            3,
        )

    def display_window(self):
        if self.success:
            if self.new_frame.shape[0] > 0 and self.new_frame.shape[1] > 0:
                cv2.imshow(self.window_name, self.new_frame)
                cv2.waitKey(1)
        else:
            cv2.waitKey(0)
            print("Zero frames available")

    def close_window(self):
        self.camera.release()
        cv2.destroyAllWindows()
