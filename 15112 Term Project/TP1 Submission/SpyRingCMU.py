from cmu_graphics import *
import random
import math
import time
import copy

def onAppStart(app):
    setActiveScreen('home')
    app.width = 650
    app.height = 650
    # home
    app.homeScreen = '''cmu://872385/33944698/A+dark+figure+with+a+briefcase+peering+around+a+corner+in+a+city+at+night,
                        +with+another+dark+figure+walking+ahead,+facing+the+correct+way,+and+it+is+raining+(1).png'''
    app.titlePt1 = 'cmu://872385/33944839/cooltext468551696595664.png'
    app.titlePt2 = 'cmu://872385/33944848/cooltext468551712153001.png'
    # game
    app.map = 'cmu://872385/33943134/Screenshot+2024-10-18+172538+(1).png'
    app.cities = getRandomCities(app)
    app.currCity1 = None
    app.currCity2 = None
        # highlighting
    app.highlights = {'newGame': 'gray', 'tutorial': 'gray', 'credits': 'gray',\
                      'Control': 'white', 'Strike': 'white', 'Wait': 'white', 'Locate': 'white',\
                      'Build': 'white', 'Demolish': 'white', 'Go Deep': 'white', 'Prepare': 'white',\
                      'gameExit': 'white', 'tutorialExit': 'white', 'creditsExit': 'white',\
                      'yes': 'white', 'no': 'white'}
    app.spy1Highlight = None
    app.spy2Highlight = None
        # spy icons
    app.minSpawnDistance = 400
    app.spyWidth, app.spyHeight = 20, 70
    app.spy1x, app.spy1y, app.spy2x, app.spy2y = randomStartLocation(app)
    app.spy1Selected = False
    app.spy2Selected = False
    app.spiesTogether = False
        # turns
    app.turnCounter = 0
    app.redTurn = True
    app.blueTurn = False
        # actions
    app.actions = ['Control', 'Strike', 'Wait', 'Locate', 'Build', 'Demolish', 'Go Deep', 'Prepare']
    app.actionULCoords = [(270, 570),(360, 570),(450, 570),(540, 570),(630, 570),(720, 570),(810, 570),(900, 570)]
    app.redActionsLeft = 3
    app.blueActionsLeft = 3
        # intel
    app.intel1 = 0
    app.intel2 = 0
        # suspicion
    app.suspicion1 = 0
    app.suspicion2 = 0

    
# HOME

# maybe add rain to the main screen later?
class Raindrop:
    def __init__(self, x0, y0, x1, y1, dx, dy):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.dx = dx
        self.dy = dy
        return Raindrop

def home_redrawAll(app):
    drawHomeBackground(app)
    drawHomeButtons(app)

def drawHomeBackground(app):
    drawImage(app.homeScreen, 0, 0)
    drawImage(app.titlePt1, 350, 130)
    drawImage(app.titlePt2, 400, 180)
    
    drawLine(350, 60, 415, 385, fill = 'red', opacity = 30)
    drawCircle(415, 385, 3, fill = 'red', opacity = 70)
    
def drawHomeButtons(app):
    # New game
    rectX = 220
    rectY = 372
    rectWidth = 100
    rectHeight = 36
    drawRect(rectX, rectY, rectWidth, rectHeight, fill = 'darkSlateGray', border = app.highlights['newGame'],\
             borderWidth = 2, opacity = 50, rotateAngle = 5)
    drawLabel('New Game', rectX + rectWidth//2, rectY + rectHeight//2, align = 'center', \
               size = 14, fill = 'limeGreen', bold= True, font = 'orbitron', rotateAngle = 5)
    # Tutorial
    rectX = 215
    rectY = 415
    rectWidth = 105
    rectHeight = 36
    drawRect(rectX, rectY, rectWidth, rectHeight, fill = 'darkSlateGray', border = app.highlights['tutorial'],\
             borderWidth = 2, opacity = 50, rotateAngle = 5)
    drawLabel('Tutorial', rectX + rectWidth//2, rectY + rectHeight//2, align = 'center', \
               size = 14, fill = 'limeGreen', bold = True, font = 'orbitron', rotateAngle = 5)
    # Credits
    cx = 50
    cy = 50
    cr = 40
    drawCircle(cx, cy, cr, fill = 'darkSlateGray', border = app.highlights['credits'],\
               borderWidth = 2, opacity = 50)
    drawLabel('Credits', cx, cy, fill = 'limeGreen', bold = True, font = 'orbitron')

def home_onMouseMove(app, mouseX, mouseY):
    app.highlights['newGame'] = 'limeGreen' if inBox(220, 372, 100, 36, mouseX, mouseY) else 'gray'
    app.highlights['tutorial'] = 'limeGreen' if inBox(215, 415, 105, 36, mouseX, mouseY) else 'gray'
    app.highlights['credits'] = 'limeGreen' if inCircle(50, 50, 40, mouseX, mouseY) else 'gray'
    
def home_onMousePress(app, mouseX, mouseY):
    if inBox(220, 372, 100, 36, mouseX, mouseY):
        app.width = 1000
        setActiveScreen('game')
    elif inBox(215, 415, 105, 36, mouseX, mouseY):
        pass
    elif inCircle(50, 50, 40, mouseX, mouseY):
        setActiveScreen('credits')
        
# GAME

class City:
    def __init__(self, cx, cy, name, abbrev, status, possibleConnections, realConnections, maxConnections):
        self.cx = cx
        self.cy = cy
        self.name = name
        self.abbrev = abbrev
        self.status = status
        self.possibleConnections = possibleConnections
        self.realConnections = realConnections
        self.maxConnections = maxConnections
        return City
        
    def __repr__(self):
        return f'({self.cx}, {self.cy}, {self.name}, {self.abbrev}, {self.status}, {self.possibleConnections}, {self.realConnections}, {self.maxConnections})'
    
    def __eq__(self, other):
        if isinstance(self, City) and isinstance(other, City):
            return self.cx == other.cx and self.cy == other.cy and self.name == other.name and self.abbrev == other.abbrev and\
                   self.status == other.status and self.possibleConnections == other.possibleConnections and\
                   self.realConnections == other.realConnections and self.maxConnections == other.maxConnections
        else:
            return False
    
class Action:
    def __init__(self, cx, cy, width, height, label, highlighted):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.label = label
        self.highlighted = highlighted
        return Action
    
    def __repr__(self):
        return f'({self.cx}, {self.cy}, {self.width}, {self.height}, {self.label}, {self.highlighted})'

def game_redrawAll(app):
    drawMap(app)
    drawExitButton(app)
    drawDossier(app)
    drawIntel(app)
    drawTurnMarker(app)
    drawActionCountBoxes(app)
    drawSuspicionMeter(app)
    drawActionBoxes(app)
    drawTravelLines(app)
    drawCities(app)
    drawSpyIcons(app)

def drawMap(app):
    drawImage(app.map, 0, 0)
    drawRect(0, 500, 1000, 650, fill = 'black') # covers up bottom of screen

def drawExitButton(app):
    buttonUL = (940, 20)
    buttonWidth = 40
    buttonHeight = 40
    drawRect(buttonUL[0], buttonUL[1], buttonWidth, buttonHeight, fill = None, border = app.highlights['gameExit'])
    drawLabel('X', 960, 40, size = 40, fill = 'red', bold = True)
    
def drawDossier(app):
    dossier = 'cmu://872385/35273263/a0a35196f90b43dc34d532c2252070c0+(1).jpg'
    dossierX = 15
    dossierY = 460
    drawImage(dossier, dossierX, dossierY)

def drawIntel(app):
    intelX = 40
    intelY = 360
    intelWidth = 80
    intelHeight = 80
    drawRect(intelX, intelY, intelWidth, intelHeight, fill = None, border = 'limeGreen')
    drawLabel('Intel:', intelX + intelWidth//2 + 2, intelY + 22, fill = 'limeGreen', size = 20, font = 'orbitron',  bold = True)
    if app.redTurn:
        drawLabel(f'{app.intel1}', intelX + intelWidth//2, intelY + 52, fill = 'limeGreen', size = 30, font = 'orbitron')
    elif app.blueTurn:
        drawLabel(f'{app.intel2}', intelX + intelWidth//2, intelY + 52, fill = 'limeGreen', size = 30, font = 'orbitron')
    
def drawTurnMarker(app):
    if app.redTurn:
        drawLabel("Red Turn", 650, 530, fill = 'limeGreen', font = 'orbitron', bold = True, size = 30)
    elif app.blueTurn:
        drawLabel("Blue Turn", 650, 530, fill = 'limeGreen', font = 'orbitron', bold = True, size = 30)

def drawActionCountBoxes(app):
    actionBoxes = [True, True, False, False]
    drawLabel('Actions:', 380, 500, fill = 'limeGreen', size = 20, font = 'orbitron', bold = True)
    for i in range(len(actionBoxes)):
        if actionBoxes[i] == True:
            drawRect(435 + 20*i, 497, 10, 10, fill = 'limeGreen')
        else:
            drawRect(435 + 20*i, 497, 10, 10, fill = None, border = 'limeGreen', borderWidth = 2)

def drawSuspicionMeter(app):
    drawRect(400, 525, 120, 30, fill = None, border = 'limeGreen')
    drawLabel('Suspicion:', 330, 540, fill = 'limeGreen', size = 20, font = 'orbitron', bold = True)
    if app.redTurn == True:
        drawLabel(f'{app.suspicion1}', 460, 540, fill = 'limeGreen', size = 20, font = 'orbitron')
    elif app.blueTurn == True:
        drawLabel(f'{app.suspicion2}', 460, 540, fill = 'limeGreen', size = 20, font = 'orbitron')
    
def drawActionBoxes(app):
    actionButtonLabels = ['Control', 'Strike', 'Wait', 'Locate', 'Build', 'Demolish', 'Go Deep', 'Prepare']
    for i in range(len(actionButtonLabels)):
        action = Action(310 + i*90, 600, 80, 60, actionButtonLabels[i], False)
        drawRect(action.cx, action.cy, action.width, action.height, align = 'center', fill = None,\
                 border = app.highlights[actionButtonLabels[i]], borderWidth = 2)
        drawLabel(action.label, action.cx, action.cy, size = 14, font = 'orbitron', fill = 'limeGreen', bold = True)

def drawTravelLines(app):
    for city in app.cities:
        x0 = city.cx
        y0 = city.cy
        for connectedCity in city.realConnections:
            x1 = app.cityCoords[connectedCity][0]
            y1 = app.cityCoords[connectedCity][1]
            drawLine(x0, y0, x1, y1, fill = 'lightGreen', lineWidth = 2)
        
def drawCities(app):
    for city in app.cities:
        if city.status == 2:
            drawCircle(city.cx, city.cy, 10, fill = 'crimson')
        elif city.status == 1:
            drawCircle(city.cx, city.cy, 10, fill = 'lightSalmon')
        elif city.status == 0:
            drawCircle(city.cx, city.cy, 10, fill = 'gray')
        elif city.status == -1:
            drawCircle(city.cx, city.cy, 10, fill = 'lightSkyBlue')
        elif city.status == -2:
            drawCircle(city.cx, city.cy, 10, fill = 'royalBlue')
            
        drawCircle(city.cx, city.cy, 6, fill = 'white')
        drawCircle(city.cx, city.cy, 2, fill = 'black')
        drawRect(city.cx - 15, city.cy + 15, 30, 13, fill = 'black', opacity = 70)
        drawLabel(city.abbrev, city.cx, city.cy + 20, fill = 'white', font = 'orbitron', bold = True, size = 12)
        
def getRandomCities(app):
    randCities = []
    app.numCities = 35
    app.cityCoords = {"Algiers"      :(480,230,"ALG",0,['Ankara','Bermuda','Cairo','Lagos','Madrid'],3),\
                      "Anchorage"    :(80,160,'ANCH',0,['Honolulu','San Francisco','Yellowknife'],2),\
                      "Ankara"       :(560,210,'ANK',0,['Cairo','Delhi','Moscow','Ur'],3),\
                      "Beijing"      :(750,200,'BEI',0,['Delhi','Hanoi','Novosibrisk','Tokyo','Ur','Vladivostok'],5),\
                      "Berlin"       :(505,170,'BER',0,['Algiers','London','Madrid','St.Petersburg'],3),\
                      "Bermuda"      :(360,240,'BRM',0,['Bogota','Lagos','Madrid','New York'],4),\
                      "Bogota"       :(280,320,'BOG',0,['Bermuda','Lagos','Lima','Mexico City'],1),\
                      "Cairo"        :(520,245,'CAI',0,['Algiers','Ankara','Khartoum','Lagos'],3),\
                      "Chicago"      :(240,200,'CHI',0,['New York','San Francisco','Yellowknife'],2),\
                      "Delhi"        :(660,250,'DEH',0,['Ankara','Beijing','Hanoi','Khartoum','Singapore'],3),\
                      "Hanoi"        :(740,270,'HAN',0,['Delhi','Jakarta','Singapore','Tokyo'],3),\
                      "Honolulu"     :(80, 280,'HONO',0,['Anchorage','Mexico City','Honolulu'],2),\
                      "Iceland"      :(410,120,'ICE',0,['London','St.Petersburg','Yellowknife'],3),\
                      "Jakarta"      :(800,340,'JAK',0,['Hanoi','Singapore','Sydney','Tokyo'],3),\
                      "Johannesburg" :(520,380,'JOH',0,['Khartoum','Lagos','Madagascar','Sao Paulo'],3),\
                      "Khartoum"     :(550,300,'KHAR',0,['Cairo','Delhi','Johannesburg','Madagascar'],3),\
                      "Lagos"        :(460,290,'LAG',0,['Algiers','Bermuda','Bogota','Johannesburg'],3),\
                      "Lima"         :(290,380,'LIM',0,['Bogota','Sao Paulo','Santiago'],2),\
                      "London"       :(450,155,'LON',0,['Berlin','Iceland','Madrid','New York'],3),\
                      "Madagascar"   :(580,360,'MAD',0,['Johannesburg','Khartoum','Singapore','Sydney'],3),\
                      "Madrid"       :(440,200,'MAD',0,['Algiers','Bermuda','London','New York'],2),\
                      "Mexico City"  :(220,270,'MEXC',0,['Bogota', 'Chicago','Honolulu','New York','San Francisco'],5),\
                      "Moscow"       :(580,150,'MOS',0,['Ankara','Berlin','St.Petersburg','Ur'],4),\
                      "New York"     :(290,210,'NYC',0,['Bermuda','Chicago','Iceland','London','Madrid','Mexico City'],5),\
                      "Novosibrisk"  :(700,140,'NOV',0,['Beijing','Moscow','Ur','Vladivostok'],3),\
                      "Santiago"     :(280,440,'SAN',0,['Honolulu','Lima','Sao Paulo'],3),\
                      "San Francisco":(170,220,'SAN',0,['Honolulu', "Mexico City", "Chicago", "Yellowknife"],3),\
                      "Sao Paulo"    :(340,400,'SAU',0,['Johannesburg','Lagos','Lima','Santiago'],3),\
                      "Singapore"    :(720,310,'SING',0,['Delhi','Hanoi','Jakarta','Madagascar'],1),\
                      "St.Petersburg":(540,120,'STP',0,['Berlin','Iceland','London','Moscow'],3),\
                      "Sydney"       :(880,400,'SYD',0,['Jakarta','Madagascar','Tokyo'],2),\
                      "Tokyo"        :(820,220,'TOK',0,['Beijing','Hanoi','Jakarta','Sydney','Vladivostok'],4),\
                      "Ur"           :(640,170,'UR', 0,['Ankara','Beijing','Moscow','Novosibrisk'],3),\
                      "Vladivostok"  :(820,160,'VLA',0,['Beijing','Novosibrisk','Tokyo'],3),\
                      "Yellowknife"  :(200,160,'YEL',0,['Anchorage','Chicago','Iceland','San Francisco'],3)}
    
    chosenCities = random.sample(list(app.cityCoords), app.numCities)
    for city in chosenCities:
        copiedCoords = copy.deepcopy(app.cityCoords)
        cx = copiedCoords[city][0]
        cy = copiedCoords[city][1]
        name = city
        abbrev = copiedCoords[city][2]
        status = copiedCoords[city][3]
        possibleConnections = copiedCoords[city][4]
        maxConnections = copiedCoords[city][5]
        realConnections = []
        for connection in possibleConnections:
            randIndex = random.randint(0, len(possibleConnections) - 1)
            if len(realConnections) == maxConnections:
                break
            else:
                connectedCity = possibleConnections[randIndex]
                realConnections.append(connectedCity)
                possibleConnections.pop(randIndex)
        randCities.append(City(cx, cy, name, abbrev, status, possibleConnections, realConnections, maxConnections))
    return randCities
    
def randomStartLocation(app):
    copiedCities = copy.copy(app.cities)
    randCity1 = random.choice(copiedCities)
    # remove the one we already chose
    copiedCities.remove(randCity1)
    randCity2 = random.choice(copiedCities)
    # keep selecting until they spawn far enough away
    while distance(randCity1.cx, randCity1.cy, randCity2.cx, randCity2.cy) < app.minSpawnDistance:
        randCity2 = random.choice(copiedCities)
        
    app.currCity1 = City(randCity1.cx, randCity1.cy, randCity1.name, randCity1.abbrev, randCity1.status,\
                         randCity1.possibleConnections, randCity1.realConnections, randCity1.maxConnections)
    app.currCity2 = City(randCity2.cx, randCity2.cy, randCity2.name, randCity2.abbrev, randCity2.status,\
                         randCity2.possibleConnections, randCity2.realConnections, randCity2.maxConnections)
    return (randCity1.cx, randCity1.cy, randCity2.cx, randCity2.cy) 

def drawSpyIcons(app):
    if app.spiesTogether: 
    # draw special w/two spies in one node
        drawPolygon(app.spy1x, app.spy1y, app.spy1x-10, app.spy1y-20, app.spy1x, app.spy1y-30, app.spy1x+10, app.spy1y-20, \
                    fill = 'red', border = app.spy1Highlight, borderWidth = 2)
        drawCircle(app.spy1x, app.spy1y - 18, 3, fill = 'gold')
        drawPolygon(app.spy2x+10, app.spy2y+10, app.spy2x, app.spy2y-10, app.spy2x+10, app.spy2y-20, app.spy2x+20, app.spy2y-10, \
                    fill = 'dodgerBlue', border = app.spy2Highlight, borderWidth = 2)
        drawCircle(app.spy2x+10, app.spy2y - 8, 3, fill = 'gold')
    else: 
    # normal drawing for both spies
        drawPolygon(app.spy1x, app.spy1y, app.spy1x-10, app.spy1y-20, app.spy1x, app.spy1y-30, app.spy1x+10, app.spy1y-20, \
                    fill = 'red', border = app.spy1Highlight, borderWidth = 2)
        drawCircle(app.spy1x, app.spy1y - 18, 3, fill = 'gold')
        drawPolygon(app.spy2x, app.spy2y, app.spy2x-10, app.spy2y-20, app.spy2x, app.spy2y-30, app.spy2x+10, app.spy2y-20, \
                    fill = 'dodgerBlue', border = app.spy2Highlight, borderWidth = 2)
        drawCircle(app.spy2x, app.spy2y - 18, 3, fill = 'gold')
 
# Game controllers below

def game_onStep(app):
    app.spiesTogether = app.currCity1 == app.currCity2

def game_onMouseMove(app, mouseX, mouseY):
    app.spy1Highlight = 'white' if mouseInSpy1(app, mouseX, mouseY) else None
    app.spy2Highlight = 'white' if mouseInSpy2(app, mouseX, mouseY) else None
    app.highlights['gameExit'] = 'limeGreen' if mouseInXButton(app, mouseX, mouseY) else 'white'
    for i, action in enumerate(app.actions):
        app.highlights[action] = 'lightGreen' if mouseInAction(app, mouseX, mouseY, i) else 'white'

def game_onMousePress(app, mouseX, mouseY):
    app.spy1Selected = True if mouseInSpy1(app, mouseX, mouseY) else False
    app.spy2Selected = True if mouseInSpy2(app, mouseX, mouseY) else False
    # actions
    if mouseInAction(app, mouseX, mouseY, 0):
        if app.redTurn and app.currCity1.status < 2:
            i = app.cities.index(app.currCity1)
            app.cities[i].status += 1
            app.currCity1.status += 1
            app.turnCounter += 1
        elif app.blueTurn == 1 and app.currCity2.status > -2:
            i = app.cities.index(app.currCity2)
            app.cities[i].status -= 1 
            app.currCity2.status -= 1
            app.turnCounter += 1
        else:
            print('Invalid!')
        checkTurn(app)
    elif mouseInAction(app, mouseX, mouseY, 1):
        if app.redTurn and app.spiesTogether:
            print('Red Wins')
        elif app.blueTurn == 1 and app.spiesTogether:
            print('Blue Wins')
        else:
            print('Strike Failed!')
        app.turnCounter += 1
        checkTurn(app)
    elif mouseInAction(app, mouseX, mouseY, 2):
        app.turnCounter += 1
        checkTurn(app)
    elif mouseInAction(app, mouseX, mouseY, 3):
        pass
    elif mouseInAction(app, mouseX, mouseY, 4):
        pass
    elif mouseInAction(app, mouseX, mouseY, 5):
        pass
    elif mouseInAction(app, mouseX, mouseY, 6):
        pass
    elif mouseInAction(app, mouseX, mouseY, 7):
        pass
    elif mouseInXButton(app, mouseX, mouseY):
        setActiveScreen('areYouSure')
    
def game_onMouseDrag(app, mouseX, mouseY):
    if app.spy1Selected:
        app.spy1x, app.spy1y = mouseX, mouseY
    elif app.spy2Selected:
        app.spy2x, app.spy2y = mouseX, mouseY
            
def game_onMouseRelease(app, mouseX, mouseY):
    if app.spy1Selected:
        app.spy1Highlight = None
        for city in app.cities:
            if (distance(city.cx, city.cy, mouseX, mouseY) <= 20) and city != app.currCity1\
               and isValidMove(app, app.currCity1, city):
                app.spy1x = city.cx
                app.spy1y = city.cy
                app.currCity1 = City(app.spy1x, app.spy1y, city.name, city.abbrev, city.status,\
                                     city.possibleConnections, city.realConnections, city.maxConnections)
                app.turnCounter += 1
                checkTurn(app)
        # invalid move!
        app.spy1x = app.currCity1.cx
        app.spy1y = app.currCity1.cy
                
    elif app.spy2Selected:
        app.spy2Highlight = None
        for city in app.cities:
            if (distance(city.cx, city.cy, mouseX, mouseY) <= 20) and city != app.currCity2\
               and isValidMove(app, app.currCity2, city):
                app.spy2x = city.cx
                app.spy2y = city.cy
                app.currCity2 = City(app.spy2x, app.spy2y, city.name, city.abbrev, city.status,\
                                     city.possibleConnections, city.realConnections, city.maxConnections)
                app.turnCounter += 1
                checkTurn(app)
        # invalid move!
        app.spy2x = app.currCity2.cx
        app.spy2y = app.currCity2.cy

def isValidMove(app, currentCity, nextCity):
    if (currentCity.name in nextCity.realConnections) or (nextCity.name in currentCity.realConnections):
        return True
    else:
        return False
        
def checkTurn(app):
    if app.turnCounter % 2 == 0 and app.turnCounter != 0:
        app.redTurn = not app.redTurn
        app.blueTurn = not app.blueTurn

def mouseInAction(app, mouseX, mouseY, i):
    actionWidth = 80
    actionHeight = 60
    if i < len(app.actionULCoords):
        actionX, actionY = app.actionULCoords[i]
        return inBox(actionX, actionY, actionWidth, actionHeight, mouseX, mouseY)
    else:
        return False
        
def mouseInSpy1(app, mouseX, mouseY):
    if app.spy1x - app.spyWidth/2 <= mouseX <= app.spy1x + app.spyWidth/2 and \
       app.spy1y - app.spyHeight/2 <= mouseY <= app.spy1y + app.spyWidth/2 and \
       app.redTurn:
          return True
    return False
    
def mouseInSpy2(app, mouseX, mouseY):
    if app.spy2x - app.spyWidth/2 <= mouseX <= app.spy2x + app.spyWidth/2 and \
       app.spy2y - app.spyHeight/2 <= mouseY <= app.spy2y + app.spyWidth/2 and \
       app.blueTurn:
          return True
    return False

def mouseInXButton(app, mouseX, mouseY):
    XButtonUL = (940, 20)
    XButtonWidth = 40
    XButtonHeight = 40
    return inBox(XButtonUL[0], XButtonUL[1], XButtonWidth, XButtonHeight, mouseX, mouseY)
    
#--------* Are You Sure secondary screen (I wrote this during Hack112! This is tweaked significantly though)

def areYouSure_redrawAll(app):
    drawMap(app)
    drawRect(330, 200, 340, 160, fill = 'black', border = 'white', borderWidth = 2)
    
    drawLabel('Are you sure you want to quit?', 500, 240, fill = 'limeGreen', size = 20, bold = True)
    drawLabel('Yes', 420, 305, fill = 'limeGreen', size = 25)
    drawLabel('No', 580, 305, fill = 'limeGreen', size = 25)
    
    drawRect(360, 280, 120, 50, fill = None, border = app.highlights['yes'], borderWidth = 2)
    drawRect(520, 280, 120, 50, fill = None, border = app.highlights['no'], borderWidth = 2)
        
def areYouSure_onMouseMove(app, mouseX, mouseY):
    app.highlights['yes'] = 'limeGreen' if inBox(360, 280, 120, 50, mouseX, mouseY) else 'white'
    app.highlights['no'] = 'limeGreen' if inBox(520, 280, 120, 50, mouseX, mouseY) else 'white'

def areYouSure_onMousePress(app, mouseX, mouseY):
    if inBox(360, 280, 120, 50, mouseX, mouseY):
        app.width = 650
        app.height = 650
        setActiveScreen('home')
    elif inBox(520, 280, 120, 50, mouseX, mouseY):
        setActiveScreen('game')

# CREDITS

def credits_redrawAll(app):
    drawRect(0, 0, 650, 650, fill = 'black')
    drawRect(600, 20, 40, 40, fill = None, border = app.highlights['creditsExit'], borderWidth = 2)
    drawLabel('X', 620, 40, fill = 'red', size = 40)
    drawLabel('Credits', 325, 100, fill = 'limeGreen', size = 40, font = 'orbitron')
    drawLabel('---------------------------', 325, 140, fill = 'white', size = 20)
    drawLabel('Inspired by: Two Spies, a Royal Pixel game', 325, 180, fill = 'limeGreen', size = 25, font = 'orbitron')
    drawLabel('Derrick Siu', 450, 240, fill = 'white', size = 25, font = 'orbitron')
    drawLabel('Programming & UX: Microsoft Copilot', 325, 280, fill = 'limeGreen', size = 25, font = 'orbitron')
    drawLabel('----------------------------', 460, 285, fill = 'limeGreen', size = 25)
    drawLabel('The bestest TA in the world:', 260, 340, fill = 'limeGreen', size = 25, font = 'orbitron')
    drawLabel('Varun', 510, 340, fill = 'white', size = 25, font = 'orbitron')
    drawLabel('Definitely not the profs:', 325, 400, fill = 'limeGreen', size = 25, font = 'orbitron')
    drawLabel('David Kosbie & Austin Schick', 325, 435, fill = 'white', size = 25, font = 'orbitron')
    
def credits_onMouseMove(app, mouseX, mouseY):
    app.highlights['creditsExit'] = 'limeGreen' if inBox(600, 20, 40, 40, mouseX, mouseY) else 'gray'
    
def credits_onMousePress(app, mouseX, mouseY):
    setActiveScreen('home') if inBox(600, 20, 40, 40, mouseX, mouseY) else setActiveScreen('credits')

# MISC

def distance(x0, y0, x1, y1):
    return(((x1-x0)**2 + (y1-y0)**2)**0.5)
    
def inBox(x, y, width, height, mouseX, mouseY):
    return (x <= mouseX <= x + width) and (y <= mouseY <= y + height)

def inCircle(x, y, r, mouseX, mouseY):
    return distance(x, y, mouseX, mouseY) <= r
    
runAppWithScreens('home')
    