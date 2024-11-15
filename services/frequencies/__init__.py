import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

FILES_PATH = './downloads'


def read_files():
    files = os.listdir(FILES_PATH)
    data = []
    for file in files:
        with open(f"{FILES_PATH}/{file}", 'r') as f:
            data.append(json.load(f))
    return data


def get_lotteries(lottery_data):
    return [lottery for year_list in lottery_data for lottery in year_list if lottery.get("numbers")]


def get_numbers_and_stars(lotteries):
    return ([number for lottery in lotteries for number in lottery.get("numbers")],
            [stars for lottery in lotteries for stars in lottery.get("stars")])


def get_number_results(lottery_numbers, lotteries_length):
    return [{number: {"frequency": frequency, "percentage": round(frequency * 100 / lotteries_length, 2)}}
            for number, frequency in sorted(Counter(lottery_numbers).items(), key=lambda x: x[1], reverse=True)]


def get_star_results(lottery_stars, lotteries_length):
    return [{star: {"frequency": frequency, "percentage": round(frequency * 100 / lotteries_length, 2)}}
            for star, frequency in sorted(Counter(lottery_stars).items(), key=lambda x: x[1], reverse=True)]


def get_last_dates(lotteries):
    last_date = {}
    for lottery in lotteries:
        lottery_date = datetime.fromisoformat(lottery["date"])
        for number in lottery["numbers"]:
            if number not in last_date or lottery_date > last_date[number]:
                last_date[number] = lottery_date

    return [{"number": number, "last_date": date.strftime('%Y-%m-%d')} for number, date in last_date.items()]


def write_results(number_results, star_results, most_probable_combination):
    results = {
        "numbers_stats": number_results,
        "stars_stats": star_results,
        "most_probable_combination": most_probable_combination
    }
    path_name = f"results/{datetime.now().strftime("%Y/%b/")}"
    Path(path_name).mkdir(parents=True, exist_ok=True)
    file_name = f"{path_name}/{datetime.now().strftime("%d")}.json"
    with open(file_name, "w") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


def calculate():
    lottery_data = read_files()
    lotteries = get_lotteries(lottery_data)

    last_dates = get_last_dates(lotteries)
    lottery_numbers, lottery_stars = get_numbers_and_stars(lotteries)

    numbers_result = get_number_results(lottery_numbers, len(lotteries))
    stars_result = get_star_results(lottery_stars, len(lotteries))

    most_probable_combination = {
        "numbers": sorted([list(number.keys())[0] for number in numbers_result[:5]]),
        "stars": sorted([list(star.keys())[0] for star in stars_result[:2]])
    }

    write_results(numbers_result, stars_result, most_probable_combination)
    print("most_probable_combination:", most_probable_combination)
