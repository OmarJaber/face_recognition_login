import cv2
import numpy as np
import os
import frappe
from frappe.auth import LoginManager

def verify_face(user_email, **kwargs):
    # Ensure the folder path in ERPNext files directory
    files_path = frappe.get_site_path('public', 'files', 'User Face Models')
    user_folder = os.path.join(files_path, user_email)
    
    # Check if the user's folder exists
    if not os.path.exists(user_folder):
        return { "message": "Face images not found for this user." }
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return { "message": "Failed to open camera." }

    # Initialize the face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            continue
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Extract the face region from the frame and resize it
            face_region = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_region, (100, 100))
            
            # Compare the captured face with the stored face models in user's folder
            for filename in sorted(os.listdir(user_folder)):
                if filename.endswith('.jpg'):
                    image_path = os.path.join(user_folder, filename)
                    stored_face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    
                    # Resize stored_face to match face_resized dimensions
                    stored_face_resized = cv2.resize(stored_face, (100, 100))
                    
                    # Compare the resized faces
                    similarity = calculate_similarity(face_resized, stored_face_resized)
                    cv2.putText(frame, f"Similarity: {similarity:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
                    if similarity > 0.95:  # Example threshold (95% similarity)
                        cap.release()
                        cv2.destroyAllWindows()
                        
                        # Log the user in
                        # login_manager = LoginManager()
                        # login_manager.user = user_email
                        # login_manager.post_login()
                        
                        # Prepare JSON response for success
                        return { "message": "Face verified successfully." }
        
        # Display the frame with rectangles and similarity text
        cv2.imshow('Face Recognition', frame)
        
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Prepare JSON response for failure
    return { "message": "Face verification failed." }

def calculate_similarity(face1, face2):
    # Implement your face comparison logic here
    # Example: Calculate similarity using MSE or other techniques
    mse = ((face1 - face2) ** 2).mean()
    similarity = 1 - mse / 255.0  # Normalize to a similarity score (0-1)
    return similarity


