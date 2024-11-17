import json
import os
from datetime import date
from datetime import datetime

from dotenv import load_dotenv

from services import WEEK_DAY_EQUIVALENCE
from services.requests import get_page


def handle_response(raw_response):
    lotteries = []
    for raw_lottery in raw_response:
        original_combination = raw_lottery.get("combinacion").split("C")
        combination = [int(number) for number in raw_lottery.get("combinacion").split("-")]
        winner_list = raw_lottery.get("escrutinio")
        original_revenue = [raw_lottery.get("premios")[:-2], raw_lottery.get("premios")[-2:]]
        original_collection = [raw_lottery.get("recaudacion")[:-2], raw_lottery.get("recaudacion")[-2:]]

        lottery = {
            "date": raw_lottery.get("fecha_sorteo"),
            "week_day": WEEK_DAY_EQUIVALENCE[raw_lottery.get("dia_semana").lower()],
            "numbers": combination[0:5],
            "stars": combination[5:7],
            "has_winner": winner_list[0].get("ganadores") != '0',
            "winners": [int(prize.get("ganadores")) for prize in winner_list if prize.get("ganadores")],
            "revenue": float(f"{original_revenue[0]}.{original_revenue[1]}"),
            "earnings": float(f"{original_collection[0]}.{original_collection[1]}")
        }
        lotteries.append(lottery)
    return lotteries
