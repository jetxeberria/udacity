from collections import defaultdict


keymap = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def parse_content(content):
    parsed = {}
    lines = content.split("\n")
    parsed = {l.split(" ")[0]: int(l.split(" ")[1]) for l in lines}
    return parsed


def make_tree(words):
    tree = {}
    for k, v in words.items():
        subtree = tree
        for level, c in enumerate(list(k)):
            if c not in subtree:
                subtree[c] = {}
            subtree = subtree[c]
            if level == len(k) - 1:
                subtree["$" + k] = v
    return tree


def predict(trie, numbers):
    candidate_subtries = predict_numbers(trie, numbers)
    candidate_words = extract_words(candidate_subtries)
    sorted_words = sort_words(candidate_words)
    return sorted_words


def predict_numbers(trie, numbers):
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
    return candidate_subtries


def extract_words(subtries):
    words = []
    for subtrie in subtries:
        sub_words = list(words_generator(subtrie))
        if sub_words:
            words.extend(sub_words)
    return set(words)


# def words_generator(subtrie):
#     words = []
#     for k, v in subtrie.items():
#         if isinstance(v, dict):
#             yield list(words_generator(v))[0]
#         elif isinstance(v, list):
#             for g in k:
#                 yield list(words_generator(v))[0]
#         if k.startswith("$"):
#             yield (k, v)  # yield words
#
#
def words_generator(subtrie):
    words = []
    for k, v in subtrie.items():
        if isinstance(v, dict):
            for words in words_generator(v):
                yield words
        elif isinstance(v, list):
            for g in k:
                for words in words_generator(v):
                    yield words
        if k.startswith("$"):
            yield (k[1:], v)  # yield words


#

#
# def words_generator(subtrie):
# words = []
# for k, v in subtrie.items():
# if isinstance(v, dict):
# words.append(list(words_generator(v))[0])
# elif isinstance(v, list):
# for g in k:
# words.append(list(words_generator(v))[0])
# if k.startswith("$"):
# words.append((k, v))  # yield words
# return words
#
#
def sort_words(words_s):
    words = list(words_s)
    sorted_words = []
    for i in range(len(words)):
        highest = words[0]
        for word2 in words:
            if word2[1] >= highest[1] and word2 is not highest:
                highest = word2
        sorted_words.append(highest)
        words.pop(words.index(highest))
    return sorted_words
