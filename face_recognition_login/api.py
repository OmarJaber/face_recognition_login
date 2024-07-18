import frappe
from face_recognition_login.face_recognition_login.collect_face_model import collect_face_model as collect_model
from face_recognition_login.face_recognition_login.verify_face import verify_face as verify_model

@frappe.whitelist(allow_guest=True)
def collect_face_model(user_email):
    return collect_model(user_email)

@frappe.whitelist(allow_guest=True)
def verify_face(user_email):
    return verify_model(user_email)
