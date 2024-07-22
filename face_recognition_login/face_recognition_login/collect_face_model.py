import cv2
import os
import numpy as np
import frappe

def collect_face_model(user_email):
    try:
        # Folder setup
        models_folder = frappe.utils.get_files_path('Users Face Model')
        if not os.path.exists(models_folder):
            os.makedirs(models_folder)

        npz_file_path = os.path.join(models_folder, f'{user_email}_faces.npz')

        # Capture and process video frames
        cap = cv2.VideoCapture(0)
        count = 0
        collected_faces = []

        while count < 200:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                collected_faces.append(face)

                # Update progress in cache
                progress = (count / 200) * 100
                frappe.cache().hset('face_model_progress', user_email, progress)

                if count >= 200:
                    break

        np.savez_compressed(npz_file_path, faces=np.array(collected_faces))

        cap.release()

        # Clear progress from cache after completion
        frappe.cache().hdel('face_model_progress', user_email)

        return "Face models collected successfully."

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Collect Face Model Error')
        raise e

@frappe.whitelist()
def get_progress(user_email):
    progress = frappe.cache().hget('face_model_progress', user_email)
    return progress if progress else 0
