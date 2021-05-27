from collections import defaultdict


keymap = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
    }

def parse_content(content):
    parsed = {}
    lines = content.split("\n")
    parsed = {l.split(" ")[0]:int(l.split(" ")[1]) for l in lines}
    return parsed


def make_tree(words):
    tree = {}
    for k, v in words.items():
        subtree = tree
        for level, c in enumerate(list(k)):
            if c not in subtree:
                subtree[c] = {}
            subtree = subtree[c]
            if level == len(k)-1:
                subtree['$'+k] = v
    return tree

def predict(trie, numbers):
    candidate_subtries = [trie]
    for number in str(numbers):
        match_found = False
        for k in keymap[number]:
            for i, subtrie in enumerate(candidate_subtries):
                if k == subtrie:
                    candidate_subtries.append(subtrie[k])
                    candidate_subtries.pop(i)
                    match_found = True
        if not match_found:
            candidate_subtries.clear()
    candidate_words = extract_words(candidate_subtries)
    sorted_words = sort_words(candidate_words)
    return candidate_words


def extract_words(subtries):
    words = []
    for subtrie in subtries:
        sub_words = list(words_generator(subtrie))
        if sub_words:
            words.append(sub_words)
    return words

def words_generator(subtrie):
    for k, v in subtrie.items():
        if k.startswith("$"):
            yield (k, v)
        else:
            subtrie = words_generator(v)
    return


def sort_words(words):
    highest = words[0]
    sorted_words = []
    for word in words:
        for word2 in words:
            if word2[1] >= highest[1] and word2[0] != highest[0]:
                highest = word2
        sorted_words.append(highest)
    return sorted_words
