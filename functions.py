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

def getDoid(text):
    if text != "":
        doidTitles = get_Title(construct_URL(quote(text),0,True))
        doidPurls = get_Purl(construct_URL(quote(text),0,True))
        zip_iterator = zip(doidTitles,doidPurls)
        doid = dict(zip_iterator)
        return doid
    else:
        return None

def getMondo(text):
    if text != "":
        mondoTitles = get_Title(construct_URL(quote(text),0,False))
        mondoPurls = get_Purl(construct_URL(quote(text),0,False))
        zip_iterator = zip(mondoTitles,mondoPurls)
        mondo = dict(zip_iterator)
        return mondo
    else:
        return None

def get_JSON(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text

def construct_URL(queryTerm,startNum,yesDOID):
    baseURL = "https://www.ebi.ac.uk/ols/api/search?q="
    iriURL = "&groupField=iri"

    if len(queryTerm) == 0:
        return ""

    # This refers to page numbers
    pageIndexURL = f"&start={startNum}"

    # Constructing DOID or MONDO PURLs
    if yesDOID == True:
        doidURL = "&ontology=doid"
        url = baseURL + queryTerm + iriURL + pageIndexURL + doidURL
    else:
        mondoURL = "&ontology=mondo"
        url = baseURL + queryTerm + iriURL + pageIndexURL + mondoURL
    
    return url

def get_Purl(url):

    if len(url) == 0:
        return ""
    # # This finds the total number of results
    # maxResultNum = my_json["response"]["numFound"]
    
    # Initialize list and start page
    my_purls = []

    # Only get the top 5 PURLS
    numberPURLs = 5
    # Retireve JSON data using constructed URL
    try:
        json_Text = get_JSON(url)
        my_json = json.loads(json_Text)

        for label in my_json["response"]["docs"]:
            if len(my_purls) < numberPURLs and label["type"] == "class":
                my_purls.append(label["iri"])
    except:
        print("An exception has occured")

    return my_purls

def get_Title(url):

    if len(url) == 0:
        return ""
    # # This finds the total number of results
    # maxResultNum = my_json["response"]["numFound"]
    
    # Initialize list and start page
    titles = []

    # Only get the top 5 PURLS
    numberPURLs = 5
    # Retireve JSON data using constructed URL
    try:
        json_Text = get_JSON(url)
        my_json = json.loads(json_Text)

        for label in my_json["response"]["docs"]:
            if len(titles) < numberPURLs and label["type"] == "class":
                titles.append(label["label"])
    except:
        print("An exception has occured")

    return titles
