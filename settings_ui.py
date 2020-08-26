from functools import partial
from tkinter import *
from tkinter import filedialog
import tkinter.colorchooser as cc
from pathlib import Path
import math
import json

from settings import conf as st
from labeled_textfield import LabelEntry
from label_spinbox import LabeledSpin
from var_ui_names import variable_presentation_names as ui_txt


def roundcolor(color):
	rgb = list(color[0])
	rgb[0] = math.floor(rgb[0])
	rgb[1] = math.floor(rgb[1])
	rgb[2] = math.floor(rgb[2])
	return rgb


class SettingsUI(Frame):
	def __init__(self, master):
		super().__init__(master)

		self.master = master
		self.settings = {}
		self.get_current_settings()
		self.create_specials()

		self.color_parent = Frame(self, pady=10, padx=50)
		self.int_parent = Frame(self, pady=10)
		self.bool_parent = Frame(self, pady=10)
		self.create_color_setters()
		self.create_ints()
		self.create_bools()

		# Close button
		close_btn = Button(self, text='X', fg='white', bg='red')
		close_btn.configure(command=self.exit, bd=0)
		close_btn.place(relx=0.93, rely=0.003)

		# Packing
		self.pack_all()
		self.place(relx=0.5, rely=0.5, anchor="center")

		# Special options (save and load settings)
		options = Frame(self)
		exp_btn = Button(options, text='Export settings', command=self.export)
		exp_btn.configure(fg='white', bg='black', bd=0)
		exp_btn.pack(side='left')
		exp_btn = Button(options, text='Load settings', command=self.load)
		exp_btn.configure(fg='black', bg='green', bd=0)
		exp_btn.pack(side='left')
		options.pack()

		# Styling
		for widget in self.color_widgets.values():
			widget.config(bd=0, bg='#CCC', fg='#131313')
		for widget in self.bool_widgets.values():
			widget.config(bd=0, fg='#131313')
		for widget in self.int_widgets.values():
			widget.label.config(bd=0, fg='#131313')
			widget.spin.config(fg='black', bg='#BBB')
	
	def export(self):
		self.update()
		folder = Path(Path.cwd(), 'saves')
		if not folder.exists(): folder.mkdir()

		file = filedialog.asksaveasfilename(initialdir=folder,
			title='Save settings',
			filetypes = (("JSON files", "*.json"), ("All files","*.*")))
		file = Path(file)
		file.touch()
		with file.open('w') as f:
			json.dump(st, f)

	def load(self):
		folder = Path(Path.cwd(), 'saves')
		if not folder.exists(): folder.mkdir()
		file = filedialog.askopenfilename(initialdir=str(folder),
			title='Open settings file',
			filetypes = (("JSON files", "*.json"), ("All files","*.*")))
		file = Path(file)

		settings = None
		with file.open() as f:
			settings = json.load(f)
		for key, value in settings.items():
			st[key] = value
		self.get_current_settings()
		self.update()

	def update(self):
		st['speed'] = float(self.speedvar.get())
		for key, conf in self.settings.items():
			if type(conf) is IntVar or type(conf) is BooleanVar:
				st[key] = conf.get()

	def get_current_settings(self):
		for key, config in st.items():
			if type(config) is not list:
				if type(config) is int:
					if not key in self.settings.keys():
						self.settings[key] = IntVar(self)
					self.settings[key].set(config)
				elif type(config) is bool:
					if not key in self.settings.keys():
						self.settings[key] = BooleanVar(self)
					self.settings[key].set(config)
			else:						# Color setter
				if len(config) == 3:
					self.settings[key] = config

	def create_color_setters(self):
		parent = self.color_parent
		widgets = self.color_widgets = {}
		self.color_children = self.create_wgrid(parent, widgets)

	def create_ints(self):
		parent = self.int_parent
		widgets = self.int_widgets = {}
		self.int_children = self.create_wgrid(parent, widgets)

	def create_bools(self):
		parent = self.bool_parent
		widgets = self.bool_widgets = {}
		self.bool_children = self.create_wgrid(parent, widgets)

	def create_wgrid(self, parent, widgets):
		""" Returns the frames list (each column of the grid is a widget) """
		wcount = None
		if parent == self.int_parent:
			wcount = len(list(filter(
				lambda x: type(x) is IntVar, self.settings.values())))
		elif parent == self.color_parent:
			wcount = len(list(filter(
				lambda x: type(x) is list, self.settings.values())))
		elif parent == self.bool_parent:
			wcount = len(list(filter(
				lambda x: type(x) is BooleanVar, self.settings.values())))

		# Each frame (children) is a ground of a number of wperfrm widgets
		wperfrm = math.floor( math.sqrt(wcount) )
		fcount = wcount/wperfrm
		if fcount - math.floor(fcount) > 0:
			fcount = math.ceil(fcount)
		fcount = int(fcount)
		children = [Frame(parent) for i in range(fcount)]

		
		class gridincrementer:
			""" Pretty much 2D array logic (widgets inside frames) """
			def __init__(self, w, f, wperf):
				self.w, self.f = w, f
				self.wperf = wperf
			def increment(self):
				if self.w < self.wperf:
					self.w += 1
				else: self.w, self.f = 0, self.f+1
		c = gridincrementer(0, 0, wperfrm)

		for var, conf in self.settings.items():
			if type(conf) is IntVar and parent == self.int_parent:
				if var == 'radius':
					widgets[var] = LabeledSpin(children[c.f], self.settings[var], 
						ui_txt[var], interval=(2, 512))
				else:
					widgets[var] = LabeledSpin(children[c.f], self.settings[var], ui_txt[var])
				c.increment()

			elif type(conf) is BooleanVar and parent == self.bool_parent:
				widgets[var] = Checkbutton(children[c.f], text=ui_txt[var])
				widgets[var].config(variable=self.settings[var])
				c.increment()

			elif type(conf) is list and parent == self.color_parent:
				widgets[var] = Button(children[c.f], text=ui_txt[var])
				widgets[var].config(command=partial(self.choose_color, var))
				c.increment()
		return children

	def create_specials(self):
		frm = self.global_frame = Frame(self)
		
		self.speedvar = StringVar()
		self.speedvar.set(str(st['speed']))
		self.speed_widget = LabelEntry(frm, text=ui_txt['speed'], width=4)
		self.speed_widget.entry.configure(textvariable=self.speedvar)
		
	def pack_all(self):
		self.speed_widget.pack()

		# Colors
		for widget in self.color_widgets.values():
			widget.pack(anchor='e')
		for child in self.color_children:
			child.pack(side='left')

		# Ints
		for widget in self.int_widgets.values():
			widget.pack(anchor='e')
		for child in self.int_children:
			child.pack(side='left')

		# Bools
		for widget in self.bool_widgets.values():
			widget.pack(anchor='w')
		for child in self.bool_children:
			child.pack(side='left')

		self.global_frame.pack()
		self.int_parent.pack()
		self.bool_parent.pack()
		self.color_parent.pack()

	def choose_color(self, attribute):
		chooser = cc.Chooser(master=self, initialcolor=tuple(st[attribute]))
		st[attribute] = roundcolor(chooser.show())

	def set_setting(self, attribute):
		value = self.settings[attribute].get()
		st[attribute] = value

	def exit(self):
		self.master.destroy()
		self.update()