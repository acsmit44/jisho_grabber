from bs4 import BeautifulSoup
import json
import re
import os
import sys

def make_new_word(word_info):
    left = 0
    right = 0
    word_info = word_info.replace("<br>", "")
    word_info = word_info.replace("<ruby>", "")
    word_info = word_info.replace("</ruby>", "")
    word_info = word_info.replace("<rb>", "")
    word_info = word_info.replace("</rb>", "")
    word_info = word_info.replace("<rt>", "[")
    word_info = word_info.replace("</rt>", "]")
    word_info = re.sub(".\[[^\[\]]+\]", lambda m: " " + m.group(), word_info)
    if len(word_info) > 0 and word_info[0] == " ":
        word_info = word_info[1:]
    word_info = word_info.replace("[]", "")
    return word_info

if __name__ == '__main__':
    # get paths for file dumping and make sure they exist
    dumpsdir = os.path.join(os.getcwd(), 'vocab_dumps')
    if not os.path.isdir(dumpsdir):
        sys.exit("Error: vocab_dumps folder is missing or you are in the wrong" +\
                 "directory.  Please try again.")
    jsonloadpath = os.path.join(dumpsdir, 'vocab_words.json')
    jsondumppath = os.path.join(dumpsdir, 'new_words.json')

    # load existing vocab words
    with open(jsonloadpath, 'r') as infile:
        print("Loading json...")
        old_vocab = json.load(infile)
        print("Finished loading json.")
    
    new_words = []

    for word in old_vocab:
        make_new_word(word[1])
        this_word = [make_new_word(word[1])]
        this_word.extend(word[2:])
        new_words.append(this_word)

    with open(jsondumppath, 'w') as outfile:
        print("Dumping words into json...")
        json.dump(new_words, outfile, indent=2)
        print("Json has taken a dump.  Or been dumped or whatever")
