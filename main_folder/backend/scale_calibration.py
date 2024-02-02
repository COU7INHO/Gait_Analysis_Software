"""
PixelToCentimeter Class

This class defines a PixelToCentimeter object for calibrating pixel-to-centimeter conversion in a video stream using user-drawn lines.

Dependencies:
- cv2: OpenCV library for computer vision.
- math: Python standard library for mathematical operations.

Attributes:
- camera_index: Index of the camera to be used for video capture (default is 0).
- camera: VideoCapture object for accessing the camera feed.
- start_point_horizontal, end_point_horizontal: Points defining the horizontal calibration line.
- clicked_horizontal: Flag indicating whether the horizontal line is being clicked.
- draw_horizontal_line: Flag indicating whether to draw the horizontal calibration line.
- start_point_vertical, end_point_vertical: Points defining the vertical calibration line.
- clicked_vertical: Flag indicating whether the vertical line is being clicked.
- draw_vertical_line: Flag indicating whether to draw the vertical calibration line.
- frame_with_line: Copy of the frame with drawn calibration lines.
- pixel_to_cm_horizontal, pixel_to_cm_vertical: Pixel-to-centimeter conversion factors for horizontal and vertical lines.

Note: Integration with PyQt5 GUI is needed for better interaction and visualization.
"""

import math

import cv2


class PixelToCentimeter:
    def __init__(self, camera_index=0):
        """
        Initializes the PixelToCentimeter object.

        Parameters:
        - camera_index (int): Index of the camera to be used for video capture (default is 0).
        """
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            print("Error: Could not open video.")
            exit()

        self.start_point_horizontal = None
        self.end_point_horizontal = None
        self.clicked_horizontal = False
        self.draw_horizontal_line = True

        self.start_point_vertical = None
        self.end_point_vertical = None
        self.clicked_vertical = False
        self.draw_vertical_line = True
        self.frame_with_line = None

        cv2.namedWindow("Video with Line")
        cv2.setMouseCallback("Video with Line", self.handle_mouse_event)

        self.pixel_to_cm_horizontal = None
        self.pixel_to_cm_vertical = None

    def draw_line_on_frame(
        self, frame, start_point, end_point, line_length, display=True
    ):
        """
        Draws a calibration line on the frame and displays its length in centimeters.
        """
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
        """
        Handles mouse events for defining calibration lines.
        """
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

    def run(self):
        """
        Runs the calibration process, allowing the user to draw horizontal and vertical lines.
        """
        while True:
            ret, frame = self.camera.read()

            if not ret:
                break

            frame_height, frame_width, _ = frame.shape

            frame_with_line = frame.copy()

            # Calibrate horizontally
            if (
                self.start_point_horizontal is not None
                and self.end_point_horizontal is not None
                and self.draw_horizontal_line
            ):
                length_horizontal = math.sqrt(
                    (self.end_point_horizontal[0] - self.start_point_horizontal[0]) ** 2
                    + (self.end_point_horizontal[1] - self.start_point_horizontal[1])
                    ** 2
                )
                # Calculate the conversion factor from pixels to centimeters horizontally
                real_length_horizontal = 10
                self.pixel_to_cm_horizontal = real_length_horizontal / length_horizontal

                self.draw_line_on_frame(
                    frame_with_line,
                    self.start_point_horizontal,
                    self.end_point_horizontal,
                    real_length_horizontal,
                    display=True,
                )
                print(f"\n Width cm = {frame_width * self.pixel_to_cm_horizontal}")

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
                real_length_vertical = 5
                self.pixel_to_cm_vertical = real_length_vertical / length_vertical

                self.draw_line_on_frame(
                    frame_with_line,
                    self.start_point_vertical,
                    self.end_point_vertical,
                    real_length_vertical,
                    display=True,
                )
                print(f"\n Height cm = {frame_height * self.pixel_to_cm_vertical}")

            cv2.imshow("Video with Line", frame_with_line)

            key = cv2.waitKey(1)

            if key == 13:  # 13 is the ASCII code for the Enter key
                self.draw_horizontal_line = self.draw_vertical_line = False

            if key & 0xFF == ord("q"):  # Exit the loop if 'q' key is pressed
                break

        self.camera.release()
        cv2.destroyAllWindows()

    def get_pixel_to_cm_conversion_horizontal(self):
        """
        Returns the pixel-to-centimeter conversion factor for horizontal calibration.
        """
        return self.pixel_to_cm_horizontal

    def get_pixel_to_cm_conversion_vertical(self):
        """
        Returns the pixel-to-centimeter conversion factor for vertical calibration.
        """
        return self.pixel_to_cm_vertical


# Usage
if __name__ == "__main__":
    pixel_to_cm_calibrator = PixelToCentimeter()
    pixel_to_cm_calibrator.run()
    pixel_to_cm_calibrator.get_pixel_to_cm_conversion_horizontal()
    pixel_to_cm_calibrator.get_pixel_to_cm_conversion_vertical()()
