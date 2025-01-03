from cmu_graphics import *
from collections import defaultdict
import random
import math
import time
import copy

# Instructions
# AI

def onAppStart(app):
    setActiveScreen('home')
    app.width = 650
    app.height = 650
    # HOME
    app.homeScreen = '''cmu://872385/33944698/A+dark+figure+with+a+briefcase+peering+around+a+corner+in+a+city+at+night,
                        +with+another+dark+figure+walking+ahead,+facing+the+correct+way,+and+it+is+raining+(1).png''' # Generated using Copilot
    app.titlePt1 = 'cmu://872385/33944839/cooltext468551696595664.png' # From cooltext.com
    app.titlePt2 = 'cmu://872385/33944848/cooltext468551712153001.png' # From cooltext.com
    # SETUP
    app.setupScreen = 'cmu://872385/35316558/unblured+(1)+(1).jpeg' # from iStockphoto.com
    app.selectedMode = 'twoPlayers'
    app.specsSelected = False
    app.sliderMessage = 'Balanced, +0'
    app.numRounds = None
    app.currRound = 1
    app.aiDifficulty = None
    app.aiOn = False
    app.sliderX = 325
    app.sliderY = 240
    app.startingIntel = 0
    # NAME
    app.player1 = 'Type your name'
    app.player2 = 'Type your name'
    app.playerTypingName = 'player1'
    app.spyColor1 = 'red'
    app.spyColor2 = 'dodgerBlue'
    #--------* color selection
    app.rows = 2
    app.cols = 4
    app.cellBorderWidth = 2
    app.colorBoard = [['red', 'orange', 'yellow', 'green'],
                      ['dodgerBlue', 'indigo', 'pink', 'violet']]
    app.boardLeft1 = 120
    app.boardLeft2 = 370
    app.boardTop = 380
    
    app.player1Selecting = False
    app.selection1 = (0, 0)
    app.selection2 = (1, 0)

    app.selectionLocked = False
    # GAME
    app.map = 'cmu://872385/33943134/Screenshot+2024-10-18+172538+(1).png' # Generated using Copilot, then AI clarified
    app.cities = getRandomCities(app)
    app.numRounds = None
    app.currCity1 = None
    app.currCity2 = None
    app.transferTime = 5
    app.warningMessage = ''
    #--------* highlighting
    app.highlights = {'newGame': 'gray', 'tutorial': 'gray', 'credits': 'gray', 'rounds3': 'gray',\
                      'rounds5': 'gray', 'rounds7': 'gray','Control': 'white', 'Strike': 'white',\
                      'Wait': 'white', 'Locate': 'white', 'Go Deep': 'white', 'Expose': 'white',\
                      'Prepare': 'white', 'setupExit': 'white', 'gameExit': 'white', 'tutorialExit': 'white',\
                      'creditsExit': 'white', 'yes': 'white', 'no': 'white', 'aiEasy': 'gray', 'aiMedium': 'gray',\
                      'aiHard': 'gray', 'ai00': 'gray', 'twoPlayers': 'limeGreen', 'againstAI': 'gray', 'intelSelector': 'limeGreen',\
                      'prepDocuments': 'gray', 'backToBriefing': 'gray', 'launchMission': 'gray', 'typeName1': 'gray',\
                      'typeName2': 'gray', 'spy1': None, 'spy2': None, 'continueOperation': 'white', 'backToBase': 'white',\
                      'sliderMessage': 'white'}
    #--------* spy icons
    app.minSpawnDistance = 400
    app.spyWidth, app.spyHeight = 20, 70
    app.spy1x, app.spy1y, app.spy2x, app.spy2y = randomStartLocation(app)
    app.spy1Selected = False
    app.spy2Selected = False
    app.spiesTogether = False
    #--------* turns
    app.redTurn = True
    app.blueTurn = False
    #--------* actions
    app.actions = ['Control', 'Strike', 'Wait', 'Locate', 'Go Deep', 'Expose', 'Prepare']
    app.actionULCoords = [(270, 570),(375, 570),(480, 570),(585, 570),(690, 570),(795, 570),(900, 570)]
    app.redActionsLeft = 3
    app.blueActionsLeft = 3
    #--------* cover
    app.redCover = False
    app.blueCover = False
    app.deepCover1 = False
    app.deepCover2 = False
    #--------* intel
    app.intel1 = 0
    app.intel2 = 0
    #--------* suspicion
    app.suspicion1 = 0
    app.suspicion2 = 0
    #--------* mission end
    app.missionWin1 = False
    app.missionWin2 = False
    app.missionWinMethod = None
    app.winTracker = []
    #--------* operation end
    app.operationWin1 = False
    app.operationWin2 = False
    
# HOME

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
        setActiveScreen('setup')
    elif inBox(215, 415, 105, 36, mouseX, mouseY):
        app.width = 1000
        setActiveScreen('tutorial')
    elif inCircle(50, 50, 40, mouseX, mouseY):
        setActiveScreen('credits')

# SETUP

def setup_redrawAll(app):
    drawSetupBackground(app)
    drawExitButton(app, 600, 20, app.highlights['setupExit'])
    drawTwoPlayerSetup(app)
    drawAISetup(app)
    drawPrepDocuments(app)
    
def drawSetupBackground(app):
    setupBackground = drawImage(app.setupScreen, 0, 0)
    drawRect(80, 80, 490, 490, border = 'white', borderWidth = 2, opacity = 50)
    
def drawTwoPlayerSetup(app):
    drawLabel('Two Players:', 325, 140, fill = app.highlights['twoPlayers'], size = 30, font = 'orbitron', bold = True)
    drawLabel('-------------------------------------', 325, 180, fill = 'white', size = 25)
    drawStartingIntel(app)
    drawRoundsSelector(app)
    
def drawStartingIntel(app):
    drawLabel('Starting Intel:', 325, 215, fill = 'white', size = 20, font = 'orbitron')
    drawLabel(app.sliderMessage, app.sliderX, 280, fill = app.highlights['sliderMessage'], size = 20, font = 'orbitron', bold = True)
    drawRect(160, 250, 325, 2, fill = 'gray')
    drawRect(app.sliderX - 20, app.sliderY, 40, 20, fill = app.highlights['intelSelector'], border = 'black')
    
def drawRoundsSelector(app):
    drawLabel('Number of Rounds:', 325, 320, fill = 'white', size = 20, font = 'orbitron')
    drawRect(170, 350, 80, 50, fill = None, border = app.highlights['rounds3'])
    drawRect(280, 350, 80, 50, fill = None, border = app.highlights['rounds5'])
    drawRect(390, 350, 80, 50, fill = None, border = app.highlights['rounds7'])
    drawLabel('3', 210, 375, fill = app.highlights['rounds3'], size = 25, font = 'orbitron', bold = True)
    drawLabel('5', 320, 375, fill = app.highlights['rounds5'], size = 25, font = 'orbitron', bold = True)
    drawLabel('7', 430, 375, fill = app.highlights['rounds7'], size = 25, font = 'orbitron', bold = True)
    
def drawAISetup(app):
    drawLabel('Against AI:', 325, 440, fill = app.highlights['againstAI'], size = 30, bold = True, font = 'orbitron')
    drawLabel('-------------------------------------', 325, 480, fill = 'white', size = 25)
    drawRect(102, 500, 100, 50, fill = None, border = app.highlights['aiEasy'])
    drawRect(217, 500, 100, 50, fill = None, border = app.highlights['aiMedium'])
    drawRect(332, 500, 100, 50, fill = None, border = app.highlights['aiHard'])
    drawRect(447, 500, 100, 50, fill = None, border = app.highlights['ai00'])
    drawLabel('Easy', 152, 522, fill = app.highlights['aiEasy'], size = 20, font = 'orbitron')
    drawLabel('Medium', 268, 522, fill = app.highlights['aiMedium'], size = 20, font = 'orbitron')
    drawLabel('Hard', 382, 522, fill = app.highlights['aiHard'], size = 20, font = 'orbitron')
    drawLabel('00', 498, 522, fill = app.highlights['ai00'], size = 20, font = 'orbitron')
    
def drawPrepDocuments(app):
    if app.specsSelected:
        drawRect(500, 280, 120, 80, fill = 'black', border = app.highlights['prepDocuments'], borderWidth = 2)
        drawLabel('Prepare', 560, 305, fill = 'limeGreen', size = 16, font = 'orbitron', bold = True)
        drawLabel('Documents', 560, 330, fill = 'limeGreen', size = 16, font = 'orbitron', bold = True)
    
def setup_onMouseMove(app, mouseX, mouseY):
    app.highlights['setupExit'] = 'limeGreen' if mouseInExitButton(app, 600, 20, mouseX, mouseY) else 'white'
    app.highlights['prepDocuments'] = 'limeGreen' if inBox(500, 280, 120, 80, mouseX, mouseY) else 'gray'
    if app.selectedMode == 'twoPlayers':
        app.highlights['againstAI'] = 'limeGreen' if inBox(240, 430, 170, 25, mouseX, mouseY) else 'gray'
        if not app.specsSelected:
            app.highlights['rounds3'] = 'limeGreen' if inBox(170, 350, 80, 50, mouseX, mouseY) else 'gray'
            app.highlights['rounds5'] = 'limeGreen' if inBox(280, 350, 80, 50, mouseX, mouseY) else 'gray'
            app.highlights['rounds7'] = 'limeGreen' if inBox(390, 350, 80, 50, mouseX, mouseY) else 'gray'
            
    elif app.selectedMode == 'againstAI':
        app.highlights['twoPlayers'] = 'limeGreen' if inBox(210, 130, 230, 25, mouseX, mouseY) else 'gray'
        if not app.specsSelected:
            app.highlights['aiEasy'] = 'limeGreen' if inBox(102, 500, 100, 50, mouseX, mouseY) else 'gray'
            app.highlights['aiMedium'] = 'limeGreen' if inBox(217, 500, 100, 50, mouseX, mouseY) else 'gray'
            app.highlights['aiHard'] = 'limeGreen' if inBox(332, 500, 100, 50, mouseX, mouseY) else 'gray'
            app.highlights['ai00'] = 'limeGreen' if inBox(447, 500, 100, 50, mouseX, mouseY) else 'gray'

def setup_onMousePress(app, mouseX, mouseY):
    if inBox(210, 130, 230, 25, mouseX, mouseY): # two players button
        app.selectedMode = 'twoPlayers'
        app.specsSelected = False
        app.highlights['intelSelector'] = 'limeGreen'
        clearAIHighlights(app)
    if app.selectedMode == 'twoPlayers':
        if inBox(170, 350, 80, 50, mouseX, mouseY):
            app.numRounds = 3
            app.specsSelected = True
            clearTwoPlayerHighlights(app)
            app.highlights['rounds3'] = 'limeGreen'
        elif inBox(280, 350, 80, 50, mouseX, mouseY):
            app.numRounds = 5
            app.specsSelected = True
            clearTwoPlayerHighlights(app)
            app.highlights['rounds5'] = 'limeGreen'
        elif inBox(390, 350, 80, 50, mouseX, mouseY):
            app.numRounds = 7
            app.specsSelected = True
            clearTwoPlayerHighlights(app)
            app.highlights['rounds7'] = 'limeGreen'
        # updates the win tracker accordingly
        if app.numRounds != None:
            app.winTracker = app.numRounds * [None]
            
    if inBox(240, 430, 170, 25, mouseX, mouseY): # against AI button
        app.selectedMode = 'againstAI'
        app.specsSelected = False
        clearTwoPlayerHighlights(app)
    if app.selectedMode == 'againstAI':
        if inBox(102, 500, 100, 50, mouseX, mouseY):
            app.aiOn = True
            app.aiDifficulty = 'easy'
            app.specsSelected = True
            clearAIHighlights(app)
            app.highlights['aiEasy'] = 'limeGreen'
        elif inBox(217, 500, 100, 50, mouseX, mouseY):
            app.aiOn = True
            app.aiDifficulty = 'medium'
            app.specsSelected = True
            clearAIHighlights(app)
            app.highlights['aiMedium'] = 'limeGreen'
        elif inBox(332, 500, 100, 50, mouseX, mouseY):
            app.aiOn = True
            app.aiDifficulty = 'hard'
            app.specsSelected = True
            clearAIHighlights(app)
            app.highlights['aiHard'] = 'limeGreen'
        elif inBox(447, 500, 100, 50, mouseX, mouseY):
            app.aiOn = True
            app.aiDifficulty = '00'
            app.specsSelected = True
            clearAIHighlights(app)
            app.highlights['ai00'] = 'limeGreen'
    if inBox(500, 280, 140, 80, mouseX, mouseY) and app.specsSelected: 
        setActiveScreen('name')
    elif mouseInExitButton(app, 600, 20, mouseX, mouseY):
        setActiveScreen('home')

def clearAIHighlights(app):
    if app.selectedMode != 'againstAI':
        app.highlights['againstAI'] = 'gray'
    app.highlights['aiEasy'] = 'gray'
    app.highlights['aiMedium'] = 'gray'
    app.highlights['aiHard'] = 'gray'
    app.highlights['ai00'] = 'gray'

def clearTwoPlayerHighlights(app):
    if app.selectedMode != 'twoPlayers':
        app.highlights['twoPlayers'] = 'gray'
        app.highlights['intelSelector'] = 'gray'
    app.highlights['rounds3'] = 'gray'
    app.highlights['rounds5'] = 'gray'
    app.highlights['rounds7'] = 'gray'

def setup_onMouseDrag(app, mouseX, mouseY):
    if (160 <= mouseX <= 490 and 200 <= mouseY <= 300) and app.selectedMode == 'twoPlayers':
        app.sliderX = mouseX
    # slider in the middle 
    if 300 <= app.sliderX <= 340:
        app.sliderMessage = 'Balanced, +0'
        app.intel1 = app.intel2 = 0
        app.highlights['sliderMessage'] = 'white'
    # slider traversing left
    elif app.sliderX < 300:
        if 260 <= app.sliderX < 300:
            app.sliderMessage = 'P1, +10'
            app.intel1 = 10
        elif 220 <= app.sliderX < 260:
            app.sliderMessage = 'P1, +20'
            app.intel1 = 20
        elif 180 <= app.sliderX < 220:
            app.sliderMessage = 'P1, +30'
            app.intel1 = 30
        else:
            app.sliderMessage = 'P1, +40'
            app.intel1 = 40
        app.highlights['sliderMessage'] = 'red'
    # slider traversing right
    elif app.sliderX > 340:
        if 340 <= app.sliderX < 380:
            app.sliderMessage = 'P2, +10'
            app.intel2 = 10
        elif 380 <= app.sliderX < 420:
            app.sliderMessage = 'P2, +20'
            app.intel2 = 20
        elif 420 <= app.sliderX < 460:
            app.sliderMessage = 'P2, +30'
            app.intel2 = 30
        else:
            app.sliderMessage = 'P2, +40'
            app.intel2 = 40
        app.highlights['sliderMessage'] = 'dodgerBlue'
    
# NAME 

def name_redrawAll(app):
    drawNameBackground(app)
    drawTitles(app)
    drawNameInputs(app)
    drawAvatars(app)
    drawColorSelection(app)
    drawToBriefing(app)
    drawLaunchMission(app)
    
def drawNameBackground(app):
    setupBackground = drawImage(app.setupScreen, 0, 0)
    drawRect(80, 120, 490, 400, border = 'white', borderWidth = 2, opacity = 50)
    
def drawTitles(app):
    drawLabel('Player 1', 200, 160, fill = 'limeGreen', size = 25, font = 'orbitron', bold = True)
    drawLabel('Player 2', 450, 160, fill = 'limeGreen', size = 25, font = 'orbitron', bold = True)
    drawLine(325, 120, 325, 520, fill = 'gray', lineWidth = 2)

def drawNameInputs(app):
    drawRect(120, 300, 160, 40, fill = None, border = app.highlights['typeName1'])
    drawRect(370, 300, 160, 40, fill = None, border = app.highlights['typeName2'])
    drawLabel(app.player1, 200, 320, size = 15, fill = 'limeGreen', font = 'orbitron', bold = True)
    drawLabel(app.player2, 450, 320, size = 15, fill = 'limeGreen', font = 'orbitron', bold = True)

def drawAvatars(app):
    drawPolygon(200, 220, 220, 240, 200, 280, 180, 240, fill = app.spyColor1)
    drawCircle(200, 240, 7, fill = 'gold')
    drawPolygon(450, 220, 470, 240, 450, 280, 430, 240, fill = app.spyColor2)
    drawCircle(450, 240, 7, fill = 'gold')
    
def drawColorSelection(app):
    drawBoardBorder(app, 120, 380, 160, 80)
    drawBoardBorder(app, 370, 380, 160, 80)
    drawBoard(app, app.colorBoard, 120, 380, 160, 80)
    drawBoard(app, app.colorBoard, 370, 380, 160, 80)
    
def drawToBriefing(app):
    drawRect(10, 280, 100, 80, fill = 'black', border = app.highlights['backToBriefing'], borderWidth = 2)
    drawLabel('Back to', 57, 305, fill = 'limeGreen', size = 16, font = 'orbitron', bold = True)
    drawLabel('Briefing', 57, 330, fill = 'limeGreen', size = 16, font = 'orbitron', bold = True)
    
def drawLaunchMission(app):
    drawRect(540, 280, 100, 80, fill = 'black', border = app.highlights['launchMission'], borderWidth = 2)
    drawLabel('Launch', 590, 305, fill = 'red', size = 16, font = 'orbitron', bold = True)
    drawLabel('Mission', 590, 330, fill = 'red', size = 16, font = 'orbitron', bold = True)
    
# From good 'ol Tetris.

def drawBoard(app, boardName, x, y, width, height):
    for row in range(app.rows):
        for col in range(app.cols):
            color = boardName[row][col]
            drawCell(app, row, col, color, x, y, width, height)

def drawBoardBorder(app, x, y, width, height):
    drawRect(x - 5, y - 5, width + 10, height + 10,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color, left, top, width, height):
    cellLeft, cellTop = getCellLeftTop(app, row, col, left, top, width, height)
    cellWidth, cellHeight = getCellSize(app, width, height)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill = color, border = 'black',
             borderWidth = app.cellBorderWidth)
    if app.spyColor1 == color:
        drawLabel('1', cellLeft + cellWidth//2, cellTop + cellHeight//2, fill = 'limeGreen', size = 30, font = 'orbitron', bold = True)
    elif app.spyColor2 == color:
        drawLabel('2', cellLeft + cellWidth//2, cellTop + cellHeight//2, fill = 'limeGreen', size = 30, font = 'orbitron', bold = True)

def getCellLeftTop(app, row, col, left, top, width, height):
    cellWidth, cellHeight = getCellSize(app, width, height)
    cellLeft = left + col * cellWidth
    cellTop = top + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app, width, height):
    cellWidth = width / app.cols
    cellHeight = height / app.rows
    return (cellWidth, cellHeight)

def getCell(app, x, y, width, height):
    if app.player1Selecting:
        dx = x - app.boardLeft1
        dy = y - app.boardTop
    else:
        dx = x - app.boardLeft2
        dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app, width, height)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None
          
def name_onMouseMove(app, mouseX, mouseY):
    if inBox(120, 300, 160, 40, mouseX, mouseY):
        app.highlights['typeName1'] = 'limeGreen' 
    else:
        app.playerTypingName = None
        app.highlights['typeName1'] = 'gray'
        
    if inBox(370, 300, 160, 40, mouseX, mouseY):
        app.highlights['typeName2'] = 'limeGreen' 
    else:
        app.playerTypingName = None
        app.highlights['typeName2'] = 'gray'
    # color selection
    app.player1Selecting = True if mouseX <= app.width//2 else False
    # forward/back buttons      
    app.highlights['backToBriefing'] = 'limeGreen' if inBox(10, 280, 100, 80, mouseX, mouseY) else 'gray'
    app.highlights['launchMission'] = 'limeGreen' if inBox(540, 280, 100, 80, mouseX, mouseY) else 'gray'
     
def name_onMousePress(app, mouseX, mouseY):
    # more color selecting
    selectedCell = getCell(app, mouseX, mouseY, 160, 80)
    if selectedCell != None:
        row = selectedCell[0]
        col = selectedCell[1]
        color = app.colorBoard[row][col]
        if app.player1Selecting and color != app.spyColor2:
            app.spyColor1 = color
        elif not app.player1Selecting and color != app.spyColor1: 
            app.spyColor2 = color
        
    # other buttons   
    if inBox(120, 300, 160, 40, mouseX, mouseY):
        app.player1 = '|'
        app.playerTypingName = 'player1'
    elif inBox(370, 300, 160, 40, mouseX, mouseY):
        app.player2 = '|'
        app.playerTypingName = 'player2'
    elif inBox(10, 280, 100, 80, mouseX, mouseY):
        setActiveScreen('setup')
    elif inBox(540, 280, 100, 80, mouseX, mouseY):
        app.width = 1000
        setActiveScreen('game') 
          
def name_onKeyPress(app, key):
    # player1 typing name...
    if app.playerTypingName == 'player1':
        if app.player1 == '|':
            app.player1 = ''
        if key == 'backspace' and len(app.player1) >= 0:
            app.player1 = app.player1[:-1]
            app.player1 = '|'
        elif key == 'space':
            app.player1 += ' '
        elif len(app.player1) <= 15 and key.isalpha():
            app.player1 += key
    # player2 typing name...
    elif app.playerTypingName == 'player2':
        if app.player2 == '|':
            app.player2 = ''
        if key == 'backspace' and len(app.player2) >= 0:
            app.player2 = app.player2[:-1]
            app.player2 = '|'
        elif key == 'space':
            app.player2 += ' '
        elif len(app.player2) <= 15 and key.isalpha():
            app.player2 += key

# TUTORIAL

def drawTutorialBackground(app):
    drawMap(app)
    drawDossier(app)
    drawIntel(app)
    drawActionCountBoxes(app)
    drawSuspicionMeter(app)
    drawActionBoxes(app)
    drawTravelLines(app)
    drawCities(app)
    drawSpyIcons(app)

def tutorial_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial(app)

def drawTutorial(app):
    drawRect(250, 250, 500, 150, opacity = 60, border = 'gold')
    drawLabel('Welcome to spy school, Agent.', 500, 300, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('(click anywhere to continue)', 500, 340, fill = 'limeGreen', size = 20, font = 'orbitron')

def tutorial_onMousePress(app, mouseX, mouseY):
    setActiveScreen('tutorial2')
    
# Tutorial Screen 2

def tutorial2_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial2(app)
    
def drawTutorial2(app):
    drawRect(180, 360, 540, 100, opacity = 60, border = 'gold')
    drawLabel('This is your character pin. Find it on the map.', 450, 390, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('Your opponent is the opposite color.', 450, 430, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLine(180, 460, 70, 510, fill = 'white', lineWidth = 3)
    drawCircle(70, 510, 5, fill = 'limeGreen')

def tutorial2_onMousePress(app, mouseX, mouseY):
    setActiveScreen('tutorial3')
    
def tutorial3_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial3(app)
    
def drawTutorial3(app):
    drawRect(220, 260, 560, 200, opacity = 60, border = 'gold')
    drawLabel('These are your action and suspicion trackers.', 500, 300, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('Suspicion is gained by moving, failed strikes,', 500, 340, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel("and controlling cities' informants.", 500, 380, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('Any suspicion over 100 is fatal!', 500, 420, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLine(600, 460, 600, 480, fill = 'white', lineWidth = 3)
    drawLine(600, 480, 520, 500, fill = 'white', lineWidth = 3)
    drawLine(600, 480, 540, 540, fill = 'white', lineWidth = 3)
    drawCircle(520, 500, 5, fill = 'limeGreen')
    drawCircle(540, 540, 5, fill = 'limeGreen')
    
def tutorial3_onMousePress(app, mouseX, mouseY):
    setActiveScreen('tutorial4')
    
def tutorial4_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial4(app)

def drawTutorial4(app):
    drawRect(200, 250, 650, 120, opacity = 60, border = 'gold')
    drawLabel('Move by dragging your pin to a connected city.', 525, 280, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('When you do, you gain COVER, hiding your exact location.', 525, 320, fill = 'limeGreen', size = 20, font = 'orbitron')

def tutorial4_onMousePress(app, mouseX, mouseY):
    setActiveScreen('tutorial5')
    
def tutorial5_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial5(app)

def drawTutorial5(app):
    drawRect(100, 20, 800, 440, opacity = 60, border = 'gold')
    drawLabel('This is the action bar.', 500, 50, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('_____________________________________', 500, 70, fill = 'white')
    drawLabel('Control: Control a city. Opponent will blow cover when entering. Gain 3 intel per turn.',\
               500, 100, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLabel('Strike: Attempt a strike at current location. Win if opponent is there.', 500, 150, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLabel('Wait: Decrease suspicion by 20 and gain cover.', 500, 200, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLabel("Locate (10 Intel): Blow opponent's cover.", 500, 250, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLabel('Go Deep (20 Intel): Your cover cannot be blown for 1 turn, including Locate actions.', 500, 300, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLabel("Expose (20 Intel): Raise opponent's suspicion by 25.", 500, 350, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLabel('Prepare (40 Intel): Get an additional action.', 500, 400, fill = 'limeGreen', size = 16, font = 'orbitron')
    drawLine(500, 460, 620, 580, fill = 'white', lineWidth = 3)
    drawCircle(620, 580, 5, fill = 'limeGreen')
    
def tutorial5_onMousePress(app, mouseX, mouseY):
    setActiveScreen('tutorial6')

def tutorial6_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial6(app)

def drawTutorial6(app):
    drawRect(130, 260, 740, 150, opacity = 60, border = 'gold')
    drawLabel('One more thing: cutting off a city from all immediate neighbors', 500, 300, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('forms a SPYRING. You automatically control the cut-off city.', 500, 350, fill = 'limeGreen', size = 20, font = 'orbitron')

def tutorial6_onMousePress(app, mouseX, mouseY):
    setActiveScreen('tutorial7')
    
def tutorial7_redrawAll(app):
    drawTutorialBackground(app)
    drawTutorial7(app)
    
def drawTutorial7(app):
    drawRect(200, 260, 600, 140, opacity = 60, border = 'gold')
    drawLabel("Alright, that's everything. Good luck out there.", 500, 300, fill = 'limeGreen', size = 20, font = 'orbitron')
    drawLabel('*Transmission Terminated*', 500, 350, fill = 'limeGreen', size = 20, font = 'orbitron')

def tutorial7_onMousePress(app, mouseX, mouseY):
    app.width = 650
    setActiveScreen('home')
    
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
        
    def __repr__(self):
        return f'({self.cx}, {self.cy}, {self.name}, {self.abbrev}, {self.status}, {self.possibleConnections}, {self.realConnections}, {self.maxConnections})'
    
    def __eq__(self, other):
        if isinstance(self, City) and isinstance(other, City):
            return self.cx == other.cx and self.cy == other.cy and self.name == other.name and self.abbrev == other.abbrev and\
                   self.status == other.status and self.possibleConnections == other.possibleConnections and\
                   self.realConnections == other.realConnections and self.maxConnections == other.maxConnections
        else:
            return False
    
    def __hash__(self):
        return hash(str(self))
    
class Action:
    def __init__(self, cx, cy, width, height, label, highlighted):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.label = label
        self.highlighted = highlighted
    
    def __repr__(self):
        return f'({self.cx}, {self.cy}, {self.width}, {self.height}, {self.label}, {self.highlighted})'

def game_redrawAll(app):
    drawMap(app)
    drawExitButton(app, 940, 20, app.highlights['gameExit'])
    if not app.aiOn:
        drawRoundMarker(app)
    drawDossier(app)
    drawIntel(app)
    drawTurnMarker(app)
    drawActionCountBoxes(app)
    drawSuspicionMeter(app)
    drawActionBoxes(app)
    drawWarningMessage(app)
    drawTravelLines(app)
    drawCities(app)
    drawSpyIcons(app)

def drawMap(app):
    drawImage(app.map, 0, 0)
    drawRect(0, 500, 1000, 650, fill = 'black') # covers up bottom of screen

def drawRoundMarker(app):
    drawLabel(f'Mission {app.currRound}/{app.numRounds}', 110, 40, fill = 'limeGreen', size = 25, font = 'orbitron', bold = True)
    
def drawDossier(app):
    dossier = 'cmu://872385/35273263/a0a35196f90b43dc34d532c2252070c0+(1).jpg'
    dossierX = 15
    dossierY = 460
    drawImage(dossier, dossierX, dossierY)
    if app.redTurn:
        drawPolygon(72, 487, 57, 500, 72, 530, 87, 500, fill = app.spyColor1, rotateAngle = -5)
        drawCircle(72, 502, 5, fill = 'gold')
    elif app.blueTurn:
        drawPolygon(72, 487, 57, 500, 72, 530, 87, 500, fill = app.spyColor2, rotateAngle = -5)
        drawCircle(72, 502, 5, fill = 'gold')

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
        if app.player1 != '' and app.player1 != '|' and app.player1 != 'Type your name':
            drawLabel(f"{app.player1}'s Turn", 700, 530, fill = 'limeGreen', font = 'orbitron', bold = True, size = 30)
        else:
            drawLabel(f"{app.spyColor1.capitalize()}'s Turn", 700, 530, fill = 'limeGreen', font = 'orbitron', bold = True, size = 30)
    elif app.blueTurn:
        if app.player2 != '' and app.player2 != '|' and app.player2 != 'Type your name':
            drawLabel(f"{app.player2}'s Turn", 700, 530, fill = 'limeGreen', font = 'orbitron', bold = True, size = 30)
        else:
            drawLabel(f"{app.spyColor2.capitalize()}'s Turn", 700, 530, fill = 'limeGreen', font = 'orbitron', bold = True, size = 30)

def drawActionCountBoxes(app):
    actionBoxes = 2
    drawLabel('Actions:', 380, 500, fill = 'limeGreen', size = 20, font = 'orbitron', bold = True)
    if app.redTurn:
        for i in range(app.redActionsLeft):
            drawRect(435 + 20*i, 497, 10, 10, fill = 'limeGreen')
            drawRect(435 + 20*i, 497, 10, 10, fill = None, border = 'limeGreen', borderWidth = 2)
    elif app.blueTurn:
        for i in range(app.blueActionsLeft):
            drawRect(435 + 20*i, 497, 10, 10, fill = 'limeGreen')
            drawRect(435 + 20*i, 497, 10, 10, fill = None, border = 'limeGreen', borderWidth = 2)

def drawSuspicionMeter(app):
    drawRect(400, 525, 120, 30, fill = None, border = 'limeGreen')
    drawLabel('Suspicion:', 330, 540, fill = 'limeGreen', size = 20, font = 'orbitron', bold = True)
    if app.redTurn == True:
        if app.suspicion1 != 0:
            drawRect(400, 525, int(app.suspicion1 * 1.2), 30, fill = findSuspicionMeterFill(app.suspicion1), opacity = 50)
        drawLabel(f'{app.suspicion1}', 460, 540, fill = 'limeGreen', size = 20, font = 'orbitron')
    elif app.blueTurn == True:
        if app.suspicion2 != 0:
            drawRect(400, 525, int(app.suspicion2 * 1.2), 30, fill = findSuspicionMeterFill(app.suspicion2), opacity = 50)
        drawLabel(f'{app.suspicion2}', 460, 540, fill = 'limeGreen', size = 20, font = 'orbitron')
    
def findSuspicionMeterFill(suspicion):
    if 0 <= suspicion <= 25:
        return 'lightGreen'
    elif 25 < suspicion <= 50:
        return 'yellow'
    elif 50 < suspicion <= 75:
        return 'orange'
    else:
        return 'red'

def drawActionBoxes(app):
    for i in range(len(app.actions)):
        action = Action(310 + i*105, 600, 95, 60, app.actions[i], False)
        drawRect(action.cx, action.cy, action.width, action.height, align = 'center', fill = None,\
                 border = app.highlights[app.actions[i]], borderWidth = 2)
        drawLabel(action.label, action.cx, action.cy - 5, size = 14, font = 'orbitron', fill = 'limeGreen', bold = True)
    # addition intel costs
    drawLabel('(10)', 625, 615, fill = 'limeGreen', size = 15, font = 'orbitron')
    drawLabel('(20)', 730, 615, fill = 'limeGreen', size = 15, font = 'orbitron')
    drawLabel('(20)', 835, 615, fill = 'limeGreen', size = 15, font = 'orbitron')
    drawLabel('(40)', 940, 615, fill = 'limeGreen', size = 15, font = 'orbitron')
    
def drawWarningMessage(app):
    drawLabel(app.warningMessage, 700, 480, fill = 'red', size = 25, font = 'orbitron', bold = True)
    
def drawTravelLines(app):
    for city in app.cities:
        x0 = city.cx
        y0 = city.cy
        for connectedCity in city.realConnections:
            x1 = app.cityCoords[connectedCity].cx
            y1 = app.cityCoords[connectedCity].cy
            drawLine(x0, y0, x1, y1, fill = 'lightGreen', lineWidth = 2)
        
def drawCities(app):
    for city in app.cities:
        if city.status >= 1:
            city.status = 1 # defensive
            drawCircle(city.cx, city.cy, 10, fill = app.spyColor1)
        elif city.status == 0:
            drawCircle(city.cx, city.cy, 10, fill = 'gray')
        elif city.status <= -1:
            city.status = -1 # defensive
            drawCircle(city.cx, city.cy, 10, fill = app.spyColor2)
            
        drawCircle(city.cx, city.cy, 6, fill = 'white')
        drawCircle(city.cx, city.cy, 2, fill = 'black')
        drawRect(city.cx - 15, city.cy + 15, 30, 13, fill = 'black', opacity = 70)
        drawLabel(city.abbrev, city.cx, city.cy + 20, fill = 'white', font = 'orbitron', bold = True, size = 12)
        
def getRandomCities(app):
    randCities = []
    app.numCities = 35
    app.cityCoords = {"Algiers"      :City(480,230,'Algiers','ALG',0,['Ankara','Bermuda','Cairo','Lagos','Madrid'],[],2),
                      "Anchorage"    :City(80,160,'Anchorage','ANCH',0,['Honolulu','San Francisco','Yellowknife'],[],2),
                      "Ankara"       :City(560,210,'Ankara','ANK',0,['Cairo','Delhi','Moscow','Ur'],[],3),
                      "Beijing"      :City(750,200,'Beijing','BEI',0,['Delhi','Hanoi','Novosibrisk','Tokyo','Ur','Vladivostok'],[],4),
                      "Berlin"       :City(505,170,'Berlin','BER',0,['Algiers','London','Madrid','St.Petersburg'],[],4),
                      "Bermuda"      :City(360,240,'Bermuda','BRM',0,['Bogota','Lagos','Madrid','New York'],[],3),
                      "Bogota"       :City(280,320,'Bogota','BOG',0,['Bermuda','Lagos','Lima','Mexico City'],[],2),
                      "Cairo"        :City(520,245,'Cairo','CAI',0,['Algiers','Ankara','Khartoum','Lagos'],[],3),
                      "Chicago"      :City(240,200,'Chicago','CHI',0,['New York','San Francisco','Yellowknife'],[],2),
                      "Delhi"        :City(660,250,'Delhi','DEH',0,['Ankara','Beijing','Hanoi','Khartoum','Singapore'],[],4),
                      "Hanoi"        :City(740,270,'Hanoi','HAN',0,['Delhi','Jakarta','Singapore','Tokyo'],[],3),
                      "Honolulu"     :City(80, 280,'Honolulu','HONO',0,['Anchorage','Mexico City','Honolulu'],[],2),
                      "Iceland"      :City(410,120,'Iceland','ICE',0,['London','St.Petersburg','Yellowknife'],[],1),
                      "Jakarta"      :City(800,340,'Jakarta','JAK',0,['Hanoi','Singapore','Sydney','Tokyo'],[],3),
                      "Johannesburg" :City(520,380,'Johannesburg','JOH',0,['Khartoum','Lagos','Madagascar','Sao Paulo'],[],3),
                      "Khartoum"     :City(550,300,'Khartoum','KHAR',0,['Cairo','Delhi','Johannesburg','Madagascar'],[],3),
                      "Lagos"        :City(460,290,'Lagos','LAG',0,['Algiers','Bermuda','Bogota','Johannesburg'],[],3),
                      "Lima"         :City(290,380,'Lima','LIM',0,['Bogota','Sao Paulo','Santiago'],[],2),
                      "London"       :City(450,155,'London','LON',0,['Berlin','Iceland','Madrid','New York'],[],3),
                      "Madagascar"   :City(580,360,'Madagascar','MAD',0,['Johannesburg','Khartoum','Singapore','Sydney'],[],1),
                      "Madrid"       :City(440,200,'Madrid','MAD',0,['Algiers','Bermuda','London','New York'],[],2),
                      "Mexico City"  :City(220,270,'Mexico City','MEXC',0,['Bogota', 'Chicago','Honolulu','New York','San Francisco'],[],3),
                      "Moscow"       :City(580,150,'Moscow','MOS',0,['Ankara','Berlin','St.Petersburg','Ur'],[],4),
                      "New York"     :City(290,210,'New York','NYC',0,['Bermuda','Chicago','Iceland','London','Madrid','Mexico City'],[],4),
                      "Novosibrisk"  :City(700,140,'Novosibrisk','NOV',0,['Beijing','Moscow','Ur','Vladivostok'],[],2),
                      "Santiago"     :City(280,440,'Santiago','SAN',0,['Honolulu','Lima','Sao Paulo'],[],2),
                      "San Francisco":City(170,220,'San Francisco','SAN',0,['Honolulu', "Mexico City", "Chicago", "Yellowknife"],[],3),
                      "Sao Paulo"    :City(340,400,'Sao Paulo','SAU',0,['Johannesburg','Lagos','Lima','Santiago'],[],2),
                      "Singapore"    :City(720,310,'Singapore','SING',0,['Delhi','Hanoi','Jakarta','Madagascar'],[],3),
                      "St.Petersburg":City(540,120,'St.Petersburg','STP',0,['Berlin','Iceland','London','Moscow'],[],3),
                      "Sydney"       :City(880,400,'Sydney','SYD',0,['Jakarta','Madagascar','Tokyo'],[],2),
                      "Tokyo"        :City(820,220,'Tokyo','TOK',0,['Beijing','Hanoi','Jakarta','Sydney','Vladivostok'],[],4),
                      "Ur"           :City(640,170,'Ur','UR', 0,['Ankara','Beijing','Moscow','Novosibrisk'],[],1),
                      "Vladivostok"  :City(820,160,'Vladivostok','VLA',0,['Beijing','Novosibrisk','Tokyo'],[],2),
                      "Yellowknife"  :City(200,160,'Yellowknife','YEL',0,['Anchorage','Chicago','Iceland','San Francisco'],[],1)}
    
    chosenCities = random.sample(list(app.cityCoords.values()), app.numCities)
    for chosenCity in chosenCities:
        while len(chosenCity.realConnections) < chosenCity.maxConnections:
            randIndex = random.randint(0, len(chosenCity.possibleConnections) - 1)
            newConnection = chosenCity.possibleConnections[randIndex]
            chosenCity.realConnections.append(newConnection) 
            chosenCity.possibleConnections.pop(randIndex) # fine to mutate since it will reset every mission
        for connection in chosenCity.realConnections:
            i = findIndexByName(chosenCities, connection)
            if i != None:
                chosenCities[i].realConnections.append(chosenCity.name) # ensures bidirectionality on the graph
    return chosenCities

def findIndexByName(chosenCities, connection):
    for i in range(len(chosenCities)):
        if chosenCities[i].name == connection:
            return i
    
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
    if app.spiesTogether and (not app.redCover and not app.blueCover) and (not app.deepCover1 and not app.deepCover2): 
    # draw special w/two spies in one node
        drawPolygon(app.spy1x, app.spy1y, app.spy1x-10, app.spy1y-20, app.spy1x, app.spy1y-30, app.spy1x+10, app.spy1y-20, \
                    fill = app.spyColor1, border = app.highlights['spy1'], borderWidth = 2)
        drawCircle(app.spy1x, app.spy1y - 18, 3, fill = 'gold')
        drawPolygon(app.spy2x+10, app.spy2y+10, app.spy2x, app.spy2y-10, app.spy2x+10, app.spy2y-20, app.spy2x+20, app.spy2y-10, \
                    fill = app.spyColor2, border = app.highlights['spy2'], borderWidth = 2)
        drawCircle(app.spy2x+10, app.spy2y - 8, 3, fill = 'gold')
    else:
        if app.redTurn or (not app.redCover and not app.deepCover1):
            drawPolygon(app.spy1x, app.spy1y, app.spy1x-10, app.spy1y-20, app.spy1x, app.spy1y-30, app.spy1x+10, app.spy1y-20, \
                        fill = app.spyColor1, border = app.highlights['spy1'], borderWidth = 2)
            drawCircle(app.spy1x, app.spy1y - 18, 3, fill = 'gold')
        if app.blueTurn or (not app.blueCover and not app.deepCover2):
            drawPolygon(app.spy2x, app.spy2y, app.spy2x-10, app.spy2y-20, app.spy2x, app.spy2y-30, app.spy2x+10, app.spy2y-20, \
                        fill = app.spyColor2, border = app.highlights['spy2'], borderWidth = 2)
            drawCircle(app.spy2x, app.spy2y - 18, 3, fill = 'gold')
 
# Game controllers below

def game_onMouseMove(app, mouseX, mouseY):
    app.highlights['spy1'] = 'white' if mouseInSpy1(app, mouseX, mouseY) else None
    app.highlights['spy2'] = 'white' if mouseInSpy2(app, mouseX, mouseY) else None
    app.highlights['gameExit'] = 'limeGreen' if mouseInExitButton(app, 940, 20, mouseX, mouseY) else 'white'
    for i, action in enumerate(app.actions):
        app.highlights[action] = 'lightGreen' if mouseInAction(app, mouseX, mouseY, i) else 'white'

# if a city is completely cut off with controlled cities of one color, it becomes controlled by that player too
# surrounded != cut off; the controlled cities must be immediate neighbors to the surrounded city.
def checkCitySurrounded(app):
    for city in app.cities:
        surrounded = True
        if app.redTurn:
            for connected in city.realConnections:
                status = app.cityCoords[connected].status
                if status == -1 or status == 0:
                    surrounded = False
                    break
            if surrounded:
                city.status = 1
        elif app.blueTurn:
            for connected in city.realConnections:
                status = app.cityCoords[connected].status
                if status == 1 or status == 0:
                    surrounded = False
                    break
            if surrounded:
                city.status = -1

def game_onMousePress(app, mouseX, mouseY):
    app.spy1Selected = True if mouseInSpy1(app, mouseX, mouseY) else False
    app.spy2Selected = True if mouseInSpy2(app, mouseX, mouseY) else False
    # Control
    if mouseInAction(app, mouseX, mouseY, 0):
        if app.redTurn and app.currCity1.status < 1:
            i = app.cities.index(app.currCity1)
            # if already controlled by blue
            if app.cities[i].status == -1:
                if app.spiesTogether:
                    app.currCity2.status += 2
                app.cities[i].status += 2
                app.currCity1.status += 2
            # if neutral
            else:
                if app.spiesTogether:
                    app.currCity2.status += 1
                app.cities[i].status += 1
                app.currCity1.status += 1
            # if you control the city your opponent is in, reveal them
            if app.spiesTogether:
                app.blueCover = False
            # ending on a control also reveals your position
            app.redCover = False
            app.suspicion1 += 10
            app.redActionsLeft -= 1
        elif app.blueTurn and app.currCity2.status > -1:
            j = app.cities.index(app.currCity2)
            # if already controlled by red
            if app.cities[j].status == 1:
                if app.spiesTogether:
                    app.currCity1.status -= 2
                app.cities[j].status -= 2
                app.currCity2.status -= 2
            # if neutral
            else:
                if app.spiesTogether:
                    app.currCity2.status -= 1
                app.cities[j].status -= 1
                app.currCity2.status -= 1
            if app.spiesTogether:
                app.redCover = False
            app.blueCover = False
            app.suspicion2 += 10
            app.blueActionsLeft -= 1
        else:
            app.warningMessage = 'Already Controlled!'
        checkCitySurrounded(app)
        # checkSpyRingCreated(app)
        checkTurn(app)
    # Strike
    elif mouseInAction(app, mouseX, mouseY, 1):
        if app.redTurn and app.spiesTogether:
            app.missionWin1 = True
            # updates win tracker & stars
            try:
                lastWin1 = app.winTracker.index(f'{app.spyColor1}')
                app.winTracker[lastWin1 + 1] = app.spyColor1
            except ValueError:
                app.winTracker[0] = app.spyColor1
            app.missionWinMethod = 'strike'
            # is the game over?
            finalStarIndex = app.numRounds//2 
            if app.winTracker[finalStarIndex] == app.spyColor1:
                app.operationWin1 = True
                setActiveScreen('endOperation')
            elif app.currRound < app.numRounds:
                setActiveScreen('endMission')
        elif app.blueTurn and app.spiesTogether:
            app.missionWin2 = True
            # updates win tracker & stars
            try:
                lastWin2 = app.winTracker.index(f'{app.spyColor2}')
                app.winTracker[lastWin2 - 1] = app.spyColor2
            except ValueError:
                app.winTracker[-1] = app.spyColor2
            app.missionWinMethod = 'strike'
            # is the game over?
            finalStarIndex = app.numRounds//2 
            if app.winTracker[finalStarIndex] == app.spyColor2:
                app.operationWin2 = True
                setActiveScreen('endOperation')
            elif app.currRound < app.numRounds:
                setActiveScreen('endMission')
        else:
            if app.redTurn:
                app.suspicion1 += 25
                app.redActionsLeft -= 1
                app.redCover = False
            elif app.blueTurn:
                app.suspicion2 += 25
                app.blueActionsLeft -= 1
                app.blueCover = False
            app.warningMessage = 'Strike Failed!'
        checkTurn(app)
    # Wait (decreases suspicion)
    elif mouseInAction(app, mouseX, mouseY, 2):
        if app.redTurn:
            app.suspicion1 -= 20
            if app.suspicion1 < 0:
                app.suspicion1 = 0
            app.redActionsLeft -= 1
            app.redCover = True if app.currCity1.status != -1 else False
        elif app.blueTurn:
            app.suspicion2 -= 20
            if app.suspicion2 < 0:
                app.suspicion2 = 0
            app.blueActionsLeft -= 1
            app.blueCover = True if app.currCity2.status != 1 else False
        checkTurn(app)
    # Locate (doesn't work if target in deep cover)
    elif mouseInAction(app, mouseX, mouseY, 3):
        if app.redTurn:
            if app.intel1 < 10:
                app.warningMessage = 'Not enough Intel!'
            elif app.deepCover2:
                app.warningMessage = 'Target in deep cover!'
            else:
                app.intel1 -= 10
                app.blueCover = False
                app.redActionsLeft -= 1
        elif app.blueTurn:
            if app.intel2 < 10:
                app.warningMessage = 'Not enough Intel!'
            elif app.deepCover1:
                app.warningMessage = 'Target in deep cover!'
            else:
                app.intel2 -= 10
                app.redCover = False
            app.blueActionsLeft -= 1
        checkTurn(app)
    # Deep Cover
    elif mouseInAction(app, mouseX, mouseY, 4):
        if app.redTurn:
            if app.intel1 < 20:
                app.warningMessage = 'Not enough Intel!'
            else:
                app.intel1 -= 20
                app.deepCover1 = True
            app.redActionsLeft -= 1
        elif app.blueTurn:
            if app.intel2 < 20:
                app.warningMessage = 'Not enough Intel!'
            else:
                app.intel2 -= 20
                app.deepCover2 = True
            app.blueActionsLeft -= 1
        checkTurn(app)
    # Expose
    elif mouseInAction(app, mouseX, mouseY, 5):
        if app.redTurn:
            if app.intel1 < 20:
                app.warningMessage = 'Not enough Intel!'
            else:
                app.intel1 -= 20
                app.suspicion2 += 25
                if app.suspicion2 >= 100:
                    try:
                        lastWin1 = app.winTracker.index(f'{app.spyColor1}')
                        app.winTracker[lastWin1 + 1] = app.spyColor1
                    except ValueError:
                        app.winTracker[0] = app.spyColor1
                    app.missionWin1 = True
                    app.missionWinMethod = 'exposé'
                    # game over?
                    finalStarIndex = app.numRounds//2 
                    if app.winTracker[finalStarIndex] == app.spyColor1:
                        app.operationWin1 = True
                        setActiveScreen('endOperation')
                    elif app.currRound < app.numRounds:
                        setActiveScreen('endMission')
            app.redActionsLeft -= 1
        elif app.blueTurn:
            if app.intel2 < 20:
                app.warningMessage = 'Not enough Intel!'
            else:
                app.intel2 -= 20
                app.suspicion1 += 25
                if app.suspicion1 >= 100:
                    try:
                        lastWin2 = app.winTracker.index(f'{app.spyColor2}')
                        app.winTracker[lastWin2 - 1] = app.spyColor2
                    except ValueError:
                        app.winTracker[-1] = app.spyColor2
                    app.missionWin2 = True
                    app.missionWinMethod = 'exposé'
                    # game over?
                    finalStarIndex = app.numRounds//2 
                    if app.winTracker[finalStarIndex] == app.spyColor2:
                        app.operationWin2 = True
                        setActiveScreen('endOperation')
                    elif app.currRound < app.numRounds:
                        setActiveScreen('endMission')
            app.blueActionsLeft -= 1
        checkTurn(app)
    # Prepare
    elif mouseInAction(app, mouseX, mouseY, 6):
        if app.redTurn:
            if app.intel1 < 40:
                app.warningMessage = 'Not enough Intel!'
            else:
                app.intel1 -= 40
                app.redActionsLeft += 1
        elif app.blueTurn:
            if app.intel2 < 20:
                app.warningMessage = 'Not enough Intel!'
            else:
                app.intel2 -= 40
                app.blueActionsLeft += 1
    # Exit
    elif mouseInExitButton(app, 940, 20, mouseX, mouseY):
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
                app.suspicion1 += 5
                app.redActionsLeft -= 1
                if not app.spiesTogether:
                    app.redCover = True
                else:
                    app.redCover = False
                    app.spiesTogether = True
                checkTurn(app)
        # invalid move! Puts spy back
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
                app.suspicion2 += 5
                app.blueActionsLeft -= 1
                if not app.spiesTogether:
                    app.blueCover = True
                else:
                    app.blueCover = False
                    app.spiesTogether = True
                checkTurn(app)
        # invalid move! Puts spy back
        app.spy2x = app.currCity2.cx
        app.spy2y = app.currCity2.cy

def isValidMove(app, currentCity, nextCity):
    if (currentCity.name in nextCity.realConnections) or (nextCity.name in currentCity.realConnections):
        return True
    else:
        return False
        
def checkTurn(app):
    app.spiesTogether = (app.currCity1 == app.currCity2)
    if app.redActionsLeft == 0 or app.blueActionsLeft == 0:
        if app.redTurn:
            app.redActionsLeft = 3
            app.deepCover2 = False
            app.blueCover = False
            # generate intel
            for city in app.cities:
                if city.status == 1:
                    app.intel1 += 3
            # walked into an enemy controlled city, or the enemy spy!
            if app.currCity1.status == -1 or app.spiesTogether:
                app.redCover = False
        elif app.blueTurn:
            app.blueActionsLeft = 3
            app.deepCover1 = False
            app.redCover = False
            # generate intel
            for city in app.cities:
                if city.status == -1:
                    app.intel2 += 3
            # walked into an enemy controlled city, or the enemy spy!
            if app.currCity2.status == 1 or app.spiesTogether:
                app.blueCover = False
        # toggle who's turn it is
        app.redTurn = not app.redTurn
        app.blueTurn = not app.blueTurn
        app.warningMessage = ''
        if not app.aiOn:
            setActiveScreen('transfer')
        else:
            print('hi')
            setActiveScreen('aiThinking')
            print('bye')
            if app.aiDifficulty == 'easy':
                AIMakeBestMove(app, 1, False)
            elif app.aiDifficulty == 'medium':
                AIMakeBestMove(app, 2, False)
            elif app.aiDifficulty == 'hard':
                AIMakeBestMove(app, 3, False)
            elif app.aiDifficulty == '00':
                AIMakeBestMove(app, 4, False)
            # defensive check
            for city in app.cities:
                if city.status <= -1:
                    city.status = -1
                elif city.status >= 1:
                    city.status = 1
            # flip turn back to the player
            app.redTurn = not app.redTurn
            app.blueTurn = not app.blueTurn
            setActiveScreen('game')

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
    
#--------* Are You Sure secondary screen (I wrote this during Hack112! This is tweaked significantly though)

def areYouSure_redrawAll(app):
    drawMap(app)
    drawRect(330, 200, 340, 160, fill = 'black', border = 'white', borderWidth = 2)
    
    drawLabel('Are you sure you want to quit?', 500, 240, fill = 'limeGreen', size = 16, font = 'orbitron', bold = True)
    drawLabel('Yes', 420, 305, fill = 'limeGreen', size = 25, font = 'orbitron')
    drawLabel('No', 580, 305, fill = 'limeGreen', size = 25, font = 'orbitron')
    
    drawRect(360, 280, 120, 50, fill = None, border = app.highlights['yes'], borderWidth = 2)
    drawRect(520, 280, 120, 50, fill = None, border = app.highlights['no'], borderWidth = 2)
        
def areYouSure_onMouseMove(app, mouseX, mouseY):
    app.highlights['yes'] = 'limeGreen' if inBox(360, 280, 120, 50, mouseX, mouseY) else 'white'
    app.highlights['no'] = 'limeGreen' if inBox(520, 280, 120, 50, mouseX, mouseY) else 'white'

def areYouSure_onMousePress(app, mouseX, mouseY):
    if inBox(360, 280, 120, 50, mouseX, mouseY):
        app.width = 650
        app.height = 650
        resetOperation(app)
        setActiveScreen('home')
    elif inBox(520, 280, 120, 50, mouseX, mouseY):
        setActiveScreen('game')
        
#--------* Transfer Screen between player turns (so secrecy is maintained)

def transfer_redrawAll(app):
    drawMap(app)
    drawRect(330, 200, 340, 160, fill = 'black', border = 'white', borderWidth = 2)
    drawLabel('Transfer the screen', 500, 230, fill = 'limeGreen', size = 25, bold = True, font = 'orbitron')
    drawLabel('to your opponent', 500, 270, fill = 'limeGreen', size = 25, bold = True, font = 'orbitron')
    drawLabel(f'{app.transferTime}', 500, 320, fill = 'limeGreen', size = 40, bold = True, font = 'orbitron')
    
def transfer_onStep(app):
    app.stepsPerSecond = 1
    app.transferTime -= 1
    if app.transferTime == 0:
        setActiveScreen('game')
        app.transferTime = 5

#--------* AI Thinking Screen

def aiThinking_redrawAll(app):
    drawMap()
    drawRect(330, 200, 340, 160, fill = 'black', border = 'white', borderWidth = 2)
    drawLabel('AI Thinking...', 500, 270, fill = 'limeGreen', size = 25, bold = True, font = 'orbitron')
    
# END MISSION

def endMission_redrawAll(app):
    drawEndBackground(app)
    drawEndMessages(app)
    drawEndButtons(app)

def drawEndBackground(app):
    drawMap(app)
    drawRect(280, 120, 440, 400, fill = 'black', border = 'white', borderWidth = 2)
    drawLabel('Final', 500, 220, size = 20, fill = 'limeGreen', font = 'orbitron', bold = True)
    # draws the left stars (for player1 wins)
    for i in range(app.numRounds//2):
        correctedIndex = 450 - (app.numRounds//2 - 1) * 50
        drawStar(correctedIndex + 50*i, 180, 20, 5, fill = app.winTracker[i], border = 'white')
    # draws the right stars (for player2 wins)
    for i in range(app.numRounds//2 + 1, app.numRounds):
        correctedIndex = i - app.numRounds//2
        drawStar(500 + 50*correctedIndex, 180, 20, 5, fill = app.winTracker[i], border = 'white')
    # draws the final operation star (tiebreaker)
    drawStar(500, 180, 30, 5, fill = app.winTracker[app.numRounds//2], border = 'white')
    
def drawEndMessages(app):
    drawLabel('End of Mission', 500, 280, size = 40, fill = 'limeGreen', font = 'orbitron', bold = True)
    if app.missionWin1:
        drawLabel(f'{app.player1} won by {app.missionWinMethod}', 500, 360, size = 20, fill = 'limeGreen', font = 'orbitron', bold = True)
    elif app.missionWin2:
        drawLabel(f'{app.player2} won by {app.missionWinMethod}', 500, 360, size = 20, fill = 'limeGreen', font = 'orbitron', bold = True)
    
def drawEndButtons(app):
    drawRect(360, 420, 280, 40, fill = None, border = app.highlights['continueOperation'])
    drawLabel('Continue Operation', 500, 440, fill = 'limeGreen', size = 20, font = 'orbitron', bold = True)
    
def endMission_onMouseMove(app, mouseX, mouseY):
    app.highlights['continueOperation'] = 'limeGreen' if inBox(360, 420, 280, 40, mouseX, mouseY) else 'white'
    app.highlights['missionEndExit'] = 'limeGreen' if mouseInExitButton(app, 680, 120, mouseX, mouseY) else 'white'

def endMission_onMousePress(app, mouseX, mouseY):
    if inBox(360, 420, 280, 40, mouseX, mouseY):
        resetMission(app)
        setActiveScreen('game')
    
def resetMission(app):
    app.cities = getRandomCities(app)
    for city in app.cities:
        # resets all city statuses
        city.status = 0
    app.spy1x, app.spy1y, app.spy2x, app.spy2y = randomStartLocation(app) # already takes care of assigning CurrCities
    app.redCover = app.blueCover = app.deepCover1 = app.deepCover2 = False
    app.spy1Selected = app.spy2Selected = app.spiesTogether = False
    app.redActionsLeft = app.blueActionsLeft = 3
    app.intel1 = app.intel2 = 0
    app.suspicion1 = app.suspicion2 = 0
    app.warningMessage = ''
    app.currRound += 1
    
# END OPERATION 

def endOperation_redrawAll(app):
    drawEndBackground(app)
    drawOperationEndMessages(app)
    drawOperationEndButtons(app)

def drawOperationEndMessages(app):
    drawLabel('End of Operation', 500, 280, size = 30, fill = 'limeGreen', font = 'orbitron', bold = True)
    if app.operationWin1:
        drawLabel(f'{app.player1} won!', 500, 340, size = 30, fill = 'limeGreen', font = 'orbitron', bold = True)
    elif app.operationWin2:
        drawLabel(f'{app.player2} won!', 500, 340, size = 30, fill = 'limeGreen', font = 'orbitron', bold = True)
        
def drawOperationEndButtons(app):
    drawRect(360, 420, 280, 40, fill = None, border = app.highlights['backToBase'])
    drawLabel('Back to Base', 500, 440, fill = 'limeGreen', size = 20, font = 'orbitron', bold = True)

def endOperation_onMouseMove(app, mouseX, mouseY):
    app.highlights['backToBase'] = 'limeGreen' if inBox(360, 420, 280, 40, mouseX, mouseY) else 'white'
    
def endOperation_onMousePress(app, mouseX, mouseY):
    if inBox(360, 420, 280, 40, mouseX, mouseY):
        resetOperation(app)
        app.width = 650
        setActiveScreen('home')
        
def resetOperation(app):
    resetMission(app)
    app.winTracker = []
    app.numRounds = None
    app.currRound = 1
    app.missionWin1 = app.missionWin2 = False
    app.operationWin1 = app.operationWin2 = False
    
# CREDITS

def credits_redrawAll(app):
    drawRect(0, 0, 650, 650, fill = 'black')
    drawExitButton(app, 600, 20, app.highlights['creditsExit'])
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
    app.highlights['creditsExit'] = 'limeGreen' if mouseInExitButton(app, 600, 20, mouseX, mouseY) else 'white'
    
def credits_onMousePress(app, mouseX, mouseY):
    if mouseInExitButton(app, 600, 20, mouseX, mouseY):
        setActiveScreen('home') 

# MISC

def distance(x0, y0, x1, y1):
    return(((x1-x0)**2 + (y1-y0)**2)**0.5)
    
def inBox(x, y, width, height, mouseX, mouseY):
    return (x <= mouseX <= x + width) and (y <= mouseY <= y + height)

def inCircle(x, y, r, mouseX, mouseY):
    return distance(x, y, mouseX, mouseY) <= r
    
def drawExitButton(app, x, y, borderColor):
    buttonUL = (x, y)
    buttonWidth = 40
    buttonHeight = 40
    drawRect(buttonUL[0], buttonUL[1], buttonWidth, buttonHeight, fill = None, border = borderColor)
    drawLabel('X', x + buttonWidth//2, y + buttonHeight//2, size = 40, fill = 'red', bold = True)
    
def mouseInExitButton(app, exitButtonX, exitButtonY, mouseX, mouseY):
    exitButtonWidth = 40
    exitButtonHeight = 40
    return inBox(exitButtonX, exitButtonY, exitButtonWidth, exitButtonHeight, mouseX, mouseY)

# Bug squashing to-do list:
# Problems when spies land together...

# # # main function for Minimax (Thanks Janessa for inspiration!)
# AI is always minimizer

from itertools import permutations

def AIMakeBestMove(app, depth, isMaximizingPlayer):
    bestEval, bestMoves = minimax(app, depth, None, isMaximizingPlayer)
    print(bestEval, bestMoves)
    for move in bestMoves:
        applyMove(app, move, isMaximizingPlayer)

def minimax(app, depth, bestMoves, isMaximizingPlayer):
    if depth == 0 or isTerminal(app):
        print(bestMoves, 'hi')
        return (evaluate(app), bestMoves)
    
    # Maximizing player's turn
    if isMaximizingPlayer:
        maxEval = float('-inf')
        possibleMoveCombos = generateMoves(app, isMaximizingPlayer)
        oldCity = app.currCity1
        for moveCombo in possibleMoveCombos:
            for i in range(len(moveCombo)):
                moveName = moveCombo[i]
                applyMove(app, moveName, isMaximizingPlayer) # mutating
                eval = minimax(app, depth - 1, bestMoves, False)
                undoMove(app, moveName, oldCity, isMaximizingPlayer) # brings us back
                if isinstance(eval, tuple):
                    if eval[0] > maxEval:
                        maxEval = eval[0]
                        bestMoves = moveCombo
                elif eval > maxEval:
                    maxEval = eval
                    bestMoves = moveCombo
        return maxEval, bestMoves
    
    # Minimizing player's turn
    else:
        minEval = float('inf')
        possibleMoveCombos = generateMoves(app, isMaximizingPlayer)
        print(possibleMoveCombos)
        oldCity = app.currCity2
        for moveCombo in possibleMoveCombos:
            for i in range(len(moveCombo)):
                moveName = moveCombo[i]
                applyMove(app, moveName, isMaximizingPlayer) # mutating
                eval = minimax(app, depth - 1, bestMoves, True)
                undoMove(app, moveName, oldCity, isMaximizingPlayer) # brings us back
                if isinstance(eval, tuple):
                    if eval[0] < minEval:
                        minEval = eval[0]
                        bestMoves = moveCombo
                elif eval > minEval:
                    minEval = eval
                    bestMoves = moveCombo
        return minEval, bestMoves

def isTerminal(app):
    return (app.missionWin1 or app.missionWin2)

def evaluate(app):
    if app.missionWin2 or app.suspicion1 > 100:
        return float('-inf') # AI won
    elif app.missionWin1 or app.suspicion2 > 100:
        return float('inf') # AI lost
    else:
        controlledCities = 0
        centralization = distance(app.currCity2.cx, app.currCity2.cy, 500, 325)
        suspicion = app.suspicion2
        intel = app.intel2
        cover = 10 if app.blueCover else 0
        deepCover = 15 if app.deepCover2 else 0
        enemyCities = 0
        enemyCentralization = distance(app.currCity1.cx, app.currCity1.cy, 500, 325)
        enemySuspicion = app.suspicion1
        enemyIntel = app.intel1
        enemyCover = -10 if app.redCover else 0
        enemyDeepCover = -15 if app.deepCover1 else 0
        for city in app.cities:
            if city.status == 1:
                enemyCities += 1
            elif city.status == -1:
                controlledCities += 1
        playerScore = (enemyCities*1000 + enemyCentralization + enemyIntel*5 + enemyCover + 2*enemyDeepCover - enemySuspicion//5)
        AIScore = (controlledCities*1000 + centralization + intel*5 + cover + 2*deepCover - suspicion//5)
    return playerScore - AIScore

def generateMoves(app, isMaximizingPlayer):
    possibleMoves = ['Control', 'Strike', 'Wait', 'Locate', 'Go Deep', 'Expose', 'Prepare']
    if isMaximizingPlayer:
        for city in app.currCity1.realConnections:
            possibleMoves.append(app.cityCoords[city])
    else:
        for city in app.currCity2.realConnections:
            possibleMoves.append(app.cityCoords[city])
    allMoveCombos = list(permutations(possibleMoves, 3))
    validMoveCombos = []
    # remove impossible combinations based on intel requirements
    intelRequirements = {'Locate': 10, 'Go Deep': 20, 'Expose': 20, 'Prepare': 40}
    for moveCombo in allMoveCombos:
        if isMaximizingPlayer:
            if all(app.intel1 >= intelRequirements.get(move, 0) for move in moveCombo): 
                validMoveCombos.append(moveCombo)
        else:
            if all(app.intel2 >= intelRequirements.get(move, 0) for move in moveCombo):
                validMoveCombos.append(moveCombo)
    print(len(validMoveCombos))

    # makes sure we don't take too long!
    selectedMoveCombos = random.sample(validMoveCombos, min(3, len(validMoveCombos)))
    return selectedMoveCombos
    
def applyMove(app, move, isMaximizingPlayer):
    if isMaximizingPlayer:
        if isinstance(move, City):
            app.spy1x = move.cx
            app.spy1y = move.cy                                                                     
            app.currCity1 = move
            app.spiesTogether = app.currCity1 == app.currCity2
            app.suspicion1 += 5
            if not app.spiesTogether:
                app.redCover = True
        elif move == 'Control':
            i = app.cities.index(app.currCity1)
            if app.currCity1.status == -1:
                # if already controlled by blue
                if app.spiesTogether:
                    app.currCity2.status += 2
                app.cities[i].status += 2
                app.currCity1.status += 2
                # if neutral
            else:
                if app.spiesTogether:
                    app.currCity2.status += 1
                app.cities[i].status += 1
                app.currCity1.status += 1
            # if you control the city your opponent is in, reveal them
            if app.spiesTogether:
                app.blueCover = False
            # ending on a control also reveals your position
            app.redCover = False
            app.suspicion1 += 10
            app.redActionsLeft -= 1
        # Strike
        elif move == 'Strike':
            if app.redTurn and app.spiesTogether:
                app.missionWin1 = True
            elif app.blueTurn and app.spiesTogether:
                app.missionWin2 = True
            else:
                if app.redTurn:
                    app.suspicion1 += 25
                    app.redActionsLeft -= 1
                    app.redCover = False
        # Wait (decreases suspicion)
        elif move == 'Wait':
            app.suspicion1 -= 20
            if app.suspicion1 < 0:
                app.suspicion1 = 0
            app.redCover = True if app.currCity1.status != -1 else False
        # Locate (doesn't work if target in deep cover)
        elif move == 'Locate':
            if not app.deepCover2:
                app.intel1 -= 10
                app.blueCover = False
        # Deep Cover
        elif move == 'Go Deep':
            app.intel1 -= 20
            app.deepCover1 = True
        # Expose
        elif move == 'Expose':
            app.intel1 -= 20
            app.suspicion2 += 25
            if app.suspicion2 >= 100:
                app.missionWin1 = True
        # Prepare
        elif move == 'Prepare':
            app.intel1 -= 40
    else:
        if isinstance(move, City):
            app.spy2x = move.cx
            app.spy2y = move.cy                                                                     
            app.currCity2 = move
            app.spiesTogether = app.currCity1 == app.currCity2
            app.suspicion2 += 5
            if not app.spiesTogether:
                app.blueCover = True
        elif move == 'Control':
            i = app.cities.index(app.currCity2)
            if app.currCity1.status == 1:
                # if already controlled by blue
                if app.spiesTogether:
                    app.currCity1.status -= 2
                app.cities[i].status -= 2
                app.currCity2.status -= 2
                # if neutral
            else:
                if app.spiesTogether:
                    app.currCity1.status -= 1
                app.cities[i].status -= 1
                app.currCity2.status -= 1
            # if you control the city your opponent is in, reveal them
            if app.spiesTogether:
                app.redCover = False
            # ending on a control also reveals your position
            app.blueCover = False
            app.suspicion2 += 10
            app.blueActionsLeft -= 1
            checkCitySurrounded(app)
        # Strike
        elif move == 'Strike':
            if app.spiesTogether:
                app.missionWin2 = True
            else:
                app.blueCover = False
                app.suspicion2 += 25
                app.blueActionsLeft -= 1
        # Wait (decreases suspicion)
        elif move == 'Wait':
            app.suspicion2 -= 20
            if app.suspicion2 < 0:
                app.suspicion2 = 0
            app.blueCover = True if app.currCity2.status != 1 else False
            app.blueActionsLeft -= 1
        # Locate (doesn't work if target in deep cover)
        elif move == 'Locate':
            app.intel2 -= 10
            app.redCover = False
            app.blueActionsLeft -= 1
        # Deep Cover
        elif move == 'Go Deep':
            app.intel2 -= 20
            app.deepCover2 = True
            app.blueActionsLeft -= 1
        # Expose
        elif move == 'Expose':
            app.intel2 -= 20
            app.suspicion1 += 25
            if app.suspicion1 >= 100:
                app.missionWin2 = True
            app.blueActionsLeft -= 1
        # Prepare
        elif move == 'Prepare':
            app.intel2 -= 40
            app.blueActionsLeft += 1
 
def undoMove(app, move, oldCity, isMaximizingPlayer):
    if isMaximizingPlayer:
        if isinstance(move, City):
            app.spy1x = oldCity.cx
            app.spy1y = oldCity.cy                                                                     
            app.currCity1 = oldCity
            app.spiesTogether = app.currCity1 == app.currCity2
            app.suspicion1 -= 5
            if not app.spiesTogether:
                app.redCover = True
        elif move == 'Control':
            i = app.cities.index(app.currCity1)
            if app.spiesTogether:
                app.currCity1.status -= 2
                app.currCity2.status -= 2
                app.cities[i].status -= 2
            else:
                app.cities[i].status -= 1
                app.currCity1.status -= 1
            # if you control the city your opponent is in, reveal them
            app.redCover = True
            app.suspicion1 -= 10
            app.redActionsLeft += 1
            checkCitySurrounded(app)
        # Strike
        elif move == 'Strike':
            if app.redTurn and app.spiesTogether:
                app.missionWin1 = False
            elif app.blueTurn and app.spiesTogether:
                app.missionWin2 = False
            else:
                if app.redTurn:
                    app.suspicion1 -= 25
                    app.redActionsLeft += 1
                    app.redCover = True
        # Wait (decreases suspicion)
        elif move == 'Wait':
            app.suspicion1 += 20
            app.redCover = False if app.currCity1.status != -1 else True
        # Locate (doesn't work if target in deep cover)
        elif move == 'Locate':
            app.intel1 += 10
            app.blueCover = True
        # Deep Cover
        elif move == 'Go Deep':
            app.intel1 += 20
            app.deepCover1 = False
        # Expose
        elif move == 'Expose':
            app.intel1 += 20
            app.suspicion2 -= 25
            if app.suspicion2 >= 100:
                app.missionWin1 = False
        # Prepare
        elif move == 'Prepare':
            app.intel1 += 40
    else:
        if isinstance(move, City):
            app.spy2x = oldCity.cx
            app.spy2y = oldCity.cy                                                                     
            app.currCity2 = oldCity
            app.spiesTogether = app.currCity1 == app.currCity2
            app.suspicion2 -= 5
            if not app.spiesTogether:
                app.blueCover = True
        elif move == 'Control':
            i = app.cities.index(app.currCity2)
            if app.spiesTogether:
                app.currCity1.status += 2
                app.currCity2.status += 2
                app.cities[i].status += 2
            else:
                app.cities[i].status += 1
                app.currCity2.status += 1
            # if you control the city your opponent is in, reveal them
            if app.spiesTogether:
                app.blueCover = True
            app.blueCover = True
            app.suspicion2 -= 10
            app.blueActionsLeft += 1
            checkCitySurrounded(app)
        # Strike
        elif move == 'Strike':
            app.blueCover = True
            app.suspicion2 -= 25
            app.blueActionsLeft += 1
        # Wait (decreases suspicion)
        elif move == 'Wait':
            app.suspicion2 += 20
            app.blueCover = True if app.currCity2.status != 1 else False
            app.blueActionsLeft += 1
        # Locate (doesn't work if target in deep cover)
        elif move == 'Locate':
            app.intel2 += 10
            app.redCover = True
            app.blueActionsLeft += 1
        # Deep Cover
        elif move == 'Go Deep':
            app.intel2 += 20
            app.deepCover2 = False
            app.blueActionsLeft += 1
        # Expose
        elif move == 'Expose':
            app.intel2 += 20
            app.suspicion1 -= 25
            app.blueActionsLeft += 1
        # Prepare
        elif move == 'Prepare':
            app.intel2 += 40
            app.blueActionsLeft -= 1
    
runAppWithScreens('home')
    