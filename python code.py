import cv2
from deepface import DeepFace
import serial
import time
import os
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Serial Port Setup (Adjust as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # serial port for arduino

# 2. Registered Faces Directory
registered_faces_dir = "registered_faces"

# 3. Database Setup
def create_tables():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE,
            face_encoding BLOB
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            attendance_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_student(student_name, face_encoding):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO students (student_name, face_encoding)
            VALUES (?, ?)
        ''', (student_name, face_encoding))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Student {student_name} already exists.")
    finally:
        conn.close()

def record_attendance(student_name, status):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT student_id FROM students WHERE student_name = ?
    ''', (student_name,))
    student_id_result = cursor.fetchone()

    if student_id_result:
        student_id = student_id_result[0]
        cursor.execute('''
            INSERT INTO attendance (student_id, status)
            VALUES (?, ?)
        ''', (student_id, status))
        conn.commit()
    else:
        print(f"Student {student_name} not found in database.")
    conn.close()

# Call create_tables to initialize the database
create_tables()

# Add "Unknown" student to the database
add_student("Unknown", b'unknown_face_encoding')

# 4. Image Resizing Function
def resize_images(directory, target_size=(224, 224)):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            img = cv2.imread(image_path)
            if img is not None:
                resized_img = cv2.resize(img, target_size)
                cv2.imwrite(image_path, resized_img)

# Resize images before running face verification
resize_images(registered_faces_dir)

# 5. Function to Verify Face
def verify_face(webcam_image):
    best_match = None
    best_similarity = 1.0  # Initialize with a high value (lower is better)

    for filename in os.listdir(registered_faces_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            registered_image_path = os.path.join(registered_faces_dir, filename)

            try:
                result = DeepFace.verify(img1_path=registered_image_path, img2_path=webcam_image, model_name='Facenet512')
                if result['verified']:
                    similarity = result['cosine_similarity']
                    if similarity < best_similarity:
                        best_similarity = similarity
                        best_match = filename
            except ValueError as e:
                print(f"Error processing {filename}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred processing {filename}: {e}")

    return best_match, best_similarity

# 6. Webcam Capture and Verification Loop
cap = cv2.VideoCapture(0)  # 0 for default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam Feed", frame)

    # Save the captured frame
    cv2.imwrite("captured_face.jpg", frame)

    # Verify Face
    match, similarity = verify_face("captured_face.jpg")

    # 7. Serial Communication and Attendance Logic
    if match and similarity <= 0.3:  # Adjust threshold as needed
        student_name = match.split('.')[0]
        record_attendance(student_name, "Present")
        print(f"Face matched: {match}, Similarity: {similarity}, Attendance Recorded: Present")
        ser.write(b'P')  # Present
    elif match and similarity <= 0.4:  # Late if the similarity is a little worse.
        student_name = match.split('.')[0]
        record_attendance(student_name, "Late")
        print(f"Face matched late: {match}, Similarity: {similarity}, Attendance Recorded: Late")
        ser.write(b'L')  # Late
    elif match is None:
        record_attendance("Unknown", "Absent")
        print("No face detected, Attendance Recorded: Absent")
        ser.write(b'A')
    else:
        record_attendance("Unknown", "Absent")
        print("Face not recognized, Attendance Recorded: Absent")
        ser.write(b'A')  # Absent

    os.remove("captured_face.jpg")  # remove temporary file.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()

# 8. Export Attendance to XLSX
def export_attendance_to_xlsx(filename="attendance_report.xlsx"):
    conn = sqlite3.connect('attendance.db')
    query = """
    SELECT students.student_name, attendance.attendance_time, attendance.status
    FROM attendance
    JOIN students ON attendance.student_id = students.student_id
    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(filename, index=False)
    conn.close()
    print(f"Attendance report exported to {filename}")

# Export the attendance data to an Excel file
export_attendance_to_xlsx()