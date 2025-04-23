import requests

doc_id = "680755c9cbc175100a110700"

url = f"http://localhost:8000/kms/document/{doc_id}"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MzM4MTc3fQ.k0cY-zZVeznc6DzMlNZuXiVS_GSgVyBOfDHJTcOw-v0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.json())
