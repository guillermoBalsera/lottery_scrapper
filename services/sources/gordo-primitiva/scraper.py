import re

from services import WEEK_DAY_EQUIVALENCE


def handle_response(raw_response):
    lotteries = []
    for raw_lottery in raw_response:
        numbers, refund = get_combination(raw_lottery.get("combinacion"))

        winner_list = raw_lottery.get("escrutinio")
        original_revenue = [raw_lottery.get("premios")[:-2], raw_lottery.get("premios")[-2:]] \
            if raw_lottery.get("premios") else [0, 0]
        original_collection = [raw_lottery.get("recaudacion")[:-2], raw_lottery.get("recaudacion")[-2:]] \
            if raw_lottery.get("recaudacion") else [0, 0]

        lottery = {
            "date": raw_lottery.get("fecha_sorteo"),
            "week_day": WEEK_DAY_EQUIVALENCE[raw_lottery.get("dia_semana").lower()],
            "numbers": [int(number) for number in numbers],
            "refund": int(refund),
            "has_winner": winner_list[0].get("ganadores") != '0',
            "winners": [int(prize.get("ganadores")) for prize in winner_list if prize.get("ganadores")],
            "revenue": float(f"{original_revenue[0]}.{original_revenue[1]}"),
            "earnings": float(f"{original_collection[0]}.{original_collection[1]}")
        }
        lotteries.append(lottery)
    return lotteries


def get_combination(original_combination):
    numbers = re.findall(r'\d{2}', original_combination)
    c_match = re.search(r'C\((\d*)\)', original_combination)
    r_match = re.search(r'R\((\d*)\)', original_combination)
    r_value = r_match.group(1) if r_match and r_match.group(1) != '' else 0
    return numbers, r_value
