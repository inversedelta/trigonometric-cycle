from math import *
import pygame as p
import tkinter as tk
import sys

from settings_ui import SettingsUI


def event_handler(settings_button):
	for event in p.event.get():
		if event.type == p.QUIT:
			sys.exit()
		if event.type == p.KEYDOWN:
			if event.key == p.K_ESCAPE:
				sys.exit()
		elif event.type == p.MOUSEBUTTONDOWN:
			if event.button == 1:
				if settings_button.rect.collidepoint(p.mouse.get_pos()):
					open_settings()

def open_settings():
	root = tk.Tk()
	root.geometry("700x430")
	root.title("Settings")
	root.wm_attributes('-type', 'splash')
	ui = SettingsUI(root)
	root.mainloop()

def color_transition(start, end, percent):
	""" Goes from a start color to an end color, by a percent of the difference """
	r0, g0, b0 = start[0], start[1], start[2]
	r1, g1, b1 = end[0], end[1], end[2]

	newr = abs(round( (r1 - r0) * percent + r0 ))
	newg = abs(round( (g1 - g0) * percent + g0 ))
	newb = abs(round( (b1 - b0) * percent + b0 ))

	color = [newr, newg, newb]
	for i, k in enumerate(color.copy()):
		if abs(k) > 255:
			color[i] = 255

	return (color)


def rad2deg(rad):
	return 180 * rad / pi
def deg2rad(deg):
	return pi * deg / 180

def sindeg(deg):
	return sin(deg2rad(deg))
def cosdeg(deg):
	return cos(deg2rad(deg))
def tandeg(deg):
	return tan(deg2rad(deg))


def delta_axes(a, b):
	x = abs( b[0] - a[0] )
	y = abs( b[1] - a[1] )
	return x, y

def calc_dist(a, b):
	x, y = delta_axes(a, b)
	return (x**2 + y**2)//2

def calc_angle(a, b, corner):
	""" Angle (0 <= a <= 360) to the corner """
	x, y = delta_axes(a, b)
	angle = 0
	if x != 0:
		angle = rad2deg( atan(y/x) )	# 0 <= angle < 90
	else:
		angle = 90

	# Find the full angle, to 360 degrees
	if corner == 'tl':		#2 quadrant
		angle = 180 - angle
	elif corner == 'bl':	#3
		angle = 180 + angle
	elif corner == 'br': 	#4
		angle = 360 - angle

	return angle


def calc_oposite(coside, coangle):
	""" (deg) Uses the tangent to find the oposite side of a rect triangle (sin side) """
	oposite = coside * tan(deg2rad(coangle))
	return oposite


def project_angle(mypos, target, angle, quadrant):
	""" Draws a line from a point to the target rect at a given angle (degrees) """

	# Rect corner points
	corners = {
		'tl' : (target.left, target.top),
		'tr' : (target.right, target.top),
		'bl' : (target.left, target.bottom),
		'br' : (target.right, target.bottom),
	}

	# Angle between the horizontal and the distance line to the corners
	corner_angles = {}
	for key, value in corners.items():
		corner_angles[key] = calc_angle(mypos, value, key)

	dx = dy = x = y = None
	if 		corner_angles['tr'] <= angle <= corner_angles['tl'] or \
			corner_angles['bl'] <= angle <= corner_angles['br']:
		if angle <= 90 or (180 < angle < 270):
			y = target.top
			dy = mypos[1] - y
			dx = calc_oposite(dy, 90 - angle)
			x = target.centerx + dx
		elif angle <= 180 or angle >= 270:
			y = target.bottom
			dy = mypos[1] - y
			dx = calc_oposite(dy, 90 - angle)
			x = target.centerx + dx

	elif 	corner_angles['tr'] >= angle or \
			angle >= corner_angles['br'] or \
			corner_angles['tl'] <= angle <= corner_angles['bl']:

		x = target.right
		dx = x - mypos[0]
		dy = calc_oposite(dx, -angle)
		y = target.centery + dy

	return (x, y)


# f.variation = lambda a, f: (1-a) + a * abs(f(d_timerad))**3
def variation(intensity, func, value):
	""" Returns (constant + variable): intensity is how much percent of 
		the output of a function is returned. """
	""" <Func> is a function of <value>, and has to return a percentage """
	return (1-intensity) + intensity * abs(func(value))**4