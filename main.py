""" This is supposed to be executed """

import pygame as p
import sys
from math import *

from settings_button import SettingsButton
from settings import conf as s
import functions as f


p.init()
p.display.set_caption("Trigonometric cycle")
screen = p.display.set_mode((1000, 600))

rct = screen.get_rect()
settings_button = SettingsButton(screen, 'Settings', (200, 200, 200))


while True:
	f.event_handler(settings_button)
	screen.fill(s['bgklr'])
	settings_button.draw()
	
	# VARIABLES
	#-------------------------------------------------------------
	radius = s['radius']
	speed = s['speed']
	time = p.time.get_ticks()/1000		# in seconds

	radians = (speed * time) % (2*pi)
	angle = f.rad2deg(radians)
	radial_point = (
		s['circlepos'][0] + round(radius*cos(radians)), 
		s['circlepos'][1] - round(radius*sin(radians)) )
	#-------------------------------------------------------------

	
	# Co-Secant space fill
	sec = s['circlepos'][0] + radius/f.cosdeg(angle)
	cosec = s['circlepos'][1] - radius/f.sindeg(angle)
	if s['cossecfill']:
		p.draw.polygon(screen, s['cossecfillklr'], 
			(s['circlepos'], (sec, s['circlepos'][1]), (s['circlepos'][0], cosec)))


	# Circle
	p.draw.circle(screen, s['circle_klr'], # fill
		s['circlepos'], radius)
	if s['drawbd']:
		p.draw.circle(screen, s['bdklr'], 
			s['circlepos'], radius+2, s['bd'])	# contour


	# Cartesian plane lines
	if s['drawcartlines']:
		p.draw.line(screen, s['planelineskl'], (0, s['circlepos'][1]), 
			(rct.right, s['circlepos'][1]), 1)
		p.draw.line(screen, s['planelineskl'], 
			(s['circlepos'][0], rct.top), 
			(s['circlepos'][0], rct.bottom), 1)


	# Triangle fill
	if s['drawtrifill']:
		p.draw.polygon(screen, s['triangklr'], 
			(s['circlepos'], (radial_point[0], s['circlepos'][1]), radial_point))


	# Secant and cosecant
	if s['drawsec'] or s['drawcosec']:
		if s['drawsec']:
			p.draw.line(screen, s['cossecklr'], s['circlepos'], 
				(sec, s['circlepos'][1]), s['widthcossec'])
		if s['drawcosec']:
			p.draw.line(screen, s['cossecklr'], s['circlepos'], 
				(s['circlepos'][0], cosec), s['widthcossec'])
		if s['connectcossec'] and s['drawcosec'] and s['drawsec']:
			p.draw.line(screen, s['connectcossecklr'], (s['circlepos'][0], cosec), 
				(sec, s['circlepos'][1]), s['widthcnectcossec'])


	# Cos line
	if s['drawcos']:
		deltacos = lambda a: f.variation(a, cos, radians)
		width = round(s['widthcosin'] * deltacos(s['dwcosin']))
		color = f.color_transition(s['triangklr'], s['cosklr'], deltacos(s['dklr']))

		p.draw.line(screen, color, s['circlepos'], 
			(radial_point[0], s['circlepos'][1]), width)


	# Sine line
	deltasin = lambda a: f.variation(a, sin, radians)
	if s['drawsin']:
		width = round(s['widthcosin'] * deltasin(s['dwcosin']))
		color = f.color_transition(s['triangklr'], s['sinklr'], 
			deltasin(s['dklr']))

		p.draw.line(screen, color, (radial_point[0], 
			s['circlepos'][1]), radial_point, width)


	# Central line
	if s['drawradline']:
		p.draw.line(screen, s['radiusklr'], s['circlepos'], 
			radial_point, s['radwidth'])


	# Origin and radius end-point
	if s['drawradpoints']:
		p.draw.circle(screen, s['radiusklr'], s['circlepos'], 8)
		p.draw.circle(screen, s['radiusklr'], radial_point, 8)


	# Tangent line
	#-------------------------------------------------------------
	deltatan = lambda a: f.variation(a, tan, radians)
	color = f.color_transition(s['bgklr'], s['cosklr'], deltasin(1))

	if s['drawtg']:
		if s['drawtgline']:	# line from the center to the border of the screen
			quadrant = None
			_sin = sin(radians)
			_cos = cos(radians)
			if _sin >= 0 and _cos >= 0: quadrant = 1
			elif _sin > 0 and _cos < 0: quadrant = 2
			elif _sin < 0 and _cos < 0: quadrant = 3
			else: 						quadrant = 4
			
			endat = f.project_angle(s['circlepos'], rct, angle, quadrant)
			try:
				p.draw.line(screen, s['tgklr'], s['circlepos'], 
					endat, s['radtgwidth'])
			except:
				pass
			if s['drawtgenddot']: 	# to see if it's working properly
				p.draw.circle(screen, s['radiusklr'], 
					(int(endat[0]), int(endat[1])), 50)

		# Tangent
		xi = s['circlepos'][0] + s['radius']
		posi = (xi, s['circlepos'][1])
		posf = (xi, s['circlepos'][1] - tan(radians)*s['radius'])
		p.draw.line(screen, color, posi, posf, s['tgwidth'])
	#-------------------------------------------------------------


	# Cotangent
	if s['drawcotg']:
		yi = s['circlepos'][1] - s['radius']
		cotg = 1/tan(f.deg2rad(angle)) * s['radius']
		posi = (s['circlepos'][0], yi)
		posf = (s['circlepos'][0] + cotg, yi)

		# Central line
		try:
			if s['drawcotgline']:
				p.draw.line(screen, s['tgklr'], s['circlepos'], posf, s['radtgwidth'])
		except: pass

		# Value line
		color = f.color_transition(s['sinklr'], s['bgklr'], deltasin(1))
		p.draw.line(screen, color, posi, posf, s['tgwidth'])
	#-------------------------------------------------------------


	p.display.flip()