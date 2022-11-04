import cv2
import numpy as np
from start_recording.capture_video import VideoCapture

class DisplayFrames:
    def __init__(self, VideoCaptureObject:VideoCapture):
        self.VideoCaptureObject = VideoCaptureObject
    
    def show(self): 
        _, frames = self.VideoCaptureObject.read()
        frames = np.hstack(frames)
        return cv2.imshow("Frames", frames)