from Privacy import Privacy
import re

privacy = Privacy()
obj = privacy.scanObject("dataset1", "doc1", {"key1": "Please send me something here: enrico@example.org or go away!", "museum": "Irish museum of modern art", "details": [ { "address": "Meet me at MK173FE" }]})
print(obj)

# regex_zip = r"\b\d{5}(?:-\d{4})?\b"
# regex_email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
# email = re.findAll(regex_email, " enrico.daga@open.ac.uk")
# zipx = re.findAll(regex_zip, "the postcode is 01000-3456 ")
# print(email)
# print(zipx)

# import re
# pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
#
#
#
# print(re.findall(pattern, "Looking for my email enrico.daga@open.ac.uk and stuff  enrico.daga2@open.ac.uk " ))

# for match in re.finditer(pattern, "Looking for my email enrico.daga@open.ac.uk and stuff  enrico.daga2@open.ac.uk " ):
#     print('Found: %s' % ( match.group() ))