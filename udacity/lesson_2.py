from collections import defaultdict


def swap_keys_and_values(d):
    new = {}
    for k,v in d.items():
        if is_iterable(v):
            for subv in v:
                if subv not in new:
                    new[subv] = set()
                new[subv].add(k)    
        else:
            if v not in new:
                new[v] = set()
            new[v].add(k)
    return new

def flatten_sequence(seq):
    flatten = []
    if is_iterable(seq):
        for s in seq:
            if is_iterable(s):
                for i in range(len(list(s))):
                    flatten.append(list(s)[i])
            else:
                flatten.append(s)
    return flatten

def is_iterable(item):
    try:
        iterator = iter(item)
    except TypeError:
        return False
    else:
        return True

def find_anagrams(letters, words):
    all_anagrams = group_anagrams(words)
    return all_anagrams.get(letters, set())
    # Analogous to below lines:
    # for canonical, anagram in all_anagrams.items():
    #     if set(letters) == set(canonical):
    #         return anagram
    # return set()

def group_anagrams(words):
    anagrams = {}
    for word in words:
        canonical = build_canonical(word)
        if canonical not in anagrams:
            anagrams[canonical] = set()
        anagrams[canonical].add(word)
    return anagrams

def group_anagrams_udacity(words):
    anagrams = defaultdict(set, {})  # Create a dictionary subclass that adds sets for missing values.
    for word in words:
        anagrams[''.join(sorted(word))].add(word)
    return anagrams

def build_canonical(word):
    chars = list(set(word))
    chars.sort()
    return ''.join(chars)

def find_anagrams_udacity_solution(letters, words):
    # Create a dictionary mapping the canonical representation of a word to all anagrams of those letters.
    lookup = {}
    for word in words:
        key = ''.join(sorted(word))
        if key not in lookup:
            lookup[key] = set()
        lookup[key].add(word)

    # Search the lookup table for the queried letters.
    search = ''.join((sorted(letters)))
    return lookup.get(search, set())