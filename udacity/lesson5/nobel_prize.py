import json

import parser


def load_nobel_prizes(filename='prize.json'):
    with open(filename, 'r') as f:
        contents = json.load(f)
    return contents["prizes"]


def filter_prizes(prizes, fields):
    if fields:
        filtered = list(filter(lambda x: all([x[k] == str(v) for k,v in fields.items()]), prizes))
    else:
        filtered = prizes
    return filtered
    

def select_prizes(year=None, category=None, filename='prizes.json'):
    prizes = load_nobel_prizes(filename)
    fields = {}
    if year:
        fields["year"] = year
    if category:
        fields["category"] = category
    filtered = filter_prizes(prizes, fields)
    return filtered

def main(year=None, category=None):
    prizes = select_prizes(year, category)
    return prizes


if __name__ == '__main__':
    arg_parser = parser.build_parser()
    args = arg_parser.parse_args()
    main(args.year, args.category)

