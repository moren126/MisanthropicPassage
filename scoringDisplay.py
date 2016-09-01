import pygame, time

from states import GameStates
from colors import*

currentTime = time.time()

def scoringDisplay(self, objState, startTime):

    global delay
     
    punctDistance = self.BOARDWITH / 5
    punctX = self.BOARDX
    punctY = self.BOARDY / 2
    credit = objState.getCredit()
    score = self.SCORE
    
    if self.FIRSTTIMEENTRANCE:
        delay = startTime - currentTime
        self.FIRSTTIMEENTRANCE = False

    elapsedTime = startTime - currentTime - delay - self.PAUSEDTIME  
    timez = time.strftime('%H:%M:%S', time.gmtime(elapsedTime))
    
    caption(self, 'Credits', 30, punctX, punctY, 200, 30, credit) 
    caption(self, 'Rest', 30, punctX + punctDistance + 35, punctY, 200, 30, self.REST)     
    caption(self, 'Time', 30, punctX + 2 * punctDistance, punctY, 200, 30, timez)
    caption(self, 'Record', 30, punctX + 3 * punctDistance + 70, punctY, 200, 30, 'dupa')        
    caption(self, 'Score', 30, punctX + 4 * punctDistance + 90, punctY, 200, 30, score)     


def caption(self, msg, fontSize, x, y, w, h, variable):

    text = msg + ':' + str(variable) 
  
    font = pygame.font.Font(self.FONTNAME, fontSize)    
    textSurf = font.render(text, True, WHITE)
    textRect = ( ( x, (y + (h/2)) ) )
    self.displaySurface.blit(textSurf, textRect)    
  