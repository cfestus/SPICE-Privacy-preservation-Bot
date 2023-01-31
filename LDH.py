import json
import requests
from requests.auth import HTTPBasicAuth
from os import path

file_path = path.abspath(__file__)
dir_path = path.dirname(file_path)
json_file_path = path.join(dir_path,"ldh-config.json") 



class LDH:
    def __init__(self):
        with open(json_file_path) as configFile:
            self.config = json.load(configFile)


    def getALEntries(self, page, timestamp):
        headers = {
            'Content-Type': 'application/json'
        }
        if int(timestamp) == 0:
            initialTimestamp = self.config['activityLog']['initialTimestamp']
        else:
            initialTimestamp = int(timestamp)
        baseUrl = self.config['ldhServer']
        alDataset = self.config['activityLog']['datasetID']
        alDatasetKey = self.config['activityLog']['key']
        pagesize = self.config['activityLog']['pagesize']
        datasetsToExcludeStringList = ''
        for item in self.config['activityLog']['datasetsToExclude']:
            if datasetsToExcludeStringList == '':
                datasetsToExcludeStringList += '"' + item + '"'
            else:
                datasetsToExcludeStringList += ',"' + item + '"'

        query = '{"$and": [ { "_timestamp": {"$gte": ' + str(initialTimestamp) + '} }, { "$or" : [{"@type": "al:Update" }, {"@type": "al:Create" }] }, {"al:datasetId": {"$nin":['+datasetsToExcludeStringList+']}} ]}'
        queryParam = 'query=' + query
        pageParam = 'page=' + str(page)
        pagesizeParam = 'pagesize=' + str(pagesize)
        alFullUrl = baseUrl + '/browse/' + alDataset + '?' + queryParam + '&' + pagesizeParam + '&' + pageParam
        # verify=False is needed in the dev phase as api2.pp.mksmart.org has an invalid/mismatched SSL cert
        response = requests.request("GET", alFullUrl, headers=headers, auth=HTTPBasicAuth(alDatasetKey, alDatasetKey), verify=False)
        return response.json()


    def pushNotification(self, notification):
        baseUrl = self.config['ldhServer']
        notificationDataset = self.config['notifications']['datasetID']
        notificationDatasetKey = self.config['notifications']['key']
        headers = {
            'Content-Type': 'application/json'
        }
        fullUrl = baseUrl + '/object/' + notificationDataset
        singleJsonDoc = json.dumps(notification, ensure_ascii=True)
        response = requests.request("POST", fullUrl, headers=headers, auth=HTTPBasicAuth(notificationDatasetKey, notificationDatasetKey), data=singleJsonDoc, verify=False)
        return response
