"""
info do mnie z przyszlosci:
- jesli kiedys zmieni sie liczba kolorow, wzorow to tu poprawic
- 'tour': -10 dla kafelkow kosza i 'tour': -19 dla kafelkow specjalnych because of reasons 
"""

import pygame, random

from PIL import Image
from randoms import createRandoms, addSpecjalOrNot


def createSquares(objParam):
    squares = []
   
    # tworzenie pol, wszystkie ze stanem 'unoccupied'
    for x in range(objParam.COLUMNS):
        for y in range(objParam.ROWS):
            squareObj = {'x': x + 1,
                         'y': y + 1,
                         'startX': objParam.STARTX + x * objParam.SQUARESIZE,
                         'startY': objParam.STARTY + y * objParam.SQUARESIZE,
                         'sState': 'unoccupied'}         
            squares.append(squareObj)
        
    # pola poczatkowe
    for i in squares:
        if i['x'] == objParam.STARTPUZZLEX and i['y'] == objParam.STARTPUZZLEY:
            i['sState'] = 'occupied'
        if (i['x'] == objParam.STARTPUZZLEX - 1 and i['y'] == objParam.STARTPUZZLEY) or (i['x'] == objParam.STARTPUZZLEX + 1 and i['y'] == objParam.STARTPUZZLEY):
            i['sState'] = 'ready'
        if (i['x'] == objParam.STARTPUZZLEX and i['y'] == objParam.STARTPUZZLEY - 1) or (i['x'] == objParam.STARTPUZZLEX and i['y'] == objParam.STARTPUZZLEY + 1):
            i['sState'] = 'ready'    
             
    return squares
  
def charRange(c1, c2):
    # tworzenie char'ow od c1 do c2 wlacznie
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)  
  
def createOrdinaryPuzzles(objParam):
    puzzles = []
   
    # tworzenie 72 kafelkow - 6 kolorow i 12 wzorow
    for i in range(6):    
        for j in charRange('a', 'l'):
            fileName = 'utilities\p' + str(j) + '0' + str(i) + '.png'
            image = pygame.image.load(fileName)
            
            objPuzzle = {'pattern': j,
                         'colorU': i,
                         'colorR': i,
                         'colorD': i,
                         'colorL': i,
                         'tour': 0,
                         'image': image}             
            puzzles.append(objPuzzle) 

    # potrzebne do trybu Classic        
    objParam.REST = len(puzzles) 
    
    random.shuffle(puzzles)
    return puzzles   
    
def createSpecialPuzzles(objParam):
    specialPuzzles = []
    dimage = pygame.image.load('utilities\delete.png') 
    
    # kafelki z koszem
    for i in range(60):    
        objSpecPuzzle = {'pattern': 'nevermind',
                         'colorU': 'nevermind',
                         'colorR': 'nevermind',
                         'colorD': 'nevermind',
                         'colorL': 'nevermind',
                         'tour': -10,
                         'image': dimage}
        specialPuzzles.append(objSpecPuzzle) 
 
 
    #2 pola obok - 1/4
    for i in range(6):    
        pimage = pygame.image.load( ('utilities\spec2u0%s.png' % i) )
          
        objSpecPuzzle = {'pattern': i,
                         'colorU': 'neutral',
                         'colorR': 'neutral',
                         'colorD': i,
                         'colorL': i,
                         'tour': -19,
                         'image': pimage}
        specialPuzzles.append(objSpecPuzzle) 
        
    #2 pola obok - 2/4
    for i in range(6):    
        pimage = Image.open( ('utilities\spec2u0%s.png' % i) )
        pimage2 = pimage.rotate(90)
        pimage2.save( ('utilities\spec2l0%s.png' % i) )
        puzzleImage = pygame.image.load( ('utilities\spec2l0%s.png' % i) )
            
        objSpecPuzzle = {'pattern': i,
                         'colorU': 'neutral',
                         'colorR': i,
                         'colorD': i,
                         'colorL': 'neutral',
                         'tour': -19,
                         'image': puzzleImage}                 
        specialPuzzles.append(objSpecPuzzle)         
    
    #2 pola obok - 3/4
    for i in range(6):    
        pimage = Image.open( ('utilities\spec2u0%s.png' % i) )
        pimage2 = pimage.rotate(180)
        pimage2.save( ('utilities\spec2d0%s.png' % i) )
        puzzleImage = pygame.image.load( ('utilities\spec2d0%s.png' % i) )
            
        objSpecPuzzle = {'pattern': i,
                         'colorU': i,
                         'colorR': i,
                         'colorD': 'neutral',
                         'colorL': 'neutral',
                         'tour': -19,
                         'image': puzzleImage}                 
        specialPuzzles.append(objSpecPuzzle)      

    #2 pola obok - 4/4
    for i in range(6):    
        pimage = Image.open( ('utilities\spec2u0%s.png' % i) )
        pimage2 = pimage.rotate(270)
        pimage2.save( ('utilities\spec2r0%s.png' % i) )
        puzzleImage = pygame.image.load( ('utilities\spec2r0%s.png' % i) )
            
        objSpecPuzzle = {'pattern': i,
                         'colorU': i,
                         'colorR': 'neutral',
                         'colorD': 'neutral',
                         'colorL': i,
                         'tour': -19,
                         'image': puzzleImage}                 
        specialPuzzles.append(objSpecPuzzle)          
  
    random.shuffle(specialPuzzles)
    return specialPuzzles  


def createPreparedPuzzles(objParam):   
    mixed = []
    ordinary = createOrdinaryPuzzles(objParam) #objParam.REST tu jt 
    special = createSpecialPuzzles(objParam)
    
    randoms = createRandoms(72)
    k = 0
    
    ordinaryLength = len(ordinary)

    ###debug    
    #plik = open('puzle.txt', 'w')
    ###
    
    for i in range(ordinaryLength):
        temp = ordinary.pop(0)
        
        if k < len(randoms):
            if i == randoms[k]:
                temp2 = special.pop(0)    
                mixed.append(temp2)            
                k += 1  
                ###            
                #plik.write(str(temp2) + '\n')            
                ### 
        mixed.append(temp)   
        ###            
        #plik.write(str(temp) + '\n')            
        ###         
    ###
    #plik.close()
    ###    
    return mixed
    
def drawNewPuzzles(objParam):   
    left = objParam.REST
    sthToChoose = createSpecialPuzzles(objParam)
    myRange = len(sthToChoose)

    for i in range(1, left):
        temp = objParam.PREPAREDPUZZLES.pop(i)
        
        if addSpecjalOrNot():
            pos = random.randrange(0, myRange)
            temp2 = sthToChoose.pop(pos)
            objParam.PREPAREDPUZZLES.append(temp2)
    
        objParam.PREPAREDPUZZLES.append(temp)   
    
    