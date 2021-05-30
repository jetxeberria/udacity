import operator
import collections
import functools

def parse_content(content):
    words = {}
    for line in content.split('\n'):
        word, frequency = line.split()
        words[word] = int(frequency)
    return words

def node():
    return collections.defaultdict(node)

def make_tree(words):
    trie = node()
    for word, frequency in words.items():
        functools.reduce(defaultdict.__getitem__, word, trie)['$'] = (word, frequency)
    return trie


def predict(tree, numbers):
    leaves = [tree]
    for number in numbers:
        leaves = [leaf[letter] for letter in keymap[number] for leaf in leaves if letter in leaf]

    words = {}
    for node in leaves:
        words.update(get_leaves(node))

    return sorted(words.items(), key=operator.itemgetter(1), reverse=True)

def get_leaves(node):
    """Get "leaf" nodes from an internal node – a leaf node starts with '$' and has an integer value."""
    leaves = {}
    for label, child in node.items():
        if not isinstance(child, dict):  # We found a word!
            leaves[label[1:]] = child  # Strip the leading '$'
            continue
        leaves.update(get_leaves(child))  # Recurse on the children.
    return leaves