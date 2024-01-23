from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from helper import *
from cs50 import SQL
from datetime import datetime

app = Flask(__name__)

db = SQL("sqlite:///flights.db")


# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.context_processor
def current_year():
    return {"current_year": datetime.today().year}

@app.route("/")
def index():
    return render_template("index.html", countries=countries_with_url)


@app.route("/find-ticket", methods=["POST", "GET"])
def find_ticket():
    # If you get to this route through POST method
    if request.method == "POST":

        # Get the data from the initial form
        dept_country = request.form.get("dept_country")
        dept_airport_id = request.form.get("dept_airport")
        dest_airport_id = request.form.get("dest_airport")

        # If country is not in the list of countries error
        if dept_country not in countries_list:
            return error_page(message="Invalid country. You have to select a country from the options.")

        # If country is blank error
        if not dept_country:
            return error_page(message="No country selected. You have to select a country from the options.")

        # if destination airport is blank error
        if not dest_airport_id:
            return error_page(message="Select a destination airport, please!")

        # get info from airport from database
        chosen_dest_airport = db.execute(
            "SELECT * FROM airports WHERE id = ?",
            dest_airport_id
        )

        # if airport is not in database error
        if chosen_dest_airport is None:
            return error_page(message="Airport doesn't exist")

        # Select first (and supposedly only) element from the list
        try:
            chosen_dest_airport = chosen_dest_airport[0]
        except IndexError:
            return error_page(message="Airport doesn't exist")

        # if the airport somehow is not in the same country the user select before
        if chosen_dest_airport["country"] != session["destination"]:
            return error_page(message=f"This airport does not belong to {session['destination']}!")

        # if the destination airport and the departure country were selected correctly but the departure airport
        # was not yet selected, do the following
        if dest_airport_id and dept_country and not dept_airport_id:
            # Select a list of possible airports for departure
            possible_airports = db.execute(
                "SELECT * FROM airports WHERE country = ? ORDER BY iata_code",
                request.form.get("dept_country")
            )

            # render the list for the user to choose
            return render_template(
                template_name_or_list="find_ticket.html",
                dept_country=request.form.get("dept_country"),
                possible_airports=possible_airports,
                destination=session["destination"],
                chosen_dest_airport=chosen_dest_airport
            )

        # after user has already selected departure airport get the info from the airport selected
        chosen_airport = db.execute(
            "SELECT * FROM airports WHERE id = ?",
            dept_airport_id
        )

        # if there is no chosen airport in the database error
        if chosen_airport is None:
            return error_page(message="Airport doesn't exist!")

        try:
            chosen_airport = chosen_airport[0]
        except IndexError:
            return error_page(message="Airport doesn't exist!")

        # if the airport somehow is not in the same country the user select before
        if chosen_airport["country"] != dept_country:
            return error_page(message=f"This airport does not belong to {dept_country}!")

        # all was done right, now present the tickets for the route given

        # treating the dates info
        dept_date_form = request.form.get("dept_date")
        arr_date_form = request.form.get("arr_date")

        if not dept_date_form:
            return error_page(message="Must select a departure date.")

        if not arr_date_form:
            return error_page(message="Must select a arrival date.")

        try:
            dept_date = datetime(
                year=int(dept_date_form.split("-")[0]),
                month=int(dept_date_form.split("-")[1]),
                day=int(dept_date_form.split("-")[2]),
            )
        except (ValueError, IndexError, TypeError):
            return error_page(message="Invalid departure date. Please use a valid date format")

        try:
            arr_date = datetime(
                year=int(arr_date_form.split("-")[0]),
                month=int(arr_date_form.split("-")[1]),
                day=int(arr_date_form.split("-")[2]),
            )
        except (ValueError, IndexError, TypeError):
            return error_page(message="Invalid arrival date. Please use a valid date format")

        if dept_date > arr_date:
            return error_page(message="You can't choose a date for departure later than for returning")

        # Error treatment for direct flight option
        direct_flight = request.form.get("direct_flight")
        if direct_flight != "on":
            direct_flight = False
        else:
            direct_flight = True

        travel_info = get_route(
            dept_airport_iata=chosen_airport["iata_code"],
            dest_airport_iata=chosen_dest_airport["iata_code"],
            dept_date=dept_date,
            arr_date=arr_date,
            direct_flight=direct_flight
        )

        if travel_info is False:
            return error_page(message="Sorry, but we couldn't find any tickets 😓", code=500)

        return render_template(
            "found_ticket.html",
            chosen_dest_airport=chosen_dest_airport,
            chosen_airport=chosen_airport,
            travel_info=travel_info
        )

    # If you get to this route through GET method
    else:
        country = request.args.get("country_id")
        if country is None:
            return error_page(message="You have to select a country from the list.")
        if country not in countries_list:
            return error_page(message="Invalid country! You have to select a country from the list.")

        session["destination"] = country
        possible_dest_airports = db.execute(
            "SELECT * FROM airports WHERE country = ? ORDER BY iata_code",
            session["destination"]
        )

        return render_template(
            "find_ticket.html",
            countries=countries_list,
            destination=session["destination"],
            possible_dest_airports=possible_dest_airports
        )



