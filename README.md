# Automated Student Face Verification and Attendance System

This project automates student attendance using real-time facial recognition and an Arduino-based physical feedback system. It logs attendance, generates reports, and incorporates environmental sensor data.

## Table of Contents

* [Project Description](#project-description)
* [Features](#features)
* [Hardware Requirements](#hardware-requirements)
* [Software Requirements](#software-requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Repository Structure](#repository-structure)
* [Contributing](#contributing)
* [License](#license)

## Project Description

This system uses a webcam to capture student faces, compares them to a database of registered student images using DeepFace, and records attendance. An Arduino microcontroller provides physical feedback through a servo-driven indicator, LEDs, and a buzzer. It also monitors environmental conditions using an LDR and IR sensors, sending data back to the Python script. Attendance records are stored in an SQLite database and can be exported as an Excel file.

## Features

* Real-time face verification using DeepFace.
* Automated attendance marking (Present, Late, Absent).
* Physical attendance indicator controlled by a servo motor.
* Visual feedback through LEDs (red, green, yellow).
* Audible feedback through a buzzer.
* Environmental monitoring using LDR and IR sensors.
* Data logging to an SQLite database.
* Attendance report generation in Excel format.
* Handling of unknown individuals.
* Sensor failure/success messages.

## Hardware Requirements

* Laptop or desktop computer with a webcam.
* Arduino Uno microcontroller.
* Servo motor.
* LEDs (red, green, yellow).
* Active buzzer.
* LDR (Light Dependent Resistor) sensor.
* IR (Infrared) sensors (2).
* Breadboard and wiring.
* USB cable for Arduino connection.

## Software Requirements

* Python 3.x
* Arduino IDE
* Python Libraries:
    * `opencv-python`
    * `deepface`
    * `pyserial`
    * `numpy`
    * `pandas`
    * `openpyxl`

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd automated-student-attendance-system
    ```
2.  **Install Python Dependencies:**
    ```bash
    pip install -r python/requirements.txt
    ```
3.  **Prepare Student Images:**
    * Place student images in the `registered_faces/` directory.
    * Ensure images are in `.jpg`, `.jpeg`, or `.png` format.
4.  **Upload Arduino Code:**
    * Open the `arduino/attendance_system.ino` file in the Arduino IDE.
    * Connect your Arduino Uno to your computer.
    * Select the correct board and port in the Arduino IDE (Tools > Board, Tools > Port).
    * Upload the code to your Arduino.
5.  **Wiring:**
    * Connect the servo, LEDs, buzzer, LDR, and IR sensors to the Arduino according to the pin assignments in the `arduino/attendance_system.ino` code.

## Usage

1.  **Run the Python Script:**
    ```bash
    python python/face_attendance.py
    ```
2.  **Student Interaction:**
    * Students approach the webcam.
    * The system will capture their faces and perform verification.
    * The Arduino will provide physical and audible feedback.
3.  **Attendance Report:**
    * After the script is terminated, an Excel file named `attendance_report.xlsx` will be generated in the project's root directory.

## Repository Structure
