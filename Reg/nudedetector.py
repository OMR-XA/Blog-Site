import os
from nudenet import NudeDetector
from django.core.files.storage import default_storage
from django.conf import settings
import uuid

def save_temp_image(image_file):
    """Save the uploaded image temporarily in the media directory and return the file path."""
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_images')
    os.makedirs(temp_dir, exist_ok=True)  # Create the directory if it doesn't exist
    temp_filename = f"{uuid.uuid4()}_{image_file.name}"  # Generate a unique filename
    temp_path = os.path.join(temp_dir, temp_filename)
    with default_storage.open(temp_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)
    return temp_path



def check_image_safety(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        return "Error: The specified image file does not exist."
    else:
        # Initialize detector with local model
        detector = NudeDetector()

        # Detect nudity
        detection_result = detector.detect(image_path)

        # List of classes that indicate the image is not safe
        unsafe_classes = [
            "EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED"
        ]

        # List of classes that are considered covered but might still be unsafe
        covered_classes = [
            "FEMALE_BREAST_COVERED"
        ]

        # Thresholds for each class category
        unsafe_threshold = 0.50  # Experiment with different values
        covered_threshold = 0.50  # Experiment with different values

        # Check if the image is safe
        is_safe = True
        for result in detection_result:
            if result['class'] in unsafe_classes and result['score'] >= unsafe_threshold:
                is_safe = False
                break

            if result['class'] in covered_classes and result['score'] >= covered_threshold:
                is_safe = False
                break

        # Return final decision
        if is_safe:
            return "Safe"
        else:
            return "Not Safe"

# Example usage
# image_path = r"C:\Users\mirage\OneDrive\Desktop\New folder\20230202_134132.jpg"

# r = check_image_safety(image_path)

# print(r)
