import pygame, time

from os import path
from states import GameStates
from colors import*
from dataStorage import getHighScore

class Scoring(object):

    def __init__(self):
        self.CURRENTTIME = time.time()
        self.FIRSTTIMEENTRANCE = True
        self.TIMEBEFORE = 0
        self.SCORE = 0
        
        self.endOfPuzzles = False
        self.endOfCredits = False
    
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
        
        self.endOfPuzzles = False
        self.endOfCredits = False

    def scoringDisplay(self, objParam, objState, gameMode):

        global delay, record

        sizeH = objParam.FONTSIZE
        sizeW = int((200 * objParam.WIDTH) / 1900)
        dist1 = int((35 * objParam.WIDTH) / 1900)
        dist2 = int((15 * objParam.WIDTH) / 1900)        
        punctDistance = objParam.BOARDWITH / 5
        punctX = objParam.BOARDX
        punctY = objParam.BOARDY / 2
        credit = objState.getCredit()
        score = self.SCORE
                
        if gameMode == 'Classic':
            left = objParam.REST   
        elif gameMode == 'Continuous':
            left = '--'
        
        if objParam.REST == 0:
            self.endOfPuzzles = True
        if credit <= 0:
            self.endOfCredits = True
            credit = 0
        
        if self.FIRSTTIMEENTRANCE:
            delay = objParam.STARTTIME - self.CURRENTTIME
            record = getHighScore(objState)
            self.FIRSTTIMEENTRANCE = False

        if not objParam.ENDGAME:    
            elapsedTime = objParam.STARTTIME - self.CURRENTTIME - delay - objParam.PAUSEDTIME  
            self.TIMEBEFORE = elapsedTime
        else:    
            elapsedTime = self.TIMEBEFORE
        
        timez = time.strftime('%H:%M:%S', time.gmtime(elapsedTime))
        
        Scoring.caption(objParam, 'Credits', sizeH, punctX, punctY, sizeW, sizeH, credit) 
        Scoring.caption(objParam, 'Rest', sizeH, punctX + punctDistance + dist1, punctY, sizeW, sizeH, left)     
        Scoring.caption(objParam, 'Time', sizeH, punctX + 2 * punctDistance, punctY, sizeW, sizeH, timez)
        Scoring.caption(objParam, 'Record', sizeH, punctX + 3 * punctDistance + 2*dist1, punctY, sizeW, sizeH, record)        
        Scoring.caption(objParam, 'Score', sizeH, punctX + 4 * punctDistance + 2*dist1 + dist2, punctY, sizeW, sizeH, score)   

        return (score, timez)    

    def endOfPlay(self):
        return (self.endOfPuzzles, self.endOfCredits)
    
    def caption(objParam, msg, fontSize, x, y, w, h, variable):

        text = msg + ':' + str(variable) 
      
        font = pygame.font.Font(objParam.FONTNAME, fontSize)    
        textSurf = font.render(text, True, WHITE)
        textRect = ( ( x, (y + (h/2)) ) )
        objParam.displaySurface.blit(textSurf, textRect)    
