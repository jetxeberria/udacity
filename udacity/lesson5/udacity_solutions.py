import collections
import json
import parser

def count_unique_words(filename='hamlet.txt'):
    words = collections.Counter()
    # Extract the data into Python.
    with open(filename) as f:
        for line in f:
            words.update(line.split())

    # Calculate the ten most common words.
    for word, count in words.most_common(10):
        print(word, count)

def load_nobel_prizes(filename='prize.json'):
    with open(filename) as f:
        return json.load(f)


def select_prizes(year, category):
    data = load_nobel_prizes()
    prizes = data['prizes']

    for prize in prizes:
        if 'laureates' not in prize:
            continue
        if category and prize['category'].lower() != category.lower():
            continue
        if year and prize['year'] != year:
            continue

        print(f"{prize['year']} Nobel Prize in {prize['category'].title()}")
        for laureate in prize['laureates']:
            firstname = laureate['firstname']
            surname = laureate.get('surname', '')
            print(f"{firstname} {surname}: {laureate['motivation']}")

if __name__ == '__main__':
    count_unique_words('hamlet.txt')
    arg_parser = parser.build_parser()
    args = arg_parser.parse_args()
    select_prizes(args.year, args.category)
