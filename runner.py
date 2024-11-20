import argparse
import importlib
import json
import logging
import os
from datetime import date, datetime

from dotenv import load_dotenv

from services import SOURCES_MIN_YEARS, SOURCES_ACRONYMS
from services.file_reader import read_file
from services.file_writer import write_downloads_data, write_statistics_data
from services.logger import set_logging
from services.requests import get_page

MAX_DATE = date.today().year

SOURCES = ["euromillon", "primitiva", "bonoloto", "gordo-primitiva", "eurodreams", "loteria-nacional"]

ERROR_MESSAGE = "No se ha encontrado ningún registro para los parámetros introducidos."


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=str, help="Action to carry out")
    arguments = parser.parse_args()
    return arguments.action


def main():
    set_logging()

    action = get_args()
    match action:
        case "download":
            scrape_sources()
        case "statistics":
            calculate_statistics()
        case _:
            raise ValueError("Action not found")


def scrape_sources():
    logging.info(f"Starting data scrape")
    for source in SOURCES:
        logging.info(f"Processing source: {source}")
        try:
            module = importlib.import_module(f"services.sources.{source}.scraper")

            source_data = []

            for year in range(SOURCES_MIN_YEARS[source], date.today().year + 1):
                raw_response = make_source_request(year, SOURCES_ACRONYMS[source])
                logging.info(f"\tFound {len(raw_response): >4} lotteries in {year}")

                if raw_response == ERROR_MESSAGE:
                    raise YearErrorException()

                handle_response = getattr(module, "handle_response")
                source_data += handle_response(raw_response)

            sorted_data = sorted(source_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"))
            write_downloads_data(source, sorted_data)
            logging.info(f"Scraped {len(source_data)} between {SOURCES_MIN_YEARS[source]} and {date.today().year} for {source}\n")
        except YearErrorException:
            logging.warning(f"Incorrect year for source {source}. Skipping\n")
        except ModuleNotFoundError:
            logging.warning(f"Couldn't find the module for source '{source}'. Skipping\n")
        except AttributeError:
            logging.warning(f"Couldn't find function in module '{source}'. Skipping\n")
        except Exception as e:
            logging.error(f"\tAn error occurred while downloading {source}: {e}")


def calculate_statistics():
    logging.info("\nStarting to calculate data")
    for source in SOURCES:
        logging.info(f"\nCalculating statistics for {source}")
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
        except ModuleNotFoundError:
            logging.warning(f"Couldn't find the module for source '{source}'. Skipping.")
        except AttributeError:
            logging.warning(f"Couldn't find function in module '{source}'. Skipping.")
        except Exception as e:
            logging.error(f"\tAn error occurred while calculating statistics for {source}: {e}")


def make_source_request(year, acronym):
    final_date = datetime(year, 12, 31) if year < MAX_DATE else datetime.now()
    load_dotenv()
    url = os.getenv('API_URL')
    params = {
        "game_id": acronym,
        "celebrados": True,
        "fechaInicioInclusiva": datetime(year, 1, 1).strftime('%Y%m%d'),
        "fechaFinInclusiva": final_date.strftime('%Y%m%d')
    }
    return json.loads(get_page(url, params))


class YearErrorException(Exception):
    def __init__(self, message="Year error"):
        self.message = message
        super().__init__(self.message)


if __name__ == "__main__":
    main()
