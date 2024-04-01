import fitz
import os

def pdf_to_images(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]

        # Render the page as an image (PNG)
        image = page.get_pixmap(alpha=False)

        # Save the image
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        image.save(image_path)

    # Close the PDF document
    pdf_document.close()

# Example usage:
pdf_path = r'D:\ocr_project\aadhar_masking\input.pdf'
output_folder = "output_images"

pdf_to_images(pdf_path, output_folder)

