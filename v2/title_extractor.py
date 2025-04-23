import docx  # For reading Word files
import csv   # For writing to CSV
import re    # For pattern matching

def extract_dvd_data(file_path, prefix):
    doc = docx.Document(file_path)
    data = []  # List to store extracted data
    for paragraph in doc.paragraphs:  # Iterate through paragraphs
        text = paragraph.text.strip()  # Get the text and remove extra spaces
        # Pattern: Assumes format like "1. CAT DOG VOLUME 1. Season 1. Disc 1."
        match = re.search(r'^(\d+)[\.,]?\s+(.+)', text)
        if match:
            dvd_number = f"{prefix}-{match.group(1)}"  # Add prefix to the number
            title = match.group(2)       # Extract the title
            data.append([dvd_number, title])  # Add to list as [number, title]
    return data

# Main script
doc1_path = r'C:\Users\benja\Code\patricks_book\v2\Green DVD LIST.docx'
doc2_path = r'C:\Users\benja\Code\patricks_book\v2\White DVD LIST.docx'
output_csv = 'output.csv'

# Extract data from both documents with prefixes
data_from_doc1 = extract_dvd_data(doc1_path, "green")
data_from_doc2 = extract_dvd_data(doc2_path, "white")
all_data = data_from_doc2 + data_from_doc1  # White first, then green

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['dvd_num', 'title'])  # Write header row
    for row in all_data:
        writer.writerow(row)  # Write each extracted row

print(f"Extraction complete! Data saved to {output_csv}")