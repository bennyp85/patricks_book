import csv
import re
import os

def fix_dvd_num(dvd_num):
    # Already correct (e.g., white-1)
    if re.match(r'^[a-z]+-\d+$', dvd_num.strip()):
        return dvd_num.strip()
    # Match "COLOUR NUMBER" (e.g., WHITE 2)
    m = re.match(r'^([A-Z]+)\s+(\d+)$', dvd_num.strip())
    if m:
        colour = m.group(1).lower()
        number = m.group(2)
        return f"{colour}-{number}"
    # Otherwise, return as is
    return dvd_num.strip()

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "DVD_FULL_LIST.csv")
output_file = os.path.join(script_dir, "DVD_FULL_LIST_FIXED.csv")

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    header = next(reader)
    writer.writerow(header)
    for row in reader:
        if row and row[0].strip():
            row[0] = fix_dvd_num(row[0])
        writer.writerow(row)

print(f"Done. Output written to {output_file}")