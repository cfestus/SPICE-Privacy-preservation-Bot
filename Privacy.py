from commonregex import CommonRegex
import spacy
import re
import time
import re
import spacy
import datetime



class Privacy:

    def privacyViolations(self,documentID,items):
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
      
            return [{
                        "job-type": "PRIVACY-VIOLATION",
                        "Date": int(time.time()),
                        "Document ID": documentID,
                        "Status": "ALERT",
                        "SeverityScores": severityScores,
                        "Description": 'Personal identifiable information was decteted in this document',
                        'Fields': items
                }]
        


    