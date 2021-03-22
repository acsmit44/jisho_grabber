'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for processing Jisho search results and otputting
                them in a readable and convenient way.
'''

import wx
import wx.lib.scrolledpanel
from word_grabber import WordSearch

# Needs to include word, reading, meanings, common or not, and JLPT level
class SearchFrame(wx.Frame):
    word_search = WordSearch("")
    green = (0,150,0)
    red = (255,0,0)
    meaning_num = 0

    def __init__(self):
        super().__init__(parent=None, title='Jisho Grabber', size=(700, 700))
        vert_sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        search_label = wx.StaticText(self, label='Search term:')
        self.search_field = wx.TextCtrl(self)
        self.search_button = wx.Button(self, label='Search')
        self.search_button.Bind(wx.EVT_BUTTON, self.search_word)
        hsizer_1.Add(search_label, proportion=0, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=8)
        hsizer_1.Add(self.search_field, proportion=1, flag=wx.TOP, border=8)
        hsizer_1.Add(self.search_button, proportion=0, flag=wx.TOP|wx.RIGHT, border=8)
        vert_sizer.Add(hsizer_1, flag=wx.EXPAND)

        hsizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.back_button = wx.Button(self, label='Previous result')
        self.back_button.Bind(wx.EVT_BUTTON, self.prev_result)
        self.next_button = wx.Button(self, label='Next result')
        self.next_button.Bind(wx.EVT_BUTTON, self.next_result)
        hsizer_2.Add(self.back_button, proportion=1, flag=wx.LEFT, border=8)
        hsizer_2.Add(self.next_button, proportion=1, flag=wx.RIGHT, border=8)
        vert_sizer.Add(hsizer_2, flag=wx.EXPAND)

        self.search_error = wx.StaticText(self, label='No error.')
        self.search_error.SetForegroundColour(self.green)
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.search_error.SetFont(font)
        vert_sizer.Add(self.search_error, proportion=0, flag=wx.TOP|wx.LEFT|wx.RIGHT| \
                       wx.ALIGN_CENTER_HORIZONTAL, border=8)

        vert_sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), proportion=0, \
                       flag=wx.ALL|wx.EXPAND, border=8)

        hsizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        subvert_1 = wx.BoxSizer(wx.VERTICAL)
        word_label = wx.StaticText(self, label='Word:', size=(-1, 20))
        reading_label = wx.StaticText(self, label='Reading:', size=(-1, 20))
        subvert_1.Add(word_label, 0, flag=wx.LEFT|wx.RIGHT, border=8)
        subvert_1.Add(reading_label, 0, flag=wx.LEFT|wx.RIGHT, border=8)
        hsizer_3.Add(subvert_1, proportion=0)

        subvert_2 = wx.BoxSizer(wx.VERTICAL)
        self.word_result = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        self.word_reading = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        subvert_2.Add(self.word_result, 0, flag=wx.EXPAND, border=8)
        subvert_2.Add(self.word_reading, 0, flag=wx.EXPAND, border=8)
        hsizer_3.Add(subvert_2, proportion=1, flag=wx.EXPAND)

        subvert_3 = wx.BoxSizer(wx.VERTICAL)
        jlpt_label = wx.StaticText(self, label='JLPT Level:', size=(-1, 20))
        common_label = wx.StaticText(self, label='Common word?:', size=(-1, 20))
        subvert_3.Add(jlpt_label, 0, flag=wx.LEFT|wx.RIGHT, border=8)
        subvert_3.Add(common_label, 0, flag=wx.LEFT|wx.RIGHT, border=8)
        hsizer_3.Add(subvert_3, proportion=0)

        subvert_4 = wx.BoxSizer(wx.VERTICAL)
        self.jlpt_level = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        self.common_word = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        subvert_4.Add(self.jlpt_level, 0, flag=wx.RIGHT|wx.EXPAND, border=8)
        subvert_4.Add(self.common_word, 0, flag=wx.RIGHT|wx.EXPAND, border=8)
        hsizer_3.Add(subvert_4, proportion=1, flag=wx.EXPAND)

        vert_sizer.Add(hsizer_3, flag=wx.EXPAND)

        vert_sizer.Add(wx.StaticText(self, label='Meanings:'), 0, \
                       flag=wx.LEFT, border=8)

        hsizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.meanings_body = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        hsizer_4.Add(self.meanings_body, proportion=1, flag=wx.EXPAND)
        vert_sizer.Add(hsizer_4, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, \
                       border=8)

        vert_sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, \
                       wx.ALL|wx.EXPAND, 10)

        choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        choice_label = wx.StaticText(self, label='Choose a meaning:', size=(-1, 20))
        choice_sizer.Add(choice_label, proportion=0)
        self.meaning_select = wx.Choice(self)
        self.meaning_select.Bind(wx.EVT_CHOICE, self.get_meaning_choice)
        choice_sizer.Add(self.meaning_select, proportion=0)
        vert_sizer.Add(choice_sizer, proportion=0, flag=wx.RIGHT| \
                       wx.ALIGN_CENTER_HORIZONTAL, border=8)

        hsizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self, label='Add to Deck')
        hsizer_5.Add(self.add_button, proportion=1, flag=wx.RIGHT|wx.LEFT|wx.BOTTOM, border=8)
        vert_sizer.Add(hsizer_5, flag=wx.EXPAND)

        self.add_result = wx.StaticText(self, label='')
        self.add_result.SetForegroundColour(self.green)
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.add_result.SetFont(font)
        vert_sizer.Add(self.add_result, proportion=0, flag=wx.BOTTOM| \
                       wx.ALIGN_CENTER_HORIZONTAL, border=8)

        self.SetSizer(vert_sizer)
        self.Show()
    
    def check_error(self):
        self.search_error.SetLabel(self.word_search.error_msg)
        if self.word_search.error_msg == "No error.":
            self.search_error.SetForegroundColour(self.green)
            self.set_fields()
        else:
            self.search_error.SetForegroundColour(self.red)
        self.search_error.GetContainingSizer().Layout()
        return bool(self.word_search.error_msg == "No error.")

    def set_fields(self):
        self.word_result.Clear()
        self.word_reading.Clear()
        self.jlpt_level.Clear()
        self.common_word.Clear()
        self.meanings_body.Clear()
        self.meaning_select.Clear()
        self.word_result.SetValue(self.word_search.word_dict['Word'])
        self.word_reading.SetValue(self.word_search.word_dict['Reading'])
        self.jlpt_level.SetValue(self.word_search.word_dict['JLPT'])
        self.common_word.SetValue(self.word_search.word_dict['Common'])
        for cur, meaning in enumerate(self.word_search.word_dict['Meanings']):
            if meaning['Tags'] is not None:
                self.meanings_body.AppendText("{}. {}\n".format(cur + 1, meaning['Tags']))
            self.meanings_body.AppendText("{}. {}\n\n".format(cur + 1, meaning['Meaning(s)']))
        self.meaning_select.AppendItems([str(i + 1) for i in \
            range(len(self.word_search.word_dict['Meanings']))])

    def search_word(self, event):
        self.word_search = WordSearch(self.search_field.GetValue())
        self.check_error()
    
    def next_result(self, event):
        self.word_search.next_word()
        self.check_error()
    
    def prev_result(self, event):
        self.word_search.prev_word()
        self.check_error()
    
    def get_meaning_choice(self, event):
        self.meaning_num = self.meaning_select.GetSelection()

if __name__ == '__main__':
    app = wx.App()
    frame = SearchFrame()
    app.MainLoop()
    print("Program closed.")