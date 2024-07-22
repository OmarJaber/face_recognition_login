import cv2
import numpy as np
import os
import frappe
from frappe.auth import LoginManager
import time

def verify_face():
    try:
        # Ensure the folder path in ERPNext files directory
        files_path = frappe.get_site_path('public', 'files', 'Users Face Model')
        print(f"Files path: {files_path}")

        # Initialize the camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {"status": "error", "message": "Failed to open camera."}

        # Initialize the face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        face_verified = False
        face_detected = False

        start_time = time.time()  # Record the start time

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame.")
                continue

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(f"Detected faces: {len(faces)}")

            if len(faces) > 0:
                face_detected = True

            for (x, y, w, h) in faces:
                try:
                    # Draw a rectangle around the detected face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Extract the face region from the frame and resize it
                    face_region = gray[y:y+h, x:x+w]
                    face_resized = cv2.resize(face_region, (200, 200))
                    print(f"Processing face region of size: {face_resized.shape}")

                    # Compare the captured face with the stored face models
                    for npz_file in sorted(os.listdir(files_path)):
                        if npz_file.endswith('_faces.npz'):
                            npz_path = os.path.join(files_path, npz_file)
                            print(f"Loading data from: {npz_path}")
                            data = np.load(npz_path)
                            stored_faces = data['faces']
                            print(f"Loaded stored faces of shape: {stored_faces.shape}")

                            for stored_face in stored_faces:
                                stored_face_resized = cv2.resize(stored_face, (200, 200))

                                # Compare the resized faces
                                similarity = calculate_similarity(face_resized, stored_face_resized)
                                print(f"Similarity: {similarity:.2f}")

                                if similarity > 0.60:  # Example threshold (60% similarity)
                                    face_verified = True
                                    cap.release()
                                    cv2.destroyAllWindows()

                                    # Log the user in
                                    login_manager = LoginManager()
                                    login_manager.user = npz_file.replace('_faces.npz', '')
                                    login_manager.post_login()

                                    # Prepare JSON response for success
                                    return {"status": "success", "message": "Face verified", "username": npz_file.replace('_faces.npz', '')}

                except Exception as e:
                    print(f"Error processing face: {e}")

            # Exit the loop if 'q' is pressed or 10 seconds have passed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:  # 10 seconds timeout
                break

        cap.release()
        cv2.destroyAllWindows()

        # Check if any face was detected and not verified
        if face_detected and not face_verified:
            return {"status": "error", "message": "Face detected but not recognized. Please ensure your model is collected and try again."}
        
        # Check if no faces were detected
        if not face_detected:
            return {"status": "error", "message": "No face detected. Please ensure you are in view of the camera."}
        
        # Prepare JSON response for failure if no face was verified
        return {"status": "error", "message": "Sorry, we didn't recognize your face. Please collect a model for your user."}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": "error", "message": f"An internal error occurred during face verification: {e}"}

def calculate_similarity(face1, face2):
    try:
        # Ensure both faces have the same shape
        if face1.shape != face2.shape:
            face2 = cv2.resize(face2, (face1.shape[1], face1.shape[0]))

        # Implement your face comparison logic here
        # Example: Calculate similarity using MSE or other techniques
        mse = ((face1 - face2) ** 2).mean()
        similarity = 1 - mse / 255.0  # Normalize to a similarity score (0-1)
        return similarity
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0
