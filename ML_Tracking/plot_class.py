import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from motionAnalysis_class import MotionAnalysis

class MotionAnalysisGUI(QWidget):
    def __init__(self, video_source, window_title):
        super(MotionAnalysisGUI, self).__init__()

        self.obj = MotionAnalysis(video_source, window_title)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        self.obj.getFrame()
        self.obj.removeEmptyBoxes()
        self.obj.checkMarkers()
        self.obj.getCenters()
        self.obj.calcAngles()
        self.obj.timeStop()

        frame = self.obj.displayWindow()
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.timer.stop()
        self.obj.closeWindow()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Replace video_source and window_title with appropriate values
    video_source = "/Users/tiagocoutinho/Desktop/videos/espelho.mov"  # or 0 for camera
    window_title = "Motion Analysis"
    window = MotionAnalysisGUI(video_source, window_title)
    window.show()

    sys.exit(app.exec_())
