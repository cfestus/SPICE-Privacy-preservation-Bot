import json
import re
import schedule
import time
import requests
import spacy
import time
import commonregex
import pandas as pd

from commonregex import CommonRegex
from spacy import displacy
nlp = spacy.load("en_core_web_sm")


def funcCheckUserRequest():
    url = 'https://api2.pp.mksmart.org/browse/spice__activity_log'
    headers = {
        'Authorization': 'Basic YWN0aXZpdHlsb2dfcmVhZGtleTphY3Rpdml0eWxvZ19yZWFka2V5'
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    if response.status_code == 200:

        data = response.json()
        df = pd.DataFrame(data)
        maxes_by_group = df.groupby(['_id'])['_timestamp'].transform(max)
        resultData = df[df['_timestamp'] ==
                        maxes_by_group].to_dict(orient='records')
        payload = str(resultData[0]['@type'][0])

        if "Create" or "Update" in payload:
            getName = json.loads(resultData[0]['al:request']['al:payload'])
            return getName
    else:
        return '[!] HTTP {0} calling [{1}]'.format(response.status_code)


def runUserRequest():
    print("****Welcome to my bot*****")
    # namesResult = funcCheckUserRequest()
    # api_names = namesResult['name']
    character_names = []
    with open("data2.txt", "r", encoding="utf-8") as f:
        characters = f.read().split("\t")
        print("***characters***")
        print(characters)
        # characters = api_names

        for character in characters:
            names = character.split()
            for name in names:

                chedck_value = CommonRegex(name)
                if chedck_value.times:
                    character_names.append(chedck_value.times)
                    print("found times")
                if chedck_value.dates:
                    character_names.append(chedck_value.dates)
                    print("found dates")
                if chedck_value.links:
                    character_names.append(chedck_value.links)
                    print("found links")
                if chedck_value.phones:
                    character_names.append(chedck_value.phones)
                    print("found phones")
                if chedck_value.emails:
                    character_names.append(chedck_value.emails)
                    print("found emails")
                if chedck_value.credit_cards:
                    character_names.append(chedck_value.credit_cards)
                    print("found cards")
                if chedck_value.street_addresses:
                    character_names.append(chedck_value.street_addresses)
                    print("found addresses")
                if chedck_value.ips:
                    character_names.append(chedck_value.ips)
                    print("found ips")

        print("*** printing character names ***")
        print(character_names)

        charactersNames = re.sub('[!@#$]', '', str(characters))
        test = charactersNames
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(test)
        for ent in doc.ents:
            print("entity")
            print(ent)
            name = ent.text, ent.label_
            character_names.append(name)

        print("*** printing character names after NLP ***")
        print(character_names)

    # If length of character_names array > 0 (ie we found something), then build an appropriate JSON response, else return false

    return True
'''
    return {
        "job-type": "PRIVACY-VIOLATION",
        "submitted-by": "privacy-module",
        "modified": "privacy-module",
        "history": [
            {
                "message": character_names,
                "timestamp": time.time()
            }
        ],
        "message": "the document has violated the following..",
        "dataset": "",
        "status": "ALERT"
    }
'''


def printVal():
    print(runUserRequest())


print(runUserRequest())

'''
schedule.every(1).minutes.do(printVal)
while 1:
    schedule.run_pending()
    time.sleep(1)
'''
