import imgaug.augmenters as iaa
import cv2
import os
import numpy as np

# Define augmentation sequence
seq = iaa.Sequential([
    iaa.Affine(
        rotate=(0, 360),  # rotate images by -10 to 10 degrees
        translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)},  # translate images
        scale={"x": (0.8, 0.8), "y": (0.8, 0.8)}
    ),])

# Path to the directory containing voter ID images
input_dir = r'D:\ALL_OCR\VOTER_ROTATE\FRONT'

# Output directory to save augmented images
output_dir = "AUG2"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each image in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Read the image
        image = cv2.imread(os.path.join(input_dir, filename))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB (imgaug uses RGB format)
        
        # Apply augmentation
        augmented_images = [seq.augment_image(image) for _ in range(5)]  # Augment each image 5 times
        
        # Save augmented images
        base_filename, file_extension = os.path.splitext(filename)
        for i, augmented_image in enumerate(augmented_images):
            output_filename = f"{base_filename}_aug_{i}{file_extension}"
            cv2.imwrite(os.path.join(output_dir, output_filename), cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
