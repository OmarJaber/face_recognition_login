# collect_face_model.py

import cv2
import os
import shutil
import frappe

def collect_face_model(user_email):
    # Ensure the folder path in ERPNext files directory
    files_path = frappe.get_site_path('public', 'files', 'User Face Models')
    user_folder = os.path.join(files_path, user_email)
    
    # Create the directory if it doesn't exist

    if os.path.exists(user_folder):
        # Folder exists, remove existing images and collect new ones
        shutil.rmtree(user_folder)
        action_message = f'Model images for {user_email} already exist and have been replaced with new images.'
    else:
        action_message = f'Model images collected and saved for {user_email}'

    os.makedirs(user_folder, exist_ok=True)
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Collect frames from the video
    frame_count = 0
    while frame_count < 50:  # Capture 50 frames
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Extract the face region
            face = gray[y:y+h, x:x+w]

            # Save each detected face as an image file
            file_name = f'{user_email}_{frame_count}.jpg'  # Unique filename
            file_path = os.path.join(user_folder, file_name)
            cv2.imwrite(file_path, face)
        
            frame_count += 1  # Increment frame count after saving each image
            
            if frame_count >= 50:  # Exit the loop once 50 frames are captured
                break
    
    cap.release()
    cv2.destroyAllWindows()

    return action_message

# Example usage
# collect_face_model('omar.ja93@gmail.com')
