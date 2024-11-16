from datetime import datetime

from services.downloader import SPANISH_MONTHS_SHORTCUTS


def transform_row(row, year):
    if len(row[1].split("/")) == 3:
        lottery_date = datetime.strptime(row[1], '%d/%m/%Y')
    else:
        row = row if len(row[1].split("/")) < 2 else row[1:]

        row[0] = row[0].split("/")[1]
        day, month = row[1].split("-")
        lottery_date = datetime(year, SPANISH_MONTHS_SHORTCUTS[month], int(day))
    return {
        "lottery": int(row[0].replace("*", "")),
        "date": lottery_date.strftime("%Y-%m-%d"),
        "numbers": list(map(int, row[2:8])),
        "refund": int(row[8]),
        "complementary": int(row[9])
    }


def get_data_from_row(year_rows):
    final_data = []
    for row in year_rows:
        row_data = [r.text for r in row.findAll("td") if r.text != ""]
        if len(row_data) > 2 and "SORTEO" not in row_data:
            final_data.append(row_data)

    return final_data


def get_year_results(data):
    year_table = data.find("table", {"class": "histoprimi"})
    return year_table.findAll("tr") if year_table else []
