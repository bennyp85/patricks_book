import os
import re
import shutil
from collections import defaultdict

# Configuration
ICONS_DIRECTORY = r'C:\Users\benja\code\patricks_book\assets\icons_renamed'

def main():
    """
    Find PNG files with numbered suffixes (like water_1.png, water_2.png),
    rename one to the clean version (water.png) and delete the rest.
    """
    if not os.path.isdir(ICONS_DIRECTORY):
        print(f"Error: Directory not found: {ICONS_DIRECTORY}")
        return

    print(f"Scanning for numbered duplicates in: {ICONS_DIRECTORY}")
    
    # Pattern to match filenames like "name_123.png"
    pattern = re.compile(r'^(.+)_(\d+)\.png$', re.IGNORECASE)
    
    # Group files by their base name
    base_name_groups = defaultdict(list)
    
    # First, scan the directory and group files
    for filename in os.listdir(ICONS_DIRECTORY):
        if not filename.lower().endswith('.png'):
            continue
            
        match = pattern.match(filename)
        if match:
            # Extract base name and number
            base_name, number = match.groups()
            base_name_groups[base_name].append((int(number), filename))
        
    print(f"Found {len(base_name_groups)} groups of numbered files.")
    
    # Counter for statistics
    renamed_count = 0
    deleted_count = 0
    
    # Process each group
    for base_name, numbered_files in base_name_groups.items():
        clean_name = f"{base_name}.png"
        clean_path = os.path.join(ICONS_DIRECTORY, clean_name)
        
        # Sort by number to keep the lowest numbered file
        numbered_files.sort()
        
        print(f"\nProcessing group: {base_name}")
        print(f"  Files found: {[f for _, f in numbered_files]}")
        
        # Check if the clean name already exists
        if os.path.exists(clean_path):
            print(f"  Clean name '{clean_name}' already exists. Keeping this and deleting all numbered versions.")
            keep_file = clean_name
        else:
            # Keep the first file (lowest number) and rename it to the clean name
            _, keep_file = numbered_files[0]
            keep_path = os.path.join(ICONS_DIRECTORY, keep_file)
            
            try:
                shutil.copy2(keep_path, clean_path)  # Copy preserving metadata
                print(f"  Keeping '{keep_file}' and renaming to '{clean_name}'")
                renamed_count += 1
            except Exception as e:
                print(f"  Error renaming '{keep_file}' to '{clean_name}': {e}")
                continue  # Skip to next group if we can't rename
        
        # Delete all numbered files in the group
        for _, file_to_delete in numbered_files:
            file_path = os.path.join(ICONS_DIRECTORY, file_to_delete)
            try:
                os.remove(file_path)
                print(f"  Deleted: '{file_to_delete}'")
                deleted_count += 1
            except Exception as e:
                print(f"  Error deleting '{file_to_delete}': {e}")
    
    print(f"\n--- Summary ---")
    print(f"Renamed: {renamed_count} files")
    print(f"Deleted: {deleted_count} files")

if __name__ == '__main__':
    # Confirmation before running
    confirm = input("This script will rename and DELETE duplicate numbered PNG files. Have you backed up your files? (yes/no): ")
    if confirm.lower() in ('yes', 'y'):
        main()
    else:
        print("Operation cancelled. Please backup your files before running this script.")
