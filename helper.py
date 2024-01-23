# A file containing some helper functions and data

import requests
from bs4 import BeautifulSoup
from flask import redirect, render_template, session
from datetime import datetime, timedelta
from pprint import pprint
from cs50 import SQL

db = SQL("sqlite:///flights.db")


TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"

# IN ORDER FOR THIS WEB APP TO WORK YOU NEED TO USE YOUR OWN TEQUILA API KEY
# Head to https://tequila.kiwi.com/ and get one for free
# The code above won't work until you add your own valid api key
TEQUILA_API_KEY = "0000"


countries_with_url = [
    {"country": "France", "url": "france"},
    {"country": "United States", "url": "united-states"},
    {"country": "Spain", "url": "spain"},
    {"country": "Italy", "url": "italy"},
    {"country": "China", "url": "china"},
    {"country": "United Kingdom", "url": "united-kingdom"},
    {"country": "Russia", "url": "russia"},
    {"country": "Mexico", "url": "mexico"},
    {"country": "Canada", "url": "canada"},
    {"country": "Germany", "url": "germany"},
    {"country": "Austria", "url": "austria"},
    {"country": "Poland", "url": "poland"},
    {"country": "Hungary", "url": "hungary"},
    {"country": "Greece", "url": "greece"},
    {"country": "Morocco", "url": "morocco"},
    {"country": "South Africa", "url": "south-africa"},
    {"country": "Tunisia", "url": "tunisia"},
    {"country": "Algeria", "url": "algeria"},
    {"country": "Mozambique", "url": "mozambique"},
    {"country": "Zimbabwe", "url": "zimbabwe"},
    {"country": "Kenya", "url": "kenya"},
    {"country": "Uganda", "url": "uganda"},
    {"country": "Saudi Arabia", "url": "saudi-arabia"},
    {"country": "United Arab Emirates", "url": "united-arab-emirates"},
    {"country": "Egypt", "url": "egypt"},
    {"country": "Iran", "url": "iran"},
    {"country": "Jordan", "url": "jordan"},
    {"country": "Israel", "url": "israel"},
    {"country": "Brazil", "url": "brazil"},
    {"country": "Argentina", "url": "argentina"},
    {"country": "Colombia", "url": "colombia"},
    {"country": "Chile", "url": "chile"},
    {"country": "Peru", "url": "peru"},
    {"country": "Hong Kong", "url": "hong-kong"},
    {"country": "India", "url": "india"},
    {"country": "Thailand", "url": "thailand"},
    {"country": "South Korea", "url": "south-korea"},
    {"country": "Japan", "url": "japan"},
    {"country": "Indonesia", "url": "indonesia"},
    {"country": "Turkey", "url": "turkey"},
    {"country": "Macau", "url": "macau"},
    {"country": "Cyprus", "url": "cyprus"},
    {"country": "Malaysia", "url": "malaysia"},
    {"country": "Dominican Republic", "url": "dominican-republic"},
    {"country": "Qatar", "url": "qatar"},
    {"country": "Oman", "url": "oman"},
    {"country": "Bahrain", "url": "bahrain"},
    {"country": "Senegal", "url": "senegal"},
    {"country": "Namibia", "url": "namibia"},
    {"country": "Australia", "url": "australia"},
]

countries_list = [country["country"] for country in countries_with_url]
countries_list.sort()


def error_page(message, code=400):
    """Render a error message to the user"""
    return render_template("error_page.html", message=message, code=code)


def get_route(dept_airport_iata, dest_airport_iata, dept_date=datetime.now(), arr_date=datetime.now(), direct_flight=False):
    """Get you the info for the cheapest route to the destination"""

    headers = {
        "apikey": TEQUILA_API_KEY
    }

    params = {
        "fly_from": dept_airport_iata,
        "fly_to": dest_airport_iata,
        "date_from": dept_date.strftime("%d/%m/%Y"),
        "date_to": dept_date.strftime("%d/%m/%Y"),
        "return_from": arr_date.strftime("%d/%m/%Y"),
        "return_to": arr_date.strftime("%d/%m/%Y"),
        "flight_type": "round",
        # "curr": "BRL",
        "curr": "USD",
        "max_stopovers": 6,
    }

    if direct_flight:
        params["max_stopovers"] = 0

    response = requests.get(url=f"{TEQUILA_ENDPOINT}/search", headers=headers, params=params)

    try:
        if not response.json()["data"]:
            return False
    except KeyError:
        print(response.json())
        return False

    list_of_prices = [itinerary["price"] for itinerary in response.json()["data"]]

    i_min = list_of_prices.index(min(list_of_prices))
    data_min = response.json()["data"][i_min]

    for item in data_min["route"]:
        item["dTime"] = datetime.fromtimestamp(item["dTime"])
        item["aTime"] = datetime.fromtimestamp(item["aTime"])
        item["aTimeUTC"] = datetime.fromtimestamp(item["aTimeUTC"])
        item["dTimeUTC"] = datetime.fromtimestamp(item["dTimeUTC"])


    data_min["route"][-1]["flyFrom"] = data_min["route"][-2]["flyTo"]
    data_min["route"][-1]["flyTo"] = dept_airport_iata
    data_min["route"][-1]["return"] = 2

    try:
        print(data_min["route"][-1]["fare_category"])
    except KeyError:
        data_min["route"][-1]["fare_category"] = "M"

    for ticket in data_min["route"]:
        ticket_info = {
            "airline_iata_code": ticket["airline"],
            "dept_airport_iata_code": ticket["flyFrom"],
            "arr_airport_iata_code": ticket["flyTo"],
            "departure_time": ticket["dTime"],
            "arrival_time": ticket["aTime"],
            "flight_duration": ticket["aTimeUTC"] - ticket["dTimeUTC"],
        }

        try:
            ticket_info["airline_name"] = db.execute("SELECT name FROM airlines WHERE iata_code = ?", ticket_info["airline_iata_code"])[0]["name"]
        except IndexError:
            ticket_info["airline_name"] = ticket_info["airline_iata_code"]
        try:
            ticket_info["dept_airport"] = db.execute("SELECT name FROM airports WHERE iata_code = ?", ticket_info["dept_airport_iata_code"])[0]["name"]
        except IndexError:
            ticket_info["dept_airport"] = ticket_info["dept_airport_iata_code"]
        try:
            ticket_info["arr_airport"] = db.execute("SELECT name FROM airports WHERE iata_code = ?", ticket_info["arr_airport_iata_code"])[0]["name"]
        except IndexError:
            ticket_info["arr_airport"] = ticket_info["arr_airport_iata_code"]


        if ticket["fare_category"] == "M":
            ticket_info["fare_category_name"] = "Economy"
        elif ticket["fare_category"] == "W":
            ticket_info["fare_category_name"] = "Economy Premium"
        elif ticket["fare_category"] == "C":
            ticket_info["fare_category_name"] = "Business"
        elif ticket["fare_category"] == "F":
            ticket_info["fare_category_name"] = "First Class"

        flight_duration = str(ticket_info["flight_duration"])
        ticket_info["flight_duration"] = f'{flight_duration.split(":")[0]}h{flight_duration.split(":")[1]}m'

        for key, value in ticket_info.items():
            ticket[key] = value

        ticket["dTime"] = ticket["dTime"].strftime("%m/%d/%y %H:%M")
        ticket["aTime"] = ticket["aTime"].strftime("%m/%d/%y %H:%M")

    pprint(data_min)

    return data_min
