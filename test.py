import json
import re
from functions import getDuo, getMondo
from keywords import removeWords, keyList1, keyList2


# Default
match1 = False
match2 = False
text = "Disease Specific"
# Looks for "DISEASE" or "DISORDER"
for key1 in keyList1:
    pattern1 = re.compile(r'\b' + key1 + r'\b',re.IGNORECASE)
    matches1 = re.search(pattern1,text.upper())
    if matches1:
        match1 = True
        break
# Looks for GRU or HMB
for key2 in keyList2:
    pattern2 = re.compile(r'\b' + key2 + r'\b',re.IGNORECASE)
    matches2 = re.search(pattern2,text.upper())
    if matches2:
        match2 = True
        break

# If (Disease or Disorder) OR NOT (GSU or HMB)
if match1 or not match2:
    # Take consent title, remove list of key words and extra whitespaces
    for word in removeWords:
        pattern = re.compile(r"\b" + word + r"\b",re.IGNORECASE)
        text = re.sub(pattern,"",text)
    # Remove leading whitespace
    text = re.sub(r"^\W*","",text)
    # Remove trailing whitespace
    text = re.sub(r"\W*$","",text)
    # Remove random punctation
    text = re.sub(r"[,/()]"," ",text)
    # Remove 2 or more whitespace
    text = re.sub(r" +"," ",text)
    mondo = getMondo(text)
else:
    mondo = None