'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for processing Jisho search results and otputting
                them in a readable and convenient way.
'''

import json
import os
import wx
import genanki
from word_grabber import WordSearch
from search_gui import SearchFrame
from ankify import jisho_vocab, jisho_deck

if __name__ == '__main__':
    jsonpath = os.path.join(os.getcwd(), 'grab_data', 'vocab_words.json')

    if not os.path.exists(jsonpath):
        print("Creating vocab_words.json...")
        with open(jsonpath, 'w') as outfile:
            json.dump([], outfile, indent=2)

    with open(jsonpath, 'r') as infile:
        all_vocab = json.load(infile)

    app = wx.App()
    frame = SearchFrame()
    app.MainLoop()

    for new_note_fields in frame.fields_list:
        new_note = genanki.Note(
            model=jisho_vocab,
            fields=new_note_fields
        )
        jisho_deck.add_note(new_note)
    if len(frame.fields_list) > 0:
        genanki.Package(jisho_deck).write_to_file('output.apkg')
        all_vocab.extend(frame.fields_list)

    with open(jsonpath, 'w') as outfile:
        json.dump(all_vocab, outfile, indent=2)