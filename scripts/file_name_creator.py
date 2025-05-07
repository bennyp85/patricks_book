import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import sys
import hashlib
from collections import defaultdict

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Check if Tesseract is installed
def check_tesseract_installed():
    try:
        pytesseract.get_tesseract_version()
        return True
    except pytesseract.TesseractNotFoundError:
        print("ERROR: Tesseract is not installed or not properly configured.")
        print("\nInstallation instructions:")
        print("1. Download Tesseract for Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install Tesseract to the default location (usually C:\\Program Files\\Tesseract-OCR)")
        print("3. Ensure the installation path is correct in this script")
        print("   pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        print("\nAlternatively, add Tesseract to your system PATH")
        return False

IMAGE_DIRECTORY = r'C:\Users\benja\code\patricks_book\podd v1\icons'  # <<< CHANGE THIS to your image folder
ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')

# Region of Interest (ROI) for the text at the top.
# These are proportions of the image width/height. You might need to adjust these.
ROI_X_START = 0.05  # 5% from the left
ROI_Y_START = 0.01  # 1% from the top
ROI_X_END = 0.95    # 95% of width (so 5% from the right)
ROI_Y_END = 0.25    # Top 25% of height (adjust if text area is smaller/larger)

# --- Helper Functions ---
def sanitize_filename(text):
    """Cleans the extracted text to be a valid filename."""
    if not text:
        return "ocr_failed"
    # Remove leading/trailing whitespace and newlines
    text = text.strip()
    # Replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove characters not allowed in filenames
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    # Optional: Replace periods to avoid confusion with file extensions, except the last one
    # For simplicity here, we'll just replace all. You can refine this.
    # text = text.replace('.', '_')
    # Limit length (optional)
    text = text[:100] # Max 100 chars for filename base
    return text if text else "ocr_failed"

def preprocess_image_for_ocr(image_path, roi_coords):
    """Opens, crops, and preprocesses an image for better OCR results."""
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Calculate absolute ROI coordinates
        left = int(width * roi_coords['x_start'])
        top = int(height * roi_coords['y_start'])
        right = int(width * roi_coords['x_end'])
        bottom = int(height * roi_coords['y_end'])

        # Crop to the region where the text is expected
        img_cropped = img.crop((left, top, right, bottom))

        # Convert to grayscale
        img_gray = img_cropped.convert('L')

        # Optional: Increase contrast
        enhancer = ImageEnhance.Contrast(img_gray)
        img_contrasted = enhancer.enhance(2) # Factor of 2, adjust as needed

        # Optional: Binarization (thresholding)
        # img_binarized = img_contrasted.point(lambda x: 0 if x < 128 else 255, '1')
        # For these images, simple contrasting might be enough, or even just grayscale.
        # Let's try with contrasted grayscale first.
        return img_contrasted # or img_gray or img_binarized

    except Exception as e:
        print(f"Error preprocessing {image_path}: {e}")
        return None

def extract_text_from_image(image_obj):
    """Extracts text from a PIL Image object using Tesseract."""
    try:
        # --psm 6: Assume a single uniform block of text.
        # --oem 3: Default OCR Engine Mode.
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image_obj, config=custom_config)
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""

# --- New Duplicate Detection Functions ---
def calculate_image_hash(image_path):
    """Calculate a hash for an image file to identify duplicates."""
    try:
        with Image.open(image_path) as img:
            # Convert to small grayscale image to ensure consistent hashing
            img = img.resize((32, 32)).convert('L')
            # Get the raw image data
            pixel_data = list(img.getdata())
            # Calculate a hash from the pixel data
            img_hash = hashlib.md5(bytes(pixel_data)).hexdigest()
            return img_hash
    except Exception as e:
        print(f"Error calculating hash for {image_path}: {e}")
        return None

def find_duplicate_images(directory, extensions):
    """Find duplicate images in a directory based on their hash."""
    print("Scanning for duplicate images...")
    hash_to_files = defaultdict(list)
    file_count = 0
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(extensions):
            filepath = os.path.join(directory, filename)
            file_hash = calculate_image_hash(filepath)
            if file_hash:
                hash_to_files[file_hash].append(filepath)
                file_count += 1
    
    # Filter to get only duplicates
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    print(f"Scanned {file_count} files, found {len(duplicates)} sets of duplicates.")
    return duplicates

def handle_duplicates(duplicates, delete=False):
    """Process duplicate images - print info and optionally delete."""
    if not duplicates:
        return 0
    
    deleted_count = 0
    print("\n--- Duplicate Images ---")
    for img_hash, file_paths in duplicates.items():
        print(f"Duplicate set (hash: {img_hash[:8]}...):")
        # Keep the first file, consider deleting the rest
        for i, path in enumerate(file_paths):
            if i == 0:
                print(f"  [KEEP] {os.path.basename(path)}")
            else:
                if delete:
                    try:
                        os.remove(path)
                        print(f"  [DELETED] {os.path.basename(path)}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"  [ERROR DELETING] {os.path.basename(path)}: {e}")
                else:
                    print(f"  [DUPLICATE] {os.path.basename(path)}")
        print()
    
    return deleted_count

# --- Main Script ---
def main():
    # Verify Tesseract is installed before proceeding
    if not check_tesseract_installed():
        return
        
    if not os.path.isdir(IMAGE_DIRECTORY):
        print(f"Error: Directory not found: {IMAGE_DIRECTORY}")
        return

    print(f"Processing images in: {IMAGE_DIRECTORY}\n")
    
    # First, check for and handle duplicates
    duplicates = find_duplicate_images(IMAGE_DIRECTORY, ALLOWED_EXTENSIONS)
    delete_dupes = False
    if duplicates:
        response = input("Do you want to delete duplicate images? (yes/no): ").lower()
        delete_dupes = response == 'yes' or response == 'y'
        deleted_count = handle_duplicates(duplicates, delete_dupes)
        if deleted_count > 0:
            print(f"Deleted {deleted_count} duplicate images.")
    
    renamed_count = 0
    skipped_count = 0
    processed_new_filenames = set() # To handle cases where OCR might produce the same text for different images

    for filename in os.listdir(IMAGE_DIRECTORY):
        if filename.lower().endswith(ALLOWED_EXTENSIONS):
            original_filepath = os.path.join(IMAGE_DIRECTORY, filename)
            print(f"Processing: {filename}...")
            
            # Skip if file doesn't exist anymore (might have been deleted as duplicate)
            if not os.path.exists(original_filepath):
                print(f"  File no longer exists (deleted as duplicate?). Skipping.")
                continue
            
            roi_settings = {
                'x_start': ROI_X_START, 'y_start': ROI_Y_START,
                'x_end': ROI_X_END, 'y_end': ROI_Y_END
            }
            processed_img_obj = preprocess_image_for_ocr(original_filepath, roi_settings)

            if not processed_img_obj:
                skipped_count += 1
                continue

            # --- For debugging ROI, uncomment to save the cropped image ---
            # debug_roi_path = os.path.join(IMAGE_DIRECTORY, f"DEBUG_ROI_{filename}")
            # processed_img_obj.save(debug_roi_path)
            # print(f"  Saved debug ROI to: {debug_roi_path}")
            # -------------------------------------------------------------

            extracted_text = extract_text_from_image(processed_img_obj)
            sanitized_text = sanitize_filename(extracted_text)

            print(f"  Extracted: '{extracted_text.strip()}' -> Sanitized: '{sanitized_text}'")

            if sanitized_text == "ocr_failed" or not sanitized_text:
                print(f"  OCR failed or no text found for {filename}. Skipping rename.")
                skipped_count += 1
                continue

            file_ext = os.path.splitext(filename)[1]
            new_base_filename = sanitized_text
            new_filename = f"{new_base_filename}{file_ext}"
            new_filepath = os.path.join(IMAGE_DIRECTORY, new_filename)

            # Handle potential filename collisions (if different images OCR to the same text)
            counter = 1
            temp_new_filename = new_filename
            temp_new_filepath = new_filepath
            while os.path.exists(temp_new_filepath) or temp_new_filename in processed_new_filenames:
                if temp_new_filepath == original_filepath: # Trying to rename to itself
                    print(f"  New filename '{temp_new_filename}' is the same as original. Skipping rename.")
                    break # exit while loop
                temp_new_filename = f"{new_base_filename}_{counter}{file_ext}"
                temp_new_filepath = os.path.join(IMAGE_DIRECTORY, temp_new_filename)
                counter += 1
            else: # No break from while loop
                new_filename = temp_new_filename
                new_filepath = temp_new_filepath

                if new_filepath == original_filepath:
                     print(f"  New filename '{new_filename}' is the same as original. Skipping rename.")
                     skipped_count +=1
                elif os.path.exists(new_filepath):
                    print(f"  Target filename '{new_filename}' already exists (and is not the original). Skipping {filename}.")
                    skipped_count +=1
                else:
                    try:
                        os.rename(original_filepath, new_filepath)
                        print(f"  Renamed '{filename}' to '{new_filename}'")
                        processed_new_filenames.add(new_filename) # Add to set of used new names for this run
                        renamed_count += 1
                    except OSError as e:
                        print(f"  Error renaming '{filename}' to '{new_filename}': {e}")
                        skipped_count += 1
                continue # skip the outer else block if we handled collision

            # This part is reached if the 'break' happened in the while loop (renaming to itself)
            # or if collision occurred and it was not the original file
            # (already handled by the print statements inside the loop and its 'else')


    print(f"\n--- Summary ---")
    print(f"Successfully renamed: {renamed_count} images.")
    print(f"Skipped or failed: {skipped_count} images.")

if __name__ == '__main__':
    # IMPORTANT: Backup your images before running this script!
    confirm = input("Have you backed up your images? This script will rename files and can delete duplicates. (yes/no): ")
    if confirm.lower() == 'yes' or confirm.lower() == 'y':
        main()
    else:
        print("Please backup your images and then run the script again.")
    # main() # Uncomment for direct execution after you're confident