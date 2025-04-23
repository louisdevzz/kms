import requests

document_id = "68073d697fe0de018f4d3f3c"

url = f"http://localhost:8000/kms/document/{document_id}?self=true"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ1MzMyMTczfQ.tY9xeHeLjoLi0t2Lb-lOsusVn5Nn9T6xu4w8mRHVbA4"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception as e:
    print("Error parsing JSON:", e)
    print("Raw Response:", response.text)
