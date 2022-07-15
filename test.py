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
print(permissions)

