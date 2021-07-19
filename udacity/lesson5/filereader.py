import string
import json
import csv

from collections import Counter

def plain_read(filename):
    with open(filename, "r") as f:
        contents = f.read()
    return contents

def read_in_lines(filename):
    with open(filename, "r") as f:
        contents = []
        for line in f:
            contents.append(line)
    return contents

def count_words(filename, num=None):
    contents = plain_read(filename)
    words = extract_words(contents)
    count = Counter(words)
    words_count = dict(count.items())
    if num:
        words_selection = {k:v for k,v in count.most_common(num)}
    else:
        words_selection = words_count
        
    return words_selection

def extract_words(contents):
    purged_contents = remove_punctuation(contents)
    words = split_in_words(purged_contents)
    return words

def split_in_words(contents):
    lines = contents.split("\n")
    words = [
        word.strip().lower()
        for words in map(str.split, lines)
        for word in words
        ]
    return words

def remove_punctuation(contents):
    to_discard = string.punctuation
    return contents.translate(str.maketrans("", "", to_discard))

def read_json(filename):
    with open(filename, "r") as f:
        contents = json.load(f)
    return contents

def read_csv(filename, header=False):
    with open(filename, 'r') as f:
        contents = []
        if header:
            reader = csv.DictReader(f)
            contents = list(reader)
        else:
            reader = csv.reader(f)                
            for line in reader:
                contents.append(line)
    return contents