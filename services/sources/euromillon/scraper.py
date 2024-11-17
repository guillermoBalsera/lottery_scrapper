import json
import os
from datetime import date
from datetime import datetime

from dotenv import load_dotenv

from services import SPANISH_MONTHS_SHORTCUTS
from services.requests import get_page

MAX_DATE = date.today().year


def make_request(year):
    final_date = datetime(year, 12, 31) if year < MAX_DATE else date.today
    load_dotenv()
    url = os.getenv('API_URL')
    params = {
        "game_id": "EMIL",
        "celebrados": True,
        "fechaInicioInclusiva": datetime(year, 1, 1).strftime('%Y%m%d'),
        "fechaFinInclusiva":  final_date.strftime('%Y%m%d')
    }
    return json.loads(get_page(url, params))


def transform_row(row, year):
    day, month = row[1].split("-")
    lottery_date = datetime(year, SPANISH_MONTHS_SHORTCUTS[month], int(day))
    return {
        "lottery": int(row[0].replace("*", "")),
        "date": datetime.strftime(lottery_date, '%Y-%m-%d'),
        "numbers": list(map(int, row[2:7])),
        "stars": list(map(int, row[7:9]))
    }


def get_data_from_row(year_rows):
    final_data = []
    for row in year_rows:
        row_data = [r.text for r in row.findAll("td") if r.text != ""]
        if len(row_data) > 3 and "ESTRELLAS" not in row_data and "SORTEO" not in row_data:
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
