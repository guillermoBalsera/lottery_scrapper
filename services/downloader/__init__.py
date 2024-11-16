import json
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
import importlib

from services.downloader.request import get_page

SPANISH_MONTHS_SHORTCUTS = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4,
    "may": 5, "jun": 6, "jul": 7, "ago": 8,
    "sep": 9, "oct": 10, "nov": 11, "dic": 12
}

SOURCES = {
    "euromillon": "https://www.euromillones.com.es/historico/resultados-euromillones",
    "primitiva": "https://www.laprimitiva.info/historico/sorteos-la-primitiva",
    "gordo_primitiva": "https://www.elgordodelaprimitiva.com.es/gordoprimitiva/sorteos",
    "bonoloto": "https://www.loteriabonoloto.info/historico-bonoloto/sorteos"
}


def write_data(final_data, year, lottery_name):
    path_name = f"./downloads/{lottery_name}"
    Path(path_name).mkdir(parents=True, exist_ok=True)
    with open(f"{path_name}/{year}.json", "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=4)
        print(f"\tData downloaded for year {year}")


def download(min_year, max_year):
    print(f"Starting data scrape from {min_year} to {max_year}\n")
    for source, url_template in SOURCES.items():
        print(f"Processing source: {source}")
        for year in range(min_year, max_year + 1):
            page_content = get_page(year, url_template)
            soup = BeautifulSoup(page_content, "html.parser")
            try:
                module = importlib.import_module(f"services.downloader.sources.{source}")
                get_year_results_function = getattr(module, "get_year_results")
                year_table_rows = get_year_results_function(soup)
                get_data_from_row_function = getattr(module, "get_data_from_row")
                result_rows = get_data_from_row_function(year_table_rows)
                transform_row_function = getattr(module, "transform_row")
                final_data = [transform_row_function(row, year) for row in result_rows]
                write_data(final_data, year, source)
            except ModuleNotFoundError:
                print(f"Couldn't find the module for source '{source}'. Skipping.")
                break
            except AttributeError:
                print(f"Couldn't find 'get_year_results' in module '{source}'. Skipping.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
