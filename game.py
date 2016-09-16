import pygame, time, sys, random, os, pickle
from os import path
from pygame.locals import*

from parameters import Parameters
from colors import*
from button import button, checkButton
from listsCreation import createSquares, createPreparedPuzzles, drawNewPuzzles
from puzzleHandler import PuzzleHandler
from scoringDisplay import Scoring
from dataStorage import store
from randoms import insultOrNot, chooseInsult

FPS = 60
startTime = 0

#
BACK = USEREVENT + 1
DEBUGMODE = True
#

class Game(Parameters):

    def __init__(self):
        super(Game, self).__init__()
        
        # wymiary planszy
        self.COLUMNS = 12
        self.ROWS = 8

        # pozycja poczatkowa pierszego kafelka (potrzebne do tworzenia list, wiec musi byc przed create'ami)
        self.STARTPUZZLEX = 0
        self.STARTPUZZLEY = 0
        
        # parametry pol
        self.SQUARESIZE = self.PUZZLESIZE #100
        self.STARTX = self.BOARDX
        self.STARTY = self.BOARDY
        
        # tworzenie pol i kafelkow
        self.SQUARES = []
        self.PREPAREDPUZZLES = []
        self.PLACEDPUZZLES = []
        
        # parametry do wyswietlania kolejnego kafelka
        self.NEXTX = self.WIDTH - self.SQUARESIZE - ((self.BOARDX - self.SQUARESIZE) / 2)
        self.NEXTY = (self.HEIGHT - self.SQUARESIZE) / 2

        self.STARTTIME = 0        
        
        self.PAUSE = False
        self.PAUSEDTIME = 0
        
        self.NEWGAME = False   
        self.ENDGAME = False       
        #self.WIN = False
        #self.GAMEOVER = False
        
        self.SHOWPOSSIBILITIES = False
        self.POSSIBILITIES = []
        
        self.CLICKPUZZLE = True
        self.DELETEPUZZLE = False
        
        self.JUSTCOUNTER = 0
        self.TOUR = 0

        self.drawIterator = 100
        
        # parametry do wyswietlania bonusow
        self.SHOWBONUS = False
        self.BONUSVAL = 0
        self.ITSTIME = 0
        
        self.SHOWLOSS = (False, 0, 0)
        
        self.SHOWINSULT = False
        self.doItOnce = 0 

        self.fontSize = int(self.FONTSIZE / 2) #15
        
    # obsluga rozgrywki
    def runGame(self, objState):
        CLOCK = pygame.time.Clock()    
        
        # wspolczynniki zalezne od wybranego poziomu trudnosci
        trashFactor = objState.getTrashFactor()
        gameMode = objState.getMode()
        startPuzzleFactor = objState.getStartFactor()
        
        # pozycja poczatkowego kafelka
        self.STARTPUZZLEX = random.randrange(1 + startPuzzleFactor, self.COLUMNS - startPuzzleFactor)
        self.STARTPUZZLEY = random.randrange(1 + startPuzzleFactor, self.ROWS - startPuzzleFactor) 
        
        # listy potrzebne do rozgrywki
        self.SQUARES = createSquares(self)
        self.PREPAREDPUZZLES = createPreparedPuzzles(self, trashFactor, 0)

        # obiekty potrzebne do rozgrywki
        objPuzzleHandler = PuzzleHandler(self.COLUMNS, self.ROWS, self.STARTPUZZLEX, self.STARTPUZZLEY)
        objScore = Scoring()
                    
        while True:      
            # kolor tla
            self.displaySurface.fill(GROUNDCOLOR)    

            # wyswietlanie planszy    
            boardSurface = pygame.image.load(path.join('utilities', 'playboard.png'))
            boardSurfaceScaled = pygame.transform.scale(boardSurface, (self.BOARDWITH, self.BOARDHEIGHT))
            self.displaySurface.blit(boardSurfaceScaled, (self.BOARDX, self.BOARDY))      

            # czas rozpoczecia rozgrywki
            self.STARTTIME = time.time()
       
            # jesli nowa gra - ustawienie parametrow na nowa rozgrywke
            if self.NEWGAME:
                Game.setNewGame(self, objState, objScore)
                objPuzzleHandler = PuzzleHandler(self.COLUMNS, self.ROWS, self.STARTPUZZLEX, self.STARTPUZZLEY) 

            # podswietlanie pol najechanych kursorem    
            if not self.ENDGAME:
                Game.flickeringSquares(self, objPuzzleHandler)
            
            # wyswietlanie kafelka czekajacego na polozenie
            Game.nextPuzzle(self, objState, gameMode)
            
            # wyswietlanie polozonych kafelkow
            Game.placedPuzzles(self)
            
            # wyswietlanie punktacji
            result = objScore.scoringDisplay(self, objState, gameMode)
            
            # wyswietlanie napisu o pauzie        
            Game.pauseText(self)
            
            # sprawdzenie czy nie doszlo do konca rozgrywki
            endGame = objScore.endOfPlay()
            
            # KONIEC GRY - wygrana 
            if endGame[0]:  
                self.CLICKPUZZLE = False
                self.ENDGAME = True              
                objPuzzleHandler.clearFill() # na wszelki wypadek
                
                # napis 'WIN'
                w = 700 
                h = 70
                pygame.draw.rect(self.displaySurface, RED, (self.HALFWIDTH - w/2, self.HALFHEIGHT - h, w, h))
               
                fontButton = pygame.font.Font(self.FONTNAME, 50)    
                textSurfButton = fontButton.render('WIN', True, WHITE)
                textRectButton = textSurfButton.get_rect()
                textRectButton.center = (self.HALFWIDTH, self.HALFHEIGHT - 0.5 * h)
                self.displaySurface.blit(textSurfButton, textRectButton) 
                
                store(objState, result)
    
            # KONIEC GRY - koniec kredytow
            if endGame[1]:
                self.CLICKPUZZLE = False
                self.ENDGAME = True
                #self.GAMEOVER = True
                objPuzzleHandler.clearFill() # na wszelki wypadek
                
                # napis 'Game Over'
                w = 700 
                h = 70
                pygame.draw.rect(self.displaySurface, RED, (self.HALFWIDTH - w/2, self.HALFHEIGHT - h, w, h))
               
                fontButton = pygame.font.Font(self.FONTNAME, 50)    
                textSurfButton = fontButton.render('Game Over', True, WHITE)
                textRectButton = textSurfButton.get_rect()
                textRectButton.center = (self.HALFWIDTH, self.HALFHEIGHT - 0.5 * h)
                self.displaySurface.blit(textSurfButton, textRectButton)    

                if gameMode == 'Continuous':
                    store(objState, result)
           
            """
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
            """
            
            # rysowanie mozliwych ruchow po skip'ie przez ~2s          
            if self.SHOWPOSSIBILITIES:
                Game.showPossibleMoves(self, 2, STARTSHOW[0], gameMode)

               
            # if sth wyswietl premie przez 2s        
            if self.SHOWBONUS:
                msg = '+ ' + str(self.BONUSVAL)
                itsTime = self.ITSTIME
                x = self.BOARDX + 4 * (self.BOARDWITH / 5) + 90 + 50
                y = self.BOARDY / 2
                Game.bonusOrLossInfo(self, msg, 2, itsTime, x, y)
                if self.doItOnce == 0:
                    shouldInsult = insultOrNot()
                    if shouldInsult:
                        self.SHOWINSULT = True
                        timee = itsTime
                        insult = chooseInsult('plus')
                    self.doItOnce += 1
                    
                
            if self.SHOWLOSS[0]: 
                msg = '- ' + str(self.SHOWLOSS[1])
                x = self.BOARDX + 75
                y = self.BOARDY / 2
                Game.bonusOrLossInfo(self, msg, 2, self.SHOWLOSS[2], x, y)
                if self.doItOnce == 0:
                    shouldInsult = insultOrNot()  
                    if shouldInsult:
                        self.SHOWINSULT = True
                        timee = self.SHOWLOSS[2]
                        insult = chooseInsult('minus')
                    self.doItOnce += 1
                        
            if self.SHOWINSULT:   
                Game.showInsult(self, insult, 6, timee)
            
            # obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    # przycisniecie p - pauza 
                    if event.key == K_p:
                        self.PAUSE = True
                        self.PAUSEDTIME += Game.paused(self)

                # wlasny event ktory daje 'True' jak klikniety button 'Back to menu'     
                elif event.type == BACK:
                    #time.sleep(0.2)
                    objState.setState('WelcomeMenu')
                    return
                    
                # klikniecie PPM -> polozenie lub usuniecie puzla
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.CLICKPUZZLE):
                    Game.clickSquare(self, objPuzzleHandler, objScore, objState)
                    
                # klikniecie LPM -> omijanie puzzla 
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) and self.CLICKPUZZLE:
                    STARTSHOW = objPuzzleHandler.skipPuzzle(self, objState, gameMode)   
                    if STARTSHOW is not None:
                        self.SHOWLOSS = (True, STARTSHOW[1], STARTSHOW[0])    

            # przyciski z menu po lewej        
            if objState.STATE == 'Game':
                if button(self, 'New Game',     self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY - (2*self.BUTTONHEIGHT + 2*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    Game.buttonGameAction(self, 'NewGame', objState)  
                if button(self, 'Back to menu', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY - (self.BUTTONHEIGHT + 50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    Game.buttonGameAction(self, 'BackMenu', objState)
                if button(self, 'Quit',         self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY, self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    Game.buttonGameAction(self, 'Quit', objState)

            pygame.display.update()
            CLOCK.tick(FPS)
    
    # parametry na nowa rozgrywke
    def setNewGame(self, objState, objScore):
        startPuzzleFactor = objState.getStartFactor()
        self.STARTPUZZLEX = random.randrange(1 + startPuzzleFactor, self.COLUMNS - startPuzzleFactor)
        self.STARTPUZZLEY = random.randrange(1 + startPuzzleFactor, self.ROWS - startPuzzleFactor) 
        
        trashFactor = objState.getTrashFactor()
        
        self.PLACEDPUZZLES[:] = []                    
        self.SQUARES = createSquares(self)
        self.PREPAREDPUZZLES = createPreparedPuzzles(self, trashFactor, 0)
                    
        #zerowanie wyniku, czasu
        objScore.setScoring('noCumulation')
        self.STARTTIME = time.time()
        objState.setCreditFromDiff()
        
        self.PAUSEDTIME = 0  
        self.JUSTCOUNTER = 0   
        self.TOUR = 0         

        self.CLICKPUZZLE = True
        
        #self.WIN = False
        #self.GAMEOVER = False
        self.ENDGAME = False
        self.NEWGAME = False


    # wyswietlenie mozliwosci po ominieciu kafelka ktory mozna bylo polozyc    
    def showPossibleMoves(self, delay, startShow, gameMode):
        self.CLICKPUZZLE = False
        
        for i in self.POSSIBILITIES:     
            pygame.draw.rect(self.displaySurface, BRIGHTRED, (i['startX'], i['startY'], self.SQUARESIZE, self.SQUARESIZE))
                    
            # odliczanie czasu
            stopShow = time.time()
            showTime = stopShow - startShow

            # po odliczeniu opoznienia
            if showTime >= (delay - 1):
                # usuniecie omijanego kafelka z listy oczekujacych
                movingPuzzle = self.PREPAREDPUZZLES.pop(0)
                
                # w trybie 'Classic' jesli byl to zwykly kafelek, zwieksza sie tura, kafelek wraca do puli
                if gameMode == 'Classic':
                    if movingPuzzle['tour'] != -19 and movingPuzzle['tour'] != -10:
                        movingPuzzle['tour'] += 1     
                    self.PREPAREDPUZZLES.append(movingPuzzle)
                    
                # w trybie 'Continuous' kazdy ominiety kafelek zmniejsza licznik REST i nie wraca do puli
                elif gameMode == 'Continuous':
                    self.REST -= 1
                        
                self.SHOWPOSSIBILITIES = False
                self.POSSIBILITIES[:] = []
                
                # klikanie mysza znow aktywne
                self.CLICKPUZZLE = True        
    
    
    # wyswietlanie bonusow
    def bonusOrLossInfo(self, msg, delay, startShowing, x, y):
   
        stopShowing = time.time()
        showTime = stopShowing - startShowing
        
        if showTime >= (delay - 1):
            self.SHOWBONUS = False 
            self.SHOWLOSS = (False, 0, 0)
            self.BONUSVAL = 0
            self.fontSize = 15
            self.doItOnce = 0 
        else:
            font = pygame.font.Font(self.FONTNAME, self.fontSize)    
            textSurf = font.render(msg, True, WHITE)
            textRect = textSurf.get_rect()
            textRect.center = ( int(x + self.fontSize/2), int(y - self.fontSize/2) )
            self.displaySurface.blit(textSurf, textRect)  
            self.fontSize += 1
         

    def showInsult(self, msg, delay, startShowing):
        stopShowing = time.time()
        showTime = stopShowing - startShowing
        
        fontS = int((20 * self.WIDTH) / 1900)
        x = self.HALFWIDTH
        y = self.HEIGHT - 1.5 * fontS 
        
        if showTime >= (delay - 1):
            self.SHOWINSULT = False
            self.doItOnce = 0
        else:
            font = pygame.font.Font(self.FONTNAME, fontS)    
            textSurf = font.render(str(msg), True, WHITE)
            textRect = textSurf.get_rect()
            textRect.center = ( int(x + fontS/2), int(y - fontS/2) )
            self.displaySurface.blit(textSurf, textRect)  

            
            

    # zwraca najechane kursorem pole i tryb (mozliwe do polozenia, mozliwe do usuniecia)  
    def getHighlighted(self, objPuzzleHandler):
        global posX, posY 
        highlighted = {}
        mode = 0
    
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]        
        click = pygame.mouse.get_pressed()
        
        # podswietlanie pol tylko na obszarze planszy
        if self.STARTX <= mouseX < self.STARTX + self.BOARDWITH and self.STARTY <= mouseY < self.STARTY + self.BOARDHEIGHT:
        
            # pobieranie pozycji kursora w kolumnach i wierszach 
            for x in range(self.COLUMNS):
                if mouseX <= (x * self.PUZZLESIZE + self.STARTX + self.SQUARESIZE):
                    posX = x + 1
                    break
            for y in range(self.ROWS):
                if mouseY <= (y * self.PUZZLESIZE + self.STARTY + self.SQUARESIZE):
                    posY = y + 1                
                    break
            
            # odszukanie odpowiadajacych pozycji w pikselach dla kazdego najechanego pola
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
    
    # podswietlanie pol najechanych kursorem, ktore nie sa zajete
    def flickeringSquares(self, objPuzzleHandler):   
        result = Game.getHighlighted(self, objPuzzleHandler)
        highlighted = result[0]
        mode = result[1]
        
        if mode == 1:
            if (highlighted is not None and self.PREPAREDPUZZLES[0]['tour'] != -10):  
                pygame.draw.rect(self.displaySurface, YELLOW, (highlighted['startX'], highlighted['startY'], self.SQUARESIZE, self.SQUARESIZE))
     
    # obsluga klikniecia pola i usuwania polozonego kafelka
    def clickSquare(self, objPuzzleHandler, objScore, objState):
        gameMode = objState.getMode()
        result = Game.getHighlighted(self, objPuzzleHandler)
        highlighted = result[0]
        mode = result[1]        

        # tryb kladzenia kafelka
        if mode == 1 and not self.DELETEPUZZLE:
            if highlighted['sState'] == 'ready':
                isPossibleAndMore = objPuzzleHandler.isMovePossible(self, objScore, highlighted, objState)
                if isPossibleAndMore[0]:
                    highlighted['sState'] = 'occupied'
                    Game.placePuzzle(self, objPuzzleHandler, highlighted['x'], highlighted['y'], highlighted['startX'], highlighted['startY'], gameMode, isPossibleAndMore[1])
               
        # tryb usuwania kafelka        
        elif mode == 2 and self.DELETEPUZZLE:
            if highlighted['sState'] == 'occupied':
                objPuzzleHandler.deletePuzzle(self, highlighted['x'], highlighted['y']) 
                                       
    # dolaczenie kładzionego kafelka do listy polozonych kafelkow              
    def placePuzzle(self, objPuzzleHandler, posX, posY, positionX, positionY, gameMode, deleteFull):

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
            
            # aby kazdy obiekt mial inny indeks, potrzebne w PuzzleHandler
            self.JUSTCOUNTER += 1

            # jesli kladziony kafelek nie byl kafelkiem specjalnym - zmniejszenie liczby kafelkow do polozenia
            if self.PREPAREDPUZZLES[0]['tour'] != -19:
                self.REST -= 1
            
            # usuniecie polozonego kafelka z listy oczekujacych
            self.PREPAREDPUZZLES.pop(0)
            
            if gameMode == 'Continuous':
                objPuzzleHandler.deleteIfNeeded(self, posX, posY, deleteFull)

            ###    
            if deleteFull != 0:
                self.SHOWBONUS = True
                self.BONUSVAL = deleteFull
                self.ITSTIME = time.time()
        
    # wyswietlenie polozonych kalefkow    
    def placedPuzzles(self):
        for i in self.PLACEDPUZZLES:
            surface = i['pImage']
            self.displaySurface.blit(surface, (i['startX'], i['startY'])) 

    # wyswietlenie kolejnego kafelka po prawej stronie ekranu        
    def nextPuzzle(self, objState, gameMode):  
        # tlo do 'Next Puzzle'
        back = pygame.image.load('utilities\pback.png')
        self.displaySurface.blit(back, (self.NEXTX - 25, self.NEXTY - 25)) 
        
        # napis 'Next puzzle'
        font = pygame.font.Font(self.FONTNAME, 30)    
        textSurf = font.render('Next puzzle', True, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = ( self.NEXTX + 50, self.NEXTY - 50 )
        self.displaySurface.blit(textSurf, textRect)    
                
        # pierwszy polozony kafelek
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
        
        
        
        if self.REST != 0:
            surface = self.PREPAREDPUZZLES[0]['image']
            self.displaySurface.blit(surface, (self.NEXTX, self.NEXTY)) 
            if self.PREPAREDPUZZLES[0]['tour'] == -10:
                self.DELETEPUZZLE = True         
            
        else: # wyswietlenie konca puzli
            surface = pygame.image.load('utilities\end.png')
            self.displaySurface.blit(surface, (self.NEXTX, self.NEXTY))         
        
             
        # losowanie kafelkow specjalnych do dodania do pozostałych do polozenia, gdy te sa w kolejnym obiegu
        if gameMode == 'Classic': 
            if self.PREPAREDPUZZLES is not None:
                if(self.PREPAREDPUZZLES[0]['tour'] > self.TOUR):
                    trashFactor = objState.getTrashFactor()
                    drawNewPuzzles(self, self.drawIterator, trashFactor, gameMode)
                    self.TOUR += 1
                    self.drawIterator += 100
                    ###
                    #print('Tura' + str(self.TOUR))
                    ###
        elif gameMode == 'Continuous':
            if self.REST <= 2:
                trashFactor = objState.getTrashFactor()
                drawNewPuzzles(self, self.drawIterator, trashFactor, gameMode)
        


    # napis 'Press p to pause'
    def pauseText(self):
        font = pygame.font.Font(self.FONTNAME, 26)    
        textSurf = font.render('Press \'p\' to pause', True, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = ( self.NEXTX + 50, self.HEIGHT - self.BOARDY + 40)
        self.displaySurface.blit(textSurf, textRect)      
    
    # odblokowanie pauzy    
    def unpause(self):
        self.PAUSE = False
        stopPause = time.time()
        return stopPause
    
    # obsluga pauzy
    def paused(self):
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
                        
            # napis 'Press p to continue'
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
               
    # obsluga przyciskow obecnych w trakcie rozgrywki
    def buttonGameAction(self, msg, objState):
        if msg == 'NewGame':      
            self.NEWGAME = True  

        elif msg == 'BackMenu':
            self.NEWGAME = True
            event = pygame.event.Event(BACK)
            pygame.event.post(event)
                        
        elif msg == 'Quit':
            pygame.quit()
            quit()