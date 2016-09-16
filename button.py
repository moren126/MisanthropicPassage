import pygame, time, os

from colors import*

def button(obj, msg, fontSize, x, y, w, h):
    unlightedSurface = pygame.image.load(os.path.join('utilities', 'play.png'))
    lightedSurface = pygame.image.load(os.path.join('utilities', 'play2.png'))
    
    mousePosition = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mousePosition[0] > x and y + h > mousePosition[1] > y:
        #pygame.draw.rect(obj.displaySurface, BUTTONBRIGHT, (x, y, w, h))
        obj.displaySurface.blit(lightedSurface, (x, y))
        
        if click[0] == 1:
            return True              
            
    else:
        #pygame.draw.rect(obj.displaySurface, BUTTONCOLOR, (x, y, w, h))
        obj.displaySurface.blit(unlightedSurface, (x, y))

    fontButton = pygame.font.Font(obj.FONTNAME, fontSize)    
    textSurfButton = fontButton.render(msg, True, WHITE)
    textRectButton = textSurfButton.get_rect()
    textRectButton.center = ( (x + (w/2)), (y + (h/2)) )
    obj.displaySurface.blit(textSurfButton, textRectButton)   
    
def checkButton(obj, msg, fontSize, x, y):
    s = 12
    mousePosition = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + s > mousePosition[0] > x and y + s > mousePosition[1] > y:
        pygame.draw.circle(obj.displaySurface, YELLOW, ( int(x + s/2), int(y + s/4) ), s)
            
        if click[0] == 1:
            return True
                    
    else:
        pygame.draw.circle(obj.displaySurface, WHITE, ( int(x + s/2), int(y + s/4) ), s)

    fontButton = pygame.font.Font(obj.FONTNAME, fontSize)    
    textSurfButton = fontButton.render(msg, True, WHITE)
    textRectButton = ( (x + s + 20), (y - (6/8)*s) )
    obj.displaySurface.blit(textSurfButton, textRectButton)  