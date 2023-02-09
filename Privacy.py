from Scanner import Scanner
import json
import requests
import time
import spacy
import datetime
import re
import en_core_web_sm


class Privacy(Scanner):
    def __buildNotification(self, fieldName, fieldValue, piiType, piiValue, alertScore, ascoreName):
        notification = {
            "Field Name": fieldName,
            "Value": fieldValue,
            "PII Type": piiType,
            "PII Detected Value": piiValue,
            "PII Descriptiom": piiType+' was decteted',
            "Alert Score": alertScore,
            "Alert Name": ascoreName,
        }
        return notification

    def __valueToCheckPii(self, value, nlp, key):
        regex_email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        regex_zip = r"\b\d{5}(?:-\d{4})?\b"
        regex_phone = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        regex_creditcard = r"(?:\d[ -]*?){13,16}"
        regex_twitter = r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)"
        regex_ips = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        pii = {}

        if re.match(regex_email, value):
            pii['EMAIL'] = value
        if re.match(regex_zip, value):
            pii['ZIP'] = value
        if re.match(regex_phone, value):
            pii['PHONE'] = value
        if re.match(regex_creditcard, value):
            pii['CREDITCARD'] = value
        if re.match(regex_twitter, value):
            pii['TWITTER'] = value
        if re.match(regex_ips, value):
            pii['IPS'] = value
        if len(pii) == 0:
            doc = nlp(value)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "DATE"]:
                    pii[ent.label_] = ent.text
        if len(pii) == 0:
            return {"code": 400}
        else:
            return {"code": 200, "key": key, "data": pii}

    def scanObject(self, datasetID, documentID, docObject):
        items = []
        extreme = 4
        high = 3
        medium = 2
        low = 1
        ascore = 0
        ascoreName = ''
        nlp = spacy.load("en_core_web_sm")
        alart_name = ['Low', 'Medium', 'High', 'Extreme']
        assigned_value = {
            "PERSON": 4,
            "CITY": 1,
            "ADDRESS": 3,
            "NAME": 4,
            "ORG": 2,
            "GPE": 1,
            "LOC": 1,
            "CREDITCARD": 4,
            "PHONE": 4,
            "EMAIL": 4,
            "STREETADDRESS": 3,
            "STAE": 1,
            "COUNTRY": 1,
            "DATE": 1,
            "ZIP": 2,
            "POSTCODE": 2,
            "IPS": 2,
            "AGE": 2,

        }
        # nlp = en_core_web_sm.load()
        flatObject = super().flattenObject(docObject)
        # entity_to_check = ['NAME', 'ADDRESS', 'CITY', 'STATE', 'PERSON', 'ORG', 'COUNTRY', 'ZIP', 'PHONE', 'EMAIL', 'AGE', 'STREETADDRESS', 'POSTCODE', 'GPE', 'DATE', 'IPS']
        for key in flatObject:
            # if key.upper() in entity_to_check:
            valueToCheckPii = flatObject[key]
            # print(valueToCheckPii)
            values = self.__valueToCheckPii(str(valueToCheckPii), nlp, key)
            # print(values)
            if (values["code"] == 200):
                for index in values["data"]:
                    if index in assigned_value:
                        ascore = assigned_value[index]
                        ascoreName = alart_name[ascore-1]
                    else:
                        ascore = 1
                        ascoreName = 'Low'

                    items.append(self.__buildNotification(
                        key.upper(), valueToCheckPii, index, values["data"][index], ascore, ascoreName))
            # print(items)
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
