"""
info do mnie z przyszlosci:
- jesli kiedys zmieni sie liczba kolorow, wzorow to tu poprawic
- 'tour': -10 dla kafelkow kosza i 'tour': -19 dla kafelkow specjalnych because of reasons 
"""

import pygame, random

from PIL import Image
from randoms import createRandoms, addSpecjalOrNot


def createIterators(): 
    iterators = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160] 
    return iterators
    
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

def prepareSpecialPuzzlesSameColor(iteratorStarter, colorRange, nameFragment, angle, colorUexists, colorRexists, colorDexists, colorLexists):
    puzzles = []
    
    if angle == 90:
        nameFragmentAfter = 'l'
    elif angle == 180:
        nameFragmentAfter = 'd'
    elif angle == 270:    
        nameFragmentAfter = 'r'   

    for i in range(colorRange):  

        if colorUexists:
            colorU = i
        else:
            colorU = 'neutral'
            
        if colorRexists:
            colorR = i
        else:
            colorR = 'neutral'
            
        if colorDexists:
            colorD = i
        else:
            colorD = 'neutral'
            
        if colorLexists:
            colorL = i
        else:
            colorL = 'neutral'            
 
        pfileName = 'utilities\spec' + str(nameFragment) + 'u0' + str(i) + '.png' 
        
        if angle == 0:
            pimage = pygame.image.load(pfileName)
        else:
            pimage0 = Image.open(pfileName)
            pimage1 = pimage0.rotate(angle)
            pfileName2 = 'utilities\spec' + str(nameFragment) + str(nameFragmentAfter) + '0' + str(i) + '.png' 
            pimage1.save(pfileName2)
            pimage = pygame.image.load(pfileName2)        
          
        objSpecPuzzle = {'pattern': iteratorStarter,
                         'colorU': colorU,
                         'colorR': colorR,
                         'colorD': colorD,
                         'colorL': colorL,
                         'tour': -19,
                         'image': pimage}
        puzzles.append(objSpecPuzzle)
        
        iteratorStarter -= 1
        
    return puzzles        

def prepareSpecialPuzzlesDiff3Colors(iteratorStarter, colorRange, nameFragment, angle):
    puzzles = []
    
    if angle == 90:
        nameFragmentAfter = 'l'
    elif angle == 180:
        nameFragmentAfter = 'd'
    elif angle == 270:    
        nameFragmentAfter = 'r'   

    for i in range(colorRange):  

        j = i + 1
        k = i + 2
        
        if i == 4: #colorRange - 2:
            k = 0 #(colorRange - 1) % (colorRange - 1)     
        elif i == 5: #colorRange - 1:  
            j = 0 #(colorRange - 1) % (colorRange - 1)     
            k = 1 #(colorRange - 1) % (colorRange - 2)            
    
        if angle == 0:
            colorU = 'neutral'
            colorR = j
            colorD = k
            colorL = i             

        elif angle == 90:
            colorU = j
            colorR = k
            colorD = i
            colorL = 'neutral'                
            
        elif angle == 180:
            colorU = k
            colorR = i
            colorD = 'neutral'
            colorL = j  
   
        elif angle == 270:
            colorU = i
            colorR = 'neutral'
            colorD = j
            colorL = k              
         
 
        pfileName = 'utilities\spec' + str(nameFragment) + 'u0' + str(i) + '.png' 
        
        if angle == 0:
            pimage = pygame.image.load(pfileName)
        else:
            pimage0 = Image.open(pfileName)
            pimage1 = pimage0.rotate(angle)
            pfileName2 = 'utilities\spec' + str(nameFragment) + str(nameFragmentAfter) + '0' + str(i) + '.png' 
            pimage1.save(pfileName2)
            pimage = pygame.image.load(pfileName2)        
          
        objSpecPuzzle = {'pattern': iteratorStarter,
                         'colorU': colorU,
                         'colorR': colorR,
                         'colorD': colorD,
                         'colorL': colorL,
                         'tour': -19,
                         'image': pimage}
        puzzles.append(objSpecPuzzle)
        
        iteratorStarter -= 1
  
    return puzzles 


def prepareSpecialPuzzlesDiff2Colors(iteratorStarter, colorRange, nameFragment, angle):
    puzzles = []
    
    if angle == 90:
        nameFragmentAfter = 'sl'
    elif angle == 180:
        nameFragmentAfter = 'sd'
    elif angle == 270:    
        nameFragmentAfter = 'sr'   

    for i in range(colorRange):  

        j = i + 1

        if i == 5: #colorRange - 1:  
            j = 0 #(colorRange - 1) % (colorRange - 1)      
    
        if angle == 0:
            colorU = 'neutral'
            colorR = j
            colorD = 'neutral'
            colorL = i             
            
        elif angle == 90:
            colorU = j
            colorR = 'neutral'
            colorD = i
            colorL = 'neutral'  
            
        elif angle == 180:
            colorU = 'neutral'
            colorR = i
            colorD = 'neutral'
            colorL = j  
            
        elif angle == 270:
            colorU = i
            colorR = 'neutral'
            colorD = j
            colorL = 'neutral'             
 
        pfileName = 'utilities\spec' + str(nameFragment) + 's0' + str(i) + '.png' 
        
        if angle == 0:
            pimage = pygame.image.load(pfileName)
        else:
            pimage0 = Image.open(pfileName)
            pimage1 = pimage0.rotate(angle)
            pfileName2 = 'utilities\spec' + str(nameFragment) + str(nameFragmentAfter) + '0' + str(i) + '.png' 
            pimage1.save(pfileName2)
            pimage = pygame.image.load(pfileName2)        
          
        objSpecPuzzle = {'pattern': iteratorStarter,
                         'colorU': colorU,
                         'colorR': colorR,
                         'colorD': colorD,
                         'colorL': colorL,
                         'tour': -19,
                         'image': pimage}
        puzzles.append(objSpecPuzzle)
        
        iteratorStarter -= 1
        
    return puzzles 
  
def createDeletePuzzles(howMany):
    deletePuzzles = []
    dimage = pygame.image.load('utilities\delete.png') 
    
    ### kafelki z koszem
    for i in range(howMany):    
        objDelPuzzle = {'pattern': 'nevermind',
                         'colorU': 'nevermind',
                         'colorR': 'nevermind',
                         'colorD': 'nevermind',
                         'colorL': 'nevermind',
                         'tour': -10,
                         'image': dimage}
        deletePuzzles.append(objDelPuzzle) 
    
    return deletePuzzles    
  
def createSpecialPuzzles(iteratorStarters, trashFactor):
    specialPuzzles = []
      
    # 1. 1 pole - 1/4
    onecolor1 = prepareSpecialPuzzlesSameColor(iteratorStarters[0], 6, 3, 0, False, False, True, False)
    specialPuzzles.extend(onecolor1)
        
    # 2. 1 pole - 2/4 - obrot w lewo 90
    onecolor2 = prepareSpecialPuzzlesSameColor(iteratorStarters[1], 6, 3, 90, False, True, False, False)
    specialPuzzles.extend(onecolor2)    
       
    # 3. 1 pole - 3/4 - obrot w lewo 180
    onecolor3 = prepareSpecialPuzzlesSameColor(iteratorStarters[2], 6, 3, 180, True, False, False, False)
    specialPuzzles.extend(onecolor3)      
    
    # 4. 1 pole - 4/4 - obrot w lewo 270
    onecolor4 = prepareSpecialPuzzlesSameColor(iteratorStarters[3], 6, 3, 270, False, False, False, True)
    specialPuzzles.extend(onecolor4)  
    
 
    # 5. 2 pola obok - 1/4
    twocolors1 = prepareSpecialPuzzlesSameColor(iteratorStarters[4], 6, 2, 0, False, False, True, True)
    specialPuzzles.extend(twocolors1)
        
    # 6. 2 pola obok - 2/4
    twocolors2 = prepareSpecialPuzzlesSameColor(iteratorStarters[5], 6, 2, 90, False, True, True, False)
    specialPuzzles.extend(twocolors2)    
       
    # 6. 2 pola obok - 3/4
    twocolors3 = prepareSpecialPuzzlesSameColor(iteratorStarters[6], 6, 2, 180, True, True, False, False)
    specialPuzzles.extend(twocolors3)      
    
    # 8. 2 pola obok - 4/4
    twocolors4 = prepareSpecialPuzzlesSameColor(iteratorStarters[7], 6, 2, 270, True, False, False, True)
    specialPuzzles.extend(twocolors4)     

    
    # 9. 3 rozne pola obok - 1/4
    threecolors1 = prepareSpecialPuzzlesDiff3Colors(iteratorStarters[8], 6, 1, 0)   
    specialPuzzles.extend(threecolors1)
    
    # 10. 3 rozne pola obok - 2/4
    threecolors2 = prepareSpecialPuzzlesDiff3Colors(iteratorStarters[9], 6, 1, 90)   
    specialPuzzles.extend(threecolors2) 

    # 11. 3 rozne pola obok - 3/4
    threecolors3 = prepareSpecialPuzzlesDiff3Colors(iteratorStarters[10], 6, 1, 180)   
    specialPuzzles.extend(threecolors3)     
    
    # 12. 3 rozne pola obok - 4/4
    threecolors4 = prepareSpecialPuzzlesDiff3Colors(iteratorStarters[11], 6, 1, 270)   
    specialPuzzles.extend(threecolors4) 
    
    
    # 13. 2 pola naprzeciw - 1/4
    twocolors5 = prepareSpecialPuzzlesDiff2Colors(iteratorStarters[12], 6, 2, 0)
    specialPuzzles.extend(twocolors5)  

    # 14. 2 pola naprzeciw - 2/4
    twocolors6 = prepareSpecialPuzzlesDiff2Colors(iteratorStarters[13], 6, 2, 90)
    specialPuzzles.extend(twocolors6)    

    # 15. 2 pola naprzeciw - 3/4
    twocolors7 = prepareSpecialPuzzlesDiff2Colors(iteratorStarters[14], 6, 2, 180)
    specialPuzzles.extend(twocolors7) 

    # 16. 2 pola naprzeciw - 4/4
    twocolors8 = prepareSpecialPuzzlesDiff2Colors(iteratorStarters[15], 6, 2, 270)
    specialPuzzles.extend(twocolors8)      

    # 17. kosze
    lengthUntilNow = len(specialPuzzles)
    trashNumber = int (trashFactor * lengthUntilNow)
    trash = createDeletePuzzles(trashNumber)
    specialPuzzles.extend(trash) 
       
    random.shuffle(specialPuzzles)
    return specialPuzzles  


def createPreparedPuzzles(objParam, trashFactor, iteratorJump):   
    mixed = []
    ordinary = createOrdinaryPuzzles(objParam) #objParam.REST tu jt 
    iteratorStarters = createIterators()
    
    if iteratorJump > 0:
        newIteratorStarters = [i+iteratorJump for i in iteratorStarters]
        special = createSpecialPuzzles(newIteratorStarters, trashFactor)
    else:
        special = createSpecialPuzzles(iteratorStarters, trashFactor)
    
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
    
def drawNewPuzzles(objParam, iteratorJump, trashFactor, mode):   
    left = objParam.REST
    
    if mode == 'Classic':

        iteratorStarters = createIterators()
        newIteratorStarters = [i+iteratorJump for i in iteratorStarters]
        
        sthToChoose = createSpecialPuzzles(newIteratorStarters, trashFactor)
         
        if left > 1:
            for i in range(1, left):
                temp = objParam.PREPAREDPUZZLES.pop(i)
                
                if addSpecjalOrNot(0.5):
                    if not bool(sthToChoose): # jesli lista slownikow jt pusta
                        [i+iteratorJump for i in newIteratorStarters]
                        print(newIteratorStarters)   
                        sthToChoose = createSpecialPuzzles(newIteratorStarters, trashFactor)
                        drawIterator += iteratorJump
                    temp2 = sthToChoose.pop(0)
                    objParam.PREPAREDPUZZLES.insert(i, temp2) 
                    objParam.PREPAREDPUZZLES.insert(i + 1, temp)
                else:    
                    objParam.PREPAREDPUZZLES.insert(i, temp)    
                
        elif left == 1:
            if not bool(sthToChoose): # jesli lista slownikow jt pusta
                sthToChoose = createSpecialPuzzles(newIteratorStarters, trashFactor)
            temp2 = sthToChoose.pop(0)
            objParam.PREPAREDPUZZLES.append(temp2)
            
    elif mode == 'Continuous':
    
        if left == 2:
            newPuzzles = createPreparedPuzzles(objParam, trashFactor, iteratorJump)
            objParam.PREPAREDPUZZLES.extend(newPuzzles)