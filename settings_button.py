import pygame as p
from text import Text


class SettingsButton:
	def __init__(self, screen, text, color):
		r = screen.get_rect()
		x = 8/10 * r.size[0]
		y = 1/100 * r.size[1]
		xsz = 15/100 * r.size[0]
		ysz = 1/20 * r.size[1]
		self.rect = p.Rect((x, y), (xsz, ysz))
		self.screen = screen
		self.color = color
		self.text = Text(text, 18, (self.rect.x + xsz/6, self.rect.y))

	def draw(self):
		p.draw.rect(self.screen, self.color, self.rect)
		p.draw.rect(self.screen, (0,0,0), self.rect, 1)
		self.text.blit(self.screen)