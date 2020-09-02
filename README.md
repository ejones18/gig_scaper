# concert_scanner
A python script that scrapes concert data from both https://www.alttickets.com/ and https://www.seetickets.com/ for any artist(s). Now includes fuzzy matching location filter!

## What is this repository for? ##
Finding concerts for the artists you love across multiple sites. Saves results as a csv file.
* Developed and tested with Python 3.7, should work for 3.6+.

## Setup ##
* Download Python3+ from https://www.python.org/downloads/release/python-370/
* Download or clone the repository 
* Install requirements using ```pip install -r requirements.txt```

# Running the *gig_scanner.py script* #
* Populate the gigs.txt file with artists you want to scan for and run!
* Run script with or without optional location flag - ``` python gig_scanner.py --location <optional_location_here>```

## To Do ##
1. <s>Add location filter for gigs<s>
