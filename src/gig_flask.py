"""
Flask UI to display scraped gig data from gig_scanner.py module
- Ethan Jones <ejones18@sheffield.ac.uk>
- First authored: 2020-08-23
"""

from flask import Flask, request, redirect, render_template

import gig_scanner



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
        gigs = gig_scanner.main(artists_file, False)
        html_table = gigs.to_html()
        return render_template("gig_results.html", table=html_table)
    else:
        return redirect("home_page.html", message="Error")

if __name__ == "__main__":
    APP.run()
