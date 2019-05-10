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

class Obstackles:
    
    def __init__(self,Display,HorisontalPos,VerticalPos,Type,Speed):
        self.HorisontalPos = HorisontalPos
        self.VerticalPos = VerticalPos
        self.Type = Type
        self.Speed = Speed
        
    def GetPos(self):
        #print(self.Speed)
        return (self.HorisontalPos,self.VerticalPos)
    
    def GetType(self):
        return self.Type
    
    def Move(self):
        self.VerticalPos = self.VerticalPos + self.Speed
        
    def GetSpeed(self):
        return self.Speed
        
    def IncreaseSpeed(self):
        self.Speed = self.Speed + 0.5
        