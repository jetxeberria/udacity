from collections import defaultdict

def parse_content(content):
    parsed = {}
    lines = content.split("\n")
    parsed = {l.split(" ")[0]:int(l.split(" ")[1]) for l in lines}
    return parsed


def make_tree(words):
    pass

def predict(tree, numbers):
    pass