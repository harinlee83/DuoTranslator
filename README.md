# DuoTranslator

- Deployed here: https://duo-translator.herokuapp.com/

- The DUO translator is an application that ingests consent form text and maps it to suggested terms in the GA4GH Data Use Ontology Standard. It is intended to be used by researchers to easily view data use permissions, data use modifiers, and alternative possible disease mappings associated with a consent form. Developed using Flask, the DUO translator relies on HTTP requests to the Ontology Lookup Service API (https://www.ebi.ac.uk/ols/index).
- Website styling and images sourced from: https://duos.broadinstitute.org/
- Note: Helpful/Not helpful button feature not yet implemented.

![Screen Shot 2022-06-04 at 8 53 26 PM](https://user-images.githubusercontent.com/82293855/172030394-87e39f89-3a00-4b35-a315-4dfacdcaf81c.png)

## How it Works
<p align="center">
  <img src="https://user-images.githubusercontent.com/82293855/179282725-452e6e2d-2b1d-4b4f-aeb1-1a5d315ead86.png">
</p>

> When a user submits consent form text to the DUO translator, the text is sent over to the backend for data processing via an HTTP post request. Using regular expressions, the application will filter the data through a series of search patterns to identify common keywords. Based on these keywords, an algorithm will remove unnecessary terms (i.e. acronyms, conjunctions, prepositions, auxiliary verbs, etc) in the data and form an appropriate query term. The application will use this query term to construct an API endpoint for the Ontology Lookup Service API with DOID and MONDO ontology filters. The DUO translator then retrieves the top 5 MONDO and DOID purls and titles from the returned JSON object via an HTTP get request and displays this information back to the UI. Below the search results are “helpful/unhelpful” buttons which will store results and the user’s response in the server database. This user feedback will help developers to refine the search algorithm as they debug instances of failure, ultimately improving results for future users.

## How to Run

To locally start the application,
`pip install -r requirements.txt` in terminal and then run **main.py**.
