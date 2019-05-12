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

class Obstacles:
    
    def __init__(self,Display,HorisontalPos,VerticalPos,Type):
        self.HorisontalPos = HorisontalPos
        self.VerticalPos = VerticalPos
        self.Type = Type
        
    def GetPos(self):
        return (self.HorisontalPos,self.VerticalPos)
    
    def GetType(self):
        return self.Type
    
    def Move(self,Speed):
        self.VerticalPos = self.VerticalPos + Speed
        