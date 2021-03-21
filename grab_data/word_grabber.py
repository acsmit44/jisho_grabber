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
    cur_search, cur_word, max_words, page = 0, -1, 0, 1
    word_tag, primary_tag = None, None
    word_dict = {}
    word_buffer = []

    def __init__(self, searched_word):
        self.searched_word = searched_word.replace(' ', '%20').replace('#', '%23')
        results = self.get_soup("https://jisho.org/search/")
        self.primary_tag = results.find('div', id='primary')
        self.word_tag = self.primary_tag
        self.process_next_word()
    
    def get_soup(self, url):
        url = url + self.searched_word + '?page=' + str(self.page)
        self.page += 1
        webpage = requests.get(url)
        if webpage.status_code != 200:
            sys.exit("Error: There was an issue loading Jisho. Try again later.")
        soup = BeautifulSoup(webpage.content, "html.parser")
        return soup

    def next_word(self):
        if self.primary_tag is None:
            print("Error: Invalid search")
        elif self.word_tag is None:
            if self.primary_tag.find('a', class_='more') is not None:
                self.primary_tag = self.get_soup("https://jisho.org/search/")
                self.word_tag = self.primary_tag.find('div', class_='concept_light clearfix')
            else:
                print("Error: No more words")
        else:
            self.word_tag = self.word_tag.find_next('div', class_='concept_light clearfix')
        not_none = bool(self.word_tag)
        self.max_words += 1 & not_none
        self.cur_word += 1 & not_none
        return not_none

    def get_word_and_reading(self):
        word_info = self.word_tag.find('div', class_='concept_light-representation')
        # list comprehension to extract whole word as string
        word = "".join([text.get_text().strip() for text in
                        word_info.find_all('span', class_='text')])
        # list comprehension to extract kanji readings
        furigana = [furi.get_text().strip() for furi in \
                    word_info.find('span', class_='furigana').find_all('span')]
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
        self.word_dict['Common word'] = 'No'
        self.word_dict['JLPT'] = 'N/A'
        for tag in tags:
            if tag.find('Common word') != -1:
                self.word_dict['Common word'] = 'Yes'
            if tag.find('JLPT') != -1:
                self.word_dict['JLPT'] = tag.split(" ")[1][1]
    
    def get_word_meanings(self):
        meanings_info = self.word_tag.find('div', class_='meanings-wrapper')
        meaning_tags = [tag.get_text().strip() for tag in \
                        meanings_info.find_all('div', class_='meaning-tags')]
        meanings = [tag.get_text().strip() for tag in \
                    meanings_info.find_all('span', class_='meaning-meaning')]
        meanings_list = []
        for cur in range(len(meanings)):
            # ignore wikipedia definitions
            # TODO: Fix this since there will not always be as many meanings as tags
            if meaning_tags[cur].find('Wikipedia') != -1:
                continue
            meanings_list.append({'Part(s) of speech' : meaning_tags[cur], \
                                  'Meaning(s)' : meanings[cur]})
        self.word_dict['Meanings'] = meanings_list
    
    def process_next_word(self):
        # increment buffer if cur_word is not pointing to the head of the array
        if self.cur_word < self.max_words - 1:
            self.cur_word += 1
            self.word_dict = self.word_buffer[self.cur_word]
        # process a new word otherwise
        else:
            new_word = self.next_word()
            if new_word:
                self.word_dict = {}
                self.get_word_and_reading()
                self.get_word_info()
                self.get_word_meanings()
                self.word_buffer.append(self.word_dict)
    
    def go_back(self):
        # decrement buffer if possible
        if self.cur_word > 0:
            self.cur_word -= 1
            self.word_dict = self.word_buffer[self.cur_word]
        else:
            print("Error: Cannot go back.")

# Tests attempts to go forward and backward in the search results
jisho_word = WordSearch('taste')
for i in range(5):
    jisho_word.process_next_word()
for i in range(5):
    jisho_word.process_next_word()
for i in range(3):
    jisho_word.go_back()
for i in range(5):
    jisho_word.process_next_word()
for i in range(15):
    jisho_word.go_back()
for i in range(19):
    jisho_word.process_next_word()
for i in range(3):
    jisho_word.process_next_word()