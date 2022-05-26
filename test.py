# list1 = [3,6,3,2,9]
# list2 = [1,2,5,4,3]
# list3 = ["X","","X","X",""]

# duo = [list1,list2,list3]

# for index,key3 in enumerate(duo[2]):
#     if key3 == "X":
#         print(duo[0][index])
#         print(duo[1][index])
# print(duo)

import csv
from math import perm
import pandas
import requests
import json
import re
from urllib.parse import quote

list_of_terms_CSV_file = "website/csv files/TermMapping.csv"
fileArray = pandas.read_csv(list_of_terms_CSV_file)
query = fileArray["Query for:"]
purls = fileArray["If found, then add*:"]
permissions = fileArray["Primary Permission Terms"]

def getDuo(text):
    queryMatches = []
    purlMatches = []
    permissionMatches = []
    for queryTerm,purl,permission in zip(query,purls,permissions):
        # Add regex word boundaries
        pattern = re.compile(r'\b' + queryTerm + r'\b',re.IGNORECASE)
        matches = re.search(pattern,text)
        if matches and purl not in purlMatches:
            queryMatches.append(queryTerm)
            purlMatches.append(purl)
            permissionMatches.append(permission)
    if len(queryMatches) == 0:
        duo = None
    else:
        duo = [queryMatches,purlMatches,permissionMatches]
    return duo

text = "General Research Use (IRB, NPU)"
duo = getDuo(text)
print(duo)
