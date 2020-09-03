"""
Flask UI to display scraped gig data from gig_scanner.py module
- Ethan Jones <ejones18@sheffield.ac.uk>
- First authored: 2020-08-23
"""

from flask import Flask, request, redirect, render_template

import gig_scanner

#gig_scanner.main("Birmingham")

APP = Flask(__name__)

@APP.route("/", methods=["GET", "POST"])
def home_page():
    """
    Home page of the flask app.
    """
    return render_template("home_page.html")

if __name__ == "__main__":
    APP.run()