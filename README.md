# Gait Analysis Software

## Overview

This project aims to facilitate gait analysis for individuals with lower limb amputations. The primary objective is to detect gait deviations and provide solutions for correction. The software is designed with a user-friendly interface, making it accessible for healthcare professionals involved in the analysis of biomechanics during walking.

## Features

- Real-time visualization of hip, knee, and ankle angles for both left and right legs.
- Gait deviation analysis tailored for lower limb amputees.
- User-friendly interface for intuitive navigation and understanding of gait data.

## Getting Started

## Python 
This code was developed and tested using Python 3.8.10. While it may work with other Python 3 versions, it is recommended to use Python 3.8.10 for optimal compatibility.

Check your Python version by running the script:
```bash
python --version
```

## Object Detection 

### Object Detection Model
The object detection model used in this project was initially trained with [YOLOv3](https://github.com/ultralytics/yolov3). Please note that since the time of the initial training, more efficient versions of the YOLO algorithm have been developed, which may offer improved performance.

## Training Object and Anatomical Points

The object used for training the object detection model is a specific yellow marker. During data collection, it is essential to place this marker at specific anatomical points to ensure accurate detection. The marker should be visible during the majority of the gait sequence.

### Anatomical Points:

1. **Acromium:** Place the yellow marker at the acromium, ensuring it is clearly visible.

2. **Femur:** Position the marker at the femur, maintaining visibility throughout the gait.

3. **Femur Lateral Epicondyle:** Ensure the marker is placed at the lateral epicondyle of the femur for accurate detection.

4. **Tibial Lateral Malleolus vs Metatarsal:** The marker should be visible at the tibial lateral malleolus and the metatarsal region simultaneously.

### Placement Guidelines:

- Carefully position the yellow marker at each anatomical point during data collection.
- Ensure that the marker remains visible for the majority of the gait sequence to facilitate accurate object detection.

These specific placements are crucial for training and evaluating the model's performance. Adjust the camera angle and placement as needed to achieve optimal visibility of the yellow marker at the specified anatomical points.

## Clone the Github repository
```bash
git clone https://github.com/COU7INHO/Gait_Analysis_Software.git
```

## Install the requirements
To install the requirements run the command:
```bash
pip install -r requirements.txt
```

### Database setup
As the database is running locally, when you run the script for the first time, the database will be empty. To test the software effectively, make sure to create some data, patients, in the database.

### Warning
Due to computing limitations, the video analysis may run at a very low FPS rate. Please be aware of potential performance issues and consider running the software on a system with sufficient computational resources.