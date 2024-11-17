from collections import Counter
from itertools import combinations


def generic_get_pairs(lottery_data):
    number_pairs = Counter(pair for draw in lottery_data for pair in combinations(draw['numbers'], 2))
    number_triplets = Counter(triplet for draw in lottery_data for triplet in combinations(draw['numbers'], 3))

    number_pairs_dict = {str(key): value for key, value in number_pairs.items()}
    number_triplets_dict = {str(key): value for key, value in number_triplets.items()}

    return {
        "number_pairs": number_pairs_dict,
        "number_triplets": number_triplets_dict,
        "most_common_pairs": number_pairs.most_common(5),
        "most_common_triplets": number_triplets.most_common(5)
    }
