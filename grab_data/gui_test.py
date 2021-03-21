'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for processing Jisho search results and otputting
                them in a readable and convenient way.
'''

import wx
import wx.lib.scrolledpanel

# Needs to include word, reading, meanings, common or not, and JLPT level
class SearchFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Jisho Grabber', size=(600,600))

        vert_sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        search_label = wx.StaticText(self, label='Search term:')
        search_field = wx.TextCtrl(self)
        search_button = wx.Button(self, label='Search')
        add_button = wx.Button(self, label='Add to Deck')
        hsizer_1.Add(search_label, proportion=0, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=8)
        hsizer_1.Add(search_field, proportion=1, flag=wx.TOP, border=8)
        hsizer_1.Add(search_button, proportion=0, flag=wx.TOP, border=8)
        hsizer_1.Add(add_button, proportion=0, flag=wx.RIGHT|wx.TOP, border=8)
        vert_sizer.Add(hsizer_1, flag=wx.EXPAND)

        hsizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        back_button = wx.Button(self, label='Previous result')
        next_button = wx.Button(self, label='Next result')
        hsizer_2.Add(back_button, proportion=1, flag=wx.LEFT, border=8)
        hsizer_2.Add(next_button, proportion=1, flag=wx.RIGHT, border=8)
        vert_sizer.Add(hsizer_2, flag=wx.EXPAND)

        vert_sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 10)

        hsizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        subvert_1 = wx.BoxSizer(wx.VERTICAL)
        word_label = wx.StaticText(self, label='Word:', size=(-1, 20))
        reading_label = wx.StaticText(self, label='Reading:', size=(-1, 20))
        subvert_1.Add(word_label, 0, flag=wx.LEFT, border=8)
        subvert_1.Add(reading_label, 0, flag=wx.LEFT, border=8)
        hsizer_3.Add(subvert_1, proportion=0)

        subvert_2 = wx.BoxSizer(wx.VERTICAL)
        word_reading = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        word_result = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        subvert_2.Add(word_reading, 0, flag=wx.EXPAND, border=8)
        subvert_2.Add(word_result, 0, flag=wx.EXPAND, border=8)
        hsizer_3.Add(subvert_2, proportion=1, flag=wx.EXPAND)

        subvert_3 = wx.BoxSizer(wx.VERTICAL)
        jlpt_label = wx.StaticText(self, label='JLPT Level:', size=(-1, 20))
        common_label = wx.StaticText(self, label='Common word?:', size=(-1, 20))
        subvert_3.Add(jlpt_label, 0, border=8)
        subvert_3.Add(common_label, 0, border=8)
        hsizer_3.Add(subvert_3, proportion=0)

        subvert_4 = wx.BoxSizer(wx.VERTICAL)
        jlpt_level = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        common_word = wx.TextCtrl(self, style=wx.TE_READONLY, size=(-1, 20))
        subvert_4.Add(jlpt_level, 0, flag=wx.RIGHT|wx.EXPAND, border=8)
        subvert_4.Add(common_word, 0, flag=wx.RIGHT|wx.EXPAND, border=8)
        hsizer_3.Add(subvert_4, proportion=1, flag=wx.EXPAND)

        vert_sizer.Add(hsizer_3, flag=wx.EXPAND)

        self.SetSizer(vert_sizer)
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = SearchFrame()
    app.MainLoop()
    print("Done")