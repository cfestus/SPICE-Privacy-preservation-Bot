# ldh-scanning-framework
Python scripts for scanning the LDH activity log, processing the results with a scanner to look for items of interest and post results back to an LDH notification log.

## Instructions for use:
- Copy `ldh-config.json.dist` to `ldh-config.json`
- Place appropriate LDH access keys in `ldh-config.json`
- Run main.py

## Notes:
- Default pagesize is 100 and is specified in `ldh-config.json`. The main script
will continue to make requests for subsequent pages of results until all 
results are returned
- Initial timestamp is set to `1667306718`, which is the 1st November 2022. This
can be changed in `ldh-config.json`
- Once the process has run successfully, a `status.json` file will 
be created that stores the timestamp that the process last began to run. 
This is checked before the process is run again, so subsequent runs of 
the script will only look in the Activity Log for items that have 
been created since the last time the script was run
- To force the process to start again from the beginning, simply 
delete `status.json` or remove the `lastRun` entry from the file.
- `status.json` can also be used to store any other relevant state info that 
you wish to persist between job runs, simply add additional items to the 
`status` object before calling `writeStatus()`
- By default, notifications are simply printed to the screen for debugging. 
To push notifications back to the LDH, uncomment the line
`response = ldh.pushNotification(notification)` in the main loop.

## Scanner class
This is a simple and mostly empty class that will need to be populated with 
code for performing whichever document scanning you wish.

The `scanObject()` function is called for each document. It is expected to return 
an array of notifications, built using the Scanner's 
private `__buildNotification()` function. `__buildNotification()` will need
to be amended to build a notification with the appropriate structure.
The `scanObject()` function loops through each key/value 
pair within the document. In its current form, it creates a separate 
notification for each matched key/value pair but this functionality may need to
be changed depending on the type of scanning being done. For example, 
privacy scanning will likely scan through all key/value pairs and combine 
any positive results into a single notification that details these matches 
and includes an overall severity score.