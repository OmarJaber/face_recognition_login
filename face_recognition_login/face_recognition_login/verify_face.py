# verify_face.py

import cv2
import os
import frappe

def verify_face(user_email, captured_face):
    # Ensure the folder path in ERPNext files directory
    files_path = frappe.get_site_path('public', 'files', 'User Face Models')
    user_folder = os.path.join(files_path, user_email)
    
    # Check if the user's folder exists
    if not os.path.exists(user_folder):
        return { "message": "Face images not found for this user." }

    # Load each image and compare with the captured face
    for filename in sorted(os.listdir(user_folder)):
        if filename.endswith('.jpg'):
            image_path = os.path.join(user_folder, filename)
            stored_face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # Compare the captured face with the stored face
            if compare_faces(captured_face, stored_face):
                return { "message": "Face verified" }
    
    return { "message": "Face verification failed." }

def compare_faces(face1, face2):
    # Implement your face comparison logic here
    # Example: Compare using mean squared error (MSE) or other techniques
    # Here's a basic example using MSE as placeholder
    mse = ((face1 - face2) ** 2).mean()
    similarity = 1 - mse / 255.0  # Normalize to a similarity score (0-1)
    
    # Adjust threshold as needed
    if similarity > 0.95:  # Example threshold (95% similarity)
        return True
    else:
        return False

# Example usage (commented out for now)
# user_email = 'omar.ja93@gmail.com'
# captured_face = cv2.imread('captured_face.jpg', cv2.IMREAD_GRAYSCALE)
# result = verify_face(user_email, captured_face)
# print(result)
