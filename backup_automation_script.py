# add modifications to this script :
# 1. script should run automatically at a set time.
# 2. the final destination of the files should be the cloud directory not the local.

import os
import shutil
from datetime import datetime, timedelta
 
def get_daily_backups(folder_path, target_date):
    files = []
 
    for root, dirs, filenames in os.walk(folder_path):
        for name in filenames:
            if name.endswith('.bak'):
                parts = name.split('_')
 
                date_format = '%Y_%m_%d'
                if len(parts) >= 5 and len(parts[3]) == 6:
                    date_format += '_%H%M%S'
 
                try:
                    backup_date = datetime.strptime('_'.join(parts[2:5]), date_format)
                except ValueError:
                    continue
 
                if backup_date.date() == target_date:
                    files.append(os.path.join(root, name))
 
    return files
 
def copy_previous_day_files(source_folder, destination_folder):
    # Get the current date and calculate the previous day
    today = datetime.now().date()
    previous_day = today - timedelta(days=1)
 
    print(f"Current Date: {today}")
    print(f"Previous Day: {previous_day}")
 
    # Get the list of files from the previous day
    files_to_copy = get_daily_backups(source_folder, previous_day)
 
    for source_path in files_to_copy:
        # Generate the destination path
        destination_path = os.path.join(destination_folder, os.path.basename(source_path))
 
        print(f"Copying content from: {source_path} to {destination_path}")
 
        # Copy the content of the file to the destination
        shutil.copy2(source_path, destination_path)
 
        print(f"Successfully copied content from: {source_path} to {destination_path}")
 
# Set the source and destination paths
folder_path = "A:\\Backups"
destination = "A:\\Cloud"
 
# Call the function to copy content for .bak files from the previous day
copy_previous_day_files(folder_path, destination)
