'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for taking in user input via the GUI and outputting
                an Anki deck and json with all word information.
'''

import sys
import json
import os
import wx
import genanki
from word_grabber import WordSearch
from search_gui import SearchFrame
from ankify import jisho_vocab, jisho_deck

if __name__ == '__main__':
    dumpsdir = os.path.join(os.getcwd(), 'vocab_dumps')
    if not os.path.isdir(dumpsdir):
        sys.exit("Error: vocab_dumps folder is missing or you are in the wrong" +\
                 "directory.  Please try again.")
    jsonpath = os.path.join(dumpsdir, 'vocab_words.json')
    ankipath = os.path.join(dumpsdir, 'jisho_search_deck.apkg')

    # create json if none exists
    if not os.path.exists(jsonpath):
        with open(jsonpath, 'w') as outfile:
            json.dump([], outfile, indent=2)

    # load existing vocab words
    with open(jsonpath, 'r') as infile:
        print("Loading json...")
        all_vocab = json.load(infile)
        print("Finished loading json.")

    # run gui
    app = wx.App()
    frame = SearchFrame()
    app.MainLoop()

    all_vocab.extend(frame.fields_list)
    for note_fields in all_vocab:
        new_note = genanki.Note(
            model=jisho_vocab,
            fields=note_fields
        )
        jisho_deck.add_note(new_note)
    if len(all_vocab) > 0:
        genanki.Package(jisho_deck).write_to_file(ankipath)

    with open(jsonpath, 'w') as outfile:
        print("Dumping words into json...")
        json.dump(all_vocab, outfile, indent=2)
        print("Json has taken a dump.  Or been dumped or whatever")