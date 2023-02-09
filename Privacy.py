from Scanner import Scanner
import json
import requests
import time
import spacy
import datetime


class Privacy(Scanner):
    # returns an array of objects for entry into the log, or an empty array

    # returns an array of objects for entry into the log, or an empty array
    def scanObject(self, datasetID, documentID, docObject):
        items = []
        # Initialize dictionary to store PII
        pii = {}
        # Loop through all the fields in the document
        nlp = spacy.load("en_core_web_sm")

        flatObject = super().flattenObject(docObject)

        for key in flatObject:

            # Load spaCy model
            # Just a basic test here, to be replaced with appropriate document scanning

            entity_to_check = ['NAME', 'ADDRESS', 'CITY', 'STATE', 'PERSON', 'ORG',
                               'COUNTRY', 'ZIP', 'PHONE', 'EMAIL', 'AGE',
                               'STREETADDRESS', 'POSTCODE', 'GPE', 'DATE', 'IPS']

            if key.upper() in entity_to_check:

                doc = nlp(str(flatObject[key]))
                for ent in doc.ents:
                    if ent.label_ in ["PERSON", "ORG", "GPE", "LOC"]:
                        pii[ent.label_] = ent.text

                piiResult = str(pii)

                extreme = 4
                high = 3
                medium = 2
                low = 1
                ascore = 0
                ascoreName = ''
                if piiResult in ["PERSON"]:
                    ascore = extreme
                    ascoreName = 'extreme'
                elif piiResult in ["ORG"]:
                    ascore = medium
                    ascoreName = 'medium'
                elif key.upper() in ["GPE", "LOC"]:
                    ascore = low
                    ascoreName = 'low'
                elif key.upper() in ["NAME", "CREDITCARD", "PHONE", "EMAIL"]:
                    ascore = extreme
                    ascoreName = 'extreme'
                elif key.upper() in ["ADDRESS", "STREETADDRESS"]:
                    ascore = high
                    ascoreName = 'high'
                elif key.upper() in ["CITY", "STATE", "COUNTRY", "DATE"]:
                    ascore = low
                    ascoreName = 'low'
                elif key.upper() in ["ZIP", "POSTCODE", "IPS", "AGE"]:
                    ascore = medium
                    ascoreName = 'medium'
                else:
                    ascore = ascore

                items.append(self.__buildNotification(
                    key, flatObject[key], ascore, ascoreName))

        total_alert_score = 0
        severityScores = ''

        for item in items:
            total_alert_score += item['Alert Score']
            if total_alert_score >= 4:
                severityScores = "extreme"
            elif total_alert_score == 3:
                severityScores = "high"
            elif total_alert_score == 2:
                severityScores = "medium"
            else:
                severityScores = "low"

      # Get the current date
        current_date = datetime.datetime.now().date()

        return [{
            "job-type": "PRIVACY-VIOLATION",
            "Date": current_date.strftime("%m/%d/%Y"),
            "TimeStam": int(time.time()),
            "Document ID": documentID,
            "Status": "ALERT",
            "SeverityScores": severityScores,
            "Description": 'Personal identifiable information was decteted in this document',
            'Fields': items
        }]

    def __buildNotification(self, fieldName, fieldValue, alertScore, ascoreName):

        notification = {
            "Field Name": fieldName,
            "Value": fieldValue,
            "PII Type": fieldName,
            "PII Descriptiom": fieldName+' was decteted',
            "Alert Score": alertScore,
            "Alert Name": ascoreName,
        }

        return notification
