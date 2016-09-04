import pygame, time

from states import GameStates
from colors import*

class Scoring(object):

    def __init__(self):
        self.CURRENTTIME = time.time()
        self.FIRSTTIMEENTRANCE = True
        self.TIMEBEFORE = 0
        self.SCORE = 0

    def setScoring(self, mode):
    
        #jesli kumulacja wyniku to nie zerowac SCORE
        if mode == 'noCumulation':
            self.CURRENTTIME = time.time()
            self.FIRSTTIMEENTRANCE = True
            self.TIMEBEFORE = 0
            self.SCORE = 0
        elif mode == 'cumulation':
            self.CURRENTTIME = time.time()
            self.FIRSTTIMEENTRANCE = True
            self.TIMEBEFORE = 0        
        
    def scoringDisplay(self, objParam, objState, startTime):

        global delay
         
        punctDistance = objParam.BOARDWITH / 5
        punctX = objParam.BOARDX
        punctY = objParam.BOARDY / 2
        credit = objState.getCredit()
        left = objParam.REST
        score = self.SCORE
        
        if self.FIRSTTIMEENTRANCE:
            delay = startTime - self.CURRENTTIME
            self.FIRSTTIMEENTRANCE = False

        if not objParam.WIN:    
            elapsedTime = startTime - self.CURRENTTIME - delay - objParam.PAUSEDTIME  
            self.TIMEBEFORE = elapsedTime
        else:    
            elapsedTime = self.TIMEBEFORE
        
        timez = time.strftime('%H:%M:%S', time.gmtime(elapsedTime))
        
        Scoring.caption(objParam, 'Credits', 30, punctX, punctY, 200, 30, credit) 
        Scoring.caption(objParam, 'Rest', 30, punctX + punctDistance + 35, punctY, 200, 30, left)     
        Scoring.caption(objParam, 'Time', 30, punctX + 2 * punctDistance, punctY, 200, 30, timez)
        Scoring.caption(objParam, 'Record', 30, punctX + 3 * punctDistance + 70, punctY, 200, 30, 'dupa')        
        Scoring.caption(objParam, 'Score', 30, punctX + 4 * punctDistance + 90, punctY, 200, 30, score)     


    def caption(objParam, msg, fontSize, x, y, w, h, variable):

        text = msg + ':' + str(variable) 
      
        font = pygame.font.Font(objParam.FONTNAME, fontSize)    
        textSurf = font.render(text, True, WHITE)
        textRect = ( ( x, (y + (h/2)) ) )
        objParam.displaySurface.blit(textSurf, textRect)    
