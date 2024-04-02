import cv2
import numpy as np
import pytesseract
from PIL import Image
from torchsr.models.edsr import EDSR
import img2pdf
from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger
import fitz
import re
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\intern-mowleeshwaran\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def find_text(text):
    n = len(text)
    if n < 12:
        return 0
    for i in range(14, n):
        s = text[i - 14:i]
        if s[4] == " " and s[9] == " ":
            s = s.replace(" ", "")
            n1 = len(s)
            s1 = s[n1 - 12:n1]
            if s1.isnumeric() and len(s1) >= 12:
                return 1
    return 0

def addhar_check(img_array):
    u = 0
    for i in range(25):
        try:
            img = Image.fromarray(img_array[i])
            array = np.array(img)
            c = len(array.shape)
            if c == 2:
                if array[0][0] in [True, False]:
                    array = array * 255
                    img10 = array.astype(np.uint8)
                    array = np.array(img10)
            elif c == 3:
                if array[0][0][0] in [True, False]:
                    array = array * 255
                    img10 = array.astype(np.uint8)
                    array = np.array(img10)
            text = pytesseract.image_to_string(array)
            v = find_text(text)
            if v:
                break
            else:
                gaussianBlur = cv2.GaussianBlur(array, (5, 5), cv2.BORDER_DEFAULT)
                text = pytesseract.image_to_string(gaussianBlur)
                v = find_text(text)
                if v:
                    break
                else:
                    pass
        except EOFError:
            u = 0
            break
    return u

multiplication_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))

permutation_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))

#---------------------------------------------------------------------------------------------------------#

def compute_checksum(number):
    
    """Calculate the Verhoeff checksum over the provided number. The checksum
    is returned as an int. Valid numbers should have a checksum of 0."""
    
    # transform number list
    number = tuple(int(n) for n in reversed(str(number)))
    #print(number)
    
    # calculate checksum
    checksum = 0
    
    for i, n in enumerate(number):
        checksum = multiplication_table[checksum][permutation_table[i % 8][n]]
    
    #print(checksum)
    return checksum

def Regex_Search(bounding_boxes):
    possible_UIDs = []
    Result = ""
    for character in range(len(bounding_boxes)):
        if len(bounding_boxes[character]) != 0:
            Result += bounding_boxes[character][0]
        else:
            Result += '?'
    matches = [match.span() for match in re.finditer(r'\d{12}', Result)]
    for match in matches:
        UID = int(Result[match[0]:match[1]])
        if compute_checksum(UID) == 0 and UID % 10000 != 1947:
            possible_UIDs.append([UID, match[0]])
    possible_UIDs = np.array(possible_UIDs)
    return possible_UIDs

def Mask_UIDs(image_path, possible_UIDs, bounding_boxes, rtype, SR=False, SR_Ratio=[1, 1]):
    img = cv2.imread(image_path)
    if rtype == 2:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rtype == 3:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rtype == 4:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    height = img.shape[0]
    if SR == True:
        height *= SR_Ratio[1]
    for UID in possible_UIDs:
        digit1 = bounding_boxes[UID[1]].split()
        digit8 = bounding_boxes[UID[1] + 7].split()
        h1 = min(height - int(digit1[4]), height - int(digit8[4]))
        h2 = max(height - int(digit1[2]), height - int(digit8[2]))
        if SR == False:
            top_left_corner = (int(digit1[1]), h1)
            bottom_right_corner = (int(digit8[3]), h2)
            botton_left_corner = (int(digit1[1]), h2 - 3)
            thickness = h1 - h2
        else:
            top_left_corner = (int(int(digit1[1]) / SR_Ratio[0]), int((h1) / SR_Ratio[1]))
            bottom_right_corner = (int(int(digit8[3]) / SR_Ratio[0]), int((h2) / SR_Ratio[1]))
            botton_left_corner = (int(int(digit1[1]) / SR_Ratio[0]), int((h2) / SR_Ratio[1] - 3))
            thickness = int((h1) / SR_Ratio[1]) - int((h2) / SR_Ratio[1])
        img = cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 0, 0), -1)
    if rtype == 2:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif rtype == 3:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rtype == 4:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    file_name = image_path.split('/')[-1].split('.')[0] + "_masked" + "." + image_path.split('.')[-1]
    cv2.imwrite(file_name, img)
    return file_name

def Extract_and_Mask_UIDs(image_path, SR=False, sr_image_path=None, SR_Ratio=[1, 1]):
    if SR == False:
        img = cv2.imread(image_path)
    else:
        img = cv2.imread(sr_image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rotations = [[gray, 1], [cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE), 2],
                 [cv2.rotate(gray, cv2.ROTATE_180), 3], [cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE), 4],
                 [cv2.GaussianBlur(gray, (5, 5), 0), 1],
                 [cv2.GaussianBlur(cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE), (5, 5), 0), 2],
                 [cv2.GaussianBlur(cv2.rotate(gray, cv2.ROTATE_180), (5, 5), 0), 3],
                 [cv2.GaussianBlur(cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE), (5, 5), 0), 4]]
    settings = ('-l eng --oem 3 --psm 11')
    for rotation in rotations:
        cv2.imwrite('rotated_grayscale.png', rotation[0])
        bounding_boxes = pytesseract.image_to_boxes(Image.open('rotated_grayscale.png'), config=settings).split(
            " 0\n")
        possible_UIDs = Regex_Search(bounding_boxes)
        if len(possible_UIDs) == 0:
            continue
        else:
            if SR == False:
                masked_img = Mask_UIDs(image_path, possible_UIDs, bounding_boxes, rotation[1])
            else:
                masked_img = Mask_UIDs(image_path, possible_UIDs, bounding_boxes, rotation[1], True, SR_Ratio)
            return (masked_img, possible_UIDs)
    return (None, None)

def masking_pdf(input_pdf_path):
    merged_pdf = fitz.open()
    input_pdf = fitz.open(input_pdf_path)
    for page_no in range(len(input_pdf)):
        page = input_pdf.load_page(page_no)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_path = f"temp_page_{page_no}.jpg"
        img.save(img_path)
        masked_img, possible_UIDs = Extract_and_Mask_UIDs(img_path)
        if masked_img is not None:
            pdf_bytes = img2pdf.convert(masked_img)
            output_pdf_path = f"temp_page_{page_no}_masked.pdf"
            with open(output_pdf_path, "wb") as f:
                f.write(pdf_bytes)
            merged_pdf.insert_pdf(fitz.open(output_pdf_path))
        else:
            merged_pdf.insert_pdf(input_pdf, from_page=page_no, to_page=page_no)
        os.remove(img_path)
        if masked_img is not None:
            os.remove(output_pdf_path)
    output_pdf_path = "masked_output.pdf"
    merged_pdf.save(output_pdf_path)
    merged_pdf.close()
    return output_pdf_path


# Example usage:
input_pdf_path = r'D:\ocr_project\aadhar_masking\1.pdf'
output_pdf_path = masking_pdf(input_pdf_path)
print("Masked PDF saved at:", output_pdf_path)
