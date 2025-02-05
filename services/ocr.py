import cv2
import pytesseract

def extract_license_plate(image_path):
    frame = cv2.imread(image_path)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    license_plate = pytesseract.image_to_string(gray_frame, config='--psm 8')
    return license_plate.strip()
