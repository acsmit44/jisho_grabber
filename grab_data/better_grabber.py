'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Class for processing Jisho search results.
'''

import sys
import requests
from bs4 import BeautifulSoup
from utils import isKana

class WordSearch:
    cur_word, max_words, page = 0, 0, 0
    word_tag, primary_tag = None, None
    all_words = []
    word_dict = {}
    error_msg = "No error."

    def __init__(self, searched_word):
        self.searched_word = searched_word.replace(' ', '%20').replace('#', '%23')
        self.next_word()
    
    def get_soup(self):
        self.page += 1
        url = "https://jisho.org/search/" + self.searched_word + '?page=' + str(self.page)
        webpage = requests.get(url)
        if webpage.status_code != 200:
            sys.exit("Error: There was an issue loading Jisho. Try again later.")
        soup = BeautifulSoup(webpage.content, "html.parser")
        return soup
    
    def check_search(self):
        if self.max_words == 0:
            results = self.get_soup()
            self.primary_tag = results.find('div', id='primary')
            if self.primary_tag is None:
                self.error_msg = 'Error: invalid search.'
            else:
                new_words = list(self.primary_tag.find_all('div', class_='concept_light clearfix'))
                self.all_words.extend(new_words)
                self.max_words += len(new_words)
        elif self.cur_word == self.max_words:
            if self.primary_tag.find('a', class_='more') is not None:
                self.primary_tag = self.get_soup().find('div', id='primary')
                new_words = list(self.primary_tag.find_all('div', class_='concept_light clearfix'))
                self.all_words.extend(new_words)
                self.max_words += len(new_words)

    def get_word_and_reading(self):
        word_info = self.word_tag.find('div', class_='concept_light-representation')
        # list comprehension to extract whole word as string
        word = "".join([text.get_text().strip() for text in
                        word_info.find_all('span', class_='text')])
        # list comprehension to extract kanji readings
        furigana = [furi.get_text().strip() for furi in \
                    word_info.find('span', class_='furigana').find_all('span')]
        if word_info.find('ruby', class_='furigana-justify') is not None:
            reading = word_info.find('ruby', class_='furigana-justify').find('rt').get_text().strip()
        else:
            reading = ""
            for cur in range(len(word)):
                # append current char if hiragana, and append kanji reading otherwise
                reading += word[cur] if isKana(word[cur]) else furigana[cur]
        self.word_dict['Word'] = word
        self.word_dict['Reading'] = reading
    
    def get_word_info(self):
        self.word_tag_info = self.word_tag.find('div', class_='concept_light-status')
        tags = [tag.get_text().strip() for tag in \
                self.word_tag_info.find_all('span', class_='concept_light-tag')]
        self.word_dict['Common'] = 'No'
        self.word_dict['JLPT'] = 'N/A'
        for tag in tags:
            if tag.find('Common') != -1:
                self.word_dict['Common'] = 'Yes'
            if tag.find('JLPT') != -1:
                self.word_dict['JLPT'] = tag.split(" ")[1][1]
    
    def get_word_meanings(self):
        meanings_dict = {}
        meanings_list = []
        meanings_info = self.word_tag.find('div', class_='meanings-wrapper')
        meanings_children = meanings_info.findChildren('div', class_='meaning-wrapper', \
                                                       recursive=False)
        for child in meanings_children:
            meaning = child.find('span', class_='meaning-meaning')
            if meaning is not None:
                meanings_dict['Meaning(s)'] = meaning.get_text().strip()
            else:
                continue
            if child.previous_sibling is not None and child.previous_sibling.has_attr('class') \
               and child.previous_sibling['class'][0] == 'meaning-tags':
                if child.previous_sibling.get_text().strip().find('Wikipedia') != -1:
                    continue
                meanings_dict['Part(s) of speech'] = child.previous_sibling.get_text().strip()
            meanings_list.append(meanings_dict)
            meanings_dict = {}
        self.word_dict['Meanings'] = meanings_list
    
    def next_word(self):
        self.error_msg = "No error."
        self.check_search()
        # increment buffer if cur_word is not pointing to the head of the array
        if self.cur_word < self.max_words:
            self.load_data()
            self.cur_word += 1
        else:
            self.error_msg = "Error: Cannot go forward."
            print(self.error_msg)
    
    def prev_word(self):
        self.error_msg = "No error."
        # decrement buffer if possible
        if self.cur_word > 0:
            self.load_data()
            self.cur_word -= 1
        else:
            self.error_msg = "Error: Cannot go back."
            print(self.error_msg)

    def load_data(self):
        self.word_dict = {}
        self.word_tag = self.all_words[self.cur_word]
        self.get_word_and_reading()
        self.get_word_info()
        self.get_word_meanings()

if __name__ == '__main__':
    # Tests attempts to go forward and backward in the search results
    jisho_word = WordSearch('taste')
    for i in range(5):
        jisho_word.next_word()
    for i in range(5):
        jisho_word.next_word()
    for i in range(3):
        jisho_word.prev_word()
    for i in range(5):
        jisho_word.next_word()
    for i in range(15):
        jisho_word.prev_word()
    for i in range(19):
        jisho_word.next_word()
    for i in range(25):
        jisho_word.next_word()
    for i in range(19):
        jisho_word.next_word()
    for i in range(19):
        jisho_word.prev_word()