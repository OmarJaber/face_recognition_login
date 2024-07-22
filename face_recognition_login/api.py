import frappe
from face_recognition_login.face_recognition_login.collect_face_model import collect_face_model as collect_model
from face_recognition_login.face_recognition_login.verify_face import verify_face as verify_model

@frappe.whitelist(allow_guest=True)
def collect_face_model(user_email):
    try:
        response = collect_model(user_email)
        return {"status": "success", "message": response}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Collect Face Model Error')
        return {"status": "error", "message": str(e)}, 500

@frappe.whitelist(allow_guest=True)
def verify_face():
    try:
        response = verify_model()
        return {"status": "success", "message": response}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Verify Face Error')
        return {"status": "error", "message": str(e)}, 500
