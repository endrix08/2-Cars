import pygame
from pygame.locals import *

class Cars:
    
    def __init__(self,Display,LeftPos,RightPos):
        self.Display = Display
        self.LeftPosition = LeftPos
        self.RightPosition = RightPos
        self.CurrentPos = LeftPos
        
    def Change(self):
        if self.CurrentPos == self.LeftPosition:
            self.CurrentPos = self.RightPosition
        else:
            self.CurrentPos = self.LeftPosition
            
    def GetPos(self):
        return self.CurrentPos
