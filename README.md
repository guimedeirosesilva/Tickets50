# Tickets50
#### Video Demo: https://youtu.be/SUqrfV_y2lA
#### Description: A web app where you can search airplane tickets to the 50 most visited countries in the world.
#### OBS.: This was first created as my final project on the CS50 Course.

**Welcome to Tickets50!**
This is a web app where you can search airplane tickets to the 50 most visited countries in the world. At it's core, the web app relies on two features: a database and an api.

**The Tequila API**
The API been used here is called Tequila by Kiwi.com. This API gets you information about flight routes. Following the documentation on the official website, you will see that there are multiple possible parameters for the search API (https://tequila.kiwi.com/portal/docs/tequila_api/search_api). Using the correct parameters you can find specific flight routes.
OBS.: The Tequila API uses an API key which you need in order to use the API. You get one for free on https://tequila.kiwi.com/. The Code won't work until you add your own API key to the code.

**The Database**
In the database flights.db you will find two tables: airlines and airports. They are basically been used to find the airport or airline name based on the iata code been used (for more information on iata codes go to https://en.wikipedia.org/wiki/International_Air_Transport_Association_code). The reason why I'm using this is that the Tequila Search API will use as a parameter and get the information only by iata codes. But that is not very user-friendly. So in order to fix that, I'm using databases, that way I can find the information as a human would.

**The Files**
_data_scrapping.py:_ I used this file in order to scrap some data of the internet and fill the database. A part of the information I scrapped by hand, so you will not find all the code there. I used BeautifulSoup because it seemed easier, but you could certainly do the same with Selenium.

_helper.py:_ This one is where part of the magic happens. This is a file that contains function and other data that will be used by the app.py file. 
First we have two lists: _countries_with_url_ and _countries_list_. The first is a list of python dictionaries, each dict having a key/value pair for "country" and "url" (the "url" is not really an url, but it's being used for the url on the templates). And the second list is just the name of the 50 countries in alphabetical order.
Next is the _"error_page"_ function. It basic just renders a flask template for an error page. This function uses two parameters: message and error. Error is predefined as 400, but you could use the key parameter "code" to change it on the function call.
The other function on this file is _"get_route"_. I think this is one of the most complex parts of the web app (and for a pro this is probably not complex at all 😅). The function uses 5 parameters: dept_airport_iata (the iata code for the departure airport), dest_airport_iata (the iata code for the departure airport), dept_data (a datetime object for the datetime of the departure. This is predefined as the datetime for the moment the function is called), arr_date (Basically the same as the previous parameter but now for the arrival, or return trip, datetime), and finally direct_flight (This is a boolean that simply lets you say if you are going to search for direct_flights or not). Using the requests module, this function will access the API using the parameters need for a flight route to the destination you wanted. It always searches for round-trips. If the API could find any route, then it signals that something went wrong by returning False. After that on lines 111-114 it will find the cheapest route. After that the function will basically restructure some information on the data gotten from the API and add some information from the database as well.

_app.py:_ This is where Flask puts everything together. 
The first function uses the function decorator "app.context_processor" to make possible for the function "current_year" to be used in any flask template in the project. The idea is to have the year in the footer be dynamic.
After that there is the _"index"_ function. It is pretty straight forward.
And finally, we have the _"find_ticket"_ function. This function accepts two request method: on the Get method it will only work if the "country_id" value is filled in the url. It will render the template of find_tickets.html which has a conditional working to show part of the form that the user needs to send in order to get the information. After the user does that the POST method will kick-in. This is divided in two parts. The first part will show the rest of the form. And the second part will render the "found_ticket.html" template. This will show the user the route information. A big part of the code in this section deals with error treatment and possible user manipulation of the html.

**Design**
I based a lot of the design on some bootstrap templates you can find on the web.

I hope this explains thoroughly the project.
This is CS50!