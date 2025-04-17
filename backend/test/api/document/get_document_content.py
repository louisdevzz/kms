import requests

document_id = "68009cc91b467653242312c2"

url = f"http://localhost:8000/kms/document/{document_id}/content?self=true"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDg5ODQ0NH0.2Qu6UgCvl801TzqCkFVHHCys71D2WHH3R7IE5c_OQew"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

