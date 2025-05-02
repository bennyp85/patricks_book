import docx  # For reading Word files
import csv   # For writing to CSV
import re    # For pattern matching
import os    # For path operations

def extract_dvd_data(file_path, prefix):
    """
    Extracts numbered DVD entries (number and title) from a Word document.

    Args:
        file_path (str): The path to the Word document.
        prefix (str): A prefix to add to the extracted DVD numbers (e.g., "green", "white").

    Returns:
        list: A list of lists, where each inner list contains [prefixed_dvd_number, title].
    """
    print(f"Opening file: {file_path}")
    doc = docx.Document(file_path)
    data = []  # List to store extracted data

    # Updated regex:
    # ^\s* - Matches optional whitespace at the start of the line.
    # (\d+)         - Captures one or more digits (the DVD number).
    # \s* - Matches optional whitespace after the number.
    # [\.,\s-]* - Matches zero or more occurrences of a dot, comma, whitespace, or hyphen
    #                 (flexible separator).
    # \s* - Matches optional whitespace before the title.
    # (.+)          - Captures the rest of the line (the title).
    regex = re.compile(r'^\s*(\d+)\s*[\.,\s-]*\s*(.+)')

    for paragraph in doc.paragraphs:  # Iterate through paragraphs
        text = paragraph.text.strip()  # Get the text and remove extra spaces
        match = regex.search(text)
        if match:
            dvd_number = f"{prefix}-{match.group(1)}"  # Add prefix to the number
            title = match.group(2).strip()      # Extract the title and trim whitespace
            data.append([dvd_number, title])  # Add to list as [number, title]
    return data

def find_missing_numbers(data_list, prefix, max_number=999):
    """
    Finds missing numbers within the extracted DVD data for a given prefix.

    Args:
        data_list (list): A list of all extracted DVD data (from both files).
        prefix (str): The prefix to filter by (e.g., "green", "white").
        max_number (int): The maximum expected DVD number in the sequence.

    Returns:
        list: A sorted list of missing numbers for the specified prefix.
    """
    # Extract just the numbers from the DVD codes for the given prefix
    existing_numbers = set() # Use a set for efficient checking and uniqueness
    for item in data_list:
        # Check if the item starts with the correct prefix and has the expected format
        if item[0].startswith(prefix + '-'):
            try:
                # Split by '-' and take the second part, convert to int
                num_part = int(item[0].split('-')[1])
                existing_numbers.add(num_part)
            except (ValueError, IndexError):
                # This case should ideally not happen if extraction is correct,
                # but included for robustness.
                print(f"Warning: Could not parse number from DVD code: {item[0]}")

    # Find missing numbers from 1 to max_number
    all_numbers = set(range(1, max_number + 1))
    missing_numbers = all_numbers - existing_numbers
    return sorted(list(missing_numbers))

# Main script
# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct absolute paths to the documents
doc1_path = os.path.join(script_dir, 'Green DVD LIST.docx')
doc2_path = os.path.join(script_dir, 'White DVD LIST.docx')
output_csv = os.path.join(script_dir, 'output.csv')
missing_numbers_file = os.path.join(script_dir, 'missing_numbers.txt')

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")
print(f"Script directory: {script_dir}")
print(f"Looking for files: {doc1_path} and {doc2_path}")

# Determine the maximum expected number based on your collection.
# You might need to adjust this if your lists go higher.
max_dvd_number = 1000 # Set a reasonable upper limit

# Extract data from both documents with prefixes
data_from_doc1 = extract_dvd_data(doc1_path, "green")
data_from_doc2 = extract_dvd_data(doc2_path, "white")
all_data = data_from_doc2 + data_from_doc1  # Combine data, white first then green

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['dvd_num', 'title'])  # Write header row
    for row in all_data:
        writer.writerow(row)  # Write each extracted row

print(f"Extraction complete! Data saved to {output_csv}")
print(f"Total entries extracted: {len(all_data)}")

# Find missing numbers
white_missing = find_missing_numbers(all_data, "white", max_number=max_dvd_number)
green_missing = find_missing_numbers(all_data, "green", max_number=max_dvd_number)

# Write missing numbers to file
with open(missing_numbers_file, 'w', encoding='utf-8') as f:
    f.write("Missing numbers in White DVD LIST.docx:\n")
    f.write(", ".join(str(num) for num in white_missing))
    f.write(f"\n\nTotal missing white DVDs: {len(white_missing)}\n\n")

    f.write("Missing numbers in Green DVD LIST.docx:\n")
    f.write(", ".join(str(num) for num in green_missing))
    f.write(f"\n\nTotal missing green DVDs: {len(green_missing)}")

print(f"Missing numbers saved to {missing_numbers_file}")
print(f"Missing white DVDs: {len(white_missing)}")
print(f"Missing green DVDs: {len(green_missing)}")