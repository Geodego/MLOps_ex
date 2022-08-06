import requests

url = "http://192.168.1.17:8000?user=Marc"
response1 = requests.get(url)
print(f"status get request: {response1.status_code}")
print(response1.text)