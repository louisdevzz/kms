import requests


url = f"http://localhost:8000/kms/document/ids?self=true"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDg4Njc0Mn0.8LKf6QbtXP3UD9PxPlLPfvD_xWKDqzTypwlsjF562xQ"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.json())
