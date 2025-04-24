def get_digit_frequencies(filename) -> dict:
    """Returns a dictionary with the leading digits as keys and their frequencies as values."""
    file = open(filename, 'r')
    str_list = []
    while str_list := file.readlines():
        pass
    ret_dict = dict()
    for line in str_list:
        if not ret_dict[line[0]]:
            ret_dict[line[0]] = 0
        ret_dict[line[0]] += 1
    return ret_dict

def get_digit_proportions(filename) -> dict:
    """Returns a dictionary with the leading digits as keys and their proportions as values."""
    frequencies = get_digit_frequencies(filename)
    total = sum(frequencies.values())
    ret_dict = dict()
    for key, value in frequencies.items():
        ret_dict[key] = value / total
    return ret_dict