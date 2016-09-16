import random

def createRandoms(puzzleNumber):
    results = []
    specNumber = int(0.1 * puzzleNumber)
    specDist = int(puzzleNumber / specNumber)
    specDistR = 0
            
    for i in range(specNumber):
        specDistR += random.randrange(specDist - 2, specDist + 2)
        results.insert(i, specDistR)
    return results  
    
def addSpecjalOrNot(percentage):
    randomNumber = random.random()    
    if randomNumber <= percentage:
        return True
    else:
        return False
        
def insultOrNot():
    chances = random.random() 
                    
    if chances <= 0.5:
        return True             
    else:
        return False

def chooseInsult(circumstances):

    insultPlus =    ['Fine. Whatever.', 
                    'You\'ve done so well for someone with your education level',
                    'You could do better',
                    'Nobody loves you anyway',
                    'No one will even notice that you have died',
                    'I love you like a fat kid loves cake',
                    'I\'m surprised you could do that',
                    'Hope it\'s worth it'
                    ]   

    insultMinus =   ['You getting upset? Why?',
                    'I don\'t care you\'re vegan',
                    'You never gonna be apache helicopter',
                    'I bet you cry during sex',
                    'Don\'t worry about your feelings, no one else does',
                    'Boooring',
                    'I\'m not even mad',
                    'I\'m only joking',
                    'lol',
                    'oh man/woman/non binary person...'
                    ] 
                    
    if circumstances == 'plus':
        plusIndex = random.randrange(0, len(insultPlus))
        plusInsult = insultPlus[plusIndex]
        return plusInsult
    elif circumstances == 'minus':
        minusIndex = random.randrange(0, len(insultMinus))
        minusInsult = insultMinus[minusIndex]
        return minusInsult                     