"""
Python module to scrap gig data
- Ethan Jones <ejones18@sheffield.ac.uk>
- First authored: 2020-08-23
"""

import argparse
import os
import sys
import re
import requests
import bs4
from fuzzywuzzy import fuzz, process

import pandas as pd

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def main(location=None):
    """Scrape and display gig data for desired artist(s)."""
    column_names = ['Artist', 'Venue', 'Date/Time', 'Price', 'Gig Status']
    gig_dataframe = pd.DataFrame(columns=column_names)
    gig_file_path = os.path.join(ROOT_PATH, "gigs.txt")
    try:
        artists = pd.read_csv(gig_file_path, header=None)
    except:
        print(f"{gig_file_path} not found...")
        sys.exit()
    artists = artists[0].to_list()
    for artist in artists:
        try:
            url = build_base_url(artist, 1)
            data = scrape_see(url)
            gig_dataframe = gig_dataframe.append([data])
            url = build_base_url(artist, 0)
            data = scrape_alt(url)
            gig_dataframe = gig_dataframe.append([data])
        except:
            continue
    gig_dataframe.reset_index(drop=True, inplace=True)
    if location != None:
        for index, row in gig_dataframe.iterrows():
            if fuzz.WRatio(location, row['Venue']) < 60:
                gig_dataframe.drop(index, inplace=True)
    print(gig_dataframe)
    results_file = os.path.join(ROOT_PATH, "gigs.csv")
    gig_dataframe.to_csv(results_file, index=False)

def build_base_url(artist, site):
    """Builds URL to fetch base gig data."""
    artist = clean_artist_name(artist, site)
    if site == 0:
        url = f"https://www.alttickets.com/{artist}-tickets"
    else:
        url = f"https://www.seetickets.com/tour/{artist}"
    return url

def clean_artist_name(artist, site):
    """Cleans the artists name from input."""
    if artist.find(" ") != -1:
        artist = artist.replace(" ", "-")
    elif artist.find("'") != -1:
        if site == 0:
            artist = artist.replace("'", "")
        else:
            artist = artist.replace("'", "-")
    return artist.lower()

def scrape_see(url):
    """Scrapes gig data from seetickets."""
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    artists = []
    venues = []
    dates = []
    prices = []
    gig_states = []
    gigs = soup.find_all('a', {'class': 'g-blocklist-link view-order-link'})
    for gig in gigs:
        try:
            artist_and_venue = gig['title'].split(',')
            city = re.sub('[^A-Za-z0-9,]+', '', gig.find('span', {'class': 'g-blocklist-sub-text'}).text.strip()).split(',')[-1]
            artist = artist_and_venue[0]
            venue = artist_and_venue[1].strip()
            if venue.find(city) == -1:
                venue = venue + " - " + city
            date = gig.find('time', {'class': 'hour'}).text + gig.find('time').text
            price_url = f"https://www.seetickets.com{gig['href']}"
            try:
                price = fetch_price(price_url, 1)
            except:
                price = "N/A"
            try:
                gig_state = fetch_see_state(price_url)
            except:
                gig_state = gig.find('span', {'class': 'g-blocklist-action'}).text.strip()
            gig_states.append(gig_state)
            prices.append(price)
            artists.append(artist)
            venues.append(venue)
            dates.append(date)
        except:
            continue
    gig_data = pd.DataFrame(list(zip(artists, venues, dates, prices, gig_states)),
                            columns=['Artist', 'Venue', 'Date/Time', 'Price', 'Gig Status'])
    return gig_data

def scrape_alt(url):
    """Scrapes gig data from alttickets."""
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    artists = []
    venues = []
    dates = []
    prices = []
    gig_state = []
    gigs = soup.find_all('div', {'class': 'ticket-data parent-col centered col-xs-10 col-sm-8'})
    for gig in gigs:
        try:
            try:
                state = gig.find('a')['title']
            except:
                state = gig.find('span', {'class': 'button-title'}).text
            if state == "":
                state = gig.find('span', {'class': 'button-title'}).text
            if state == "Book Tickets":
                state = "Tickets available"
                price_url = f"https://www.alttickets.com/{gig.find('a')['href']}"
                price = fetch_price(price_url, 0)
            else:
                price = "N/A"
            gig_info = gig.find('div', {'class': 'ticket-details'})
            try:
                artist = gig_info.find('h2').find('h2').text
            except:
                artist = "Unavailable"
            try:
                venue = gig_info.find('h2').find('h3').text
            except:
                venue = "Unavailable."
            try:
                date = re.sub("[^A-Za-z0-9:/']+", ' ', 
                              gig_info.find('h2').find('time').text).strip()
            except:
                date = "Unavailable"
            try:
                more_info = gig_info.find('h2').find('p').text
            except:
                more_info = "No extra information"
            gig_state.append(state)
            prices.append(price)
            artists.append(artist)
            venues.append(venue)
            dates.append(date)
        except:
            continue
    gig_data = pd.DataFrame(list(zip(artists, venues, dates, prices, gig_state)),
                            columns=['Artist', 'Venue', 'Date/Time', 'Price', 'Gig Status'])
    return gig_data

def fetch_see_state(url):
    """Fetches state of gig on Seetickets."""
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    try:
        state = soup.find('td', {'class': 'note quantity'}).text.strip()
    except:
        if soup.find('button', {'id': 'buyTickets'}):
            state = "Tickets available"
        else:
            state = "Error"
    return state

def fetch_price(url, site):
    """
    Fetches the price of the gigs
    """
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    if site == 0:
        price = soup.find('div', {'class': 'price'}).find('h3').text
    else:
        price = re.findall('£[0-9]+.[0-9]+', soup.find('td', {'rowspan': 1}).text)[0]
    return price

def parse_options():
    """Parse command line options."""
    parser = argparse.ArgumentParser(description=("This is a command line interface (CLI) for "
                                                  "the gig_scanner module"),
                                     epilog="Ethan Jones, 2020-08-23")
    parser.add_argument("--location", dest="location", action="store", type=str,
                        required=False, metavar="name_of_artist",
                        help="Location.")
    options = parser.parse_args()
    return options

if __name__ == "__main__":
    OPTIONS = parse_options()
    main(OPTIONS.location)
