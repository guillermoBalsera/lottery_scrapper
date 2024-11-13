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
    with open(f"./downloads/{year}.json", "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=4)
        print(f"\tData downloaded for year {year}")


def transform_row(row, year):
    day, month = row[1].split("-")
    return {
        "lottery": int(row[0].replace("*", "")),
        "date": datetime(year, SPANISH_MONTHS_SHORTCUTS[month], int(day)).isoformat(),
        "numbers": list(map(int, row[2:7])),
        "stars": list(map(int, row[7:9]))
    }


def get_data_from_row(year_rows):
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
    return year_table.findAll("tr") if year_table else []


def get_year_page(year):
    url = f"https://www.euromillones.com.es/historico/resultados-euromillones-{year}.html"
    for attempt in range(10):
        try:
            response = requests.get(url)
            if response.ok:
                return response.text
        except requests.RequestException as e:
            print(f"Request error on {url}: {e}")
        sleep(1)
    raise ValueError(f"Failed to fetch data for {year} after 10 attempts")


def download(min_year, max_year):
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    print(f"Starting data scrape from {min_year} to {max_year}\n")
    for year in range(min_year, max_year + 1):
        page_content = get_year_page(year)
        soup = BeautifulSoup(page_content, "html.parser")
        year_table_rows = get_year_results(soup)
        result_rows = get_data_from_row(year_table_rows)
        final_data = [transform_row(row, year) for row in result_rows]
        write_data(final_data, year)
