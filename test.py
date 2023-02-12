from Privacy import Privacy
import re

# Test Data 1
privacy = Privacy()
obj = privacy.scanObject("dataset1", "doc1", {"key1": "Please send me something on @drcfu [preferably 13/02/2023] here: enrico@example.org or go away!",
                         "museum": "Irish museum of modern art", "details": [{"address": "Meet me at MK17 3FE (or 99950) or festus@piisolution.org"},
                                                                             {"purchases": "James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903"}]})

# RESULT for Test 1
# [{'job-type':'PRIVACY-VIOLATION', 'Date':'02/11/2023', 'TimeStamp':1676159892, 'Document ID':'doc1', 'Status':'ALERT', 'SeverityScores':'EXTREME',
# 'Description': 'Personal identifiable information was decteted in this document', 'Fields': [{'Field Name':'KEY1', 'Value':'Please send me something on @drcfu [preferably 13/02/2023] here: enrico@example.org
# or go away!', 'PII Type': 'EMAIL', 'PII Detected Value': ['enrico@example.org'], 'PII Descriptiom': 'EMAIL was decteted', 'Alert Score': 4, 'Alert Name': 'Extreme'}, {'Field Name': 'KEY1',
# 'Value': 'Please send me something on @drcfu [preferably 13/02/2023] here: enrico@example.org or go away!', 'PII Type': 'SOCIALMEDIA', 'PII Detected Value': ['drcfu'],
# 'PII Descriptiom': 'SOCIALMEDIA was decteted', 'Alert Score': 3, 'Alert Name': 'High'}, {'Field Name': 'KEY1', 'Value': 'Please send me something on @drcfu [preferably 13/02/2023] here: enrico@example.org or
# go away!', 'PII Type': 'DATE', 'PII Detected Value': ['13/02/2023'], 'PII Descriptiom': 'DATE was decteted', 'Alert Score': 1, 'Alert Name': 'Low'}, {'Field Name': 'DETAILS/0/ADDRESS', 'Value': 'Meet me at
# MK17 3FE (or 99950) or festus@piisolutionå.org', 'PII Type': 'EMAIL', 'PII Detected Value': ['festus@piisolution.org'], 'PII Descriptiom': 'EMAIL was decteted', 'Alert Score': 4, 'Alert Name': 'Extreme'},
# {'Field Name': 'DETAILS/0/ADDRESS', 'Value': 'Meet me at MK17 3FE (or 99950) or festus@piisolution.org', 'PII Type': 'ZIP', 'PII Detected Value': ['99950'], 'PII Descriptiom': 'ZIP was decteted',
# 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': 'DETAILS/0/ADDRESS', 'Value': 'Meet me at MK17 3FE (or 99950) or festus@piisolution.org', 'PII Type': 'POSTCODE', 'PII Detected Value': [('MK17', '3FE')],
# 'PII Descriptiom': 'POSTCODE was decteted', 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper
# Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903', 'PII Type': 'ZIP', 'PII Detected Value': ['10003'], 'PII
# Descriptiom': 'ZIP was decteted', 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper Square,
# New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903', 'PII Type': 'VISACARD', 'PII Detected Value': ['4007702835532454'],
# 'PII Descriptiom': 'VISACARD was decteted', 'Alert Score': 4, 'Alert Name': 'Extreme'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper
# Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903', 'PII Type': 'MASTERCARD', 'PII Detected Value': [
# '5425233430109903'], 'PII Descriptiom': 'MASTERCARD was decteted', 'Alert Score': 4, 'Alert Name': 'Extreme'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255,
# then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903', 'PII Type': 'IPS', 'PII Detected Value': [
# '255.255.255.255'], 'PII Descriptiom': 'IPS was decteted', 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255, t
# hen to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903', 'PII Type': 'STREETADDRESS',
# 'PII Detected Value': [''], 'PII Descriptiom': 'STREETADDRESS was decteted', 'Alert Score': 3, 'Alert Name': 'High'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected
# via 255.255.255.255, then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454, 5425233430109903', 'PII Type':
# 'ADDRESS', 'PII Detected Value': ['20 Cooper Square, New York, NY 10003'], 'PII Descriptiom': 'ADDRESS was decteted', 'Alert Score': 3, 'Alert Name': 'High'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': '
# James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454,
# 5425233430109903', 'PII Type': 'DATE', 'PII Detected Value': ['12/03/1999'], 'PII Descriptiom': 'DATE was decteted', 'Alert Score': 1, 'Alert Name': 'Low'}, {'Field Name': 'DETAILS/1/PURCHASES', 'Value': '
# James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure there is cash,4007702835532454,
# 5425233430109903', 'PII Type': 'DATE OF BIRTH', 'PII Detected Value': [('born on', '12/03/1999')], 'PII Descriptiom': 'DATE OF BIRTH was decteted', 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': '
# DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure
# there is cash,4007702835532454, 5425233430109903', 'PII Type': 'PERSON', 'PII Detected Value': 'James', 'PII Descriptiom': 'PERSON was decteted', 'Alert Score': 4, 'Alert Name': 'Extreme'}, {'Field Name': '
# DETAILS/1/PURCHASES', 'Value': 'James born on 12/03/1999, connected via 255.255.255.255, then to 20 Cooper Square, New York, NY 10003, USA for payment of all the things you want to buy because I am not sure
# there is cash,4007702835532454, 5425233430109903', 'PII Type': 'GPE', 'PII Detected Value': 'USA', 'PII Descriptiom': 'GPE was decteted', 'Alert Score': 1, 'Alert Name': 'Low'}]}]


# Test data 2
# obj = privacy.scanObject(
#     "document_id", "docObject", {"Key2": "I saw James Smith of Google LTD in MK7 6AA while I visited UK"})

# RESULT for Test 2
# [{'job-type': 'PRIVACY-VIOLATION', 'Date': '02/11/2023', 'TimeStamp': 1676154460, 'Document ID': 'docObject', 'Status': 'ALERT', 'SeverityScores': 'EXTREME',
# 'Description': 'Personal identifiable information was decteted in this document',
# 'Fields': [{'Field Name': 'KEY2', 'Value': 'I saw James Smith of Google LTD in MK7 6AA while I visited UK', 'PII Type': 'POSTCODE', 'PII Detected Value': [('MK7', '6AA')],
# 'PII Descriptiom': 'POSTCODE was decteted', 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': 'KEY2', 'Value': 'I saw James Smith of Google LTD in MK7 6AA while I visited UK',
# 'PII Type': 'PERSON', 'PII Detected Value': 'James Smith', 'PII Descriptiom': 'PERSON was decteted', 'Alert Score': 4, 'Alert Name': 'Extreme'},
# {'Field Name': 'KEY2', 'Value': 'I saw James Smith of Google LTD in MK7 6AA while I visited UK', 'PII Type': 'ORG', 'PII Detected Value': 'Google LTD',
# 'PII Descriptiom': 'ORG was decteted', 'Alert Score': 2, 'Alert Name': 'Medium'}, {'Field Name': 'KEY2', 'Value': 'I saw James Smith of Google LTD in MK7 6AA while I visited UK',
# 'PII Type': 'GPE', 'PII Detected Value': 'UK', 'PII Descriptiom': 'GPE was decteted', 'Alert Score': 1, 'Alert Name': 'Low'}]}]

print(obj)
