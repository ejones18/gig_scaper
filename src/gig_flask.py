"""
Flask UI to display scraped gig data from gig_scanner.py module
- Ethan Jones <ejones18@sheffield.ac.uk>
- First authored: 2020-08-23
"""

import os

from flask import Flask, request, redirect, render_template
from geopy.geocoders import Nominatim

import gig_scanner

GELOCATOR = Nominatim(user_agent="gig_scanner - ethanj129@gmail.com")

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

APP = Flask(__name__)

@APP.route("/", methods=["GET", "POST"])
def home_page():
    """
    Home page of the flask app.
    """
    return render_template("home_page.html")
    
@APP.route("/gig_results", methods=["GET", "POST"])
def gig_results():
    """Scans for gigs used passed in file."""
    if request.method == "POST" and "artistFileUpload" in request.files:
        artists_file = request.files["artistFileUpload"].stream
        if request.form.get('Location'):
            gigs = gig_scanner.main(artists_file, False, request.form.get('Location'))
        else:
            gigs = gig_scanner.main(artists_file, False)
        coords = {}
        for index, row in gigs.iterrows():
            try:
                location = GELOCATOR.geocode(row["Venue"])
                coords[row["Artist"]+ " " + row["Venue"]] = (location.longitude, location.latitude)
            except:
                continue
        html_table = gigs.to_html()
        return render_template("gig_results.html", table=html_table,
                               coords=coords, bing_key=BING_KEY)
    else:
        return redirect("home_page.html", message="Error")

def load_bing_key(api_key_file):
    """
    Loads the bing maps API key.
    """
    try:
        with open(api_key_file) as fid:
            key = fid.read().strip()
    except FileNotFoundError:
        warnings.warn("Failed to load Bing Maps API key - you will not be able to make new "
                      "queries to the Bing Maps API!")
        return None
    return key

API_KEY_FILE = os.path.join(ROOT_PATH, "bing_api_key.txt")
BING_KEY = load_bing_key(API_KEY_FILE)
