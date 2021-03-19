'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for processing Jisho search results and otputting
                them in a readable and convenient way.
'''

import json
from grabber import process_search_results

with open('vocab_words.json', 'r') as infile:
    data = json.load(infile)

data.append(process_search_results('cool')[0])

with open('vocab_words.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)