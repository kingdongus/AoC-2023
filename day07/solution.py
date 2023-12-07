import sys
from collections import Counter
from functools import cmp_to_key

from toolbox.toolbox import input_file_name

strength_order_part_1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
strength_order_part_2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']


def parse_cards_and_bids(data):
    ret = []
    for line in data:
        s = line.replace('\n', '')
        s = s.split(' ')
        ret.append((list(s[0]), int(s[1])))
    return ret


def is_full_house(hand):
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    values = list(counts.values())
    return sorted(values) == [2, 3]


def is_two_pair(hand):
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    values = list(counts.values())
    return sorted(values) == [1, 2, 2]


def is_n_of_a_kind(hand, n):
    counts = {}

    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    for count in counts.values():
        if count == n:
            return True

    return False


def is_five_of_a_kind(hand):
    return is_n_of_a_kind(hand, 5)


def is_four_of_a_kind(hand):
    return is_n_of_a_kind(hand, 4)


def is_three_of_a_kind(hand):
    return is_n_of_a_kind(hand, 3)


def is_one_pair(hand):
    return is_n_of_a_kind(hand, 2)


relative_strength_functions = [is_five_of_a_kind,
                               is_four_of_a_kind,
                               is_full_house,
                               is_three_of_a_kind,
                               is_two_pair,
                               is_one_pair]


def has_higher_card(hand_1, hand_2, strength_order):
    for a, b in zip(hand_1, hand_2):
        if strength_order.index(a) < strength_order.index(b):
            return 1
        elif strength_order.index(a) > strength_order.index(b):
            return -1
    return 0


def has_higher_card_part_1(hand1, hand2):
    return has_higher_card(hand1, hand2, strength_order_part_1)


def has_higher_card_part_2(hand1, hand2):
    return has_higher_card(hand1, hand2, strength_order_part_2)


def hand_comparator_part_1(hand_1, hand_2):
    strength_first = determine_hand_strength(hand_1)
    strength_second = determine_hand_strength(hand_2)

    if strength_first < strength_second:
        return 1

    if strength_first > strength_second:
        return -1

    return has_higher_card_part_1(hand_1, hand_2)


def determine_hand_strength(hand):
    strength_first = sys.maxsize
    idx = 0
    for f in relative_strength_functions:
        if f(hand):
            strength_first = idx
            break
        idx += 1
    return strength_first


def hand_comparator_part_2(hand_1, hand_2):
    strength_first = determine_hand_strength(replace_jokers(hand_1))
    strength_second = determine_hand_strength(replace_jokers(hand_2))

    if strength_first < strength_second:
        return 1

    if strength_first > strength_second:
        return -1

    return has_higher_card_part_2(hand_1, hand_2)


def replace_jokers(hand):
    num_jokers = hand.count('J')

    if num_jokers == 0:
        return hand
    if num_jokers == 5:
        return ['A', 'A', 'A', 'A', 'A']

    # get card that is most common, tie-break for highest value
    hand_without_jokers = list(filter(lambda a: a != 'J', hand))
    num_most_common = Counter(hand_without_jokers).most_common(1)[0][1]
    most_common_highest_value = sorted(list(
        set([x for x in hand_without_jokers if hand_without_jokers.count(x) == num_most_common])),
        key=lambda x: strength_order_part_1.index(x))[0]

    # replace jokers with most common highest value card
    modified = hand[::]
    for i in range(len(modified)):
        if modified[i] == 'J':
            modified[i] = most_common_highest_value
    return modified


def comparator_part_1(first, second):
    return hand_comparator_part_1(first[0], second[0])


def comparator_part_2(first, second):
    return hand_comparator_part_2(first[0], second[0])


def part_1(problem):
    cards_and_bids = sorted(parse_cards_and_bids(problem), key=cmp_to_key(comparator_part_1))

    idx = 1
    s = 0
    for _, bid in cards_and_bids:
        delta = bid * idx
        s += delta
        idx += 1
    return s


def part_2(problem):
    cards_and_bids = sorted(parse_cards_and_bids(problem), key=cmp_to_key(comparator_part_2))

    idx = 1
    s = 0
    for _, bid in cards_and_bids:
        delta = bid * idx
        s += delta
        idx += 1
    return s


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))

    with open(input_file_name) as problem:
        print(part_2(problem))
