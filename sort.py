import os
import shutil
import re

def sort_images_by_suffix(source_folder):
    """
    Organizes .tif files into subfolders based on channel markers.
    Returns a message and a success boolean.
    """
    if not os.path.exists(source_folder):
        return "Folder not found.", False

    files = [f for f in os.listdir(source_folder) if f.lower().endswith('.tif')]
    if not files:
        return "No .tif files found.", False

    moved_count = 0
    for filename in files:
        parts = re.split(r'_(405|488)', filename)

        if len(parts) > 1:
            parent_folder_name = parts[0].strip()
            target_dir = os.path.join(source_folder, parent_folder_name, 'im')
            os.makedirs(target_dir, exist_ok=True)

            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_dir, filename)

            try:
                shutil.move(source_path, target_path)
                moved_count += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")

    return f"Successfully moved {moved_count} files.", True
