import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import Optional, List, Dict, Any

SCOPES = ['https://www.googleapis.com/auth/drive']

class GDriveCore:
    """Google Drive API Client for easy file and folder management.
    
    This class provides a simplified interface for common Google Drive operations
    including file uploads, downloads, folder management, and search capabilities.
    """

    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json') -> None:
        """Initialize and authenticate the Google Drive client.
        
        Args:
            credentials_file: Path to the OAuth 2.0 credentials JSON file
            token_file: Path where the user's access token will be saved
        """
        self.service = self._authenticate(credentials_file, token_file)

    def _authenticate(self, credentials_file: str, token_file: str) -> Any:
        """Authenticate and return the Google Drive service.
        
        Args:
            credentials_file: Path to the OAuth 2.0 credentials JSON file
            token_file: Path where the user's access token will be saved
            
        Returns:
            An authenticated Google Drive service object
        """
        creds = None
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            except ValueError:
                os.remove(token_file)
                creds = None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        return build('drive', 'v3', credentials=creds)

    def upload(self, file_path: str, parent_id: Optional[str] = None, 
               properties: Optional[Dict[str, str]] = None) -> str:
        """Upload a file to Google Drive with optional custom properties.
        
        Args:
            file_path: Local path to the file to upload
            parent_id: Optional ID of the parent folder in Google Drive
            properties: Optional dictionary of custom properties to add to the file
            
        Returns:
            The ID of the uploaded file in Google Drive
        """
        file_name = os.path.basename(file_path)
        metadata = {'name': file_name}
        if parent_id:
            metadata['parents'] = [parent_id]
        if properties:
            metadata['properties'] = properties

        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=metadata, media_body=media, fields='id').execute()
        return file.get('id')

    def list_files(self, query: Optional[str] = None) -> List[Dict[str, str]]:
        """List files in Google Drive based on a query.
        
        Args:
            query: Optional query string following Google Drive API syntax
            
        Returns:
            List of dictionaries containing file information (id, name)
        """
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])

    def download(self, file_id: str, local_path: str) -> None:
        """Download a file from Google Drive.
        
        Args:
            file_id: The ID of the file in Google Drive
            local_path: Local path where the file should be saved
        """
        request = self.service.files().get_media(fileId=file_id)
        with open(local_path, 'wb') as f:
            f.write(request.execute())

    def delete(self, file_id: str) -> None:
        """Delete a file from Google Drive.
        
        Args:
            file_id: The ID of the file to delete
        """
        self.service.files().delete(fileId=file_id).execute()

    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """Create a new folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to create
            parent_id: Optional ID of the parent folder
            
        Returns:
            The ID of the created folder
        """
        metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        if parent_id:
            metadata['parents'] = [parent_id]
        folder = self.service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')

    def move(self, file_id: str, new_parent_id: str, 
             old_parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Move a file to a new folder.
        
        Args:
            file_id: The ID of the file to move
            new_parent_id: The ID of the destination folder
            old_parent_id: Optional ID of the current parent folder
            
        Returns:
            Updated file metadata including new parent information
        """
        file = self.service.files().update(
            fileId=file_id,
            addParents=new_parent_id,
            removeParents=old_parent_id,
            fields='id, parents'
        ).execute()
        return file

    def update_metadata(self, file_id: str, new_name: Optional[str] = None,
                       new_description: Optional[str] = None) -> Dict[str, Any]:
        """Update file metadata.
        
        Args:
            file_id: The ID of the file to update
            new_name: Optional new name for the file
            new_description: Optional new description for the file
            
        Returns:
            Updated file metadata
        """
        metadata = {}
        if new_name:
            metadata['name'] = new_name
        if new_description:
            metadata['description'] = new_description
        updated_file = self.service.files().update(
            fileId=file_id,
            body=metadata,
            fields='id, name, description'
        ).execute()
        return updated_file

    def search(self, name_contains: Optional[str] = None,
               mime_type: Optional[str] = None) -> List[Dict[str, str]]:
        """Search for files in Google Drive.
        
        Args:
            name_contains: Optional string to search for in file names
            mime_type: Optional MIME type to filter results
            
        Returns:
            List of matching files with their IDs and names
        """
        query = []
        if name_contains:
            query.append(f"name contains '{name_contains}'")
        if mime_type:
            query.append(f"mimeType='{mime_type}'")
        query = " and ".join(query)
        return self.list_files(query=query)

    def batch_delete(self, file_ids: List[str]) -> None:
        """Delete multiple files from Google Drive.
        
        Args:
            file_ids: List of file IDs to delete
        """
        for file_id in file_ids:
            self.delete(file_id)