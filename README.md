# Lower Limb Amputee Gait Analysis Software

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