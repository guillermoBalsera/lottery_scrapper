import argparse
from datetime import date

from downloader import download
from frequencies import calculate

MIN_YEAR = 2004
MAX_YEAR = date.today().year + 1


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
            max_year = MAX_YEAR if max_year < MAX_YEAR else max_year
            download(min_year, max_year)
        case "frequencies":
            calculate()


if __name__ == "__main__":
    main()
