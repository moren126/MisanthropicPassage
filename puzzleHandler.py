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
              
    def createRowsFill(self):
        p = [0] * self.ROWS
        p.pop(self.STARTPUZZLEY - 1)    
        p.insert((self.STARTPUZZLEY - 1), 1)          
        return p

    def createColumnsFill(self):
        p = [0] * self.COLUMNS 
        p.pop(self.STARTPUZZLEX - 1)    
        p.insert((self.STARTPUZZLEX - 1), 1)    
        return p             
      
    def deletePuzzle(self, objParam, x, y):

        global temp
        
        for i in objParam.PLACEDPUZZLES:
            if i['x'] == x and i['y'] == y:
                temp = i['index']

        PuzzleHandler.delElementFromCollumn(self, x)    
        PuzzleHandler.delElementFromRow(self, y)         
                
        if temp is not None:        
            objParam.PLACEDPUZZLES[:] = [d for d in objParam.PLACEDPUZZLES if d.get('index') != temp]
        else:
            #komunikat o niedozwolonym ruchu
            pass


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
                    #print(occupiedNeighbor)            

            
        objParam.PREPAREDPUZZLES.pop(0)
        objParam.DELETEPUZZLE = False        
        
    def skipPuzzle(self, objParam, objState): 
    
        # jesli byla mozliwosc polozenia kafelka, przekazanie mozliwych pozycji dalej (usuwanie kafelka z listy tez dalej)
        if not PuzzleHandler.wasItNecessary(self, objParam):
            temp = objState.getCredit()
            objState.setCredit(temp - 3)
            objParam.SHOWPOSSIBILITIES = True
            startShow = time.time()
            return startShow
            
        # jesli nie bylo mozliwosci, usuwanie z listy juz teraz
        movingPuzzle = objParam.PREPAREDPUZZLES.pop(0)
        
        if movingPuzzle['tour'] != -19 and movingPuzzle['tour'] != -10:
            movingPuzzle['tour'] += 1  
            objParam.PREPAREDPUZZLES.append(movingPuzzle) 
        elif movingPuzzle['tour'] == -10: 
            objParam.DELETEPUZZLE = False
            #print(objParam.DELETEPUZZLE)    
            
        #objParam.PREPAREDPUZZLES.append(movingPuzzle)      

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
        
    def isMovePossible(self, objParam, objScore, puzzle):
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
            return True
        else:
            return False
         
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
    
        if self.COLFILL[posX - 1] == self.ROWS:
            return True
        else:
            return False
            
    def isRowFull(self, posY):
        temp = self.ROWFILL.pop(posY - 1)    
        self.ROWFILL.insert((posY - 1), temp + 1)      

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

            