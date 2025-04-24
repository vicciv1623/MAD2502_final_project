import math

def get_digit_frequencies(filename: str, digits: list) -> dict:
    """Returns a dictionary with the leading digits (passed in as list) as keys and their frequencies as values."""
    file = open(filename, 'r')
    str_list = []
    while str_list := file.readlines():
        pass
    ret_dict = dict()
    for digit in digits:
        ret_dict[digit] = 0
    for line in str_list:
        ret_dict[line[0]] += 1
    return ret_dict

def get_digit_proportions(filename: str) -> dict:
    """Returns a dictionary with the leading digits as keys and their proportions as values."""
    frequencies = get_digit_frequencies(filename)
    total = sum(frequencies.values())
    ret_dict = dict()
    for key, value in frequencies.items():
        ret_dict[key] = value / total
    return ret_dict

def get_expected_frequencies(digits: list) -> dict:
    """Returns a dictionary with the digits as keys and their expected frequencies as leading digits as values."""
    expected_dict = dict()
    for index, digit in enumerate(digits):
        expected_dict[digit] = math.log(1 + 1/index, len(digits))
    return expected_dict