import requests

document_id = "680096a538a0c7035d0fdc9f"

url = f"http://localhost:8000/kms/document/{document_id}?self=true"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDg5NTEzM30.COj8qtcyYP8C3zcoOGFFk6IBC9hfU5XG2oUg1Fjk7lU"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception as e:
    print("Error parsing JSON:", e)
    print("Raw Response:", response.text)
