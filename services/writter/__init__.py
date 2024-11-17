import json
from pathlib import Path


def write_downloads_data(final_data, lottery_name):
    path_name = f"./downloads"
    Path(path_name).mkdir(parents=True, exist_ok=True)
    with open(f"{path_name}/{lottery_name}.json", "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=4)
