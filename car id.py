import cv2
import PIL.Image
import google.generativeai as genai

# Configure the API key for Gemini
genai.configure(api_key="AIzaSyBxwLZSyL8MCnZcFpx66kHs5KI_3Ce6Dpk")

# Function to capture the image from the webcam
def capture_image():
    cam = cv2.VideoCapture(0)  # Start the camera
    cv2.namedWindow("Capture Car Image")
    
    img_name = None  # Initialize img_name to None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Capture Car Image", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # Press ESC to close the window without saving the image
            print("Closing without capturing")
            break
        elif k % 256 == 32:
            # Press SPACE to capture the image
            img_name = "car_image.png"
            cv2.imwrite(img_name, frame)
            print(f"Image saved as {img_name}")
            break

    cam.release()
    cv2.destroyAllWindows()

    return img_name

# Function to detect and crop the number plate from the car image
def detect_and_crop_number_plate(image_path):
    # Load the pre-trained Haar Cascade for number plate detection
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

    # Load the captured image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Detect number plates in the image
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(plates) == 0:
        print("No number plate detected.")
        return None

    # Crop the number plate region
    for (x, y, w, h) in plates:
        plate_img = img[y:y+h, x:x+w]
        cropped_plate_img_name = "cropped_number_plate.png"
        cv2.imwrite(cropped_plate_img_name, plate_img)
        print(f"Cropped number plate image saved as {cropped_plate_img_name}")
        return cropped_plate_img_name

    return None

# Function to send the cropped number plate image to Gemini API
def send_image_to_gemini(image_path):
    # Open the cropped image using PIL
    image = PIL.Image.open(image_path)

    # Assuming there's a model in Gemini for handling images (substitute 'gemini-1.5-flash' with correct model)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Send the image to the model and generate content (assumes the model can accept images)
    # Adjust the method for sending images if it's different in the actual API
    response = model.generate_content(image)

    if response:
        print(f"Extracted Text from Gemini: {response.text}")
        return response.text
    else:
        print("Failed to extract text from the image using Gemini.")
        return None

# Main logic to capture image, detect number plate, crop it, and send to Gemini API
def main():
    # Capture the car image
    image_path = capture_image()

    if image_path is None:
        print("No image captured.")
        return

    # Detect and crop the number plate from the car image
    cropped_plate_image = detect_and_crop_number_plate(image_path)

    # If a number plate is detected and cropped, send it to the Gemini API for text extraction
    if cropped_plate_image:
        extracted_text = send_image_to_gemini(cropped_plate_image)

        if extracted_text:
            print("Extracted Information from Number Plate via Gemini:")
            print(extracted_text)
        else:
            print("No text extracted from the number plate via Gemini.")
    else:
        print("No number plate found to send to Gemini for text extraction.")

if __name__ == "__main__":
    main()
