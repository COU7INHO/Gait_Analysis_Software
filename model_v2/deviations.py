
from main_gui import MainWindow


class GaitDeviation(MainWindow):
    def __init__(self):
        super().__init__()
        self.gait_direction = self.video_widget.init_video.direction

    def gait_phases_time(self):
        pass
