import pygame, time

from colors import*

class PuzzleHandler(object):

    def __init__(self, columns, rows, startPuzzleX, startPuzzleY):
        self.COLUMNS = columns
        self.ROWS = rows
        self.STARTPUZZLEX = startPuzzleX
        self.STARTPUZZLEY = startPuzzleY 
        self.ROWFILL = PuzzleHandler.createRowsFill(self)
        self.COLFILL = PuzzleHandler.createColumnsFill(self)
        self.POINT1 = 1
        self.POINT2 = 2
        self.POINT3 = 3
        self.POINT4 = 4
        self.BONUS1 = 20
        self.BONUS2 = 30
        self.BONUS3 = 80
        #self.BONUS = 0
    
    # licznik zapelnienia wierszy    
    def createRowsFill(self):
        p = [0] * self.ROWS
        p.pop(self.STARTPUZZLEY - 1)    
        p.insert((self.STARTPUZZLEY - 1), 1)          
        return p

    # licznik zapelnienia kolumn    
    def createColumnsFill(self):
        p = [0] * self.COLUMNS 
        p.pop(self.STARTPUZZLEX - 1)    
        p.insert((self.STARTPUZZLEX - 1), 1)    
        return p             
    
    # usuwanie pojedynczego kafelka    
    def deletePuzzle(self, objParam, x, y):
        global temp
        
        L = R = U = D = LU = LD = RU = RD = UU = RR = DD = LL = 'nothing'
        uppern = rightn = downn = leftn = False
        
        # znalezienie indeksu kafelka do usuniecia (dlatego indeksy musza byc unikatowe przy tworzeniu list)
        for i in objParam.PLACEDPUZZLES:
            if i['x'] == x and i['y'] == y:
                temp = i['index']
        
        # usuwanie obiektu o znalezionym indeksie    
        if temp is not None:        
            objParam.PLACEDPUZZLES[:] = [d for d in objParam.PLACEDPUZZLES if d.get('index') != temp]
        else:
            #komunikat o niedozwolonym ruchu
            pass

        # aktualizacja licznikow zapelnienia    
        PuzzleHandler.delElementFromCollumn(self, x)    
        PuzzleHandler.delElementFromRow(self, y)     
          
          
        ### wydobywanie 12 stanow pol, ktore trzeba sprawdzic
        for i in objParam.SQUARES: 
            
            # sasiedzi 2-go stopnia, przekatne    
            if i['x'] == x - 1 and i['y'] == y - 1:
                LU = i['sState']
            if i['x'] == x - 1 and i['y'] == y + 1:
                LD = i['sState']
            if i['x'] == x + 1 and i['y'] == y - 1:
                RU = i['sState']
            if i['x'] == x + 1 and i['y'] == y + 1:
                RD = i['sState']
            
            # sasiedzi 2-go stopnia, prostopalde i rownolegle             
            if i['x'] == x and i['y'] == y - 2:
                UU = i['sState']
            if i['x'] == x + 2 and i['y'] == y:
                RR = i['sState']
            if i['x'] == x and i['y'] == y + 2:
                DD = i['sState']
            if i['x'] == x - 2 and i['y'] == y:
                LL = i['sState']    
               
            # sasiedzi 1-go stopnia   
            if i['x'] == x - 1 and i['y'] == y:               
                L = i['sState']
            if i['x'] == x + 1 and i['y'] == y:
                R = i['sState']
            if i['x'] == x and i['y'] == y - 1:
                U = i['sState'] 
            if i['x'] == x and i['y'] == y + 1:
                D = i['sState']           

   
        ### sprawdzanie stanow pol
   
        # lewy sasiad    
        if L == 'occupied':
            leftn = True
        elif L == 'unoccupied':
            leftn = False                    
        elif L == 'ready':
            leftn = False
            if ( LU != 'occupied' and LD != 'occupied' and LL != 'occupied' ):
                L = 'unoccupied'  

        # prawy sasiad            
        if R == 'occupied':
            rightn = True
        elif R == 'unoccupied':
            rightn = False                    
        elif R == 'ready':
            rightn = False
            if ( RU != 'occupied' and RD != 'occupied' and RR != 'occupied' ):
                R = 'unoccupied'  
    
        # gorny sasiad        
        if U == 'occupied':
            uppern = True
        elif U == 'unoccupied':
            uppern = False                    
        elif U == 'ready':
            uppern = False
            if ( LU != 'occupied' and RU != 'occupied' and UU != 'occupied' ):
                U = 'unoccupied'  

        # dolny sasiad    
        if D == 'occupied':
            downn = True
        elif D == 'unoccupied':
            downn = False    
        elif D == 'ready': 
            downn = False
            if ( LD != 'occupied' and RD != 'occupied' and DD != 'occupied' ):
                D = 'unoccupied'              

        
        ### czy byli sasiedzi wokol usuwanego kafelka
        occupiedNeighbor = ( (leftn or rightn) or (uppern or downn) )
            
        ### aktualizacja stanow pol
        for i in objParam.SQUARES: 
        
            # sasiedzi 1-go stopnia   
            if i['x'] == x - 1 and i['y'] == y:               
                i['sState'] = L
            if i['x'] == x + 1 and i['y'] == y:
                i['sState'] = R
            if i['x'] == x and i['y'] == y - 1:
                i['sState'] = U 
            if i['x'] == x and i['y'] == y + 1:
                i['sState'] = D 
                
            # usuwany kafelek            
            if i['x'] == x and i['y'] == y:
                # jesli mial sasiadow stan zmieniony na 'ready'
                if occupiedNeighbor:
                    i['sState'] = 'ready'
                # jesli nie mial sasiadow stan zmieniony na 'unoccupied'    
                else:    
                    i['sState'] = 'unoccupied'
          
        # usuwanie obiektu kosza z PREPAREDPUZZLES     
        objParam.PREPAREDPUZZLES.pop(0)
        
        objParam.DELETEPUZZLE = False        
 
    # usuwanie kolumny lub wiersza
    def deleteColumnOrRow(self, objParam, columnOrRow, pos):

        deletingColumn = deletingRow = False
        
        if columnOrRow == 'x':
            fixedKey = 'x'
            fixedValue = pos
            #changingValue = y
            deletingRange = self.ROWS + 1
            deletingColumn = True
        elif columnOrRow == 'y':
            fixedKey = 'y'
            fixedValue = pos
            #changingValue = x
            deletingRange = self.COLUMNS + 1  
            deletingRow = True    

        # znalezienie wszystkich obiektow z podanej kolumny lub wiersza
        for i in objParam.PLACEDPUZZLES:
            if deletingColumn:
                if i['x'] == fixedValue:
                    x = i['x']
                    y = i['y']
                    # aktualizacja licznikow zapelnienia 
                    PuzzleHandler.delElementFromCollumn(self, x)    
                    PuzzleHandler.delElementFromRow(self, y)  
            elif deletingRow:                    
                if i['y'] == fixedValue:
                    x = i['x']
                    y = i['y']
                    # aktualizacja licznikow zapelnienia 
                    PuzzleHandler.delElementFromCollumn(self, x)    
                    PuzzleHandler.delElementFromRow(self, y)                     

        # usuwanie obiektow o znalezionej kolumnie lub wierszu          
        objParam.PLACEDPUZZLES[:] = [d for d in objParam.PLACEDPUZZLES if d.get(fixedKey) != fixedValue]

        # aktualizacja stanow pol dla kazdego y w zakresie istniejacych rzedow (dla podanego x)
        for changingValue in range(1, deletingRange):
        
            if deletingColumn:
                x = fixedValue
                y = changingValue
            elif deletingRow:          
                x = changingValue
                y = fixedValue        
        
            L = R = U = D = LU = LD = RU = RD = UU = RR = DD = LL = 'nothing'
            uppern = rightn = downn = leftn = False
            
            ### wydobywanie 12 stanow, ktore trzeba sprawdzic
            for i in objParam.SQUARES: 
                
                # sasiedzi 2-go stopnia, przekatne    
                if i['x'] == x - 1 and i['y'] == y - 1:
                    LU = i['sState']
                if i['x'] == x - 1 and i['y'] == y + 1:
                    LD = i['sState']
                if i['x'] == x + 1 and i['y'] == y - 1:
                    RU = i['sState']
                if i['x'] == x + 1 and i['y'] == y + 1:
                    RD = i['sState']
                
                # sasiedzi 2-go stopnia, prostopalde i rownolegle             
                if i['x'] == x and i['y'] == y - 2:
                    UU = i['sState']
                if i['x'] == x + 2 and i['y'] == y:
                    RR = i['sState']
                if i['x'] == x and i['y'] == y + 2:
                    DD = i['sState']
                if i['x'] == x - 2 and i['y'] == y:
                    LL = i['sState']    
                   
                # sasiedzi 1-go stopnia   
                if i['x'] == x - 1 and i['y'] == y:               
                    L = i['sState']
                if i['x'] == x + 1 and i['y'] == y:
                    R = i['sState']
                if i['x'] == x and i['y'] == y - 1:
                    U = i['sState'] 
                if i['x'] == x and i['y'] == y + 1:
                    D = i['sState']           

            ### sprawdzanie stanow
       
            # lewy sasiad    
            if L == 'occupied':
                leftn = True
            elif L == 'unoccupied':
                leftn = False                    
            elif L == 'ready':
                leftn = False
                if ( LU != 'occupied' and LD != 'occupied' and LL != 'occupied' ):
                    L = 'unoccupied'  

            # prawy sasiad            
            if R == 'occupied':
                rightn = True
            elif R == 'unoccupied':
                rightn = False                    
            elif R == 'ready':
                rightn = False
                if ( RU != 'occupied' and RD != 'occupied' and RR != 'occupied' ):
                    R = 'unoccupied'  
        
            # gorny sasiad        
            if U == 'occupied':
                uppern = True
            elif U == 'unoccupied':
                uppern = False                    
            elif U == 'ready':
                uppern = False
                if ( LU != 'occupied' and RU != 'occupied' and UU != 'occupied' ):
                    U = 'unoccupied'  

            # dolny sasiad    
            if D == 'occupied':
                downn = True
            elif D == 'unoccupied':
                downn = False    
            elif D == 'ready': 
                downn = False
                if ( LD != 'occupied' and RD != 'occupied' and DD != 'occupied' ):
                    D = 'unoccupied'              

            
            ### czy byli sasiedzi wokol usuwanego kafelka
            occupiedNeighbor = ( (leftn or rightn) or (uppern or downn) )
                
            ### aktualizacja stanow
            for i in objParam.SQUARES: 
            
                # sasiedzi 1-go stopnia   
                if i['x'] == x - 1 and i['y'] == y:               
                    i['sState'] = L
                if i['x'] == x + 1 and i['y'] == y:
                    i['sState'] = R
                if i['x'] == x and i['y'] == y - 1:
                    i['sState'] = U 
                if i['x'] == x and i['y'] == y + 1:
                    i['sState'] = D 
                    
                # usuwany kafelek            
                if i['x'] == x and i['y'] == y:
                    if occupiedNeighbor:
                        i['sState'] = 'ready'
                    else:    
                        i['sState'] = 'unoccupied'          

    def skipPuzzle(self, objParam, objState, mode): 
    
        # jesli byla mozliwosc polozenia kafelka, przekazanie mozliwych pozycji dalej (usuwanie kafelka z listy tez dalej)
        if not PuzzleHandler.wasItNecessary(self, objParam):
            temp = objState.getCredit()
            objState.setCredit(temp - 3)
            objParam.SHOWPOSSIBILITIES = True
            startShow = time.time()
            objParam.SHOWLOSS = True
            return (startShow, 3)
            
        # jesli nie bylo mozliwosci, usuwanie z listy oczekujacych juz teraz
        movingPuzzle = objParam.PREPAREDPUZZLES.pop(0)
        
        if mode == 'Classic':
            if movingPuzzle['tour'] != -19 and movingPuzzle['tour'] != -10:
                movingPuzzle['tour'] += 1  
                objParam.PREPAREDPUZZLES.append(movingPuzzle) 
            elif movingPuzzle['tour'] == -10: 
                objParam.DELETEPUZZLE = False
        elif mode == 'Continuous':
            if objParam.PREPAREDPUZZLES[0]['tour'] != -19:
                objParam.REST -= 1
            if movingPuzzle['tour'] == -10: 
                objParam.DELETEPUZZLE = False                
                
    def wasItNecessary(self, objParam):
        # sprawdzenie czy omijanie bylo nieuniknione - True gdy brak mozliwosci polozenia kafelka, albo kosz
        
        if objParam.PREPAREDPUZZLES[0]['tour'] == -10:
            return True
        
        possibilities = []
    
        for k in objParam.SQUARES:
            if k['sState'] == 'ready':
                posX = k['x']
                posY = k['y']
                startXPossible = k['startX']
                startYPossible = k['startY']
                pattern = objParam.PREPAREDPUZZLES[0]['pattern']
                colorU = objParam.PREPAREDPUZZLES[0]['colorU']
                colorR = objParam.PREPAREDPUZZLES[0]['colorR']
                colorD = objParam.PREPAREDPUZZLES[0]['colorD']
                colorL = objParam.PREPAREDPUZZLES[0]['colorL']
                
                L = R = U = D = True 

                for i in objParam.PLACEDPUZZLES:   
                    if ( i['x'] == posX - 1 and i['y'] == posY ):
                        if ( colorL == 'neutral' ):
                            L = True 
                        elif ( i['pPattern'] == pattern ) or ( i['pColorR'] == colorL or i['pColorR'] == 'neutral' ):
                            L = True
                        else:
                            L = False
                    if ( i['x'] == posX + 1 and i['y'] == posY ): 
                        if ( colorR == 'neutral' ):
                            R = True  
                        elif ( i['pPattern'] == pattern ) or ( i['pColorL'] == colorR or i['pColorL'] == 'neutral' ):
                            R = True
                        else:
                            R = False                
                    if ( i['x'] == posX and i['y'] == posY - 1 ): 
                        if ( colorU == 'neutral' ):
                            U = True 
                        elif ( i['pPattern'] == pattern ) or ( i['pColorD'] == colorU or i['pColorD'] == 'neutral' ):
                            U = True  
                        else:
                            U = False                
                    if ( i['x'] == posX and i['y'] == posY + 1 ):
                        if ( colorD == 'neutral' ):
                            D = True 
                        elif ( i['pPattern'] == pattern ) or ( i['pColorU'] == colorD or i['pColorU'] == 'neutral' ):
                            D = True                         
                        else:
                            D = False                

                if (L and R) and (U and D): 
                    objPossible = {'x': posX,
                                   'y': posY,
                                   'startX': startXPossible,
                                   'startY': startYPossible}                                   
                    possibilities.append(objPossible)
 
        if len(possibilities) != 0:
            objParam.POSSIBILITIES = possibilities  
            return False
        else:
            return True
        
    def isMovePossible(self, objParam, objScore, puzzle, objState):
        # sprawdzenie czy ruch jt mozliwy, jesli tak obliczane sa tez punkty za polozenie kafelka
        L = R = U = D = True 
        left = right = up = down = 0
       
        posX = puzzle['x']
        posY = puzzle['y']
        pattern = objParam.PREPAREDPUZZLES[0]['pattern']
        colorU = objParam.PREPAREDPUZZLES[0]['colorU']
        colorR = objParam.PREPAREDPUZZLES[0]['colorR']
        colorD = objParam.PREPAREDPUZZLES[0]['colorD']
        colorL = objParam.PREPAREDPUZZLES[0]['colorL']
        
        premiumScore = PuzzleHandler.anyCollumnsRows(self, posX, posY)
        BONUS = premiumScore 
        
        for i in objParam.PLACEDPUZZLES:   
            if ( i['x'] == posX - 1 and i['y'] == posY ):
                if ( colorL == 'neutral' ):
                    L = True 
                    down = 1
                elif ( i['pPattern'] == pattern ) or ( i['pColorR'] == colorL or i['pColorR'] == 'neutral' ):
                    L = True
                    left = 1
                else:
                    L = False
            if ( i['x'] == posX + 1 and i['y'] == posY ): 
                if ( colorR == 'neutral' ):
                    R = True 
                    down = 1            
                elif ( i['pPattern'] == pattern ) or ( i['pColorL'] == colorR or i['pColorL'] == 'neutral' ):
                    R = True
                    right = 1
                else:
                    R = False                
            if ( i['x'] == posX and i['y'] == posY - 1 ): 
                if ( colorU == 'neutral' ):
                    U = True 
                    down = 1
                elif ( i['pPattern'] == pattern ) or ( i['pColorD'] == colorU or i['pColorD'] == 'neutral' ):
                    U = True 
                    up = 1
                else:
                    U = False                
            if ( i['x'] == posX and i['y'] == posY + 1 ):
                if ( colorD == 'neutral' ):
                    D = True 
                    down = 1
                elif ( i['pPattern'] == pattern ) or ( i['pColorU'] == colorD or i['pColorU'] == 'neutral' ):
                    D = True 
                    down = 1
                else:
                    D = False                

        if (L and R) and (U and D):  
            criteria = left + right + up + down
            if criteria == 1:
                if premiumScore != 0:
                    premiumScore -= self.POINT1
                objScore.SCORE += (self.POINT1 + premiumScore)
            elif criteria == 2:
                if premiumScore != 0:
                    premiumScore -= self.POINT2
                objScore.SCORE += (self.POINT2 + premiumScore) 
            elif criteria == 3:
                if premiumScore != 0:
                    premiumScore -= self.POINT3
                objScore.SCORE += (self.POINT3 + premiumScore)
            elif criteria == 4:
                if premiumScore != 0:
                    premiumScore -= self.POINT4
                objScore.SCORE += (self.POINT4 + premiumScore)             
            return (True, BONUS)
        else:
            lossTime = time.time()
            objParam.SHOWLOSS = (True, 1, lossTime)
            temp = objState.getCredit()
            objState.setCredit(temp - 1)
            return (False, 0)
     
    def deleteIfNeeded(self, objParam, posX, posY, bonus):
        # na podstawie bonusa odtwarzane co jt pelne - kolumna, rzad lub oba  
            
        if bonus == self.BONUS1:   # usun kolumne
            for i in objParam.PLACEDPUZZLES:
                if i['x'] == posX:
                    #PuzzleHandler.deleteCollumn(self, objParam, posX)
                    PuzzleHandler.deleteColumnOrRow(self, objParam, 'x', posX)

        elif bonus == self.BONUS2: # usun wiersz
            for i in objParam.PLACEDPUZZLES:
                if i['y'] == posY:
                    #PuzzleHandler.deleteRow(self, objParam, posY)  
                    PuzzleHandler.deleteColumnOrRow(self, objParam, 'y', posY)
                    
        elif bonus == self.BONUS3: # usun kolumne i wiersz
            for i in objParam.PLACEDPUZZLES:
                if i['x'] == posX:
                    #PuzzleHandler.deleteCollumn(self, objParam, posX)
                    PuzzleHandler.deleteColumnOrRow(self, objParam, 'x', posX)
                if i['y'] == posY:
                    #PuzzleHandler.deleteRow(self, objParam, posY)  
                    PuzzleHandler.deleteColumnOrRow(self, objParam, 'y', posY)                    

    def anyCollumnsRows(self, posX, posY):
        hits = 0
        
        if PuzzleHandler.isCollumnFull(self, posX):
            hits += 1
        if PuzzleHandler.isRowFull(self, posY):
            hits += 2
            
        if hits == 1:
            return self.BONUS1
        elif hits == 2:
            return self.BONUS2
        elif hits == 3:
            return self.BONUS3
        else:
            return 0
        
    def isCollumnFull(self, posX):
        temp = self.COLFILL.pop(posX - 1)    
        self.COLFILL.insert((posX - 1), temp + 1)    
        
        ###
        #print('Kolumna ' + str(posX) + ' , zapelnienie: ' + str(temp))
        ###

        if self.COLFILL[posX - 1] == self.ROWS:
            return True
        else:
            return False
            
    def isRowFull(self, posY):
        temp = self.ROWFILL.pop(posY - 1)    
        self.ROWFILL.insert((posY - 1), temp + 1)      
 
        ###
        #print('Rzad ' + str(posY) + ' , zapelnienie: ' + str(temp))
        ###
 
        if self.ROWFILL[posY - 1] == self.COLUMNS:
            return True
        else:
            return False       

    def delElementFromCollumn(self, posX):
        temp = self.COLFILL.pop(posX - 1)    
        self.COLFILL.insert((posX - 1), temp - 1)    
            
    def delElementFromRow(self, posY):
        temp = self.ROWFILL.pop(posY - 1)    
        self.ROWFILL.insert((posY - 1), temp - 1)      
               
    def clearFill(self):    
        self.ROWFILL[:] = []
        self.COLFILL[:] = []     
            
           
    def debugShowPossible(self, objParam):

        possibilities = []
    
        for k in objParam.SQUARES:
            if k['sState'] == 'ready':
                posX = k['x']
                posY = k['y']
                startXPossible = k['startX']
                startYPossible = k['startY']
                pattern = objParam.PREPAREDPUZZLES[0]['pattern']
                colorU = objParam.PREPAREDPUZZLES[0]['colorU']
                colorR = objParam.PREPAREDPUZZLES[0]['colorR']
                colorD = objParam.PREPAREDPUZZLES[0]['colorD']
                colorL = objParam.PREPAREDPUZZLES[0]['colorL']
                
                L = R = U = D = True 

                for i in objParam.PLACEDPUZZLES:   
                    if ( i['x'] == posX - 1 and i['y'] == posY ):
                        if ( colorL == 'neutral' ):
                            L = True 
                        elif ( i['pPattern'] == pattern ) or ( i['pColorR'] == colorL or i['pColorR'] == 'neutral' ):
                            L = True
                        else:
                            L = False
                    if ( i['x'] == posX + 1 and i['y'] == posY ): 
                        if ( colorR == 'neutral' ):
                            R = True  
                        elif ( i['pPattern'] == pattern ) or ( i['pColorL'] == colorR or i['pColorL'] == 'neutral' ):
                            R = True
                        else:
                            R = False                
                    if ( i['x'] == posX and i['y'] == posY - 1 ): 
                        if ( colorU == 'neutral' ):
                            U = True 
                        elif ( i['pPattern'] == pattern ) or ( i['pColorD'] == colorU or i['pColorD'] == 'neutral' ):
                            U = True  
                        else:
                            U = False                
                    if ( i['x'] == posX and i['y'] == posY + 1 ):
                        if ( colorD == 'neutral' ):
                            D = True 
                        elif ( i['pPattern'] == pattern ) or ( i['pColorU'] == colorD or i['pColorU'] == 'neutral' ):
                            D = True                         
                        else:
                            D = False                

                if (L and R) and (U and D): 
                    objPossible = {'x': posX,
                                   'y': posY,
                                   'startX': startXPossible,
                                   'startY': startYPossible}                                   
                    possibilities.append(objPossible)
 
        if len(possibilities) != 0:
            objParam.POSSIBILITIES = possibilities
            return possibilities     
        else:
            possibilities = []
            return possibilities

            