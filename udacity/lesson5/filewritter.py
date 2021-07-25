import string
import json
import csv

def write_json(filename, contents):
    with open(filename, "w") as f:
        json.dump(contents, f, indent=2)
        
# def write_csv(filename, contents, header=False):

