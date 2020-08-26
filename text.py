import pygame as p


default = "./unispace/unispace.ttf"

class Text:
    def __init__(self, content, size, position, color=(0,0,0), font=None):
        self.text = content
        self.position = position
        self.color = color
        self.font = None

        if size > 0:
            if font == None:
                self.font = p.font.Font(default, size)
            else:
                self.font = p.font.Font(font, size)
        else:
            msg = "The font size must be positive"
            raise Exception(msg)

    def blit(self, surface):
        self.surf = self.font.render(self.text, 0, self.color)
        rect = p.Rect((self.position), (0,0))
        surface.blit(self.surf, rect)

