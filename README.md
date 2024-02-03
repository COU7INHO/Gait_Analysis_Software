# Lower Limb Amputee Gait Analysis Software

## Overview

This project aims to facilitate gait analysis for individuals with lower limb amputations. The primary objective is to detect gait deviations and provide solutions for correction. The software is designed with a user-friendly interface, making it accessible for healthcare professionals involved in the analysis of biomechanics during walking.

## Features

- Real-time visualization of hip, knee, and ankle angles for both left and right legs.
- Gait deviation analysis tailored for lower limb amputees.
- User-friendly interface for intuitive navigation and understanding of gait data.

## Getting Started

### Prerequisites

- Python 3.8.10
- Required Python packages (specified in requirements.txt)

Before running the script, ensure that you have PostgreSQL installed on your system. Additionally, create the following table in your PostgreSQL database to store patient data:

```sql
CREATE TABLE patient (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    amputation_level VARCHAR(50) NOT NULL,
    amputated_limb VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    district VARCHAR(50) NOT NULL
);
```

### Github Repository

```bash
git clone https://github.com/COU7INHO/Gait_Analysis_Software.git
```

### Warning
Due to computing limitations, the video analysis may run at a very low FPS rate. Please be aware of potential performance issues and consider running the software on a system with sufficient computational resources.