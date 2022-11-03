import cv2
import imutils


class VideoCapture:
    def __init__(self, camera_indices, width=600):
        self.camera_indexes = camera_indices
        self.width = width 
        self.cameras = []
        for camera_index in camera_indices:
            self.cameras.append(cv2.VideoCapture(camera_index))

    def read(self, resize = True):
        running = []
        frames = []
        for camera in self.cameras:
            running_aux, frame_aux = camera.read()
            if resize:
                frame_aux = imutils.resize(frame_aux, self.width)
            running.append(running_aux)
            frames.append(frame_aux)
        return running, frames

    def release(self):
        for camera in self.cameras:
            camera.release()