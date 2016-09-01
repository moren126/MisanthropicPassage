import pygame, time, sys, random
from pygame.locals import* # pygame evemty w tym są np QUIT

from parameters import Parameters
#from states import GameStates
from colors import*
from button import button
from listsCreation import createSquares, createPreparedPuzzles, drawNewPuzzles
from puzzleHandler import PuzzleHandler
from scoringDisplay import scoringDisplay


FPS = 60 #15 #30
startTime = 0

#
PAUSE = False
BACK = USEREVENT + 1
DEBUGMODE = True
#

class Game(Parameters):

    def __init__(self):
        super(Game, self).__init__()
        
        # wymiary planszy
        self.COLUMNS = 12
        self.ROWS = 8

        # pozycja poczatkowa pierszego kafla (potrzebne do tworzenia list, wiec musi byc przed create'ami)
        self.STARTPUZZLEX = random.randrange(1, self.COLUMNS)
        self.STARTPUZZLEY = random.randrange(1, self.ROWS) 
        
        # parametry pol
        self.SQUARESIZE = 100
        self.STARTX = self.BOARDX
        self.STARTY = self.BOARDY
        
        # tworzenie pol i kafelkow
        self.SQUARES = createSquares(self)
        self.PREPAREDPUZZLES = createPreparedPuzzles(self)
        self.PLACEDPUZZLES = []
        
        # parametry do wyswietlania kolejnego kafelka
        self.NEXTX = self.WIDTH - self.SQUARESIZE - ((self.BOARDX - self.SQUARESIZE) / 2)
        self.NEXTY = (self.HEIGHT - self.SQUARESIZE) / 2
        
        # parametry na nowa rozgrywke (+ self.STARTPUZZLEX/Y z powyzej)
        self.SCORE = 0
        self.FIRSTTIMEENTRANCE = True
        
        self.PAUSE = False
        self.PAUSEDTIME = 0
        
        self.NEWGAME = False    
        self.WIN = False
        
        self.SHOWPOSSIBILITIES = False
        self.POSSIBILITIES = []
        
        self.CLICKPUZZLE = True
        self.DELETEPUZZLE = False
        
        self.JUSTCOUNTER = 0
        self.TOUR = 0
        
        
  
    def runGame(self, objState):
    
        CLOCK = pygame.time.Clock()
        
        objPuzzleHandler = PuzzleHandler(self.COLUMNS, self.ROWS, self.STARTPUZZLEX, self.STARTPUZZLEY)

        ### audio 
        #pygame.mixer.music.load('utilities\suspense.mp3')
        #pygame.mixer.music.play(-1)
        ###
                    
        while True:      
            self.displaySurface.fill(GROUNDCOLOR)            
            logoSurface = pygame.image.load('utilities\playboard.png')
            self.displaySurface.blit(logoSurface, (self.BOARDX, self.BOARDY))      

            startTime = time.time()
       
            if self.NEWGAME:
                Game.setNewGame(self, objState, objPuzzleHandler)

            Game.flickeringSquares(self, objPuzzleHandler)
            Game.nextPuzzle(self)
            Game.placedPuzzles(self)
            scoringDisplay(self, objState, startTime)
            
            
            ### testowanie
            if DEBUGMODE:
                # wyswietlanie wszystkich pol ze stanem 'ready'
                for i in self.SQUARES:
                   if i['sState'] == 'ready':
                        pygame.draw.rect(self.displaySurface, GREENER, (i['startX'], i['startY'], self.SQUARESIZE, self.SQUARESIZE))          

                # wyswietlanie wszystkich mozliwych pol
                temp = objPuzzleHandler.debugShowPossible(self) 
                if len(temp) != 0:
                    for i in temp:
                        pygame.draw.rect(self.displaySurface, GREEN, (i['startX'], i['startY'], self.SQUARESIZE, self.SQUARESIZE))          
            
            
            # rysowanie mozliwych ruchow przez ~2s          
            if self.SHOWPOSSIBILITIES:
                Game.showPossibleMoves(self, 2, STARTSHOW)
                        
    
            # obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
       
                elif event.type == KEYDOWN:
                    # przycisniecie p - pauza 
                    if event.key == K_p:
                        self.PAUSE = True
                        self.PAUSEDTIME += Game.paused(self)
                    ### 
                    elif self.WIN and event.key == K_m:
                        objState.setState('WelcomeMenu')
                        return                        
                    ### 

                # wlasny event ktory daje 'True' jak klikniety button 'Back to menu'     
                elif event.type == BACK:
                    objState.setState('WelcomeMenu')
                    return
                    
                # klikniecie PPM -> polozenie lub usuniecie puzla
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.CLICKPUZZLE):
                    Game.clickSquare(self, objPuzzleHandler)
                    
                # klikniecie LPM -> omijanie puzzla 
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) and self.CLICKPUZZLE:
                    STARTSHOW = objPuzzleHandler.skipPuzzle(self, objState)    

            # przyciski z menu po lewej        
            if objState.STATE == 'Game':
                if button(self, 'New Game',     30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (self.BUTTONHEIGHT + 50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    Game.buttonGameAction(self, 'New Game', objState)  
                if button(self, 'Back to menu', 30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (2*self.BUTTONHEIGHT + 2*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    Game.buttonGameAction(self, 'Back to menu', objState)
                if button(self, 'Quit',         30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (3*self.BUTTONHEIGHT + 3*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    Game.buttonGameAction(self, 'Quit', objState)

                    
            Game.pauseText(self)
  
            pygame.display.update()
            CLOCK.tick(FPS)
    
    def setNewGame(self, objState, objPuzzleHandler):
        self.STARTPUZZLEX = random.randrange(1, self.COLUMNS)
        self.STARTPUZZLEY = random.randrange(1, self.ROWS) 
                
        self.PLACEDPUZZLES[:] = []                    
        self.SQUARES = createSquares(self)
        self.PREPAREDPUZZLES = createPreparedPuzzles(self)
                    
        #zerowanie wyniku, czasu
        self.SCORE = 0
        self.FIRSTTIMEENTRANCE = True
        startTime = time.time()
        self.PAUSEDTIME = 0       
        objPuzzleHandler = PuzzleHandler(self.COLUMNS, self.ROWS, self.STARTPUZZLEX, self.STARTPUZZLEY) 
        self.JUSTCOUNTER = 0   
        self.TOUR = 0         
        objState.setCreditFromDiff()
        self.NEWGAME = False

    # po ominieciu kafelka ktory mozna bylo polozyc    
    def showPossibleMoves(self, delay, STARTSHOW):
        self.CLICKPUZZLE = False
        for i in self.POSSIBILITIES:     
            pygame.draw.rect(self.displaySurface, BRIGHTRED, (i['startX'], i['startY'], self.SQUARESIZE, self.SQUARESIZE))
                    
            #odliczanie timera
            stopShow = time.time()
            showTime = stopShow - STARTSHOW

            if showTime >= (delay - 1):
                movingPuzzle = self.PREPAREDPUZZLES.pop(0)
                if movingPuzzle['tour'] != 'irrelevant':
                    movingPuzzle['tour'] += 1 
                    self.PREPAREDPUZZLES.append(movingPuzzle) 
                self.SHOWPOSSIBILITIES = False
                self.POSSIBILITIES[:] = []
                self.CLICKPUZZLE = True        
    
    def getHighlighted(self, objPuzzleHandler):
        global posX, posY 
        highlighted = {}
        mode = 0
    
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]        
        click = pygame.mouse.get_pressed()
        
        #podswietlanie pol tylko na obszarze planszy
        if self.STARTX <= mouseX < self.STARTX + self.BOARDWITH and self.STARTY <= mouseY < self.STARTY + self.BOARDHEIGHT:
        
            #pobieranie pozycji w kolumnach i wierszach 
            for x in range(self.COLUMNS):
                if mouseX <= (x * 100 + self.STARTX + self.SQUARESIZE):
                    posX = x + 1
                    break
            for y in range(self.ROWS):
                if mouseY <= (y * 100 + self.STARTY + self.SQUARESIZE):
                    posY = y + 1                
                    break
            
            #odszukanie odpowiadajacych pozycji w pikselach dla kazdego najechanego pola
            for i in self.SQUARES:
            
                if i['x'] == posX and i['y'] == posY:
                
                    # tylko niezajete pola moga sie podswietlac gdy kladziemy kafelki
                    if i['sState'] != 'occupied':
                        highlighted = i
                        mode = 1
                        
                    # tylko zajete pola moga sie podswietlac gdy usuwamy   
                    elif i['sState'] == 'occupied': 
                        highlighted = i
                        mode = 2

        return (highlighted, mode)
    
    def flickeringSquares(self, objPuzzleHandler):
    
        global posX, posY, highlighted 
        mode = 0
       
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]        
        click = pygame.mouse.get_pressed()
        
        #podswietlanie pol tylko na obszarze planszy
        if self.STARTX <= mouseX < self.STARTX + self.BOARDWITH and self.STARTY <= mouseY < self.STARTY + self.BOARDHEIGHT:
        
            #pobieranie pozycji w kolumnach i wierszach 
            for x in range(self.COLUMNS):
                if mouseX <= (x * 100 + self.STARTX + self.SQUARESIZE):
                    posX = x + 1
                    break
            for y in range(self.ROWS):
                if mouseY <= (y * 100 + self.STARTY + self.SQUARESIZE):
                    posY = y + 1                
                    break
            
            #odszukanie odpowiadajacych pozycji w pikselach dla kazdego najechanego pola
            for i in self.SQUARES:
            
                if i['x'] == posX and i['y'] == posY:
                
                    # tylko niezajete pola moga sie podswietlac gdy kladziemy kafelki
                    if i['sState'] != 'occupied':
                        highlighted = i
                        mode = 1
                        
                    # tylko zajete pola moga sie podswietlac gdy usuwamy   
                    elif i['sState'] == 'occupied': 
                        highlighted = i
                        mode = 2

        if mode == 1:
            if (highlighted is not None and self.PREPAREDPUZZLES[0]['tour'] != -10):  
                pygame.draw.rect(self.displaySurface, YELLOW, (highlighted['startX'], highlighted['startY'], self.SQUARESIZE, self.SQUARESIZE))
            
    def clickSquare(self, objPuzzleHandler):
    
        highlighted = Game.getHighlighted(self, objPuzzleHandler)

        # tryb kladzenia kafelka
        if highlighted[1] == 1 and not self.DELETEPUZZLE:
            if highlighted[0]['sState'] == 'ready':
                if objPuzzleHandler.isMovePossible(self, highlighted[0]):
                    highlighted[0]['sState'] = 'occupied'
                    Game.placePuzzle(self, highlighted[0]['x'], highlighted[0]['y'], highlighted[0]['startX'], highlighted[0]['startY'])
            elif highlighted[0]['sState'] == 'unoccupied':   
                #komunikat o niedozowlonym ruchu
                pass
                
        # tryb usuwania kafelka        
        elif highlighted[1] == 2 and self.DELETEPUZZLE:
            if highlighted[0]['sState'] == 'occupied':
                objPuzzleHandler.deletePuzzle(self, highlighted[0]['x'], highlighted[0]['y']) 
                                       
                  
    def placePuzzle(self, posX, posY, positionX, positionY):

        for i in self.SQUARES:
            if (i['x'] == posX - 1 and i['y'] == posY) or (i['x'] == posX + 1 and i['y'] == posY):
                if i['sState'] != 'occupied':
                    i['sState'] = 'ready'
            if (i['x'] == posX and i['y'] == posY - 1) or (i['x'] == posX and i['y'] == posY + 1):
                if i['sState'] != 'occupied':
                    i['sState'] = 'ready'          

        if self.REST != 0:
            objPuzzle = {   'index': self.JUSTCOUNTER,
                            'x': posX,
                            'y': posY,
                            'startX': positionX,
                            'startY': positionY,
                            'pImage': self.PREPAREDPUZZLES[0]['image'],
                            'pPattern': self.PREPAREDPUZZLES[0]['pattern'],
                            'pColorU': self.PREPAREDPUZZLES[0]['colorU'],
                            'pColorR': self.PREPAREDPUZZLES[0]['colorR'],
                            'pColorD': self.PREPAREDPUZZLES[0]['colorD'],
                            'pColorL': self.PREPAREDPUZZLES[0]['colorL'],
                            }        
            self.PLACEDPUZZLES.append(objPuzzle)
            
            self.JUSTCOUNTER += 1

            if self.PREPAREDPUZZLES[0]['tour'] != 'irrelevant':
                self.REST -= 1
            
            self.PREPAREDPUZZLES.pop(0)

        if self.REST == 0:        
            self.WIN = True  
            ###
            print('Game.placePuzzle linia ~341: WIN!')
            ###
            
    def placedPuzzles(self):
        for i in self.PLACEDPUZZLES:
            surface = i['pImage']
            self.displaySurface.blit(surface, (i['startX'], i['startY'])) 

    def nextPuzzle(self):  
        #tlo do Next Puzzle
        back = pygame.image.load('utilities\pback.png')
        self.displaySurface.blit(back, (self.NEXTX - 25, self.NEXTY - 25)) 
        
        #napis 'Next puzzle'
        font = pygame.font.Font(self.FONTNAME, 30)    
        textSurf = font.render('Next puzzle', True, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = ( self.NEXTX + 50, self.NEXTY - 50 )
        self.displaySurface.blit(textSurf, textRect)    
                
        #pierwszy puzzel
        if len(self.PLACEDPUZZLES) == 0:
            startImage = pygame.image.load('utilities\start.png')
            objPuzzle = {   'index': 1519,
                            'x': self.STARTPUZZLEX,
                            'y': self.STARTPUZZLEY,
                            'startX': self.STARTX + (self.STARTPUZZLEX - 1) * self.SQUARESIZE,
                            'startY': self.STARTY + (self.STARTPUZZLEY - 1) * self.SQUARESIZE,
                            'pImage': startImage,
                            'pPattern': 'anything',  
                            'pColorU': 'neutral',
                            'pColorR': 'neutral',
                            'pColorD': 'neutral',
                            'pColorL': 'neutral',}        
            self.PLACEDPUZZLES.append(objPuzzle)
        

        if self.PREPAREDPUZZLES[0]['tour'] > self.TOUR:
            #losowanie specjali do dodania do pozostałych puzzli
            drawNewPuzzles(self)
            self.TOUR += 1
        
        if self.REST != 0:
            surface = self.PREPAREDPUZZLES[0]['image']
            self.displaySurface.blit(surface, (self.NEXTX, self.NEXTY)) 
            if self.PREPAREDPUZZLES[0]['tour'] == -10:
                self.DELETEPUZZLE = True         
            
        else: #wyswietlenie konca puzli
            surface = pygame.image.load('utilities\end.png')
            self.displaySurface.blit(surface, (self.NEXTX, self.NEXTY)) 


    def pauseText(self):
        #napis 'Press p to pause'
        font = pygame.font.Font(self.FONTNAME, 26)    
        textSurf = font.render('Press \'p\' to pause', True, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = ( self.NEXTX + 50, self.HEIGHT - self.BOARDY - 13 )
        self.displaySurface.blit(textSurf, textRect)      
               
    def unpause(self):
        #pygame.mixer.music.unpause()
        self.PAUSE = False
        stopPause = time.time()
        return stopPause
    
    def paused(self): #dziala, ale poprawic
        #pygame.mixer.music.pause()

        startPause = time.time()
        
        while self.PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        stopPause = Game.unpause(self) 
                        pauseTime = stopPause - startPause
                        return pauseTime
                        #print(time.strftime('%H:%M:%S', time.gmtime(pauseTime)))    
                        
            #kliknij p by kontynuowac
            w = 700 
            h = 70
            pygame.draw.rect(self.displaySurface, RED, (self.HALFWIDTH - w/2, self.HALFHEIGHT - h, w, h))

            s = pygame.Surface( (self.BOARDWITH, self.BOARDHEIGHT), pygame.SRCALPHA )   # per-pixel alpha
            s.fill( (190,190,190,5) )                        
            self.displaySurface.blit( s,(self.BOARDX, self.BOARDY) )
            
            fontButton = pygame.font.Font(self.FONTNAME, 50)    
            textSurfButton = fontButton.render('Press \'p\' to continue', True, WHITE)
            textRectButton = textSurfButton.get_rect()
            textRectButton.center = (self.HALFWIDTH, self.HALFHEIGHT - 0.5 * h)
            self.displaySurface.blit(textSurfButton, textRectButton)    
            
            pygame.display.update()
            #clock.tick(15)               

    # okazja do pocwiczenia nadpisania f-cji z WelcomeScreen bottonAction        
    def buttonGameAction(self, msg, objState):

        if msg == 'New Game':      
            self.NEWGAME = True  

        elif msg == 'Back to menu':
            #print('Back to menu')
            event = pygame.event.Event(BACK)
            pygame.event.post(event)
                        
        elif msg == 'Quit':
            pygame.quit()
            quit()
                        
 
            
            
            
"""

            
            # obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == QUIT:
                    Game.terminate()

                elif event.type == KEYDOWN:

                    #
                    elif event.key == K_p:
                        PAUSE = True
                        Game.paused(windowParameters)
                    #
                    elif winMode and event.key == K_m:
                        return

                elif event.type == KEYUP:


                    elif event.key == K_ESCAPE:
                        Game.terminate()

            if not gameOverMode:
                # ruszanie gracza w odpowiednim kierunku
                if moveLeft:
                    playerObj['x'] -= windowParameters.MOVERATE
                if moveRight:
                    playerObj['x'] += windowParameters.MOVERATE
                if moveUp:
                    playerObj['y'] -= windowParameters.MOVERATE
                if moveDown:
                    playerObj['y'] += windowParameters.MOVERATE

                if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0:
                    playerObj['bounce'] += 1

                if playerObj['bounce'] > windowParameters.BOUNCERATE:
                    playerObj['bounce'] = 0

                # sprawdzanie kolizji z wrogimi kapibarami
                for i in range(len(enemyObjs)-1, -1, -1):
                    enObj = enemyObjs[i]
                    if 'rect' in enObj and playerObj['rect'].colliderect(enObj['rect']):
                    
                        # doszło do kolizji
                        if enObj['width'] * enObj['height'] <= playerObj['size']**2:
                            # gracz jt większy i zjada kapibarę
                            eatens += 1
                            playerObj['size'] += int( (enObj['width'] * enObj['height'])**0.2 ) + 1
                            del enemyObjs[i]

                            if playerObj['facing'] == LEFT:
                                playerObj['surface'] = pygame.transform.scale(L_CAP_IMG, (playerObj['size'], playerObj['size']))
                            if playerObj['facing'] == RIGHT:
                                playerObj['surface'] = pygame.transform.scale(R_CAP_IMG, (playerObj['size'], playerObj['size']))

                            if playerObj['size'] > windowParameters.WINSIZE:
                                winMode = True

                        elif not invulnerableMode:
                            # gracz jt mniejszy i traci zdrowie
                            injured = pygame.mixer.Sound('capybara_barks_mono.wav')
                            injured.play()
                            invulnerableMode = True
                            invulnerableStartTime = time.time()
                            playerObj['health'] -= 1
                            if playerObj['health'] == 0:
                                gameOverMode = True
                                gameOverStartTime = time.time()
            else:
                # koniec gry
                w = 300 
                h = 130
                pygame.draw.rect(windowParameters.displaySurface, windowParameters.RED, (windowParameters.HALFWIDTH - w/2, windowParameters.HALFHEIGHT - h/2, w, h))
                
                windowParameters.displaySurface.blit(gameOverSurf, gameOverRect)
                pygame.mixer.music.fadeout(1000)
                if time.time() - gameOverStartTime > GAMEOVERTIME:
                    return

            # sprawdzenie czy gracz wygrał
            if winMode:
                windowParameters.displaySurface.blit(winSurf, winRect)
                windowParameters.displaySurface.blit(winSurf2, winRect2)
                pygame.mixer.music.fadeout(1000)
                #pygame.mixer.music.stop()

            pygame.display.update()
            FPSCLOCK.tick(FPS)
    
    def unpause():
        global PAUSE
        pygame.mixer.music.unpause()
        PAUSE = False
    
    def paused(self):
        pygame.mixer.music.pause()

        while PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        Game.unpause()   
                        
            #kliknij p by kontynuowac
            w = 300 
            h = 50
            pygame.draw.rect(self.displaySurface, self.RED, (self.HALFWIDTH - w/2, self.HALFHEIGHT - h, w, h))

            fontButton = pygame.font.Font('Kenzo Regular Italic.otf', 30)    
            textSurfButton = fontButton.render('Click \'p\' to continue', True, self.WHITE)
            textRectButton = textSurfButton.get_rect()
            textRectButton.center = (self.HALFWIDTH, self.HALFHEIGHT - 0.5*h)
            self.displaySurface.blit(textSurfButton, textRectButton)    
            
            pygame.display.update()
            #clock.tick(15)   
            
    def terminate():
        pygame.quit()
        sys.exit()
  """