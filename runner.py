import argparse
import importlib
from datetime import date

from bs4 import BeautifulSoup

from services import SOURCES
from services.requests import get_page
from services.writter import write_downloads_data

MIN_YEAR = 2004
MAX_YEAR = date.today().year


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=str, help="Action to carry out")
    parser.add_argument("-min", "--min_year", type=int, help="First year to download", default=MIN_YEAR)
    parser.add_argument("-max", "--max_year", type=int, help="Last year to download", default=MAX_YEAR)
    arguments = parser.parse_args()
    return arguments.action, arguments.min_year, arguments.max_year


def main():
    action, min_year, max_year = get_args()
    match action:
        case "download":
            min_year = MIN_YEAR if min_year < MIN_YEAR else min_year
            max_year = MAX_YEAR if max_year > MAX_YEAR else max_year
            scrape_sources(min_year, max_year)
        case "frequencies":
            calculate_frequencies()


def scrape_sources(min_year, max_year):
    print(f"Starting data scrape from {min_year} to {max_year}\n")
    for source, url_template in SOURCES.items():
        final_data = []
        print(f"\nProcessing source: {source}")
        for year in range(min_year, max_year + 1):
            page_content = get_page(year, url_template)
            soup = BeautifulSoup(page_content, "html.parser")
            try:
                module = importlib.import_module(f"services.sources.{source}.scraper")
                get_year_results_function = getattr(module, "get_year_results")
                year_table_rows = get_year_results_function(soup)
                get_data_from_row_function = getattr(module, "get_data_from_row")
                result_rows = get_data_from_row_function(year_table_rows)
                transform_row_function = getattr(module, "transform_row")
                final_data += [transform_row_function(row, year) for row in result_rows]
                print(f"\tData downloaded for year {year}")
            except ModuleNotFoundError:
                print(f"Couldn't find the module for source '{source}'. Skipping.")
                break
            except AttributeError:
                print(f"Couldn't find function in module '{source}'. Skipping.")
                break
            except Exception as e:
                print(f"\tAn error occurred {source}, {year}:\n\t\t{e}")
        write_downloads_data(final_data, source)


def calculate_frequencies():
    pass


if __name__ == "__main__":
    main()
