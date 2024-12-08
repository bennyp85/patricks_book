import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import os

# Input PDF path
pdf_path = "/home/ben/patricks_book/assets/PODD.pdf"

# Output folder for extracted icons
output_folder = "/home/ben/patricks_book/icons"
os.makedirs(output_folder, exist_ok=True)

# Open the PDF file
doc = fitz.open(pdf_path)

# Iterate through each page
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    print(f"Processing page {page_num + 1}...")
    
    # Render the page as a PIL image
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_np = np.array(img)
    
    # Convert to grayscale and apply edge detection
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area (adjust threshold as needed)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust threshold based on icon size
            x, y, w, h = cv2.boundingRect(contour)
            icon = img.crop((x, y, x + w, y + h))
            icon_name = f"page{page_num + 1}_icon{idx + 1}.png"
            icon.save(os.path.join(output_folder, icon_name))
            print(f"Saved {icon_name}")

print("All icons have been processed.")