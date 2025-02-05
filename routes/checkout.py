from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from database import parking_records
from services.ocr import extract_license_plate

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout', methods=['POST'])
def checkout():
    file = request.files['car_image']
    if not file:
        return jsonify({"error": "No image provided"}), 400

    image_path = os.path.join("static/images", file.filename)
    file.save(image_path)
    
    license_plate = extract_license_plate(image_path)
    if not license_plate:
        return jsonify({"error": "Could not extract license plate"}), 400

    record = parking_records.find_one({"license_plate": license_plate, "exit_time": None})

    if not record:
        return jsonify({"error": "No active parking session found"}), 400

    entry_time = datetime.fromisoformat(record["entry_time"])
    exit_time = datetime.now()
    duration = (exit_time - entry_time).total_seconds() / 60

    duration_display = f"{duration / 60:.2f} hours" if duration > 60 else f"{int(duration)} minutes"
    amount_due = round(duration * 2, 2)  # Example rate: ₹2 per minute

    parking_records.update_one({"license_plate": license_plate}, {
        "$set": {"exit_time": exit_time.isoformat(), "duration": duration_display, "amount_due": amount_due}
    })

    return jsonify({
        "message": "Check-out successful",
        "license_plate": license_plate,
        "entry_time": record["entry_time"],
        "exit_time": exit_time.isoformat(),
        "duration": duration_display,
        "amount_due": f"₹{amount_due}"
    }), 200
