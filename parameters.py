import pygame, tkinter, os

from colors import*

class Parameters(object):

    def __init__(self):
    
        #parametry
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'          #okno na srodku ekranu
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = '10, 30'   #okno w lewym gornym rogu 
        
        root = tkinter.Tk()
        self.WIDTH = root.winfo_screenwidth() - 20
        self.HEIGHT = root.winfo_screenheight() - 80
        self.HALFWIDTH = int(self.WIDTH / 2)
        self.HALFHEIGHT = int(self.HEIGHT / 2) 
           
        self.displaySurface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        #parametry planszy
        self.BOARDWITH = int(0.63158 * self.WIDTH)  #1200
        self.BOARDHEIGHT = int(0.8 * self.HEIGHT)  #800
        self.BOARDX = (self.WIDTH - self.BOARDWITH) / 2 
        self.BOARDY = (self.HEIGHT - self.BOARDHEIGHT) / 2 + 25
        
        
        self.PUZZLESIZE = int(self.BOARDHEIGHT/8)
        

        #odleglosc miedzy przyciskami
        self.BUTTONWIDTH = int(0.12632 * self.WIDTH) #240
        self.BUTTONHEIGHT = int(0.05 * self.HEIGHT)  #50
        self.BUTTONDISTANCEX = int(((self.WIDTH - self.BOARDWITH) /2 - self.BUTTONWIDTH ) / 2)
        self.BUTTONDISTANCEH = int((self.HALFHEIGHT - 125 - 4 * 40)/2)
        
        self.BUTTONDOWNY = self.HEIGHT - self.BOARDY
        
        self.FONTNAME = 'utilities\Mechanical.otf'
        self.FONTSIZE = int((30 * self.WIDTH) / 1900)
        self.FONTSIZEMAIN = int((110 * self.WIDTH) / 1900)
        
    def showTitle(self):    
        self.displaySurface.fill(GROUNDCOLOR)
        font = pygame.font.Font(self.FONTNAME, self.FONTSIZEMAIN) 
        textSurf = font.render('Passive-aggressive Passage', True, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = (self.HALFWIDTH, self.HEIGHT - (self.HEIGHT - self.FONTSIZEMAIN))
        self.displaySurface.blit(textSurf, textRect) 

        
if __name__ == '__main__':
    objParameters = Parameters()
    #objParameters.getParameters()         