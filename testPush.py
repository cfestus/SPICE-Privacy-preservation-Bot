import requests
from requests.auth import HTTPBasicAuth
import json

# replace <dataset-id> with the id of your LDH dataset (eg f3883602-b187-47b1-9815-75ea7d12fbc5 )
# replace <access-key> with the LDH API key that has write permission to push docs into your dataset
datasetID = '***'
url = "https://api2.pp.mksmart.org/object/"+datasetID
LDHAccessKey = '***'
headers = {
        'Content-Type': 'application/json'
    }

item = {
    'attrib1': 'foozzzz',
    'attrib2': 'barzzzz'
}

singleJsonDoc = json.dumps(item, ensure_ascii=True)
response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth(LDHAccessKey, LDHAccessKey), data=singleJsonDoc, verify=False)
print(response.text)
