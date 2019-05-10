import pygame,sys,time,random,threading
from pygame.locals import *
from class_cars import *
pygame.init()

width = 400
height = 600
white = (255,255,255)

Display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Two Cars")
clock = pygame.time.Clock()
OutOfGame_screen = pygame.image.load('OutOfGameScreen.bmp')
TWO_CARS_subtitle = pygame.image.load('Subtitle_2 CARS.gif')
PAUSE_subtitle = pygame.image.load('Subtitle_PAUSE.gif')
GAME_OVER_subtitle = pygame.image.load('Subtitle_GAME OVER.gif')
Btn_start = pygame.image.load('Play.gif')
Btn_start_green = pygame.image.load('Play_green.gif')
InGame_Screen = pygame.image.load('Road.bmp')
BlueCar = pygame.image.load('blueCar.bmp')
BlueCircle = pygame.image.load('blueCircle.bmp')
BlueSquare = pygame.image.load('blueSquare.bmp')
RedCar = pygame.image.load('redCar.bmp')
RedCircle= pygame.image.load('redCircle.bmp')
RedSquare= pygame.image.load('redSquare.bmp')

mousex, mousey = 0,0
clickx, clicky = 0,0
score = 0
mClicked = False
btnPressed = False
Entry = True
obstackles = []

def Home_Screen(subtitle):
    global score
    global btnPressed
    global Entry
    Entry = True
    
    Display.blit(OutOfGame_screen,(0,0))
    WriteToScreen('Latest highscore: '+str(score), (150,20))
    if subtitle == TWO_CARS_subtitle:
        subHPos = 77
    elif subtitle == PAUSE_subtitle:
        subHPos = 88
    else:
        subHPos = 6
        score = 0
    Display.blit(subtitle,(subHPos,114))
    Display.blit(Btn_start,(100,250))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    Button(200,350,63,Btn_start,Btn_start_green)
    pygame.display.update()
    clock.tick(30)

def WriteToScreen(text,position):
    font = pygame.font.SysFont('mingliuextbpmingliuextbmingliuhkscsextb', 20, bold=True) #the long stuff is the name of the font type :P
    surface = font.render(text, True, (255, 255, 255))
    Display.blit(surface, position)

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
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
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
                Game_Screen()
        else:
            Display.blit(figureInactive,(100,250))
            pygame.display.update()
        clock.tick(10)

def GenerateObstackle(color):
    global Entry
    global obstackles

    speed = 4
    time.sleep(random.randint(0,4))
    while Entry:           
        print('inRedThread')
        if color == 'red':
            lane = random.choice((30,130))
            oType = random.choice((RedCircle,RedSquare))
        elif color == 'blue':
            lane = random.choice((230,330))
            oType = random.choice((BlueCircle,BlueSquare))
        else:
            print("Unexpected error:", sys.exc_info()[0]) # Exception handling needed!
        obstackle = Obstackles(Display,lane,-40,oType,speed)
        obstackles.append(obstackle)
        
        if random.randint(5,9)-speed >= 0:
            sleeptime = random.randint(5,9)-speed
        else:
            sleeptime = 2
        time.sleep(sleeptime) # valahogy még mindig bemegy 0 alá a sleeptime!
        speed = obstackle.GetSpeed()
    #ez az adaptáció a sebességhez jónak tűnik mert a meglévők nem csúsznak szét
    # de mintha gyorsítás után az újak nagyobb távokkal helyeződnének le
    # és kellene rá valami védelem is hogy ne mehessen be 0 alá a sleep :P

def Game_Screen():
    print('inMainThread')
    global score
    global Entry
    global obstackles
    global btnPressed
    btnPressed = False # valszeg máshol szebb lenne beállítani
    redCar = Cars(Display,30,130) # a car is 40x75 px
    blueCar = Cars(Display,230,330)
    
    redThread = threading.Thread(target=GenerateObstackle, args=('red',))
    blueThread = threading.Thread(target=GenerateObstackle, args=('blue',))
    redThread.start()
    blueThread.start()
    
    while Entry:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    redCar.Change()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    blueCar.Change()
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #if pygame.mouse.get_pressed() == (1,0,0):
                    #obstackles.append(GenerateBlueObstackle())
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (0,0,1):
                    # with lambda?
                    for element in obstackles:
                        element.IncreaseSpeed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE: # threadek leaállítása!
                    Entry = False
                    redThread.join()
                    blueThread.join()
                    Home_Screen(PAUSE_subtitle)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        Display.blit(InGame_Screen,(0,0))
        Display.blit(RedCar,(redCar.GetPos(),480))
        Display.blit(BlueCar,(blueCar.GetPos(),480))
        
        for element in obstackles:
            objTopPos = element.GetPos()
            objType = element.GetType()
            
            Display.blit(objType,objTopPos)
            element.Move()
            
            if objTopPos[1] >= 480-40 and objTopPos[1] <= 555-40: #car
                if objTopPos[0] == redCar.GetPos() or objTopPos[0] == blueCar.GetPos():
                    if objType == RedCircle or objType == BlueCircle:
                        score = score + 1
                        obstackles.remove(element)
                        for element in obstackles:
                            element.IncreaseSpeed() #megoldani h minden elem sebessége közös legyen
                    else:
                        Entry = False
                        redThread.join()
                        blueThread.join()
                        obstackles = []
                        Home_Screen(GAME_OVER_subtitle)
            if objTopPos[1] >= 600-40:
                if objType == RedCircle or objType == BlueCircle:
                    Entry = False
                    redThread.join()
                    blueThread.join()
                    obstackles = []
                    Home_Screen(GAME_OVER_subtitle)
            if objTopPos[1] >= 600: #bottom of screen
                obstackles.remove(element)
                
        WriteToScreen('Score: '+str(score), (280,20))
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    
    Home_Screen(TWO_CARS_subtitle)
    
    pygame.quit()
    sys.exit()