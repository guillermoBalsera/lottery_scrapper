import argparse
import importlib
from datetime import date

from services.file_reader import read_file
from services.file_writer import write_downloads_data, write_statistics_data

MIN_YEAR = 2004
MAX_YEAR = date.today().year

SOURCES = ["euromillon", "primitiva", "bonoloto", "el_gordo", "eurodreams", "loteria_nacional"]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=str, help="Action to carry out")
    arguments = parser.parse_args()
    return arguments.action


def main():
    action = get_args()
    match action:
        case "download":
            scrape_sources()
        case "statistics":
            calculate_statistics()
        case _:
            raise ValueError("Action not found")


def scrape_sources():
    print(f"Starting data scrape")
    for source in SOURCES:
        print(f"Processing source: {source}")
        try:
            module = importlib.import_module(f"services.sources.{source}.scraper")

            for year in range(MIN_YEAR, MAX_YEAR + 1):
                make_request_function = getattr(module, "make_request")
                raw_response = make_request_function(year)
                print(f"\tFound {len(raw_response)} lotteries")
                # write_downloads_data(raw_response, source)
        except ModuleNotFoundError:
            print(f"Couldn't find the module for source '{source}'. Skipping.")
            break
        except AttributeError:
            print(f"Couldn't find function in module '{source}'. Skipping.")
            break
        except Exception as e:
            print(f"\tAn error occurred while downloading {source}:\n\t\t{e}")


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
