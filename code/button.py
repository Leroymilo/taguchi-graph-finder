#button class for the interface :

import pygame as pg

pg.init()
font = pg.font.SysFont('System', 32)

class Button :
    def __init__(self, C, shape, text, action) :
        self.C = C
        self.size = shape
        self.rect = pg.Rect(self.C, self.size)
        self.text = font.render(text, True, (0, 0, 0))
        x, y = C
        w, h = shape
        self.textC = (x+(w-self.text.get_width())//2, y+(h-self.text.get_height())//2)
        self.action = action
    
    def click(self, x, y) :
        if self.C[0] <= x <= self.C[0]+self.size[0] and self.C[1] <= y <= self.C[1]+self.size[1] :
            return self.action
    
    def display(self, Window) :
        pg.draw.rect(Window, (180, 180, 180), self.rect)
        Window.blit(self.text, self.textC)