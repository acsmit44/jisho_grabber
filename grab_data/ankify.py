'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    The description for Anki notes, models, and decks are kept
                in this file.  IDs for the various types are hard-coded and
                should not be changed.
'''

import genanki

engtojpn_front = '''<span style=" font-size: 25px;  ">{{Meaning}}</span>'''

engtojpn_back  = '''{{FrontSide}}

<hr id=answer>
<span style="font-size: 100px; font-family: Mincho;">{{Word}}</span><br>
<span style="font-size: 32px; ">{{Reading}}<br /><br></span>

<span style="font-size: 22px; ">Parts of speech: {{Parts of speech}}<br></span>
<span style="font-size: 22px; ">JLPT Level: N{{JLPT Level}}<br></span>
<span><a  href="http://jisho.org/word/{{Word}}">Jisho</a></span>'''

jpntoeng_front = '''<span style=" font-size: 25px;  ">{{Word}}</span>'''

jpntoeng_back  = '''{{FrontSide}}

<hr id=answer>
<span style="font-size: 50px; font-family: Mincho;">{{Meaning}}</span><br>
<span style="font-size: 32px; ">{{Reading}}<br /><br></span>

<span style="font-size: 22px; ">Parts of speech: {{Parts of speech}}<br></span>
<span style="font-size: 22px; ">JLPT Level: N{{JLPT Level}}<br></span>
<span><a  href="http://jisho.org/word/{{Word}}">Jisho reference</a></span>'''

CSS = '''.card {
 font-family: Arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.reading {
  text-align: left;
}'''

jisho_vocab = genanki.Model(
    1568352783,
    'Japanese Vocab',
    fields=[
        {'name': 'Word'},
        {'name': 'Reading'},
        {'name': 'Meaning'},
        {'name': 'Parts of speech'},
        {'name': 'JLPT Level'}
        # Add common word
    ],
    templates=[
        {
            'name': 'Eng -> Jpn',
            'qfmt': engtojpn_front,
            'afmt': engtojpn_back
        },
        {
            'name': 'Jpn -> Eng',
            'qfmt': jpntoeng_front,
            'afmt': jpntoeng_back
        },
    ],
    css=CSS,
)

jisho_deck = genanki.Deck(
    1457351146,
    'Jisho Vocab'
)

# Example of creating a new note
new_note = genanki.Note(
    model=jisho_vocab,
    fields=['味覚', 'みかく', 'taste; palate; sense of taste', 'Na-adjective, Noun', '1']
)

jisho_deck.add_note(new_note)
genanki.Package(jisho_deck).write_to_file('output.apkg')