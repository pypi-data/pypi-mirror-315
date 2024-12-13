# gdrive-core

A minimal and functional Google Drive API wrapper for Python. Easily perform Google Drive file operations like upload, download, list, delete, and manage metadata with an intuitive class-based interface.

## Features

- **Flexible Authentication**: Supports OAuth2 and Service Account authentication.
- **File Management**: Upload (with progress tracking), download (with progress tracking), list, and delete files effortlessly. Supports streamed uploads/downloads.
- **Folder Management**: Create folders and organize files.
- **Custom Metadata**: Add and manage arbitrary custom properties to files, and update metadata.
- **Batch Operations**: Delete multiple files at once using parallel processing.
- **Advanced Search**: Search for files using multiple criteria such as name, MIME type, and trashed status.
- **File Sharing**: Share files with specific permissions.
- **File Revisions**: Access a file's revision history.
- **Copy Files**: Create copies of existing files.
- **Storage Quota**: Retrieve information about your Google Drive storage usage.
- **Push Notifications**: Set up webhooks to watch for file changes.
- **File Export**: Export Google Workspace files in various formats.
- **OOP Interface**: Interact with Google Drive through a clean, class-based API.
- **Logging**: Integrated logging for better monitoring and debugging.
- **Retry Mechanism**: Automatic retries for API calls to handle transient errors.


## Installation

Install the package using pip:

```bash
pip install gdrive-core
```

## Setup

Before using `gdrive-core`, ensure you have:

1. **Google Cloud Credentials**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Drive API** for your project.
   - Download the `credentials.json` file for either an OAuth 2.0 Client ID or a Service Account.
   - Place the `credentials.json` file in your working directory.
   - **For OAuth2:**
        - The first time you run the program with OAuth2, it will prompt you to authenticate via a browser.
        - A `token.json` file will be created to store access tokens for future use.
   - **For Service Account:**
        - No `token.json` file is necessary as credentials are managed by the `credentials.json` file.

## Usage

### 1. Authenticate and Initialize the Client

Initialize the `GDriveCore` client for interacting with Google Drive. You can choose between `oauth2` and `service_account` authentication types.

```python
from gdrive_core import GDriveCore

# Initialize the client with OAuth2
client = GDriveCore(auth_type='oauth2', credentials_file='credentials.json', token_file='token.json')

# Initialize the client with Service Account
# client = GDriveCore(auth_type='service_account', credentials_file='credentials.json')
```

### 2. Upload a File with Custom Metadata and Progress Tracking

Upload a file to Google Drive, optionally adding custom properties and using a callback function to track progress.

```python
def upload_progress(progress):
    print(f"Upload progress: {progress:.2f}%")

# Upload a file with progress tracking and custom properties
file_id = client.upload('example.txt', properties={'is-penguin': 'true', 'category': 'animal'}, progress_callback=upload_progress)
print(f"Uploaded file ID: {file_id}")
```

### 3. List Files

List files in the root directory or filter files using queries.

```python
# List all files
files = client.list_files()
print("Files in Drive:")
for f in files:
    print(f"- {f['name']} (ID: {f['id']})")
```

### 4. Download a File with Progress Tracking

Download a file from Google Drive using its file ID. You can track the progress using a callback function.

```python
def download_progress(progress):
    print(f"Download progress: {progress:.2f}%")

# Download a file
download_path = 'downloaded_example.txt'
client.download(file_id, download_path, progress_callback=download_progress)
print(f"File downloaded to: {download_path}")
```

### 5. Create a Folder

Create a new folder in Google Drive to organize your files.

```python
# Create a folder
folder_id = client.create_folder('NewFolder')
print(f"Folder created with ID: {folder_id}")
```

### 6. Move a File to a Folder

Move an existing file into a specific folder.

```python
# Move the file to the new folder
client.move(file_id, new_parent_id=folder_id)
print("File moved successfully!")
```

### 7. Update File Metadata

Update a file's name or description.

```python
# Update file metadata
client.update_metadata(file_id, metadata={'name': 'renamed_example.txt', 'description': 'Updated metadata'})
print("File metadata updated!")
```

### 8. Search for Files

Search for files matching specific criteria like name, MIME type, and trashed status.

```python
# Search for files
results = client.search(query_params={'name_contains': 'example', 'mime_type': 'text/plain', 'trashed': 'false'})
print("Search results:")
for file in results:
    print(f"- {file['name']} (ID: {file['id']})")
```

### 9. Batch Delete Files

Delete multiple files at once by providing their file IDs.

```python
# Batch delete files
deletion_results = client.batch_delete([file_id])
print(f"Files deleted successfully: {deletion_results}")
```

### 10. Share a File

Share a file with another user with a specific role (e.g., reader, writer).

```python
# Share file with reader access
share_result = client.share(file_id, email='user@example.com', role='reader')
print(f"File shared successfully: {share_result}")
```

### 11. Get File Revisions

Get a list of previous versions (revisions) of a file.

```python
# Get file revisions
revisions = client.get_file_revisions(file_id)
print(f"File revisions: {revisions}")
```

### 12. Copy a File

Create a copy of an existing file.

```python
# Create a copy of the file
copied_file_id = client.copy_file(file_id, new_name='example_copy.txt')
print(f"Copied file ID: {copied_file_id}")
```

### 13. Get Storage Quota

Retrieve the storage usage of your Google Drive.

```python
# Get storage quota
quota = client.get_storage_quota()
print(f"Storage quota: {quota}")
```

### 14. Watch File for Changes

Set up a webhook to receive notifications when the file is modified.

```python
# Watch file for changes
watch_response = client.watch_file(file_id, webhook_url='https://your-webhook-url.com')
print(f"Watch setup result: {watch_response}")
```

### 15. Export a File

Export a Google Workspace file to a specific format.

```python
# Export file to PDF
exported_file = client.export_file(file_id, mime_type='application/pdf')
with open('exported.pdf', 'wb') as f:
    f.write(exported_file.read())
print(f"File exported to 'exported.pdf'")
```

## Full Example

Here is a more complete example showcasing multiple features.

```python
from gdrive_core import GDriveCore
import os

# Initialize the client
client = GDriveCore('credentials.json')

# Create a dummy file
with open('example.txt', 'w') as f:
  f.write("This is an example file.")

# Upload a file
file_id = client.upload('example.txt', properties={'is-penguin': 'true'})
print(f"Uploaded file ID: {file_id}")

# Create a folder
folder_id = client.create_folder('NewFolder')
print(f"Created folder ID: {folder_id}")

# Move the file to the folder
client.move(file_id, new_parent_id=folder_id)
print("File moved successfully!")

# List files in the folder
files = client.list_files(query=f"'{folder_id}' in parents")
print("Files in folder:")
for f in files:
    print(f"- {f['name']} (ID: {f['id']})")

# Download the file
download_path = 'downloaded_example.txt'
client.download(file_id, download_path)
print(f"File downloaded to: {download_path}")

# Update file metadata
client.update_metadata(file_id, metadata={'name':'renamed_example.txt', 'description': 'Updated metadata'})
print("File metadata updated!")

# Search for files
search_results = client.search(query_params={'name_contains': 'renamed_example'})
print("Search results:", search_results)

# Delete the file
client.delete(file_id)
print("File deleted successfully!")

# Clean up the dummy file
os.remove('example.txt')
```

## Troubleshooting

- **Missing `credentials.json`**: Ensure the `credentials.json` file is placed in the working directory.
- **Token Issues (OAuth2)**: If you face authentication problems, delete the `token.json` file and re-authenticate.
- **Service Account Issues**: Ensure the service account has the necessary permissions to access your Google Drive.
- **Custom Metadata**: Ensure custom property keys and values conform to Google Drive's property limitations.
- **Rate Limits**: Google Drive API has rate limits. If you encounter issues, consider implementing retry mechanisms or exponential backoff.

## License

`gdrive-core` is released under the MIT License.