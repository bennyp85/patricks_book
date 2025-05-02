import csv
import os

def combine_files(missing_file, output_file):
    # Dictionary to track unique entries using dvd_num as key
    unique_entries = {}
    
    # Read the missing.txt file
    with open(missing_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            
            # Try to parse the line as dvd_num,title
            parts = line.split(',', 1)
            if len(parts) == 2:
                dvd_num = parts[0].strip()
                title = parts[1].strip()
                unique_entries[dvd_num] = title
    
    # Read the output.csv file if it exists
    if os.path.exists(output_file):
        with open(output_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Skip header if present
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    dvd_num = row[0].strip()
                    title = row[1].strip()
                    # Only add if not already present
                    if dvd_num not in unique_entries:
                        unique_entries[dvd_num] = title
    
    # Write the combined results to a new CSV file
    with open('combined_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['dvd_num', 'title'])
        for dvd_num, title in sorted(unique_entries.items()):
            writer.writerow([dvd_num, title])
    
    print(f"Combined file created: combined_output.csv with {len(unique_entries)} unique entries")

if __name__ == "__main__":
    # Use the correct paths to the files in the v2 directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    missing_file = os.path.join(script_dir, "missing.txt")
    output_file = os.path.join(script_dir, "output.csv")
    
    # Check if files exist
    if not os.path.exists(missing_file):
        print(f"Error: {missing_file} not found!")
    elif not os.path.exists(output_file):
        print(f"Error: {output_file} not found!")
    else:
        combine_files(missing_file, output_file)