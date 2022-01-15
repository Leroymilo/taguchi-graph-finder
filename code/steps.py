#step class for the process
#A step has a bunch of buttons with actions to exexcute. Additionnal sprites are drawn from the main display function.

from tkinter import Button
from button import *

class Step :
    def __init__(self, name) :
        self.name = name
        self.buttons = []
    
    def click(self, x, y) :
        for button in self.buttons :
            action = button.click(x, y)
            if action is not None :
                return action
    
    def display(self, Window) :
        for button in self.buttons :
            button.display(Window)

step0 = Step('step0')
step0.buttons.append(Button((420, 600), (240, 50), 'Change graph type', 'nextgraphtype'))
step0.buttons.append(Button((680, 600), (180, 50), 'I want this one', 'nextStep'))

step1 = Step('step1')
step1.buttons.append(Button((420, 600), (240, 50), 'I want another graph', 'prevStep'))
step1.buttons.append(Button((680, 600), (180, 50), 'Find solutions', 'process'))

step2 = Step('step2')
step2.buttons.append(Button((0, 0), (200, 50), 'Change links', 'prevStep'))
step2.buttons.append(Button((390, 600), (240, 50), 'previous solution', 'prevSol'))
step2.buttons.append(Button((650, 600), (240, 50), 'next solution', 'nextSol'))

steps = [step0, step1, step2]