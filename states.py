class GameStates(object):

    def __init__(self):

        self.STATE = 'WelcomeMenu'
    
        #parametry poziomu trudnosci (domyslnie easy)
        self.DIFFNAME = 'Easy'
        self.CREDIT = 40

    ### stan gry    
    def setState(self, state):
        self.STATE = state           

    ### poziomy trudnosci 
    def setEasy(self):
        self.DIFFNAME = 'Easy'
        self.CREDIT = 40

    def setMedium(self):
        self.DIFFNAME = 'Medium'
        self.CREDIT = 30
        
    def setHard(self):
        self.DIFFNAME = 'Hard'
        self.CREDIT = 20        
             
             
    def setDifficulty(self, name):
        if name == 'Easy':
            GameStates.setEasy(self)
        elif name == 'Medium':
            GameStates.setMedium(self)     
        elif name == 'Hard':
            GameStates.setHard(self)
    
    def setCreditFromDiff(self):
        if self.DIFFNAME == 'Easy':
            GameStates.setEasy(self)
        elif self.DIFFNAME == 'Medium':
            GameStates.setMedium(self)      
        elif self.DIFFNAME == 'Hard':
            GameStates.setHard(self)
    
    def setCredit(self, credit):
        self.CREDIT = credit
        
    def getCredit(self):
        return self.CREDIT

if __name__ == '__main__':
    objGameStates = GameStates()  