from flask import Blueprint, render_template,request
import re
from functions import getDoid, getDuo, getMondo
from keywords import removeWords, keyList1, keyList2

views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
def home():
    return render_template("home.html")

@views.route('/results',methods = ['POST'])
def submit():

    # Default
    match1 = False
    match2 = False

    # Save user input text
    originalText = request.form.get("text")
    text = originalText

    # Looks for "disease" or "disorder" in input text
    for key1 in keyList1:
        pattern1 = re.compile(r'\b' + key1 + r'\b',re.IGNORECASE)
        matches1 = re.search(pattern1,text)
        if matches1:
            match1 = True
            break

    # Looks for variations of "General Research Use" or "Health/Medical/Biomedical" in input text
    for key2 in keyList2:
        pattern2 = re.compile(r'\b' + key2 + r'\b',re.IGNORECASE)
        matches2 = re.search(pattern2,text)
        if matches2:
            match2 = True
            break

    # Algorithm for looking for alternate disease mappings
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

        # Get DOID and MONDO only for alternative disease mapping
        mondo = getMondo(text)
        doid = getDoid(text)
    else:
        mondo = {}
        doid = {}

    duo = getDuo(originalText)
    return render_template("results.html",originalText=originalText, duo = duo, doid = doid, mondo = mondo)
