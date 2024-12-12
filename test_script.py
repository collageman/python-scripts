import os
import shutil
from datetime import datetime, timedelta
import schedule
import time
from onedrivesdk import AuthProvider, HttpProvider, OneDriveClient

def authenticate_onedrive():
    redirect_uri = 'http://localhost:8080'
    client_secret = ''  # Replace with your client secret
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    auth_provider = AuthProvider(
        client_id='your_client_id',  # Replace with your client ID
        scopes=scopes)

    client = OneDriveClient('your_client_id', auth_provider, http_provider=HttpProvider(), redirect_uri=redirect_uri)
    auth_url = client.auth_provider.get_auth_url(redirect_uri)
    print('Paste this URL into your browser, authenticate, and paste the resulting URL here:')
    print(auth_url)
    auth_code = input('Paste URL here:')
    client.auth_provider.authenticate(auth_code, redirect_uri, client_secret)
    return client

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

def copy_previous_day_files(source_folder, destination_client):
    # Get the current date and calculate the previous day
    today = datetime.now().date()
    previous_day = today - timedelta(days=1)

    print(f"Current Date: {today}")
    print(f"Previous Day: {previous_day}")

    # Get the list of files from the previous day
    files_to_copy = get_daily_backups(source_folder, previous_day)

    for source_path in files_to_copy:
        # Generate the destination path
        destination_path = os.path.basename(source_path)
        print(f"Copying content from: {source_path} to {destination_path}")

        # Upload the content of the file to the destination
        with open(source_path, 'rb') as file:
            destination_client.item(drive='me', id='root').children[destination_path].upload(file)

        print(f"Successfully copied content from: {source_path} to {destination_path}")

# Set the source and destination paths
folder_path = "A:\\Backups"

# Authenticate and establish connection to OneDrive
onedrive_client = authenticate_onedrive()

# Schedule the script to run daily at a specific time (e.g., 2:00 AM)
schedule.every().day.at("02:00").do(lambda: copy_previous_day_files(folder_path, onedrive_client))

while True:
    schedule.run_pending()
    time.sleep(1)
