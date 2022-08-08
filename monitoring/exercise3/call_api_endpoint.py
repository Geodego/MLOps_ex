import subprocess
import requests

# access to API endpoints from the workspace command line.
print('access to API endpoints from the workspace command line')
response1 = subprocess.run(['curl', 'http://127.0.0.1:8000?user=Geof'], capture_output=True).stdout
response2 = subprocess.run(['curl', 'http://127.0.0.1:8000/size?filename=testdata.csv'], capture_output=True).stdout
response3 = subprocess.run(['curl', 'http://127.0.0.1:8000/summary?filename=testdata.csv'], capture_output=True).stdout
for item in [response1, response2, response3]:
    print(item)


# access to API endpoints using the requests module.
print('access to API endpoints using the requests module')
response4 = requests.get('http://127.0.0.1:8000?user=Geof').content
response5 = requests.get('http://127.0.0.1:8000/size?filename=testdata.csv').content
response6 = requests.get('http://127.0.0.1:8000/summary?filename=testdata.csv').content
for item in [response4, response5, response6]:
    print(item)


