from Scanner import Scanner
import json
import requests
import time
import spacy
import datetime
import re
import en_core_web_sm

nlp = spacy.load("en_core_web_sm")


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
        regex_age = r"born on \d{2}/\d{2}/\d{4}"
        regex_postcode = r"\b([A-Z]{1,2}\d[A-Z]|[A-Z]{1,2}\d{1,2})\ +\d[A-Z-[CIKMOV]]{2}\b"
        regex_street_address = r"\d+\s+[A-Za-z]+\s+[A-Za-z]+"
        regex_address = r"\d+\s+[A-Za-z]+\s+[A-Za-z]+,[\sA-Za-z]+,\s[A-Za-z]+\s\d+"

        pii = {}

        find_email = re.findall(regex_email, value)
        if find_email:
            pii['EMAIL'] = find_email
        find_zip = re.findall(regex_zip, value)
        if find_zip:
            pii['ZIP'] = find_zip
        find_phone = re.findall(regex_phone, value)
        if find_phone:
            pii['PHONE'] = find_phone
        find_creditcard = re.findall(regex_creditcard, value)
        if find_creditcard:
            pii['CREDITCARD'] = find_creditcard
        find_twitter = re.findall(regex_twitter, value)
        if find_twitter:
            pii['TWITTER'] = find_twitter
        find_ips = re.findall(regex_ips, value)
        if find_ips:
            pii['IPS'] = find_ips
        find_age = re.findall(regex_age, value)
        if find_age:
            birthdate = find_age.group().split(" ")[-1]
            age = calculate_age(birthdate)
            pii['AGE'] = find_age
        find_postcode = re.findall(regex_postcode, value)
        if find_postcode:
            pii['POSTCODE'] = find_postcode
        find_street_address = re.findall(regex_street_address, value)
        if find_street_address:
            pii['STREETADDRESS'] = find_street_address
        find_address = re.findall(regex_address, value)
        if find_address:
            pii['ADDRESS'] = find_address

        # if len(pii) == 0:
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
        EXTREME = 4
        HIGH = 3
        MEDIUM = 2
        LOW = 1
        ascore = 0
        ascoreName = ''

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
        # flatten the docObject
        flatObject = super().flattenObject(docObject)
        # print('flatten object: ', flatObject)

        for key in flatObject:
            # if key.upper() in entity_to_check:
            valueToCheckPii = flatObject[key]
            values = self.__valueToCheckPii(str(valueToCheckPii), nlp, key)
            #print(key, values)
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

        # If the method does not catch any PII, return an empty list
        if not items:
            return []

        total_alert_score = 0
        severityScores = ''
        for item in items:
            total_alert_score += item['Alert Score']
            if total_alert_score >= 4:
                severityScores = "EXTREME"
            elif total_alert_score == 3:
                severityScores = "HIGH"
            elif total_alert_score == 2:
                severityScores = "MEDIUM"
            else:
                severityScores = "LOW"

      # Get the current date
        current_date = datetime.datetime.now().date()
        return [{
            "job-type": "PRIVACY-VIOLATION",
            "Date": current_date.strftime("%m/%d/%Y"),
            "TimeStamp": int(time.time()),
            "Document ID": documentID,
            "Status": "ALERT",
            "SeverityScores": severityScores,
            "Description": 'Personal identifiable information was decteted in this document',
            'Fields': items
        }]
