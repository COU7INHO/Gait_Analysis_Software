import cv2
from motionAnalysis_class import MotionAnalysis

obj = MotionAnalysis("/Users/tiagocoutinho/Desktop/videos/ciclo.mov", "video")

obj.open_camera()
obj.init_time()
obj.get_video_frame()
obj.init_tracker()

while True:
    obj.get_video_frame()
    obj.remove_empty_boxes()
    obj.check_markers()
    obj.markers_centers()
    obj.gait_direction()
    obj.get_filtered_angles()
    obj.lines()
    obj.labels()
    obj.end_time()
    obj.display_window()

    if cv2.waitKey(1) == ord("q"):
        break

obj.close_window()
