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

    # Default booleans for algorithm decision making
    match1 = False
    match2 = False

    # Save user input text
    originalText = request.form.get("text")
    processedText = originalText

    # Get Data Use Permissions and Data Use Modifiers
    duo = getDuo(originalText)

    # Criteria 1: Looks for "disease" or "disorder" in input text
    for key1 in keyList1:
        pattern1 = re.compile(r'\b' + key1 + r'\b',re.IGNORECASE)
        matches1 = re.search(pattern1,processedText)
        if matches1:
            match1 = True
            break

    # Criteria 2: Looks for variations of "General Research Use" or "Health/Medical/Biomedical" in input text
    for key2 in keyList2:
        pattern2 = re.compile(r'\b' + key2 + r'\b',re.IGNORECASE)
        matches2 = re.search(pattern2,processedText)
        if matches2:
            match2 = True
            break

    # Get Alternative Disease Mappings:
    # If (Disease or Disorder) OR NOT (GSU or HMB)
    if match1 or not match2:
        # Take consent title, remove list of key words and extra whitespaces
        for word in removeWords:
            pattern = re.compile(r"\b" + word + r"\b",re.IGNORECASE)
            processedText = re.sub(pattern,"",processedText)
        # Remove leading whitespace
        processedText = re.sub(r"^\W*","",processedText)

        # Remove trailing whitespace
        processedText = re.sub(r"\W*$","",processedText)

        # Remove random punctation
        processedText = re.sub(r"[,/()]"," ",processedText)

        # Remove 2 or more whitespace
        processedText = re.sub(r" +"," ",processedText)

        # Get DOID and MONDO only for alternative disease mapping
        mondo = getMondo(processedText)
        doid = getDoid(processedText)
    else:
        mondo = {}
        doid = {}
    
    return render_template("results.html",originalText=originalText, duo = duo, doid = doid, mondo = mondo)
