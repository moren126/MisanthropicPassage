import pygame

from colors import*


def button(self, msg, fontSize, x, y, w, h):

    mousePosition = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mousePosition[0] > x and y + h > mousePosition[1] > y:
        pygame.draw.rect(self.displaySurface, BUTTONBRIGHT, (x, y, w, h))
            
        if click[0] == 1:
            return True
                    
    else:
        pygame.draw.rect(self.displaySurface, BUTTONCOLOR, (x, y, w, h))

    fontButton = pygame.font.Font(self.FONTNAME, fontSize)    
    textSurfButton = fontButton.render(msg, True, WHITE)
    textRectButton = textSurfButton.get_rect()
    textRectButton.center = ( (x + (w/2)), (y + (h/2)) )
    self.displaySurface.blit(textSurfButton, textRectButton)     

