# concert_scanner
A python script that scrapes concert data from both https://www.alttickets.com/ and https://www.seetickets.com/ for any artist(s). Now includes fuzzy matching location filter and Flask UI! <br> NOTE: The geocoder used might not be able to recognise some venues which may result in misplotted pins or none at all. 

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

### Example ###
``` 
python .\gig_scanner.py --artist-file "C:\Users\EJones820\Desktop\Projects\scraping\concert_scanner\src\gigs.txt" --location "Bristol" 
````
*Note: gigs.txt only contains one artists - The Night Cafe*

Should expect an output of a dataframe along these lines
```
            Artist          Venue           Date/Time   Price         Gig Status
6   The Night Cafe  SWX - Bristol  6:30 PM Tue 18 May  £15.52  Tickets available
20  The Night Cafe  Bristol - SWX      18:30 18/05/21  £15.19  Tickets available
```
## Running the *gig_flask.py flask application* ##
* Create file for your Bing Maps API key called bing_api_key.txt in src folder
* Add user_agent in *gig_flask.py* script (near the top) - any identifying string i.e. <your_email_and_project_name>
* Launch flask using ``` python gig_flask.py``` OR ```launch_gig_ui.ps1``` - if using powershell
* Navigate to http://localhost:5000/ (Chrome recommended)

## To Do ##
1. <s>Add location filter for gigs</s>
2. Flask application with map displaying gigs - *Still needs testing*
3. <s>Rewrite coords so venue names can be labelled to pushpins on map</s>
4. <s>Add location filter for Flask UI</s>
