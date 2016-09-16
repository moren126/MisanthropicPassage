class GameStates(object):

    def __init__(self):

        self.STATE = 'WelcomeMenu'
    
        self.MODE = 'Classic'
    
        #parametry poziomu trudnosci (domyslnie easy)
        self.DIFFNAME = 'Easy'
        self.CREDIT = 40
        self.TRASHFACTOR = 0.3
        self.STARTFACTOR = 2

    ### stan gry    
    def setState(self, state):
        if state == 'WelcomeMenu':
            self.STATE = 'WelcomeMenu'
        elif state == 'DiffMenu':
            self.STATE = 'DiffMenu'
        elif state == 'ScoreMenu':
            self.STATE = 'ScoreMenu'    
        elif state == 'Game':
            self.STATE = 'Game'    
        else:
            print('Wrong STATE name')        
        
    ### tryb rozgrywki
    def setMode(self, name):    
        if name == 'Classic':
            self.MODE = 'Classic'
        elif name == 'Continuous':
            self.MODE = 'Continuous'
        else:
            print('Wrong MODE name')
            
    def getMode(self):        
        return self.MODE
        
    ### poziomy trudnosci 
    def setEasy(self):
        self.DIFFNAME = 'Easy'
        self.CREDIT = 40
        self.TRASHFACTOR = 0.3
        self.STARTFACTOR = 2

    def setMedium(self):
        self.DIFFNAME = 'Medium'
        self.CREDIT = 30
        self.TRASHFACTOR = 0.2
        self.STARTFACTOR = 1
        
    def setHard(self):
        self.DIFFNAME = 'Hard'
        self.CREDIT = 20
        self.TRASHFACTOR = 0.1    
        self.STARTFACTOR = 0        
    
    def getDifficulty(self):
        return self.DIFFNAME
    
             
    def setDifficulty(self, name):
        if name == 'Easy':
            GameStates.setEasy(self)
        elif name == 'Medium':
            GameStates.setMedium(self)     
        elif name == 'Hard':
            GameStates.setHard(self)
        else:
            print('Wronf DIFFICULTY name')
    
    def setCreditFromDiff(self):
        if self.DIFFNAME == 'Easy':
            GameStates.setEasy(self)
        elif self.DIFFNAME == 'Medium':
            GameStates.setMedium(self)      
        elif self.DIFFNAME == 'Hard':
            GameStates.setHard(self)
        else:
            print('Wronf DIFFICULTY name')        
    
    def setCredit(self, credit):
        self.CREDIT = credit
        
    def getCredit(self):
        return self.CREDIT
        
    def getTrashFactor(self):
        return self.TRASHFACTOR  

    def getStartFactor(self):    
        return self.STARTFACTOR        

if __name__ == '__main__':
    objGameStates = GameStates()  