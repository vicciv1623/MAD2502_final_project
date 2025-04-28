import re
import scipy.stats as stats

def word_frequencies(file_name : str):
    """Finds the frequencies of each word in a file

    Parameters:
        file_name (str): The file

    Returns:
        list[tuple(str, int)]: A list of word-frequency tuples

    """
    with open(file_name, 'r') as f:
        d = dict()
        text = re.sub("[^a-zA-Z ]", '', f.read())
        for line in text.split():
           if line in d:
               d[line] += 1
           else: d[line] = 1


    return list(d)

def word_proportions(file_name : str):
    """Finds the proportion of each word in a text file

    Parameters: file_name (str): The file

    Returns: list[tuple(str, float)]: A list of word-proportion tuples

    """
    word_freqs = dict(word_frequencies(file_name))
    with open(file_name, 'r') as f:
        text = re.sub("[^a-zA-Z ]", '', f.read())
        count = 0
        for word in text.split():
            count += 1
        for value in word_freqs.values():
            value = value / count

    return list(word_freqs)













