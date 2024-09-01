from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SERVICE_ACCOUNT_FILE = r'E:\sanjesh test\project\app\credentials.json'   # Replace with the actual path

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_gdrive(file_path, file_name, folder_id):
    try:
        # Authenticate using the service account
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        # Define file metadata
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        # Media file upload instance
        media = MediaFileUpload(file_path, mimetype='application/pdf')  # Adjust MIME type if needed

        # Create a file on Google Drive
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Generate the file's Google Drive link
        return f"https://drive.google.com/file/d/{file.get('id')}/view"
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
