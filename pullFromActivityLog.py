import requests
from requests.auth import HTTPBasicAuth
import json

baseUrl = 'https://api2.pp.mksmart.org/browse/'
alDataset = 'spice__activity_log'
alDatasetKey = 'activitylog_readkey'
pagesize = 20
page = 1
initialTimestamp = str(1667306718)   # 1st November 2022

# Exclude these datasets from our analysis
# At the very least, this should include the dataset we are using to push privacy violation results to,
# since there is no need to analyse this dataset for privacy violations
datasetsToExclude = ['spice_rdfjobs2']

headers = {
        'Content-Type': 'application/json'
    }

# This query should be generated with an appropriate timestamp filter (not 10)
query = '{"$and": [ { "_timestamp": {"$gte": '+initialTimestamp+'} }, { "$or" : [{"@type": "al:Update" }, {"@type": "al:Create" }] } ]}'
queryParam = 'query=' + query
pageParam = 'page=' + str(page)
pagesizeParam = 'pagesize=' + str(pagesize)
alFullUrl = baseUrl + alDataset + '?' + queryParam + '&' + pagesizeParam + '&' + pageParam
# verify=False is needed in the dev phase as api2.pp.mksmart.org has an invalid/mismatched SSL cert
response = requests.request("GET", alFullUrl, headers=headers, auth=HTTPBasicAuth(alDatasetKey, alDatasetKey), verify=False)
# Turn the JSON HTTP response into a Python-readable object
responseObject = response.json()
# Some attributes from the response object
numResults = int(responseObject['documentCount'])
resultsPage = int(responseObject['page'])
resultsPageSize = int(responseObject['pagesize'])

print(numResults, resultsPage, resultsPageSize)
if (numResults == resultsPageSize):
    # There is likely to be a second page of results, so another request should be made for page 2, 3...
    print("numResults == pagesize, there is likely another page of results that needs to be requested")

alEntries = responseObject['results']
for alEntry in alEntries:
    # Exclude AL entries for datasets we have decided to exclude
    #print(alEntry)
    # print('Dataset: ', alEntry['al:datasetId'])
    # print('Document ID: ', alEntry['al:documentId'])
    # payload = alEntry['al:request']['al:payload']
    # payloadObject = json.loads(payload)
    # print(payloadObject)
    # print("*****************")

    if alEntry['al:datasetId'] not in datasetsToExclude:
        print('*********************')
        print('Dataset: ', alEntry['al:datasetId'])
        print('Document ID: ', alEntry['al:documentId'])
        print('Timestamp: ', alEntry['_timestamp'])
        payload = alEntry['al:request']['al:payload']
        payloadObject = json.loads(payload)
        print(payloadObject)
        # print each key:value pair from the payload - these values are presumably the items you will analyse for privacy violations
        for key in payloadObject:
            print(key, ":", payloadObject[key])



