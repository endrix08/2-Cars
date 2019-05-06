import pygame,sys#,time,random
from pygame.locals import *
from class_cars import *
pygame.init()

width = 400
height = 600
white = (255,255,255)

Display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Two Cars")
clock = pygame.time.Clock()
Main_screen = pygame.image.load('Main screen (Mistral).bmp')
Btn_start = pygame.image.load('Play.gif')
Btn_start_green = pygame.image.load('Play_green.gif')
InGame_Screen = pygame.image.load('Road.bmp')
BlueCar = pygame.image.load('blueCar.bmp')
BlueCircle = pygame.image.load('blueCircle.bmp')
BlueSquare = pygame.image.load('blueSquare.bmp')
RedCar = pygame.image.load('redCar.bmp')
RedCircle= pygame.image.load('redCircle.bmp')
RedSquare= pygame.image.load('redSquare.bmp')

#Game = Cars(Display)

def Home_Screen():
    global btnPressed
    Display.blit(Main_screen,(0,0))
    Display.blit(Btn_start,(100,250))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    Button(200,350,63,Btn_start,Btn_start_green)
    print("balf")
    pygame.display.update()
    clock.tick(30)
        
mousex, mousey = 0,0
clickx, clicky = 0,0
mClicked = False
btnPressed = False

def isMouseOverButton(centerX,centerY,radius,mouseX,mouseY):
    mouseXdif = mouseX - centerX
    mouseYdif = mouseY - centerY
    mouseXdif2 = mouseXdif * mouseXdif
    mouseYdif2 = mouseYdif * mouseYdif
    
    return (mouseXdif2 + mouseYdif2) < (radius * radius)

def Button(centerx, centery, radius, figureInactive, figureActive):
    global mousex, mousey
    global clickx, clicky
    global mClicked
    global btnPressed
    
    while not btnPressed:
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                #print("balf")
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                print("balf2")
                clickx,clicky = event.pos
                mClicked = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if isMouseOverButton(centerx,centery,radius,mousex,mousey):
            Display.blit(figureActive,(100,250))
            pygame.display.update()
            if isMouseOverButton(centerx,centery,radius,clickx,clicky) and mClicked == True:
                mClicked = False
                btnPressed = True
                #Display.blit(InGame_Screen,(0,0))
                pygame.display.update()
        else:
            Display.blit(figureInactive,(100,250))
            pygame.display.update()
        clock.tick(10)
        
def Game_Screen():
    Entry = True
    redCar = Cars(Display,30,130) # a car is 40x75 px
    blueCar = Cars(Display,230,330)
    Display.blit(InGame_Screen,(0,0))
    
    while Entry:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                  redCar.Change()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                  blueCar.Change()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        Display.blit(InGame_Screen,(0,0))
        Display.blit(RedCar,(redCar.GetPos(),480))
        Display.blit(BlueCar,(blueCar.GetPos(),480))
        pygame.display.update()
        clock.tick(30)


#def main():
#    Obj1 = Cars(Display)

Home_Screen()
Game_Screen()
pygame.quit()
sys.exit()