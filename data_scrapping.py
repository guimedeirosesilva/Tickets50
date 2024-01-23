from cs50 import SQL
from bs4 import BeautifulSoup
import requests
import csv
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# html = requests.get("https://en.wikipedia.org/wiki/List_of_international_airports_by_country").text
# soup = BeautifulSoup(html, "html.parser")
#
# list_countries = [
#     "France",
#     "United States",
#     "Spain",
#     "Italy",
#     "China",
#     "England and Wales",
#     "Scotland",
#     "Northern Ireland",
#     "Russia",
#     "Mexico",
#     "Canada",
#     "Germany",
#     "Austria",
#     "Poland",
#     "Hungary",
#     "Greece",
#     "Morocco",
#     "South Africa",
#     "Tunisia",
#     "Algeria",
#     "Mozambique",
#     "Zimbabwe",
#     "Kenya",
#     "Uganda",
#     "Saudi Arabia",
#     "United Arab Emirates",
#     "Egypt",
#     "Iran",
#     "Jordan",
#     "Israel",
#     "Brazil",
#     "Argentina",
#     "Colombia",
#     "Chile",
#     "Peru",
#     "Hong Kong",
#     "India",
#     "Thailand",
#     "South Korea",
#     "Japan",
#     "Indonesia",
#     "Turkey",
#     "Macau",
#     "Cyprus",
#     "Malaysia",
#     "Dominican Republic",
#     "Qatar",
#     "Oman",
#     "Bahrain",
#     "Senegal",
#     "Namibia",
#     "Australia",
# ]
#
# for headline in soup.select("h4:has(> span)"):
#     if headline.select_one("span").get_text() in list_countries:
#         for tr in headline.find_next_sibling().select("tr"):
#             line = tr.get_text().strip().replace('\n\n', ',').replace('\n', ',')
#             if line == "Location,Airport,IATA Code" or line == "Location,Airport,IATA Code,State/territory":
#                 continue
#             line += f",{headline.select_one('span').get_text()}\n"
#
#             with open('airports.csv', "a", encoding="utf-8") as file:
#                 file.writelines(line)


# db = SQL("sqlite:///flights.db")
#
# with open('airports.csv', "r", encoding="utf-8") as file_csv:
#     reader = csv.DictReader(file_csv)
#     for row in reader:
#         location = row["Location"]
#         db.execute(
#             "INSERT INTO airports (iata_code, name, city, country) VALUES (?, ?, ?, ?);",
#             row["IATACode"],
#             row["Airport"],
#             row["Location"],
#             row["Country"]
#         )
        # if row["Country"] is None:
        #     db.execute(
        #         "INSERT INTO airports (iata_code, name, city, country) VALUES (?, ?, ?, ?);",
        #         row["Airport"],
        #         row["Location"],
        #         location,
        #         row["IATACode"]
        #     )
        # elif len(row) != 4:
        #     print(row)
        # else:
        #     location = row["Location"]
        #     db.execute(
        #         "INSERT INTO airports (iata_code, name, city, country) VALUES (?, ?, ?, ?);",
        #         row["IATACode"],
        #         row["Airport"],
        #         row["Location"],
        #         row["Country"]
        #     )





# from cs50 import SQL
#
# db = SQL("sqlite:///flights.db")
#
# airlines_list = []
#
# alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
#             'V', 'W', 'X', 'Y', 'Z', '0']
#
#
# URL_IATA_AIRLINES = "https://airlinecodes.info/iata/"
#
# for letter in alphabet:
#     html = requests.get(f"{URL_IATA_AIRLINES}{letter}").text
#
#     soup = BeautifulSoup(html, "html.parser")
#
#     table = soup.select_one("div.contentbody table")
#
#     rows = table.select("tr")
#
#     for row in rows:
#         data = row.select("td")
#
#         try:
#             db.execute(
#                 "INSERT INTO airlines (iata_code, name) VALUES (?, ?)",
#                 data[0].get_text(),
#                 data[2].get_text()
#             )
#             print(data[0].get_text(), data[2].get_text())
#             with open("airlines_info.txt", "a", encoding="UTF-8") as file:
#                 file.write(f"{data[0].get_text()},{data[2].get_text()}\n")
#         except IndexError:
#             pass
