import random

def createRandoms(puzzleNumber):
    results = []
    specNumber = int(0.2 * puzzleNumber)
    specDist = int(puzzleNumber / specNumber)
    specDistR = 0
            
    for i in range(specNumber):
        specDistR += random.randrange(specDist - 2, specDist + 2)
        results.insert(i, specDistR)
    return results  
    
def addSpecjalOrNot():
    randomNumber = random.random()    
    if randomNumber <= 0.4:
        return True
    else:
        return False