from tkinter import *


class LabeledSpin(Frame):
	def __init__(self, master, var, text, width='4', interval=(1,10)):
		super().__init__(master=master)
		self.label = Label(self, text=text)
		self.spin = Spinbox(self, from_=interval[0], to=interval[1], 
						width=width, textvariable=var)

		self.label.pack(side='left')
		self.spin.pack(side='left')
