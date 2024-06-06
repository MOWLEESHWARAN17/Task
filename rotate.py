import os
import cv2

def rotate_and_save_images(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all files in the input directory
    files = os.listdir(input_dir)

    for file in files:
        # Check if the file is an image (you can add more image formats as needed)
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            # Read the image
            image_path = os.path.join(input_dir, file)
            image = cv2.imread(image_path)

            # Rotate the image by 90 degrees clockwise
            rotated_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            # Save the rotated image
            cv2.imwrite(os.path.join(output_dir, "90_"+file ), rotated_90)

            # Rotate the image by 240 degrees clockwise
            rotated_240 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # Save the rotated image
            cv2.imwrite(os.path.join(output_dir, "240_"+file ), rotated_240)

# Example usage
input_directory = "D:\ALL_OCR\PAN_OCR\PAN\Straight_image"  # Directory containing input images
output_directory = "output_images"  # Directory to save rotated images
rotate_and_save_images(input_directory, output_directory)
