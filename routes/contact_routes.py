from flask import Blueprint
from flask import request
from flask import jsonify

from models.contact_model import Contact

contact_bp = Blueprint(
    "contact",
    __name__
)

@contact_bp.route(
    "/contact",
    methods=["POST"]
)
def submit_contact():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400

        name = data.get("name", "").strip()
        company = data.get("company", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        service = data.get("service", "").strip()
        message = data.get("message", "").strip()

        # Validation
        if (
            not name or
            not company or
            not email or
            not phone or
            not service or
            not message
        ):
            return jsonify({
                "success": False,
                "error": "All fields are required"
            }), 400

        print("Received Form Data:")
        print("Name:", name)
        print("Company:", company)
        print("Email:", email)
        print("Phone:", phone)
        print("Service:", service)
        print("Message:", message)

        Contact.save_contact(
            name,
            company,
            email,
            phone,
            service,
            message
        )

        return jsonify({
            "success": True,
            "message": "Contact Saved Successfully"
        }), 200

    except Exception as e:

        print("Route Error:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500