'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for processing Jisho search results and otputting
                them in a readable and convenient way.
'''

import json
import os
from word_grabber import WordSearch

jsonpath = os.path.join(os.getcwd(), 'grab_data', 'vocab_words.json')

print(os.path.exists(jsonpath))
if not os.path.exists(jsonpath):
    with open(jsonpath, 'w') as outfile:
        json.dump([], outfile, indent=2)

with open(jsonpath, 'r') as infile:
    data = json.load(infile)

jisho_search = WordSearch('taste')

with open(jsonpath, 'w') as outfile:
    json.dump(data, outfile, indent=2)