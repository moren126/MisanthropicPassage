import pygame, pickle, time
from os import path

from colors import*

def getHighScore(objState):
    
    gameMode = objState.getMode()   
    diff = objState.getDifficulty()    
    dir = path.dirname(__file__)
    content = []
    RECORD = 0
        
    try:   
        file = open( "save.p", "rb" )
        content = pickle.load( file )  
        file.close()

        for i in content:
            if i['mode'] == gameMode and i['diff'] == diff:
                RECORD = i['score']
        
    except:
        el1 = { 'index': 1, 'mode': 'Classic', 'score': 0, 'time': '--', 'diff': 'Easy', 'date': '--' }
        el2 = { 'index': 2, 'mode': 'Classic', 'score': 0, 'time': '--', 'diff': 'Medium', 'date': '--' }
        el3 = { 'index': 3, 'mode': 'Classic', 'score': 0, 'time': '--', 'diff': 'Hard', 'date': '--' }
        el4 = { 'index': 4, 'mode': 'Continuous', 'score': 0, 'time': '--', 'diff': 'Easy', 'date': '--' }
        el5 = { 'index': 5, 'mode': 'Continuous', 'score': 0, 'time': '--', 'diff': 'Medium', 'date': '--' }
        el6 = { 'index': 6, 'mode': 'Continuous', 'score': 0, 'time': '--', 'diff': 'Hard', 'date': '--' } 
        content.extend( [el1, el2, el3, el4, el5, el6] ) 
        file = open( "save.p", "wb" )
        pickle.dump( content, file ) 
        file.close()
        RECORD = 0 
        
    return RECORD    

def store(objState, gameResult):

    gameMode = objState.getMode()
    diff = objState.getDifficulty()
    dir = path.dirname(__file__)
    file = open( "save.p", "rb" )
    content = pickle.load( file )
    file.close()    
    RECORD = 0 
    t = time.time()
    date = time.strftime("%d %b %Y", time.gmtime(t))
                
    for i in content:
        if i['mode'] == gameMode and i['diff'] == diff:
            RECORD = i['score']
            temp = i['index']
                           
    if gameResult[0] > int(RECORD):  
        #content[:] = [d for d in content if d.get('index') != temp] 
        for i in content:
            if i['index'] == temp:
                i['score'] = gameResult[0]
                i['time'] = gameResult[1]
                i['date'] = date

        #content = { 'mode': gameMode, 'score': gameResult[0], 'time': gameResult[1], 'diff': diff }
        
        file = open( "save.p", "wb" )
        pickle.dump( content, file )
        file.close()
        
def showHighScore(params):

    size = int((250 * params.WIDTH) / 1900)
    sizeW = int((50 * params.WIDTH) / 1900)
    fontB = int((60 * params.WIDTH) / 1900)
    fontS = int((40 * params.WIDTH) / 1900)
    
    captionWithSize(params, 'Meaningless High Scores', params.HALFWIDTH, params.HALFHEIGHT - 4 * sizeW, fontB, 0) 
   
    captionWithSize(params, 'Mode', params.HALFWIDTH - 2*size, params.HALFHEIGHT - 2*sizeW, fontS, 1)
    captionWithSize(params, 'Difficulty', params.HALFWIDTH - size, params.HALFHEIGHT - 2*sizeW, fontS, 1)
    captionWithSize(params, 'Score', params.HALFWIDTH, params.HALFHEIGHT - 2*sizeW, fontS, 1)
    captionWithSize(params, 'Time', params.HALFWIDTH + size, params.HALFHEIGHT - 2*sizeW, fontS, 1)
    captionWithSize(params, 'Date', params.HALFWIDTH + 2*size, params.HALFHEIGHT - 2*sizeW, fontS, 1)    
    
    listOfContents = []
    dir = path.dirname(__file__)
        
    try:     
        file = open( "save.p", "rb" )
        listOfContents = pickle.load( file ) 
        file.close()    
    except:
        el1 = { 'index': 1, 'mode': 'Classic', 'score': 0, 'time': '--', 'diff': 'Easy', 'date': '--' }
        el2 = { 'index': 2, 'mode': 'Classic', 'score': 0, 'time': '--', 'diff': 'Medium', 'date': '--' }
        el3 = { 'index': 3, 'mode': 'Classic', 'score': 0, 'time': '--', 'diff': 'Hard', 'date': '--' }
        el4 = { 'index': 4, 'mode': 'Continuous', 'score': 0, 'time': '--', 'diff': 'Easy', 'date': '--' }
        el5 = { 'index': 5, 'mode': 'Continuous', 'score': 0, 'time': '--', 'diff': 'Medium', 'date': '--' }
        el6 = { 'index': 6, 'mode': 'Continuous', 'score': 0, 'time': '--', 'diff': 'Hard', 'date': '--' } 
        listOfContents.extend( [el1, el2, el3, el4, el5, el6] )        
        
    for i in listOfContents:
        if i['mode'] == 'Classic' and i['diff'] == 'Easy':
            caption(params, str(i['mode']), params.HALFWIDTH - 2*size, params.HALFHEIGHT - sizeW)
            caption(params, str(i['diff']), params.HALFWIDTH - size, params.HALFHEIGHT - sizeW)
            caption(params, str(i['score']), params.HALFWIDTH, params.HALFHEIGHT - sizeW)
            caption(params, str(i['time']), params.HALFWIDTH + size, params.HALFHEIGHT - sizeW)
            caption(params, str(i['date']), params.HALFWIDTH + 2*size, params.HALFHEIGHT - sizeW)   
    #for i in listOfContents:        
        if i['mode'] == 'Classic' and i['diff'] == 'Medium':
            caption(params, str(i['mode']), params.HALFWIDTH - 2*size, params.HALFHEIGHT)
            caption(params, str(i['diff']), params.HALFWIDTH - size, params.HALFHEIGHT)
            caption(params, str(i['score']), params.HALFWIDTH, params.HALFHEIGHT)
            caption(params, str(i['time']), params.HALFWIDTH + size, params.HALFHEIGHT)
            caption(params, str(i['date']), params.HALFWIDTH + 2*size, params.HALFHEIGHT)            
    #for i in listOfContents:        
        if i['mode'] == 'Classic' and i['diff'] == 'Hard':
            caption(params, str(i['mode']), params.HALFWIDTH - 2*size, params.HALFHEIGHT + sizeW)
            caption(params, str(i['diff']), params.HALFWIDTH - size, params.HALFHEIGHT + sizeW)
            caption(params, str(i['score']), params.HALFWIDTH, params.HALFHEIGHT + sizeW)
            caption(params, str(i['time']), params.HALFWIDTH + size, params.HALFHEIGHT + sizeW) 
            caption(params, str(i['date']), params.HALFWIDTH + 2*size, params.HALFHEIGHT + sizeW)            
        ###  
    #for i in listOfContents:    
        if i['mode'] == 'Continuous' and i['diff'] == 'Easy':
            caption(params, str(i['mode']), params.HALFWIDTH - 2*size, params.HALFHEIGHT + 2*sizeW)
            caption(params, str(i['diff']), params.HALFWIDTH - size, params.HALFHEIGHT + 2*sizeW)
            caption(params, str(i['score']), params.HALFWIDTH, params.HALFHEIGHT + 2*sizeW)
            caption(params, str(i['time']), params.HALFWIDTH + size, params.HALFHEIGHT + 2*sizeW)
            caption(params, str(i['date']), params.HALFWIDTH + 2*size, params.HALFHEIGHT + 2*sizeW)
    #for i in listOfContents:        
        if i['mode'] == 'Continuous' and i['diff'] == 'Medium':
            caption(params, str(i['mode']), params.HALFWIDTH - 2*size, params.HALFHEIGHT + 3*sizeW)
            caption(params, str(i['diff']), params.HALFWIDTH - size, params.HALFHEIGHT + 3*sizeW)
            caption(params, str(i['score']), params.HALFWIDTH, params.HALFHEIGHT + 3*sizeW)
            caption(params, str(i['time']), params.HALFWIDTH + size, params.HALFHEIGHT + 3*sizeW)
            caption(params, str(i['date']), params.HALFWIDTH + 2*size, params.HALFHEIGHT + 3*sizeW)            
    #for i in listOfContents:        
        if i['mode'] == 'Continuous' and i['diff'] == 'Hard':
            caption(params, str(i['mode']), params.HALFWIDTH - 2*size, params.HALFHEIGHT + 4*sizeW)
            caption(params, str(i['diff']), params.HALFWIDTH - size, params.HALFHEIGHT + 4*sizeW)
            caption(params, str(i['score']), params.HALFWIDTH, params.HALFHEIGHT + 4*sizeW)
            caption(params, str(i['time']), params.HALFWIDTH + size, params.HALFHEIGHT + 4*sizeW) 
            caption(params, str(i['date']), params.HALFWIDTH + 2*size, params.HALFHEIGHT + 4*sizeW)            

def caption(params, msg, x, y):
    fontButton = pygame.font.Font(params.FONTNAME, params.FONTSIZE)    
    textSurfButton = fontButton.render(msg, True, WHITE)
    textRectButton = textSurfButton.get_rect()
    textRectButton.center = (x, y)
    params.displaySurface.blit(textSurfButton, textRectButton) 

def captionWithSize(params, msg, x, y, size, underline):
    fontButton = pygame.font.Font(params.FONTNAME, size)    
    fontButton.set_underline(underline)
    textSurfButton = fontButton.render(msg, True, WHITE)
    textRectButton = textSurfButton.get_rect()
    textRectButton.center = (x, y)
    params.displaySurface.blit(textSurfButton, textRectButton)     