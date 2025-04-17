import requests

document_id = "67ff6896f9ff7650461d5b09"

url = f"http://localhost:8000/kms/document/{document_id}?self=true"

params = {
    "user_id": "vohuunhan1310@gmail.com",
}

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDg0Nzk0OH0.o6ilEH7PiRnNJ-qmeI92gOcGViYnsKDDBaV_h5sluIU"
}

response = requests.get(url, params=params, headers=headers)

print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception as e:
    print("Error parsing JSON:", e)
    print("Raw Response:", response.text)
