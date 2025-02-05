from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from typing import Tuple, Dict, Any
from werkzeug.utils import secure_filename
from database import parking_records
from services.ocr import extract_license_plate
from flask import current_app

checkin_bp = Blueprint('checkin', __name__)

@checkin_bp.route('/checkin', methods=['POST'])
def checkin() -> Tuple[Dict[str, Any], int]:
    """
    Handle parking check-in process with image-based license plate recognition.
    
    Returns:
        JSON response with check-in details or error message
    """
    # Validate image file
    if 'car_image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['car_image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Secure filename to prevent potential security issues
    filename = secure_filename(file.filename)
    
    # Use app config for image storage path if available
    images_dir = current_app.config.get('UPLOAD_FOLDER', 'static/images')
    os.makedirs(images_dir, exist_ok=True)
    
    image_path = os.path.join(images_dir, filename)
    file.save(image_path)
    
    try:
        # Extract license plate
        license_plate = extract_license_plate(image_path)
        if not license_plate:
            return jsonify({"error": "Could not extract license plate"}), 400

        # Check for existing active check-in
        existing_user = parking_records.find_one({
            "license_plate": license_plate, 
            "exit_time": None
        })
        if existing_user:
            return jsonify({
                "message": "User already checked in", 
                "license_plate": license_plate
            }), 400

        # Check if user exists in records
        user = parking_records.find_one({"license_plate": license_plate})
        
        # If user exists but no active check-in, request verification
        if user:
            return jsonify({
                "message": "Existing user, please verify your mobile number",
                "license_plate": license_plate
            }), 200

        # Get user details from request
        data = request.get_json(force=True, silent=True) or {}
        full_name = data.get("full_name")
        mobile_number = data.get("mobile_number")

        # Validate user details
        if not full_name or not mobile_number:
            return jsonify({"error": "Missing user details"}), 400

        # Create new parking entry
        new_entry = {
            "license_plate": license_plate,
            "full_name": full_name,
            "mobile_number": mobile_number,
            "entry_time": datetime.utcnow().isoformat(),
            "exit_time": None
        }

        # Insert entry into database
        parking_records.insert_one(new_entry)

        return jsonify({
            "message": "Check-in successful",
            "license_plate": license_plate,
            "full_name": full_name,
            "mobile_number": mobile_number,
            "entry_time": new_entry["entry_time"]
        }), 200

    except Exception as e:
        # Log the error and return a generic error response
        current_app.logger.error(f"Check-in error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        # Clean up uploaded image if needed
        if os.path.exists(image_path):
            os.remove(image_path)