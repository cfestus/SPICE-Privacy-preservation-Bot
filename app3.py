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
    url = "https://api2.mksmart.org/changes/0a3b44d1-bfa6-45a5-ac02-0c0a3a30e8c2"
    headers = {
        'Authorization': 'Basic M2JjMzdkMTEtMjAyZi00OGM4LWJhMDEtYmIxYjNmOTIzNjE5OjNiYzM3ZDExLTIwMmYtNDhjOC1iYTAxLWJiMWIzZjkyMzYxOQ=='
    }
    response = requests.request("GET", url, headers=headers)
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
    namesResult = funcCheckUserRequest()
    api_names = namesResult['name']
    character_names = []
    with open("data2.txt", "r", encoding="utf-8") as f:
        characters = f.read().split("\n\n")
        # characters = api_names

        for character in characters:
            names = character.split()
            for name in names:

                chedck_value = CommonRegex(name)
                if chedck_value.times:
                    character_names.append(chedck_value.times)
                if chedck_value.dates:
                    character_names.append(chedck_value.dates)
                if chedck_value.links:
                    character_names.append(chedck_value.links)
                if chedck_value.phones:
                    character_names.append(chedck_value.phones)
                if chedck_value.emails:
                    character_names.append(chedck_value.emails)
                if chedck_value.credit_cards:
                    character_names.append(chedck_value.credit_cards)
                if chedck_value.street_addresses:
                    character_names.append(chedck_value.street_addresses)
                if chedck_value.ips:
                    character_names.append(chedck_value.ips)

        charactersNames = re.sub('[!@#$]', '', str(characters))
        test = charactersNames
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(test)
        for ent in doc.ents:
            name = ent.text, ent.label_
            character_names.append(name)

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


def printVal():
    print(runUserRequest())


schedule.every(1).minutes.do(printVal)
while 1:
    schedule.run_pending()
    time.sleep(1)
