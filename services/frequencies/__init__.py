import json
import os
from collections import Counter

FILES_PATH = './downloads'


def read_files():
    files = os.listdir(FILES_PATH)
    data = []
    for file in files:
        with open(f"{FILES_PATH}/{file}", 'r') as f:
            data.append(json.load(f))
    return data


def calculate():
    lottery_data = read_files()
    lotteries = len([lottery for year_list in lottery_data for lottery in year_list if lottery.get("numbers")])
    lottery_numbers = [number for year_list in lottery_data for lottery in year_list if lottery.get("numbers") for
                       number in lottery.get("numbers")]
    lottery_stars = [star for year_list in lottery_data for lottery in year_list if lottery.get("numbers") for star in
                     lottery.get("stars")]

    numbers_result = [{number: {"frequency": frequency, "percentage": round(frequency * 100 / lotteries, 2)}} for
                      number, frequency in sorted(Counter(lottery_numbers).items(), key=lambda x: x[1], reverse=True)]
    stars_result = [{star: {"frequency": frequency, "percentage": round(frequency * 100 / lotteries, 2)}}
                    for star, frequency in sorted(Counter(lottery_stars).items(), key=lambda x: x[1], reverse=True)]

    most_probable_combination = {
        "numbers": sorted([list(number.keys())[0] for number in numbers_result[:5]]),
        "stars": sorted([list(star.keys())[0] for star in stars_result[:2]])
    }

    print(most_probable_combination)
