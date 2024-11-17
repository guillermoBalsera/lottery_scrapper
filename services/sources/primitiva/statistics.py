from collections import Counter

import pandas as pd

from services.sources import generic_get_pairs


def get_frequencies(lottery_data):
    all_numbers = Counter([num for draw in lottery_data for num in draw['numbers']])
    all_complementary = Counter([draw['complementary'] for draw in lottery_data])
    all_refunds = Counter([draw['refund'] for draw in lottery_data])

    return {
        "number_frequency": dict(all_numbers),
        "complementary_frequency": dict(all_complementary),
        "refund_frequency": dict(all_refunds)
    }


def get_pairs(lottery_data):
    return generic_get_pairs(lottery_data)


def get_yearly_trends(lottery_data):
    df = pd.DataFrame(lottery_data)
    df['date'] = pd.to_datetime(df['date'])
    df['sum_numbers'] = df['numbers'].apply(sum)
    yearly_trends = df.groupby(df['date'].dt.year)['sum_numbers'].mean()
    return yearly_trends.to_dict()


def get_even_odd(lottery_data):
    even_odd_counts = {"even": 0, "odd": 0}
    all_numbers = [num for draw in lottery_data for num in draw["numbers"]]
    for num in all_numbers:
        if num % 2 == 0:
            even_odd_counts['even'] += 1
        else:
            even_odd_counts['odd'] += 1

    return even_odd_counts
