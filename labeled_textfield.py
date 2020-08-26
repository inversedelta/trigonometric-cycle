from tkinter import *


class LabelEntry(Frame):
	def __init__(self, master, text, width):
		super().__init__(master=master)
		self.label = Label(self, text=text)
		self.label.pack(side='left')
		self.entry = Entry(self, width=width)
		self.entry.pack(side='left')

