import re

from services import WEEK_DAY_EQUIVALENCE


def handle_response(raw_response):
    lotteries = []
    for raw_lottery in raw_response:
        winners = get_combination(raw_lottery)

        winner_list = raw_lottery.get("escrutinio")
        original_revenue = [raw_lottery.get("premios")[:-2], raw_lottery.get("premios")[-2:]] \
            if raw_lottery.get("premios") else [0, 0]
        original_collection = [raw_lottery.get("recaudacion")[:-2], raw_lottery.get("recaudacion")[-2:]] \
            if raw_lottery.get("recaudacion") else [0, 0]

        lottery = {
            "date": raw_lottery.get("fecha_sorteo"),
            "week_day": WEEK_DAY_EQUIVALENCE[raw_lottery.get("dia_semana").lower()],
            "has_winner": winner_list[0].get("ganadores") != '0',
            "winners": [int(prize.get("ganadores")) for prize in winner_list if prize.get("ganadores")],
            "revenue": float(f"{original_revenue[0]}.{original_revenue[1]}"),
            "earnings": float(f"{original_collection[0]}.{original_collection[1]}")
        }
        lotteries.append(lottery)
    return lotteries


def get_combination(raw_lottery):
    prizes_names = ["primerPremio", "segundoPremio"]
    winners = []
    for prize_name in prizes_names:
        if prize_response := raw_lottery.get(prize_name):
            numbers = [int(number) for number in list(prize_response.get("decimo"))]
            winners.append(numbers)
    return winners

