import pygame, time

from parameters import Parameters
from game import Game
from states import GameStates
from button import button

class WelcomeScreen(Parameters):

    def __init__(self):
        super(WelcomeScreen, self).__init__()
     
    def main(self):
        #global clock
        
        pygame.init()   
        pygame.display.set_icon(pygame.image.load('utilities\gameIcon.png'))
        #displaySurface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('MisanthropicPassage') 
        
        #clock = pygame.time.Clock()  
        
        ### pilnowac by byla jedna instancja!
        objState = GameStates() 
        ###
         
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            WelcomeScreen.showTitle(self)
                                         
            if objState.STATE == 'WelcomeMenu':
                if button(self, 'Start',       30, self.BUTTONDISTANCEX, self.HALFHEIGHT - (self.BUTTONHEIGHT + 50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Start', objState)  
                if button(self, 'Difficulty',  30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (self.BUTTONHEIGHT - 50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Difficulty', objState)
                if button(self, 'High Scores', 30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (self.BUTTONHEIGHT + 50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'High Scores', objState)
                if button(self, 'Credits',     30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (2*self.BUTTONHEIGHT + 2*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Credits', objState)
                if button(self, 'Quit',        30, self.BUTTONDISTANCEX, self.HALFHEIGHT + (3*self.BUTTONHEIGHT + 3*50), self.BUTTONWIDTH, self.BUTTONHEIGHT):
                    WelcomeScreen.buttonAction(self, 'Quit', objState)
                
            elif objState.STATE == 'DiffMenu':    
                if button(self, 'Easy',        30, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT - self.BUTTONHEIGHT - 50, self.BUTTONWIDTH, 40):
                    WelcomeScreen.buttonAction(self, 'Easy', objState)
                if button(self, 'Medium',      30, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT, self.BUTTONWIDTH, 40):                    
                    WelcomeScreen.buttonAction(self, 'Medium', objState)
                if button(self, 'Hard',        30, (self.WIDTH - self.BUTTONWIDTH)/2, self.HALFHEIGHT + self.BUTTONHEIGHT + 50, self.BUTTONWIDTH, 40):                     
                    WelcomeScreen.buttonAction(self, 'Hard', objState)
    
            pygame.display.update()
            #clock.tick(15)                                       

    def buttonAction(self, msg, objState):

        if msg == 'Start': 
            objState.setState('Game')
            
            ###pilnowac by byla jedna instancja!
            objGame = Game()
            objGame.runGame(objState)
            ###
     
        elif msg == 'Difficulty':
            objState.setState('DiffMenu')
                        
        elif msg == 'High Scores': #TODO
            #odczytywanie danych z rozgrywki z pliku zewnetrznego
            pass
        
        elif msg == 'Credits': #TODO
            #autorstwo i z czego muzyka
            pass    
                        
        elif msg == 'Quit':
            pygame.quit()
            quit()
                        
        elif msg == 'Easy':
            objState.setDifficulty('Easy')
            objState.setState('WelcomeMenu')
                        
        elif msg == 'Medium':
            objState.setDifficulty('Medium')
            objState.setState('WelcomeMenu')
                        
        elif msg == 'Hard':
            objState.setDifficulty('Hard')
            objState.setState('WelcomeMenu')                

    
if __name__ == '__main__':
    objWelcomeScreen = WelcomeScreen()
    objWelcomeScreen.main() 