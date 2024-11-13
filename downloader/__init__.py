import json
from datetime import datetime
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

SPANISH_MONTHS_SHORTCUTS = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4,
    "may": 5, "jun": 6, "jul": 7, "ago": 8,
    "sep": 9, "oct": 10, "nov": 11, "dic": 12
}


def write_data(final_data, year):
    with open(f"./exports/{year}.json", "w") as file:
        file.write(json.dumps(final_data))
        print(f"\tData downloaded for year {year}")


def transform_row(row, year):
    Path("./exports").mkdir(parents=True, exist_ok=True)
    original_day, original_month = (row[1].split("-"))
    return {
        "lottery": int(row[0].replace("*", "")),
        "date": datetime(year, SPANISH_MONTHS_SHORTCUTS.get(original_month), int(original_day)).isoformat(),
        "numbers": [int(x) for x in row[2:7]],
        "stars": [int(x) for x in row[7:9]]
    }


def get_data_from_row(year_rows, year):
    final_data = []
    for row in year_rows:
        row_data = [r.text for r in row.findAll("td") if r.text != ""]
        if len(row_data) > 2 and "ESTRELLAS" not in row_data and "SORTEO" not in row_data:
            if len(row_data[-1]) > 7:
                row_data = row_data[0:-1]
            if row.find("td", {"class", "nmt"}) or ("SEM." == year_rows[0].find("b").text and len(row_data) == 10):
                row_data = row_data[1:]
            if "/" in list(row_data[0]):
                row_data[0] = row_data[0].split("/")[1]
            final_data.append(row_data)

    return final_data


def get_year_results(data):
    year_table = data.find("table", {"class": "histoeuro"})
    return year_table.findAll("tr")


def get_year_page(year):
    tries = 0
    while tries < 10:
        response = requests.get(f"https://www.euromillones.com.es/historico/resultados-euromillones-{year}.html")
        if response.ok:
            return response.text
        tries += 1
        sleep(1)
    raise ValueError("RETRIES EXCEEDED")


def download(min_year, max_year):
    print(f"Going to scrape data from {min_year} to {max_year - 1}\n")
    for year in range(min_year, max_year):
        data = get_year_page(year)
        beautified_data = BeautifulSoup(data, features="html.parser")
        year_table_rows = get_year_results(beautified_data)
        result_rows = get_data_from_row(year_table_rows, year)
        final_data = []
        for row in result_rows:
            final_data.append(transform_row(row, year))
        write_data(final_data, year)
