import requests

name = "Test Text Document"

url = f"http://localhost:8000/kms/document/search?name={name}"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MzMyMTczfQ.tY9xeHeLjoLi0t2Lb-lOsusVn5Nn9T6xu4w8mRHVbA4"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.json())
