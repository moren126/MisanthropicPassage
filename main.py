import pygame, time, os

from parameters import Parameters
from colors import*
from states import GameStates
from game import Game
from button import button, checkButton
from dataStorage import store, showHighScore

from scoringDisplay import Scoring

class WelcomeScreen(Parameters):

    def __init__(self):
        super(WelcomeScreen, self).__init__()
        self.WELCOMEMENU = True
        self.DIFFMENU = False
        self.SCOREMENU = False

    def main(self):        
        pygame.init()   
        
        # ikona
        pygame.display.set_icon(pygame.image.load('utilities\icon.png'))
        
        # tytul okna
        pygame.display.set_caption('PPassage') 

        # obiekt odpowiedzialny za stan gry i poziom trudnosci
        objState = GameStates() 

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            # tytul gry na glownym ekranie    
            WelcomeScreen.showTitle(self)
                  
            # przyciski        
            if objState.STATE == 'WelcomeMenu' and self.WELCOMEMENU: 
                if button(self, 'Start', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY - (3*self.BUTTONHEIGHT + 3*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Start', objState)
                if button(self, 'Difficulty', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY - (2*self.BUTTONHEIGHT + 2*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Difficulty', objState)
                if button(self, 'High Scores', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY -  (self.BUTTONHEIGHT + 50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'HighScores', objState)
                if button(self, 'Quit', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY, self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Quit', objState)
                
            elif objState.STATE == 'DiffMenu' and self.DIFFMENU: 
            
                # napis 'Difficulty'
                font = pygame.font.Font(self.FONTNAME, self.FONTSIZE+10)    
                textSurf = font.render('Difficulty', True, WHITE)
                textRect = textSurf.get_rect()
                textRect.center = ( self.HALFWIDTH, self.HALFHEIGHT - self.BUTTONHEIGHT - 100 )
                self.displaySurface.blit(textSurf, textRect)  
            
                if button(self, 'Easy',         self.FONTSIZE, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT - self.BUTTONHEIGHT - 50, self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Easy', objState)
                if button(self, 'Medium',       self.FONTSIZE, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT, self.BUTTONWIDTH, self.BUTTONHEIGHT):                    
                    WelcomeScreen.buttonAction(self, 'Medium', objState)
                if button(self, 'Hard',         self.FONTSIZE, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT + self.BUTTONHEIGHT + 50, self.BUTTONWIDTH, self.BUTTONHEIGHT):                     
                    WelcomeScreen.buttonAction(self, 'Hard', objState)
                if button(self, 'Back to menu', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY, self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'BackMenu', objState)

                # napis 'Mode'
                font = pygame.font.Font(self.FONTNAME, self.FONTSIZE+2)    
                textSurf = font.render('Mode', True, WHITE)
                textRect = ( (self.HALFWIDTH + self.HALFWIDTH/2 + 12 + 20), (self.HALFHEIGHT - 75) )
                self.displaySurface.blit(textSurf, textRect)  
                
                if checkButton(self, 'Classic', self.FONTSIZE, self.HALFWIDTH + self.HALFWIDTH/2, self.HALFHEIGHT ):
                    WelcomeScreen.buttonAction(self, 'Classic', objState) 
                if checkButton(self, 'Continuous', self.FONTSIZE, self.HALFWIDTH + self.HALFWIDTH/2, self.HALFHEIGHT + 50):
                    WelcomeScreen.buttonAction(self, 'Continuous', objState)     
                
                mode = objState.getMode()
                if mode == 'Classic':      
                    WelcomeScreen.drawCheckBox(self, self.HALFWIDTH + self.HALFWIDTH/2, self.HALFHEIGHT )       
                elif mode == 'Continuous':  
                    WelcomeScreen.drawCheckBox(self, self.HALFWIDTH + self.HALFWIDTH/2, self.HALFHEIGHT + 50)                

                diff = objState.getDifficulty()    
                if diff == 'Easy':
                    WelcomeScreen.drawselectedButton(self, 'Easy', self.FONTSIZE+2, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT - self.BUTTONHEIGHT - 50, self.BUTTONWIDTH, self.BUTTONHEIGHT)
                elif diff == 'Medium':
                    WelcomeScreen.drawselectedButton(self, 'Medium', self.FONTSIZE+2, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT, self.BUTTONWIDTH, self.BUTTONHEIGHT)
                elif diff == 'Hard':
                    WelcomeScreen.drawselectedButton(self, 'Hard', self.FONTSIZE+2, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT + self.BUTTONHEIGHT + 50, self.BUTTONWIDTH, self.BUTTONHEIGHT)  
                else:
                    print('Wrong DIFFICULTY name')
    
            elif objState.STATE == 'ScoreMenu' and self.SCOREMENU:   
                # wyswietla osiagniete wyniki 
                showHighScore(self)

                if button(self, 'Back to menu', self.FONTSIZE, self.BUTTONDISTANCEX, self.BUTTONDOWNY, self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'BackMenu', objState)    
    
    
            pygame.display.update()                                    

    # obsluga przyciskow z glownego menu        
    def buttonAction(self, msg, objState):

        if msg == 'Start': 
            time.sleep(0.2)
            #self.WELCOMEMENU = False
            objState.setState('Game')

            # obiekt odpowiedzialny za rozgrywke
            objGame = Game()
            objGame.runGame(objState)
            ###
            #someScoringObj = Scoring()
            #someScoringObj.setScoring('noCumulation')
     
        elif msg == 'Difficulty':
            time.sleep(0.2)
            self.WELCOMEMENU = False
            self.DIFFMENU = True
            objState.setState('DiffMenu')
                        
        elif msg == 'HighScores':
            time.sleep(0.2)
            self.WELCOMEMENU = False
            self.SCOREMENU = True
            objState.setState('ScoreMenu')
                         
        elif msg == 'Quit':
            pygame.quit()
            quit()
  
        elif msg == 'BackMenu':
            time.sleep(0.2)
            self.WELCOMEMENU = True
            self.DIFFMENU = False
            self.SCOREMENU = False
            objState.setState('WelcomeMenu')
            
        elif msg == 'Easy':
            time.sleep(0.2)
            objState.setDifficulty('Easy')
                        
        elif msg == 'Medium':
            time.sleep(0.2)
            objState.setDifficulty('Medium')
                        
        elif msg == 'Hard':
            time.sleep(0.2)
            objState.setDifficulty('Hard')            

        elif msg == 'Classic':
            time.sleep(0.2)
            objState.setMode('Classic')

        elif msg == 'Continuous':
            time.sleep(0.2)
            objState.setMode('Continuous')
    
    def drawCheckBox(self, x, y):
        circleRadius = 12
        pointRadius = 4
        pygame.draw.circle(self.displaySurface, WHITE, ( int(x + circleRadius/2), int(y + circleRadius/4) ), circleRadius)
        pygame.draw.circle(self.displaySurface, BLACK, ( int(x + circleRadius/2), int(y + circleRadius/4) ), pointRadius)  
        
    def drawselectedButton(self, msg, fontSize, x, y, w, h):
        #pygame.draw.rect(self.displaySurface, BUTTONBRIGHT, (x, y, w, h) )
        lightedSurface = pygame.image.load(os.path.join('utilities', 'play2.png'))
        self.displaySurface.blit(lightedSurface, (x, y))
        
        fontButton = pygame.font.Font(self.FONTNAME, fontSize)    
        textSurfButton = fontButton.render(msg, True, WHITE)
        textRectButton = textSurfButton.get_rect()
        textRectButton.center = ( (x + (w/2)), (y + (h/2)) )
        self.displaySurface.blit(textSurfButton, textRectButton)     
    
if __name__ == '__main__':
    objWelcomeScreen = WelcomeScreen()
    objWelcomeScreen.main() 