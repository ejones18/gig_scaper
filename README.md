# concert_scanner
A python script that scrapes concert data from both https://www.alttickets.com/ and https://www.seetickets.com/ for any artist(s). Now includes fuzzy matching location filter!

## What is this repository for? ##
Finding concerts for the artists you love across multiple sites. Saves results as a csv file.
* Developed and tested with Python 3.7, should work for 3.6+.

## Setup ##
* Download Python3+ from https://www.python.org/downloads/release/python-370/
* Download or clone the repository 
* Install requirements using ```pip install -r requirements.txt```

## Running the *gig_scanner.py script* as a stand-alone module ##
* Populate the gigs.txt file with artists you want to scan!
* Run script with or without optional location flag ```python gig_scanner.py --artist-file <path_to_file> --location <optional_location_here>```

## Running the *gig_flask.py flask application* ##
* Create file for your Bing Maps API key called bing_api_key.txt in src folder
* Launch flask using ``` python gig_flask.py``` OR ```launch_gig_ui.ps1``` - if using powershell
* Navigate to http://localhost:5000/ (Chrome recommended)

## To Do ##
1. <s>Add location filter for gigs</s>
2. Flask application with map displaying gigs - *Still needs testing*
3. Rewrite coords so venue names can be labelled to pushpins on map
