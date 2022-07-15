# This file contains functions that are used in views.py

import pandas
import requests
import numpy
import re
from urllib.parse import quote

list_of_terms_CSV_file = "website/csv files/TermMapping.csv"
fileArray = pandas.read_csv(list_of_terms_CSV_file)
query = fileArray["Query for:"]
purls = fileArray["If found, then add*:"]
permissions = fileArray["Primary Permission Terms"]

# Makes sure that primary permission terms is either "X" or empty string
permissions = permissions.replace(numpy.nan, '', regex=True)

def getDuo(text):
    """
    This function reads in the user input and compares it to the rows in TermMapping.csv.

    It will return a list of lists in the format [[Query Matches],[Purl matches],[Primary Permission Term Matches]]
    """
    queryMatches = []
    purlMatches = []
    permissionMatches = []

    # Compare user input with every query term in TermMapping.csv
    for queryTerm,purl,permission in zip(query,purls,permissions):

        # Add regex word boundaries
        pattern = re.compile(r'\b' + queryTerm + r'\b',re.IGNORECASE)
        matches = re.search(pattern,text)

        # If there is a match between query term and user input. Make sure it is a unique purl
        if matches and purl not in purlMatches:
            queryMatches.append(queryTerm)
            purlMatches.append(purl)
            permissionMatches.append(str(permission))
    if len(queryMatches) == 0:
        duo = []
    else:
        duo = [queryMatches,purlMatches,permissionMatches]
    return duo

def construct_URL(processedText,yesDOID):
    """
    This function takes in the processed user input (with certain words removed) and a boolean
    and construct a DOID or MONDO API endpoint
    """
    if len(processedText) != 0:
        baseURL = "https://www.ebi.ac.uk/ols/api/search?q="
        iriURL = "&groupField=iri"

        # This refers to page numbers
        pageIndexURL = "&start=0"

        # Constructing DOID or MONDO PURLs
        if yesDOID == True:
            doidURL = "&ontology=doid"
            url = baseURL + processedText + iriURL + pageIndexURL + doidURL
        else:
            mondoURL = "&ontology=mondo"
            url = baseURL + processedText + iriURL + pageIndexURL + mondoURL
        
        return url
    else:
        return None

def get_Title(url):
    """
    This function will read in an API endpoint and return a list of the top 5 search result titles from OLS
    """
    if len(url) != 0:
        # Initialize list and start page
        titles = []

        # Only get the top 5 PURLS
        numberPURLs = 5
        
        # Retireve JSON data using constructed URL
        try:
            response = requests.get(url)
            my_json = response.json()

            for label in my_json["response"]["docs"]:
                if len(titles) < numberPURLs and label["type"] == "class":
                    titles.append(label["label"])
        except:
            print("An exception has occured")

        return titles
    else:
        return None

def get_Purl(url):
    """
    This function will read in an API endpoint and return a list of the top 5 search result purls from OLS
    """
    if len(url) != 0:
        # Initialize list and start page
        my_purls = []

        # Only get the top 5 PURLS
        numberPURLs = 5

        # Retireve JSON data using constructed URL
        try:
            response = requests.get(url)
            my_json = response.json()

            for label in my_json["response"]["docs"]:
                if len(my_purls) < numberPURLs and label["type"] == "class":
                    my_purls.append(label["iri"])
        except:
            print("An exception has occured")
        return my_purls
    else:
        return None

def getDoid(processedText):
    """
    This function takes in the processed user input (with certain words removed) to retrieve all the doid titles
    and purls from OLS

    It will return a dictionary in the format {"doidTitle1": "purl1", "doidTitle2": "purl2", ...}
    """
    if len(processedText) != 0:
        doidTitles = get_Title(construct_URL(quote(processedText),True))
        doidPurls = get_Purl(construct_URL(quote(processedText),True))
        zip_iterator = zip(doidTitles,doidPurls)
        doid = dict(zip_iterator)
    else:
        doid = {}
    return doid

def getMondo(processedText):
    """
    This function takes in the processed user input (with certain words removed) to retrieve all the mondo titles
    and purls from OLS

    It will return a dictionary in the format {"mondoTitle1": "purl1", "mondoTitle2": "purl2", ...}
    """
    if len(processedText) != 0:
        mondoTitles = get_Title(construct_URL(quote(processedText),False))
        mondoPurls = get_Purl(construct_URL(quote(processedText),False))
        zip_iterator = zip(mondoTitles,mondoPurls)
        mondo = dict(zip_iterator)
    else:
        mondo = {}
    return mondo
