import pygame,sys,time,random,threading
from pygame.locals import *
from class_cars import *
pygame.init()

width = 400
height = 600

Display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Two Cars")
clock = pygame.time.Clock()
# Load images
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

Entry = True
btnPressed = False
highscore = 0
score = 0
obstacles = []
speed = 3
isFirstGame = True

def Home_Screen(subtitle):
    global score
    global btnPressed
    global Entry
    global highscore
    Entry = True
    
    Display.blit(OutOfGame_screen,(0,0)) # positioning is always from tob left corner
    WriteToScreen('Latest score: '+str(score), (110,450))
    
    if subtitle == TWO_CARS_subtitle:
        subHPos = 77
    elif subtitle == PAUSE_subtitle:
        subHPos = 88
    elif subtitle == GAME_OVER_subtitle:
        subHPos = 6
        if score > highscore:
            highscore = score
        score = 0
        
    WriteToScreen('Highscore: '+str(highscore), (217,20))
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

def Button(centerx, centery, radius, figureInactive, figureActive):
    global btnPressed
    global isFirstGame
    mousex, mousey = 0,0
    clickx, clicky = 0,0
    mClicked = False
    isEnterPressed = False
    
    while not btnPressed:
        # catch user actions
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    clickx,clicky = event.pos
                    mClicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and isFirstGame == False:
                    Display.blit(figureActive,(100,250))
                    pygame.display.update()
                    isEnterPressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and isFirstGame == False:
                    btnPressed = True
                    Game_Screen()
                    isEnterPressed = False
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if isMouseOverButton(centerx,centery,radius,mousex,mousey):
            Display.blit(figureActive,(100,250))
            pygame.display.update()
            if isMouseOverButton(centerx,centery,radius,clickx,clicky) and mClicked == True:
                mClicked = False
                btnPressed = True
                isFirstGame = False
                Game_Screen()
        else:
            if isEnterPressed == False:
                Display.blit(figureInactive,(100,250))
                pygame.display.update()
        clock.tick(30)
        
def isMouseOverButton(centerX,centerY,radius,mouseX,mouseY):
    mouseXdif = mouseX - centerX
    mouseYdif = mouseY - centerY
    mouseXdif2 = mouseXdif * mouseXdif
    mouseYdif2 = mouseYdif * mouseYdif
    
    return (mouseXdif2 + mouseYdif2) < (radius * radius)

def GenerateObstackle(color):
    global Entry
    global obstacles
    global speed

    time.sleep(random.randint(0,3))
    while Entry:           
        if color == 'red':
            lane = random.choice((30,130)) # an obstackle is 40x40 px
            oType = random.choice((RedCircle,RedSquare))
        elif color == 'blue':
            lane = random.choice((230,330))
            oType = random.choice((BlueCircle,BlueSquare))
            
        obstacle = Obstacles(Display,lane,-40,oType)
        obstacles.append(obstacle)
        
        sleeptime = random.randint(6,12)/speed
        time.sleep(sleeptime)

def Game_Screen():
    global score
    global Entry
    global obstacles
    global btnPressed
    global speed
    btnPressed = False
    redCar = Cars(Display,30,130) # a car is 40x75 px
    blueCar = Cars(Display,230,330)

    redThread = threading.Thread(target=GenerateObstackle, args=('red',))
    blueThread = threading.Thread(target=GenerateObstackle, args=('blue',))
    redThread.start()
    blueThread.start()
    
    while Entry:
        Display.blit(InGame_Screen,(0,0))
        isGameOver = False
        elementToRemove = -1
        isLaneSwitched = False
        # catch user actions
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    redCar.Change()
                    isLaneSwitched = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    blueCar.Change()
                    isLaneSwitched = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    Entry = False
                    redThread.join()
                    blueThread.join()
                    Home_Screen(PAUSE_subtitle)
            if event.type == QUIT:
                Entry = False
                redThread.join()
                blueThread.join()
                pygame.quit()
                sys.exit()
        
        redCarPos = redCar.GetPos()
        blueCarPos = blueCar.GetPos()
        
        for element in obstacles:
            element.Move(speed)
            objPos = element.GetPos()
            objType = element.GetType()
            
            Display.blit(objType,objPos)
            # handling the cases when a car hits an obstackle
            if objPos[1]+40 >= 480 and objPos[1] <= 555: # vertical position of the cars: 480-555 px
                if objPos[0] == redCarPos or objPos[0] == blueCarPos: # when on obstackle is in the same lane as a car
                    if objType == RedCircle or objType == BlueCircle: # when hits a circle
                        score += 1
                        elementToRemove = element
                        speed += 1/speed
                    else: # when hits a square
                        if isLaneSwitched: # hitting a square when car is changing lane
                            if objType == RedSquare:
                                if objPos[0] == 30:
                                    redCarPos = objPos[0]+40 # position the car towards the obstackle
                                if objPos[0] == 130:
                                    redCarPos = objPos[0]-40
                            if objType == BlueSquare:
                                if objPos[0] == 230:
                                    blueCarPos = objPos[0]+40
                                if objPos[0] == 330:
                                    blueCarPos = objPos[0]-40
                        isGameOver = True
            # handling the cases when an obstackle reaches the bottom of the screen
            if objPos[1]+40 >= 600:
                if objType == RedCircle or objType == BlueCircle:
                    isGameOver = True
            if objPos[1] >= 600: #bottom of screen: 600 px
                elementToRemove = element
        
        if elementToRemove != -1:
            obstacles.remove(elementToRemove)
        
        Display.blit(RedCar,(redCarPos,480))
        Display.blit(BlueCar,(blueCarPos,480))
        WriteToScreen('Score: '+str(score), (265,20))
        pygame.display.update()
        
        if isGameOver == True:
            Entry = False
            redThread.join()
            blueThread.join()
            obstacles.clear()
            speed = 3
            Home_Screen(GAME_OVER_subtitle)
        clock.tick(30)

if __name__ == "__main__":
    
    Home_Screen(TWO_CARS_subtitle)
    
    pygame.quit()
    sys.exit()