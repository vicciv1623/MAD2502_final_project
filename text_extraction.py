import re

def text_extraction(file_name : str, new_file_name : str):
    """Extracts all non-numerical text from a plain text file"""
    with open(file_name, 'r') as f:
        text = re.findall("[^\d]*", f.read()) #excludes digits
    return open(f"{new_file_name}.txt", text)

def word_frequencies(file_name : str) -> list[tuple(str, int)]:
    """Finds the frequencies of each word in a file"""
    with open(file_name, 'r') as f:
        d = dict()
        text = re.sub("[^a-zA-Z ]", '', f.read())
        for line in text.split():
           if line in d:
               d[line] += 1
           else: d[line] = 1


    return [(key, value) for key, value in d.items()]







