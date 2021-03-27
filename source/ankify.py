'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    The description for Anki notes, models, and decks are kept
                in this file.  IDs for the various types are hard-coded and
                should not be changed.
'''

import genanki

engtojpn_front = '''<span style=" font-size: 40px;">{{Meaning}}</span>'''

engtojpn_back  = '''{{FrontSide}}

<hr id=answer>
<span style="font-size: 75px; font-family: Mincho;">{{furigana:Word}}</span><br />

<span style="font-size: 22px; ">Part(s) of speech: {{Parts of speech}}<br></span>
<span style="font-size: 22px; ">JLPT Level: {{JLPT Level}}<br></span>
<span style="font-size: 22px; color: rgb(0,200,0)">{{Common word}}</span>
<span><a  href="http://jisho.org/word/{{kanji:Word}}">Jisho reference</a></span>'''

jpntoeng_front = '''<span style=" font-size: 75px; font-family: Mincho;">{{kanji:Word}}</span>'''

jpntoeng_back  = '''<span style=" font-size: 75px; font-family: Mincho;">{{furigana:Word}}</span>

<hr id=answer>
<span style="font-size: 40px;">{{Meaning}}</span><br /><br>

<span style="font-size: 22px; ">Part(s) of speech: {{Parts of speech}}<br></span>
<span style="font-size: 22px; ">JLPT Level: {{JLPT Level}}<br></span>
<span style="font-size: 22px; color: rgb(0,200,0);">{{Common word}}</span>
<span><a  href="http://jisho.org/word/{{kanji:Word}}">Jisho reference</a></span>'''

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
    model_id=1608179351,
    name='Jisho Search Vocab',
    fields=[
        {'name': 'Word'},
        {'name': 'Meaning'},
        {'name': 'Parts of speech'},
        {'name': 'JLPT Level'},
        {'name': 'Common word'}
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
    1870039213,
    'Jisho Vocab'
)

if __name__ == '__main__':
    # Example of creating a new note
    new_note = genanki.Note(
        model=jisho_vocab,
        fields=['味覚', 'Na-adjective, Noun', '1', 'Yes']
    )

    jisho_deck.add_note(new_note)
    genanki.Package(jisho_deck).write_to_file('output.apkg')