<h1>eZamDB: eZamówienia Data Extractor</h1>

This Python program is designed to extract tender data from the Polish public procurement database, **eZamówienia (ezamowienia.gov.pl)**, via its API. It downloads contract notices within a specified date range and for a specific CPV code, handles pagination, and saves the results to a CSV file.
It is made of following files:
* main.py - The main script orchestrating data extraction, looping through pages, and data processing.
* link_maker.py      - Responsible for constructing the API request URL, incorporating dates, CPV code, and pagination offset.
* extract.py         - Manages the HTTP requests to the eZamówienia API using requests, handles network errors, and processes the raw JSON response data into a structured list of dictionaries.
* date_transform.py  - Contains functions for stripping and converting date strings (e.g., "DD.MM.YYYY") into datetime objects for API use.
* validations.py     - Houses the validation logic for input dates (format and order) and the CPV code format.

<h3>Configure Input Parameters:</h3>
The main configuration is set at the top of the main.py file. You need to set the desired date range and the CPV code.

<h3>Runing Program:</h3>
Execute the main.py file from your terminal.

<h3>Key Features:</h3>

Data Extraction and Pagination
The main function:
Validation: First calls ***validations*** to ensure dates and CPV are correct.

First Run: Extracts the first page of data and creates a pandas DataFrame.

Looping: Enters a while True loop to handle pagination, identifying the last record's ObjectId for the SearchAfter parameter in the next link.

Termination: The loop breaks when the number of new records retrieved (new_last_num) is the same as the previous page (last_num), indicating the end of the available data.

Export: Exports the accumulated data list to output.csv.


The appending_deals function in extract.py structures the downloaded JSON data into the following fields:
* id - Internal sequential ID assigned by the script.
* ObjectId - The identifier used by the API for pagination (SearchAfter).
* tenderId - The unique ID of the tender.
* noticeNumber - The official notice number.
* bzpNumber - The BZP (Public Procurement Bulletin) number.
* orderObject - Description of the order object.
* orderType - The type of order/procedure.
* cpvCode - The CPV code associated with the tender.
* publicationDate - The date the tender was published.
* submittingOffersDate - The deadline for submitting offers.
* organizationName - The name of the procuring organization.
* organizationCity - The city of the procuring organization.
* organizationCountry - The country of the procuring organization.
* isBelowEUThreshold - Boolean indicating if the tender amount is below the EU threshold (isTenderAmountBelowEU).
* Result - The procedure result (procedureResult).
