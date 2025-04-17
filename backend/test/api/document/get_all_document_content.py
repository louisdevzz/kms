import requests
import io
import zipfile


url = f"http://localhost:8000/kms/document/content?self=true"

params = {
    "user_id": "vohuunhan1310@gmail.com",
}

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDg4Njc0Mn0.8LKf6QbtXP3UD9PxPlLPfvD_xWKDqzTypwlsjF562xQ"
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    # Stream the ZIP file
    zip_buffer = io.BytesIO()
    for chunk in response.iter_content(chunk_size=8192):
        zip_buffer.write(chunk)

    # Extract contents
    with zipfile.ZipFile(zip_buffer) as zip_file:
        zip_file.extractall("downloaded_documents")
    print(f"Extracted {len(zip_file.namelist())} documents")
else:
    print("Error:", response.json())
