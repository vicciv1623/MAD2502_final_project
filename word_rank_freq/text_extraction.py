import re
import numpy as np
import matplotlib.pyplot as plt

def word_freq_pairs(file_name : str) -> dict:
    """Finds the frequencies of each word in a file

    Parameters: file_name
    the text to be analyzed

    Returns: dict
    dictionary of word-frequency pairs
    """
    with open(file_name, 'r') as f:
        d = dict()
        text = re.sub("[^a-zA-Z ]", '', f.read())
        for line in text.split():
           if line in d:
               d[line] += 1
           else: d[line] = 1


    return d

def word_frequencies(word_freq_pairs : dict) -> np.ndarray:
    """The numerical word frequencies of each word in a file"""
    freqs = np.array(sorted(word_freq_pairs.values(), reverse = True))
    return freqs

def zipf_expected_freqs(file_name: str) -> np.ndarray:
    """Calculates the expected frequencies of words in a text if their distribution follows Zipf's Law

    Parameters: text_file
    the text to be analyzed

    Returns: np.ndarray
    the expected frequencies of words
    """

    word_freqs = word_freq_pairs(file_name)
    unique_words = len(word_frequencies(word_freqs))
    ranks = np.arange(1, unique_words + 1)
    const = np.sum(1.0 / ranks)
    norm = unique_words / const #need to normalize for zipf
    return norm / ranks

def word_count(file_name: str) -> int:
    """Counts words in a text"""
    with open(file_name, 'r') as f:
        text = re.sub("[^a-zA-Z ]", '', f.read())
        count = 0
        for word in text.split():
            count += 1

    return count

def plot_zipf(text_file: str):
    """Plots actual distribution of word frequencies in a text file versus expected frequencies
    on a loglog plot

    Parameters: text_file
    the text to be analyzed

    Returns: matplotlib plot
    """
    empirical_freqs = word_frequencies(word_freq_pairs(text_file))
    expected_freqs = zipf_expected_freqs(text_file)
    ranks = np.arange(1, len(empirical_freqs) + 1)
    plt.loglog(ranks, empirical_freqs, color = 'r', label = "Actual")
    plt.loglog(ranks, expected_freqs, color = 'b', label = "Expected")
    plt.xlabel("Log Rank")
    plt.ylabel("Log Frequency")
    plt.legend()
    plt.title(f"Zipf's Law with {text_file[:-4]}")
    plt.grid(True, which = "both", ls = "--", alpha = 0.5)
    plt.show()













