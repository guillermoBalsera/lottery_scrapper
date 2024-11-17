import argparse
import importlib
from datetime import date

from bs4 import BeautifulSoup

from services import SOURCES
from services.file_reader import read_file
from services.file_writer import write_downloads_data, write_statistics_data
from services.requests import get_page

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
        case "statistics":
            calculate_statistics()
        case _:
            raise ValueError("Action not found")


def scrape_sources(min_year, max_year):
    print(f"Starting data scrape from {min_year} to {max_year}\n")
    for source, url_template in SOURCES.items():
        final_data = []
        print(f"Processing source: {source}")
        for year in range(min_year, max_year + 1):
            page_content = get_page(year, url_template)
            soup = BeautifulSoup(page_content, "html.parser")
            try:
                module = importlib.import_module(f"services.sources.{source}.scraper")
                get_year_results_function = getattr(module, "get_year_results")
                get_data_from_row_function = getattr(module, "get_data_from_row")
                transform_row_function = getattr(module, "transform_row")

                year_table_rows = get_year_results_function(soup)
                result_rows = get_data_from_row_function(year_table_rows)
                final_data += [transform_row_function(row, year) for row in result_rows]
                print(f"\tData downloaded for year {year}")
            except ModuleNotFoundError:
                print(f"Couldn't find the module for source '{source}'. Skipping.")
                break
            except AttributeError:
                print(f"Couldn't find function in module '{source}'. Skipping.")
                break
            except Exception as e:
                print(f"\tAn error occurred while downloading {source}, {year}:\n\t\t{e}")
        write_downloads_data(final_data, source)


def calculate_statistics():
    print("\nStarting to calculate data")
    for source in SOURCES:
        print(f"\nCalculating statistics for {source}")
        try:
            module = importlib.import_module(f"services.sources.{source}.statistics")
            get_frequencies_function = getattr(module, "get_frequencies")
            get_pairs_function = getattr(module, "get_pairs")
            get_yearly_trends_function = getattr(module, "get_yearly_trends")
            get_even_odd_function = getattr(module, "get_even_odd")

            lottery_data = read_file(source)

            source_frequencies = get_frequencies_function(lottery_data)
            source_pairs = get_pairs_function(lottery_data)
            source_yearly_trends = get_yearly_trends_function(lottery_data)
            source_even_odd = get_even_odd_function(lottery_data)
            write_statistics_data(source, yearly_trends=source_yearly_trends)
        #       , pairs=source_pairs, even_odd=source_even_odd, frequencies=source_frequencies,
        except ModuleNotFoundError:
            print(f"Couldn't find the module for source '{source}'. Skipping.")
            break
        except AttributeError:
            print(f"Couldn't find function in module '{source}'. Skipping.")
            break
        except Exception as e:
            print(f"\tAn error occurred while calculating statistics {source}: \n\t\t{e}")


if __name__ == "__main__":
    main()
