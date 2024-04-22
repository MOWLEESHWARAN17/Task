import os

def rename_images(folder_path):
    # Get the list of files in the folder
    files = os.listdir(folder_path)
    
    # Ensure only image files are considered
    image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.png')]

    # Create a new folder to store renamed images
    new_folder_path = os.path.join(folder_path, 'renamed_images')
    os.makedirs(new_folder_path, exist_ok=True)

    # Rename and move each image file
    for i, file in enumerate(image_files):
        old_file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(new_folder_path, f'{i+1}.jpg')  # Rename sequentially
        os.rename(old_file_path, new_file_path)

    print(f'{len(image_files)} images renamed and moved to {new_folder_path}')

# Replace 'folder_path' with the path to your folder containing the images
folder_path = r"C:\Users\intern-mowleeshwaran\Desktop\aadhaar_images"
rename_images(folder_path)
