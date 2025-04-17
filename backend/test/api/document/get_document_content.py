import requests

document_id = "67ff6896f9ff7650461d5b09"

url = f"http://localhost:8000/kms/document/{document_id}/content?self=true"

params = {
    "user_id": "vohuunhan1310@gmail.com",
}

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDg4Njc0Mn0.8LKf6QbtXP3UD9PxPlLPfvD_xWKDqzTypwlsjF562xQ"
}

response = requests.get(url, params=params, headers=headers)

print("Status Code:", response.status_code)

