import json
import time


class Scanner:
    def __init__(self, configFilename=''):
        # Initialisation code here...
        if configFilename != '':
            with open(configFilename) as configFile:
                self.config = json.load(configFile)
        else:
            self.config = {}

    # returns an array of objects for entry into the log, or an empty array
    def scanObject(self, datasetID, documentID, docObject):
        itemsFound = False
        items = []
        # Loop through all the fields in the document
        print('*** ' + datasetID + ':' + documentID + ' ***')
        flatDoc = self.__flattenObject(docObject)
        for key in flatDoc:
            # Just a basic test here, to be replaced with appropriate document scanning
            print(key + ':' + str(flatDoc[key]))
            '''
            if '@' in docObject[key]:
                # build an appropriate notification
                itemsFound = True
                message = 'An @ symbol was found, this may indicate a email address'
                items.append(self.__buildNotification(datasetID, documentID, key, docObject[key], message))
            '''
        return items

    def flattenObject(self, originalDocument):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '/')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '/')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(originalDocument)
        return out

    def __buildNotification(self, datasetID, documentID, fieldName, fieldValue, message):
        notification = {
            "job-type": "SAMPLE-NOTIFICATION",
            "submitted-by": "LDH-SCANNER",
            "modified": int(time.time()),
            "message": message,
            "dataset": datasetID,
            "document": documentID,
            "field": fieldName,
            "value": fieldValue,
            "status": "ALERT"
        }
        return notification
