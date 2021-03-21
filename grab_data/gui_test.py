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
        super().__init__(parent=None, title='Jisho Grabber')
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        # panel1 = wx.Panel(self)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # vert_sizer = wx.BoxSizer(wx.VERTICAL)
        # panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(-1, 400), style=wx.SIMPLE_BORDER)
        # panel.SetupScrolling()

        self.search_field = wx.TextCtrl(self)
        self.search_button = wx.Button(self, label='Search')
        self.add_button = wx.Button(self, label='Add to Deck')

        top_sizer.Add(self.search_field, 1)
        top_sizer.Add(self.search_button, 0)
        # middle_sizer.Add(panel)
        # vert_sizer.Add(top_sizer)
        # vert_sizer.Add(middle_sizer)
        self.SetSizer(top_sizer)
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = SearchFrame()
    app.MainLoop()
    print("Done")