import json
from pathlib import Path


def write_downloads_data(lottery_name, final_data):
    path_name = f"./downloads"
    Path(path_name).mkdir(parents=True, exist_ok=True)
    with open(f"{path_name}/{lottery_name}.json", "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=4)


def write_statistics_data(source, **kwargs):
    for argument_name, argument_value in kwargs.items():
        path_name = f"./statistics/{source}"
        Path(path_name).mkdir(parents=True, exist_ok=True)
        with open(f"{path_name}/{argument_name}.json", "w", encoding="utf-8") as file:
            json.dump(argument_value, file, ensure_ascii=False, indent=4)
