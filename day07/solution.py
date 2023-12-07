import sys
from collections import Counter
from functools import cmp_to_key

from toolbox.toolbox import input_file_name

strength_order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
strength_order_with_joker = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']


def parse_cards_and_bids(data):
    ret = []
    for line in data:
        s = line.replace('\n', '')
        s = line.split(' ')
        ret.append((list(s[0]), int(s[1])))
    return ret


def is_full_house(cards):
    counts = {}
    for card in cards:
        counts[card] = counts.get(card, 0) + 1
    values = list(counts.values())
    return sorted(values) == [2, 3]


def is_two_pair(hand):
    counts = {}

    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    pair_count = 0

    for count in counts.values():
        if count == 2:
            pair_count += 1

    return pair_count == 2


def is_n_of_a_kind(hand, n):
    counts = {}

    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    for count in counts.values():
        if count == n:
            return True

    return False


def is_five_of_a_kind(cards):
    return is_n_of_a_kind(cards, 5)


def is_four_of_a_kind(cards):
    return is_n_of_a_kind(cards, 4)


def is_three_of_a_kind(cards):
    return is_n_of_a_kind(cards, 3)


def is_one_pair(cards):
    return is_n_of_a_kind(cards, 2)


relative_strength_functions = [is_five_of_a_kind,
                               is_four_of_a_kind,
                               is_full_house,
                               is_three_of_a_kind,
                               is_two_pair,
                               is_one_pair]


def has_higher_card(hand1, hand2):
    for a, b in zip(hand1, hand2):
        if strength_order.index(a) < strength_order.index(b):
            return 1
        elif strength_order.index(a) > strength_order.index(b):
            return -1
    return 0


def has_higher_card_part_2(hand1, hand2):
    for a, b in zip(hand1, hand2):
        if strength_order_with_joker.index(a) < strength_order.index(b):
            return 1
        elif strength_order_with_joker.index(a) > strength_order.index(b):
            return -1
    return 0


def card_comparator(first, second):
    strength_first = determine_hand_strength(first)
    strength_second = determine_hand_strength(second)

    if strength_first < strength_second:
        return 1

    if strength_first > strength_second:
        return -1

    return has_higher_card(first, second)


def determine_hand_strength(first):
    strength_first = sys.maxsize
    idx = 0
    for f in relative_strength_functions:
        if f(first):
            strength_first = idx
            break
        idx += 1
    return strength_first


def card_comparator_part_2(first, second):
    modified_first = replace_jokers(first)
    modified_second = replace_jokers(second)

    strength_first = determine_hand_strength(modified_first)
    strength_second = determine_hand_strength(modified_second)

    if strength_first < strength_second:
        return 1

    if strength_first > strength_second:
        return -1

    return has_higher_card_part_2(first, second)


def replace_jokers(hand):
    num_jokers = hand.count('J')

    if num_jokers == 0:
        return hand
    if num_jokers == 5:
        return ['A', 'A', 'A', 'A', 'A']

    hand_without_jokers = list(filter(lambda a: a != 'J', hand))

    counter = Counter(hand_without_jokers)
    num_most_common = counter.most_common(1)[0][1]
    all_most_common_elements = list(
        set([x for x in hand_without_jokers if hand_without_jokers.count(x) == num_most_common]))
    all_most_common_elements.sort(key=lambda x: strength_order.index(x))

    modified = hand[::]
    if num_jokers != 0:
        for i in range(len(modified)):
            if modified[i] == 'J':
                modified[i] = all_most_common_elements[0]
    # print(f'from {hand} to {modified}')
    return modified


def hand_comparator(first, second):
    return card_comparator(first[0], second[0])


def hand_comparator_part_2(first, second):
    return card_comparator_part_2(first[0], second[0])


def part_1(problem):
    cards_and_bids = parse_cards_and_bids(problem)
    cards_and_bids.sort(key=cmp_to_key(hand_comparator))

    idx = 1
    s = 0
    for _, bid in cards_and_bids:
        delta = bid * idx
        s += delta
        idx += 1
    return s


def part_2(problem):
    cards_and_bids = parse_cards_and_bids(problem)
    cards_and_bids.sort(key=cmp_to_key(hand_comparator_part_2))

    idx = 1
    s = 0
    for _, bid in cards_and_bids:
        delta = bid * idx
        s += delta
        idx += 1
    return s


if __name__ == '__main__':
    # print(replace_jokers(list('55JKK')))
    # print(replace_jokers(list('55AKK')))
    # print(replace_jokers(list('JJJJJ')))
    with open(input_file_name) as problem:  # 251106089
        print(part_1(problem))

    with open(input_file_name) as problem:
        print(part_2(problem))  # 250684437 too high, 250035895 too high
