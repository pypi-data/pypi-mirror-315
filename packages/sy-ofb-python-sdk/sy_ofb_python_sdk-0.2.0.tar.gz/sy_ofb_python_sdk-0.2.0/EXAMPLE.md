To start using the SDK, you'll first need to import the `Client` class from the package.

```python
from ofb_python_sdk import Client
```

### Setup

Initialize the client with your application credentials:

```python
client = Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token",
    redirect_uri="your_redirect_uri",
    disable_progress=False,  # Set to True to disable progress bar, default is False
)
```

### Upload a File

Only files smaller than 4MB can be uploaded directly. For larger files, you need to use the `upload_big_file` method.

```python
file_path = "/path/to/your/file"
file_data = open(file_path, "rb").read()
remote_path = "/path/to/onedrive/destination/file.txt"

try:
    response = client.upload_file(file_data, remote_path)
    print("Upload successful:", response.status_code)
except Exception as e:
    print("Upload failed:", e)
```

### Upload a Big File

Can upload any size of file.

```python
file_path = "/path/to/your/big/file"
file_data = open(file_path, "rb").read()
remote_path = "/path/to/onedrive/destination/big_file.txt"

try:
    response = client.upload_big_file(file_data, remote_path)
    print("Upload successful:", response.status_code)
except Exception as e:
    print("Upload failed:", e)
```

### Download a File

```python
remote_path = "/path/to/onedrive/file.txt"

try:
    file_data = client.download_file(remote_path)
    with open("downloaded_file.txt", "wb") as file:
        file.write(file_data)
    print("Download successful")
except Exception as e:
    print("Download failed:", e)
```

### Create a Folder

```python
folder_path = "/new/folder"

try:
    response = client.create_folder(folder_path)
    print("Folder creation successful:", response.status_code)
except Exception as e:
    print("Folder creation failed:", e)
```

### Delete a File

```python
remote_path = "/path/to/delete/file.txt"

try:
    response = client.delete_file(remote_path)
    print("Deletion successful:", response.status_code)
except Exception as e:
    print("Deletion failed:", e)
```

### Search a File

```python
keyword = "sometext"

try:
    result: list = client.search_files(keyword)
    print("Search successful:", result)
except Exception as e:
    print("Search failed:", e)
```

### Get a Temp Link of a File

```python
remote_path = "/path/to/onedrive/file.txt"

try:
    link = client.get_temp_link(remote_path)
    print("Temporary link:", link)
except Exception as e:
    print("Failed to get temporary link:", e)
```

### Get the Children of a Folder

```python
folder_path = "/path/to/onedrive/folder"

try:
    children = client.get_children(folder_path)
    print("Children:", children)
except Exception as e:
    print("Failed to get children:", e)
```