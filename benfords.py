import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import sys

def get_digit_frequencies(filename: str, digits: list) -> list:
    """Returns a list of the frequencies of each digit as a leading digit in the file with their indices corresponding to the indices of the digits in the "digits" list."""
    if filename.endswith('.csv'):
        try:
            with open(filename, 'r') as file:
                str_list = list(csv.reader(file))
                frequencies = [0] * len(digits)
                for str in str_list:
                    for line in str:
                        frequencies[digits.index(line[0])] += 1
        except FileNotFoundError:
            print("File not found!")
    else:
        raise ValueError('File must be .csv')
    return frequencies

def get_digit_proportions(filename: str, digits: list) -> list:
    """Returns a list of the proportions that each digit appears as a leading digit."""
    frequencies = get_digit_frequencies(filename, digits)
    proportions = []
    total = sum(frequencies)
    for frequency in frequencies:
        proportions += [frequency / total]
    return proportions

def get_expected_proportions(digits: list) -> list:
    """Returns a list of the expected proportions for when each digit should appear as a leading digit."""
    expected_proportions = []
    for index, digit in enumerate(digits):
        expected_proportions += [math.log(1 + 1/(index + 1), len(digits) + 1)]
    return expected_proportions

def get_digits(base: int):
    """Returns a list of all digits in base."""
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
    return digits[:base - 1]

def main():
    if len(sys.argv) > 3:
        raise Exception("You added too many arguments. Please provide only one file path!")
    if not 2 <= int(sys.argv[2]) <= 36:
        raise Exception("Cannot support number system.")
    digits = get_digits(int(sys.argv[2]))
    actual_proportions = get_digit_proportions(sys.argv[1], digits)
    expected_proportions = get_expected_proportions(digits)
    plt.bar(digits, actual_proportions, align='center', color = 'red')
    plt.plot(range(len(digits)), expected_proportions, color = 'blue')
    plt.plot(range(len(digits)), expected_proportions, 'o', color='blue')
    plt.title(f"Distribution of Leading Digits in {sys.argv[1]}")
    plt.xlabel("Digit")
    plt.ylabel("Proportion")
    plt.show()

if __name__ == "__main__":
	main()