import pygame, sys, random, pprint
from pygame.locals import * 

#DISPLAY MEASUREMENTS
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
SQUARESIZE = 30
BOARDWIDTH = 5
BOARDHEIGHT = 5
GAMEBOARD = 4
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SQUARESIZE)) / 6)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SQUARESIZE)) / 6)
XSQUAREGAP = int(((WINDOWWIDTH - (BOARDWIDTH * SQUARESIZE)) - (XMARGIN * 2)) / 4)
YSQUAREGAP = int(((WINDOWWIDTH - (BOARDHEIGHT * SQUARESIZE)) - (YMARGIN * 2)) / 4)
GRIDLINE = 5
SINGLEGRID = 10

# COLORS
BLACK = (0, 0, 0)
LIGHTGREEN = (18, 173, 42)
DARKGREEN = (53, 98, 68)
DARKGREY = (49, 51, 53)
DARKRED = (128, 0, 0)
RED = (255, 0, 0)

# OTHER COSTANT
EMPTY = '.'
CLICKED = 'O'
FPS = 15
row = 'row'
column = 'column'

def main():
    global WINSURF, FPSCLOCK, PLAYERPOINTS, PROGRAMPOINTS, SOUNDCLICK, SOUNDCLICKRECT, SOUNDLINE, SOUNDKEY, BYESOUND, \
           COMBOSOUND, DRAWSOUND, LOOSERSOUND, WINSOUND, WELCOMESOUND

    # TO USE IN ANY FUNCTION

    pygame.init() # INIT FOR EVERY PYGAME MODULE

    WINSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('SQUARED')
    pygame.display.set_icon(pygame.image.load('square-icon.png'))
    FPSCLOCK = pygame.time.Clock()
    SOUNDCLICK = pygame.mixer.Sound('onclick.wav')
    SOUNDCLICKRECT = pygame.mixer.Sound('clickrect.wav')
    SOUNDLINE = pygame.mixer.Sound('setline.wav')
    SOUNDKEY = pygame.mixer.Sound('keypress.wav')
    BYESOUND = pygame.mixer.Sound('byebye.wav')
    COMBOSOUND = pygame.mixer.Sound('combo.wav')
    DRAWSOUND = pygame.mixer.Sound('draw.wav')
    LOOSERSOUND = pygame.mixer.Sound('looser.wav')
    WINSOUND = pygame.mixer.Sound('win.wav')
    WELCOMESOUND = pygame.mixer.Sound('squarewelcome.wav')



    while True: # LOOP FOR GAME OVER AND MAIN GAIN

        difficultySelect()
        runGame()
        pygame.time.wait(1000)
        gameOver()
        pygame.time.wait(1000)

def runGame():

    yourTurnText = textBanner('YOUR TURN', 25)
    TURN = getTurn()
    while not initialGrid.isGaveOver():  # Game main loop

        # UPDATE ALL ON DISPLAY AT THE FIRST OF THE MAIN LOOP
        WINSURF.fill(BLACK)  # THIS WILL ALSO CLEAN UP THE SCREEN FOR EACH LOOP FIRST OF WRITING UPDATED DATA
        finalModeText = textBanner(FINALMODE+' MODE', 22, RED)
        finalModeText.setCenterBlit(100, WINDOWHEIGHT-30)
        progPointText = textBanner('COMPUTER: ' + str(initialGrid.PROGRAMPOINTS), 25, LIGHTGREEN)
        progPointText.setCenterBlit(400, 20)
        playerPointText = textBanner('PLAYER: ' + str(initialGrid.PLAYERPOINTS), 25, LIGHTGREEN)
        playerPointText.setCenterBlit(400, 45)
        startingSquareBoard.drawItAll()  # UPDATE SQUARES COLOR
        initialGrid.drawItAll()  # UPDATE GRID COLOR

        pygame.time.wait(500) # DELAY SHOWING yourTurnText

        if TURN == 'player':
            waitingForPlayer = True
            while waitingForPlayer:


                yourTurnText.setCenterBlit(200 ,25)
                pygame.display.update()

                for event in pygame.event.get():

                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        SOUNDKEY.play()
                        BYESOUND.play()
                        kill()

                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        squareXClick, squareYClick = startingSquareBoard.clickedSquare(mousex,mousey)

                        if squareXClick != None and squareYClick != None: # HAS CLICKED AND MOUSE IS OVER A SQUARE
                            copySquareBoard.squaresBoard[squareXClick][squareYClick] = CLICKED
                            copySquareBoard.colorClickedSquare()
                            SOUNDCLICKRECT.play()

                            # SET RESTRICTIVE CONDITIONS TO AVOID None VALUES FROM FUNCTION
                            if copySquareBoard.secondClickIsValid() != 'INVALID' and copySquareBoard.secondClickIsValid() != None:
                                firstSquare, secondSquare = copySquareBoard.secondClickIsValid()

                                initialGrid.update(firstSquare, secondSquare) # METHOD TO GET GRID COORDS FROM 2 SQUARES AND UPDATE IT
                                startingSquareBoard.updateAfterPlayer(firstSquare, secondSquare, TURN) #UPDATE SQUARE DATA STRUCURE ONLY WITH VALID CLICKS
                                copySquareBoard.reset() # RESET copySquareBoard MAIN STRUCTURE AND KEEP TRACKING SECONDS CLICKS ON SQUARES
                                waitingForPlayer = False
                                TURN = 'program'
                                SOUNDLINE.play()
                                initialGrid.drawItAll()
                            elif copySquareBoard.secondClickIsValid() == 'INVALID':
                                copySquareBoard.reset() #START AGAIN CONTROLLING VALIDITY OF SECOND CLICKS

                        else: SOUNDCLICK.play()


        elif TURN == 'program':

            if FINALMODE == 'HARD':
                initialGrid.getProgramMoveHardMode() # GET PROGRAM CHOICE AND UPDATE THE GRID
            elif FINALMODE == 'EASY':
                initialGrid.getProgramMoveEasyMove()
            pygame.time.wait(1000) # DELAY UPDATE GRID COLOR AFTER PROGRAM MOVES
            SOUNDLINE.play()
            initialGrid.drawItAll()  # UPDATE GRID COLOR
            TURN = 'player'

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def gameOver():
    gameOverMode = True
    while gameOverMode:

        WINSURF.fill(BLACK)
        pointsText = textBanner(str(initialGrid.PLAYERPOINTS)+' VS '+str(initialGrid.PROGRAMPOINTS), 100)
        pointsText.setCenterBlit(WINDOWWIDTH/2, 150)

        if initialGrid.PLAYERPOINTS > initialGrid.PROGRAMPOINTS:
            winText = textBanner('YOU WIN!', 80)
            winText.setCenterBlit(WINDOWWIDTH/2, WINDOWHEIGHT/2)
            WINSOUND.play()

        elif initialGrid.PLAYERPOINTS == initialGrid.PROGRAMPOINTS:
            drawText = textBanner('IT\'S A DRAW!', 80)
            drawText.setCenterBlit(WINDOWWIDTH/2, WINDOWHEIGHT/2)
            DRAWSOUND.play()

        elif initialGrid.PLAYERPOINTS < initialGrid.PROGRAMPOINTS:
            looseText = textBanner('YOU LOOSE!', 80, RED)
            looseText.setCenterBlit(WINDOWWIDTH/2, WINDOWHEIGHT/2)
            LOOSERSOUND.play()


        escText = textBanner('PRESS ESC TO QUIT', 40)
        escText.setCenterBlit(WINDOWWIDTH/2, WINDOWHEIGHT-YMARGIN*2)


        cText = textBanner('OR C TO CONTINUE PLAYING', 40)
        cText.setCenterBlit(WINDOWWIDTH/2, WINDOWHEIGHT-(YMARGIN))

        pygame.display.update()


        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                SOUNDKEY.play()
                BYESOUND.play()

                kill()

            if event.type == KEYDOWN:
                if event.key == K_c:
                    SOUNDKEY.play()
                    initialGrid.reset()  # RESET BEFORE RESTARTING AGAIN
                    startingSquareBoard.reset()
                    gameOverMode = False
                    break



def difficultySelect():
    WELCOMESOUND.play()
    global FINALMODE
    selectMode = True
    WINSURF.fill(BLACK)

    while selectMode:

        squaredText = textBanner('SQUARED', 120)
        squaredText.setCenterBlit(WINDOWWIDTH / 2, 150)

        playModeText = textBanner('SELECT PLAY MODE', 60)
        playModeText.setCenterBlit(WINDOWWIDTH / 2, 280)

        easyText = textBanner('EASY', 60, DARKRED)
        easyText.setCenterBlit(XMARGIN * 2.5, 380)

        hardText = textBanner('HARD', 60, DARKRED)
        hardText.setCenterBlit(WINDOWWIDTH - XMARGIN * 2.5, 380)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                SOUNDKEY.play()
                BYESOUND.play()
                kill()

            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos

                if easyText.testCollision(mouseX, mouseY):
                    SOUNDCLICKRECT.play()
                    FINALMODE = 'EASY'
                    easyText.animateSelection()
                    selectMode = False

                elif hardText.testCollision(mouseX, mouseY):
                    SOUNDCLICKRECT.play()
                    hardText.animateSelection()
                    FINALMODE = 'HARD'
                    selectMode = False

        pygame.display.update()
        pygame.time.wait(500)

    return FINALMODE

def getTurn(): # RANDOMLY CHOOSE BETWEEN PROGRAM AND PLAYER FOR STARTING
    choise = random.randint(0, 1)
    if choise == 0: return 'player'
    else: return 'program'

def columnsToPixelDownSide(colX,colY): # 0<=rowX<=4, 0<=rowY<=3
    stepX=SQUARESIZE+XSQUAREGAP
    stepY=SQUARESIZE+YSQUAREGAP
    startX=XMARGIN+int(SQUARESIZE/2)+stepX*colX
    startY=YMARGIN+SQUARESIZE+stepY*colY

    return (startX, startY)

def columnsToPixelUpSide(colX,colY): # 0<=rowX<=4, 0<=rowY<=3
    stepX=SQUARESIZE+XSQUAREGAP
    stepY=SQUARESIZE+YSQUAREGAP
    endX=XMARGIN+int(SQUARESIZE/2)+stepX*colX
    endY=YMARGIN+SQUARESIZE+YSQUAREGAP+stepY*colY

    return (endX, endY)

def rowsToPixelLeftSide(rowX,rowY): # 0<=rowX<=3, 0<=rowY<=4
    stepX=SQUARESIZE+XSQUAREGAP
    stepY=SQUARESIZE+YSQUAREGAP
    startX=XMARGIN+SQUARESIZE+stepX*rowX
    startY=YMARGIN+int(SQUARESIZE/2)+stepY*rowY

    return (startX,startY)

def rowsToPixelRightSide(rowX,rowY): # 0<=rowX<=3, 0<=rowY<=4
    stepX=SQUARESIZE+XSQUAREGAP
    stepY=SQUARESIZE+YSQUAREGAP
    endX=XMARGIN+SQUARESIZE+XSQUAREGAP+stepX*rowX
    endY=YMARGIN+int(SQUARESIZE/2)+stepY*rowY
    return (endX, endY)

class GridBoard():

    PLAYERPOINTS = 0
    PROGRAMPOINTS = 0

    @classmethod
    def mainGrid(cls):
        cls.masterGrid ={'rows':[[EMPTY for x in range(5)] for y in range(4)],'columns':[[EMPTY for x in range(4)] for y in range(5)]}
        return cls.masterGrid

    # Give to new Object a masterGrid dict
    def __init__(self):
        self.masterGrid = GridBoard.mainGrid()
        self.PLAYERPOINTS = GridBoard.PLAYERPOINTS
        self.PROGRAMPOINTS = GridBoard.PROGRAMPOINTS

    def reset(self):
        self.masterGrid = GridBoard.mainGrid()
        self.PLAYERPOINTS = GridBoard.PLAYERPOINTS
        self.PROGRAMPOINTS = GridBoard.PROGRAMPOINTS

    # Draw the object on the screen
    def drawItAll(self):
        stepX=SQUARESIZE+XSQUAREGAP
        stepY=SQUARESIZE+YSQUAREGAP
        for x in range(len(self.masterGrid['columns'])): # COLUMNS
            for y in range(len(self.masterGrid['columns'][x])):
                start=columnsToPixelUpSide(x,y)
                end=columnsToPixelDownSide(x,y)
                if self.masterGrid['columns'][x][y] == EMPTY:
                    pygame.draw.line(WINSURF,DARKGREY,start,end,GRIDLINE)
                elif self.masterGrid['columns'][x][y] == CLICKED:
                    pygame.draw.line(WINSURF,DARKRED,start,end,GRIDLINE)

        for x in range(len(self.masterGrid['rows'])): # ROWS
            for y in range(len(self.masterGrid['rows'][x])): # y= 0,1,2,3,4
                start=rowsToPixelLeftSide(x,y)
                end=rowsToPixelRightSide(x,y)
                if self.masterGrid['rows'][x][y] == EMPTY:
                    pygame.draw.line(WINSURF,DARKGREY,start,end,GRIDLINE)
                if self.masterGrid['rows'][x][y] == CLICKED:
                    pygame.draw.line(WINSURF,DARKRED,start,end,GRIDLINE)

    def update(self, firstSquare, secondSquare): #GIVEN TWO SQUARES COORDS, UPDATE COLUMN OR ROW BETWEEN THIS TWO SQUARES AS CLICKED ON GRID
        # USE ONLY AFTER PLAYER'S MOVE. NOT PROGRAM'S MOVE
        # IF THAT MOVES GIVES A POINT THEN GIVE IT TO THE PLAYER
        self.firstSquare = firstSquare
        self.secondSquare = secondSquare

        # firstSquare, secondSquare are [x,y] with (0<=x<=4, 0<=y<=4)
        if self.firstSquare[0] - self.secondSquare[0] ==  -1 and self.firstSquare[1] == self.secondSquare[1]: # same row, second square is one column right
            self.masterGrid['rows'][self.firstSquare[0]][self.firstSquare[1]]=CLICKED
            if self.isPoint(self.firstSquare[0], self.firstSquare[1], 'rows'):
                self.PLAYERPOINTS += 1

        elif self.firstSquare[0] - self.secondSquare[0] == 1 and self.firstSquare[1] == self.secondSquare[1]: # same row, second square is one column left
            self.masterGrid['rows'][self.secondSquare[0]][self.secondSquare[1]]=CLICKED
            if self.isPoint(self.secondSquare[0], self.secondSquare[1], 'rows'):
                self.PLAYERPOINTS += 1

        elif self.firstSquare[0] == self.secondSquare[0] and self.firstSquare[1] - self.secondSquare[1] ==  -1: # same column, second square is one row down
            self.masterGrid['columns'][self.firstSquare[0]][self.firstSquare[1]]=CLICKED
            if self.isPoint(self.firstSquare[0], self.firstSquare[1], 'columns'):
                self.PLAYERPOINTS += 1

        elif self.firstSquare[0] == self.secondSquare[0] and self.firstSquare[1] - self.secondSquare[1] == 1: # same column, second square is one row up
            self.masterGrid['columns'][self.secondSquare[0]][self.secondSquare[1]] = CLICKED
            if self.isPoint(self.secondSquare[0], self.secondSquare[1], 'columns'):
                self.PLAYERPOINTS += 1

    def getProgramMoveHardMode(self): # GIVEN A masterGrid state make the best posible move.
    # IT UPDATES GRID DATA STRUCTURE
    # Call update method before calling getProgramMove
    #ALGORITH

        for x1 in range(len(self.masterGrid['columns'])): # 0<=x<=4
            for y1 in range(len(self.masterGrid['columns'][x1])): # 0<=y<=3

                # 1) IF THERE IS A MOVE THAT WILL MAKE YOU WIN TAKE IT.
                if x1 == 0: # CHECK FOR OPORTUNITIES IN THE FIRST COLUMNS. LOOK RIGHT SIDES
                    if self.masterGrid['columns'][x1 + 1][y1] == CLICKED and self.masterGrid['rows'][x1][y1] == CLICKED and self.masterGrid['rows'][x1][y1 +1] == CLICKED and self.masterGrid['columns'][x1][y1] == EMPTY:
                        self.masterGrid['columns'][x1][y1] = CLICKED
                        if self.isPoint(x1, y1, 'columns'):
                            self.PROGRAMPOINTS += 1
                        return

                elif x1 == 1 or x1 == 2 or x1 == 3: #CHECK FOR OPORTUNITIES IN INTERNAL COLUMNS
                    # LOOK RIGHT SIDES AND LEFT SIDE

                    # THIS IS A COMBO.. LOOK AT THE 'AND' CONDITION
                    if (self.masterGrid['columns'][x1 + 1][y1] == CLICKED and self.masterGrid['rows'][x1][y1] == CLICKED and self.masterGrid['rows'][x1][y1 +1] == CLICKED) and \
                       (self.masterGrid['columns'][x1 - 1][y1] == CLICKED and self.masterGrid['rows'][x1 - 1][y1] == CLICKED and self.masterGrid['rows'][x1 - 1][y1 + 1] == CLICKED) and \
                        self.masterGrid['columns'][x1][y1] == EMPTY:
                        self.masterGrid['columns'][x1][y1] = CLICKED
                        if self.isPoint(x1, y1, 'columns'):
                            self.PROGRAMPOINTS += 2
                            COMBOSOUND.play()
                        return

                    # THIS IS NOT A COMBO... LOOK AT THE 'OR' CONDITION
                    elif ((self.masterGrid['columns'][x1 + 1][y1] == CLICKED and self.masterGrid['rows'][x1][y1] == CLICKED and self.masterGrid['rows'][x1][y1 +1] == CLICKED) or \
                         (self.masterGrid['columns'][x1 - 1][y1] == CLICKED and self.masterGrid['rows'][x1 - 1][y1] == CLICKED and self.masterGrid['rows'][x1 - 1][y1 + 1] == CLICKED)) and \
                          self.masterGrid['columns'][x1][y1] == EMPTY:
                        self.masterGrid['columns'][x1][y1] = CLICKED
                        if self.isPoint(x1, y1, 'columns'):
                            self.PROGRAMPOINTS += 1
                        return

                elif x1 == 4: # CHECK FOR OPORTUNITIES ON THE LAST COLUMN
                    # LOOK LEFT SIDE
                    if self.masterGrid['columns'][x1 -1][y1] == CLICKED and self.masterGrid['rows'][x1 - 1][y1] == CLICKED and self.masterGrid['rows'][x1 - 1][y1 + 1] == CLICKED and self.masterGrid['columns'][x1][y1] == EMPTY:
                        self.masterGrid['columns'][x1][y1] = CLICKED
                        if self.isPoint(x1, y1, 'columns'):
                            self.PROGRAMPOINTS += 1
                        return
        # CHECK ROWS HERE
        for x2 in range(len(self.masterGrid['rows'])):  # 0<=x<=3
            for y2 in range(len(self.masterGrid['rows'][x2])):  # 0<=y<=4

                if y2 == 0:
                    # CHECK FOR OPORTUNITIES ON THE FIRST ROWS. SEE ONLY RIGHT DOWN
                    if self.masterGrid['rows'][x2][y2 +1] == CLICKED and self.masterGrid['columns'][x2][y2] == CLICKED and self.masterGrid['columns'][x2 + 1][y2] == CLICKED and self.masterGrid['rows'][x2][y2] == EMPTY:
                        self.masterGrid['rows'][x2][y2] = CLICKED
                        if self.isPoint(x2, y2, 'rows'):
                            self.PROGRAMPOINTS += 1
                        return

                elif y2 == 1 or y2 == 2 or y2 == 3:
                    # CHECK FOR OPORTUNITIES ON THE FIRST ROWS. SEE UP AND DOWN AND SEE FOR COMBO

                    # THIS IS A COMBO
                    if (self.masterGrid['rows'][x2][y2 +1] == CLICKED and self.masterGrid['columns'][x2][y2] == CLICKED and self.masterGrid['columns'][x2 + 1][y2] == CLICKED ) and \
                       (self.masterGrid['rows'][x2][y2 - 1] == CLICKED and self.masterGrid['columns'][x2][y2 - 1] == CLICKED and self.masterGrid['columns'][x2 + 1][y2 - 1] == CLICKED) and \
                        self.masterGrid['rows'][x2][y2] == EMPTY:
                        self.masterGrid['rows'][x2][y2] = CLICKED
                        if self.isPoint(x2, y2, 'rows'):
                            self.PROGRAMPOINTS += 2
                            COMBOSOUND.play()
                        return


                    # and GOES FIRST, or GOES LATER
                    elif ((self.masterGrid['rows'][x2][y2 +1] == CLICKED and self.masterGrid['columns'][x2][y2] == CLICKED and self.masterGrid['columns'][x2 + 1][y2] == CLICKED) or \
                         (self.masterGrid['rows'][x2][y2 - 1] == CLICKED and self.masterGrid['columns'][x2][y2 - 1] == CLICKED and self.masterGrid['columns'][x2 + 1][y2 - 1] == CLICKED)) and \
                          self.masterGrid['rows'][x2][y2] == EMPTY:
                        self.masterGrid['rows'][x2][y2] = CLICKED
                        if self.isPoint(x2, y2, 'rows'):
                            self.PROGRAMPOINTS += 1
                        return

                elif y2 == 4:
                    # CHECK FOR OPORTUNITIES ON THE FIRST ROWS. SEE ONLY RIGHT UP
                    if self.masterGrid['rows'][x2][y2 - 1] == CLICKED and self.masterGrid['columns'][x2][y2 - 1] == CLICKED and self.masterGrid['columns'][x2 + 1][y2 - 1] == CLICKED and self.masterGrid['rows'][x2][y2] == EMPTY:
                        self.masterGrid['rows'][x2][y2] = CLICKED
                        if self.isPoint(x2, y2, 'rows'):
                            self.PROGRAMPOINTS += 1
                        return

        # SET A RANDOM CHOICE IF NO CONDITION IS MEET
        self.randomProgramMove(self.masterGrid)
        return

    def getProgramMoveEasyMove(self):  # GIVEN A masterGrid state make the best posible move.
        # IT UPDATES GRID DATA STRUCTURE
        # Call update method before calling getProgramMove
        # ALGORITH

        # 1) IF THERE IS A MOVE THAT WILL MAKE YOU WIN TAKE IT, DO THIS CHECKING ONLY COLUMNS
        for x1 in range(len(self.masterGrid['columns'])):  # 0<=x<=4
            for y1 in range(len(self.masterGrid['columns'][x1])):  # 0<=y<=3
                if x1 < 4:  # IF THE COLUMN IS NOT THE LAST ON THE RIGHT
                    # TWO NEAR COLUMNS ARE CLICKED.
                    if self.masterGrid['columns'][x1][y1] == CLICKED and self.masterGrid['columns'][x1 + 1][
                        y1] == CLICKED:
                        # UPPER ROW IS CLICKED BUT NOT LOWER ONE
                        if self.masterGrid['rows'][x1][y1] == CLICKED and self.masterGrid['rows'][x1][y1 + 1] == EMPTY:
                            # SET LOWER ROW AS CLICKED AND MAKE A POINT
                            self.masterGrid['rows'][x1][y1 + 1] = CLICKED
                            if self.isPoint(x1, y1 + 1, 'rows'):
                                self.PROGRAMPOINTS += 1
                            return
                        # LOWER ROW IS CLICKED BUT NOT UPPER ONE
                        elif self.masterGrid['rows'][x1][y1] == EMPTY and self.masterGrid['rows'][x1][
                                    y1 + 1] == CLICKED:
                            # SET UPPER ROW AS CLICKED AND MAKE A POINT
                            self.masterGrid['rows'][x1][y1] = CLICKED
                            if self.isPoint(x1, y1, 'rows'):
                                self.PROGRAMPOINTS += 1
                            return
                        # UPPER AND LOWER ROWS ARE EMPTY. DO NOT SELECT ONE OF THEM OR PLAYER COULD MAKE A POINT ON HIS NEXT TURN
                        elif self.masterGrid['rows'][x1][y1] == EMPTY and self.masterGrid['rows'][x1][
                                    y1 + 1] == EMPTY:  #
                            pass

                    # ONE COLUMN CLICKED, HIS RIGHT COLUMN IS EMPTY. NOT FOR LAST COLUMN
                    if self.masterGrid['columns'][x1][y1] == CLICKED and self.masterGrid['columns'][x1 + 1][
                        y1] == EMPTY:
                        # UPPER AND LOWER ROWS ARE CLICKED
                        if self.masterGrid['rows'][x1][y1] == CLICKED and self.masterGrid['rows'][x1][
                                    y1 + 1] == CLICKED:
                            # SET THE RIGHT COLUMN AS CLICKED AND MAKE A POINT
                            self.masterGrid['columns'][x1 + 1][y1] = CLICKED  # SET CLICKED RIGHT COLUMN
                            if self.isPoint(x1 + 1, y1, 'columns'):
                                self.PROGRAMPOINTS += 1
                            return
                        # UPPER ROW IS CLICKED BUT LOWER ROW IS EMPTY. DO NOT SELECT ONE OF THEM OR PLAYER COULD MAKE A POINT ON HIS NEXT TURN
                        elif self.masterGrid['rows'][x1][y1] == CLICKED and self.masterGrid['rows'][x1][
                                    y1 + 1] == EMPTY:
                            pass
                        # LOWER ROW IS CLICKED BUT UPPER ONE IS EMPTY. DO NOT SELECT ONE OF THEM OR PLAYER COULD MAKE A POINT ON HIS NEXT TURN
                        elif self.masterGrid['rows'][x1][y1] == EMPTY and self.masterGrid['rows'][x1][
                                    y1 + 1] == CLICKED:
                            pass  #
                        # LOWER AND UPPER ROW ARE BOTH EMPTY
                        elif self.masterGrid['rows'][x1][y1] == EMPTY and self.masterGrid['rows'][x1][y1 + 1] == EMPTY:
                            # SET UPPER ROW AS CLICKED. IF I SET RIGHT COLUMN THERE IS A POSSIBILITY FOR THE PLAYER TO MAKE A POINT.
                            self.masterGrid['rows'][x1][y1] = CLICKED
                            if self.isPoint(x1, y1, 'rows'):
                                self.PROGRAMPOINTS += 1
                            return

                if x1 == 4:  # THE COLUMN IS THE LAST ON THE RIGHT NOT TO CONSIDER
                    pass

                if self.masterGrid['columns'][x1][y1] == CLICKED:
                    pass

        # SET A RANDOM CHOICE
        self.randomProgramMove(self.masterGrid)
        return


    # EXAMPLE emptyGrid {'columns': [[0, 0], [0, 1]], 'rows': []}. LIST OF GRID COORDS OF EMPTY SPACES
    def randomProgramMove(self, masterGrid):  # WILL GET self.masterGrid object inside getProgramMove() method
        emptyCoordGrid = {'columns' : [], 'rows' : []}
        for x1 in range(len(masterGrid['columns'])):
            for y1 in range(len(masterGrid['columns'][x1])):
                if masterGrid['columns'][x1][y1] == EMPTY:
                    emptyCoordGrid['columns'].append([x1, y1])

        for x1 in range(len(masterGrid['rows'])):
            for y1 in range(len(masterGrid['rows'][x1])):
                if masterGrid['rows'][x1][y1] == EMPTY:
                    emptyCoordGrid['rows'].append([x1, y1])

        randomKey = random.choice(list(emptyCoordGrid)) # RANDOM CHOICE BETWEEN COLUMN OR ROW
        randomCoordsList = emptyCoordGrid[randomKey]
        randomCoords = randomCoordsList[random.randint(0, len(randomCoordsList)-1)] # 0 FOR X COORD AND 1 FOR Y COORD

        masterGrid[randomKey][randomCoords[0]][randomCoords[1]] = CLICKED
        if self.isPoint(randomCoords[0], randomCoords[1], randomKey):
            self.PROGRAMPOINTS += 1

    # CHECK IF THE GIVEN GRID COORD COMPLETES A SQUARE AND THEN RETURN TRUE
    def isPoint(self, xCoord, yCoord, position):
        if position == 'columns':
            if xCoord == 0:  # FOR THE FIRST COLUMN CHECK THE RIGHT
                if self.masterGrid['columns'][xCoord + 1][yCoord] == CLICKED and self.masterGrid['rows'][xCoord][
                    yCoord] == CLICKED and self.masterGrid['rows'][xCoord][yCoord +1] == CLICKED:
                    return True

            elif xCoord ==1 or xCoord == 2 or xCoord == 3:
                if (self.masterGrid['columns'][xCoord + 1][yCoord] == CLICKED and self.masterGrid['rows'][xCoord][
                    yCoord] == CLICKED and self.masterGrid['rows'][xCoord][yCoord + 1] == CLICKED) or \
                    (self.masterGrid['columns'][xCoord - 1][yCoord] == CLICKED and self.masterGrid['rows'][xCoord - 1][
                    yCoord] == CLICKED and self.masterGrid['rows'][xCoord - 1][yCoord + 1] == CLICKED):
                    return True

                #THIS IS A COMBO
                # IN THIS CASE THE GIVEN GRID COORD COMPLETES 2 SQUARES AND SO 2 POINTS MUST BE GIVEN
                elif (self.masterGrid['columns'][xCoord + 1][yCoord] == CLICKED and self.masterGrid['rows'][xCoord][
                    yCoord] == CLICKED and self.masterGrid['rows'][xCoord][yCoord + 1] == CLICKED) and \
                    (self.masterGrid['columns'][xCoord - 1][yCoord] == CLICKED and self.masterGrid['rows'][xCoord - 1][
                    yCoord] == CLICKED and self.masterGrid['rows'][xCoord - 1][yCoord + 1] == CLICKED):
                    COMBOSOUND.play()
                    return True

            elif xCoord == 4:  # FOR THE LAST COLUMN CHECK THE LEFT
                if self.masterGrid['columns'][xCoord - 1][yCoord] == CLICKED and self.masterGrid['rows'][xCoord - 1][
                    yCoord] == CLICKED and self.masterGrid['rows'][xCoord - 1][yCoord + 1] == CLICKED:
                    return True

        if position == 'rows':

            if yCoord == 0: # UPPER ROW
                if self.masterGrid['rows'][xCoord][yCoord + 1] == CLICKED and self.masterGrid['columns'][xCoord][
                    yCoord] == CLICKED and self.masterGrid['columns'][xCoord + 1][yCoord] == CLICKED:
                    return True

            elif yCoord == 1 or yCoord == 2 or yCoord ==3: # INTERNAL ROWS
                if (self.masterGrid['rows'][xCoord][yCoord + 1] == CLICKED and self.masterGrid['columns'][xCoord][
                    yCoord] == CLICKED and self.masterGrid['columns'][xCoord + 1][yCoord] == CLICKED) or \
                    (self.masterGrid['rows'][xCoord][yCoord - 1] == CLICKED and self.masterGrid['columns'][xCoord][
                    yCoord - 1] == CLICKED and self.masterGrid['columns'][xCoord + 1][yCoord - 1] == CLICKED):
                    return True

                #THIS IS A COMBO, TWO POINTS SHOULD BE GIVEN
                if (self.masterGrid['rows'][xCoord][yCoord + 1] == CLICKED and self.masterGrid['columns'][xCoord][
                    yCoord] == CLICKED and self.masterGrid['columns'][xCoord + 1][yCoord] == CLICKED) and \
                    (self.masterGrid['rows'][xCoord][yCoord - 1] == CLICKED and self.masterGrid['columns'][xCoord][
                    yCoord - 1] == CLICKED and self.masterGrid['columns'][xCoord + 1][yCoord - 1] == CLICKED):
                    COMBOSOUND.play()
                    return True

            elif yCoord == 4: # LOWER ROW
                if self.masterGrid['rows'][xCoord][yCoord - 1] == CLICKED and self.masterGrid['columns'][xCoord][
                    yCoord - 1] == CLICKED and self.masterGrid['columns'][xCoord + 1][yCoord - 1] == CLICKED:
                    return True

    def isGaveOver(self):
        for x1 in range(len(self.masterGrid['columns'])):
            for y1 in range(len(self.masterGrid['columns'][x1])):
                if self.masterGrid['columns'][x1][y1] == EMPTY:
                    return False

        for x1 in range(len(self.masterGrid['rows'])):
            for y1 in range(len(self.masterGrid['rows'][x1])):
                if self.masterGrid['rows'][x1][y1] == EMPTY:
                    return False

        return True

class Squares():

    # RETURN A SURFACE AND HIS RECT
    def getSquaresRect(self, top, left):
        squareSurf = pygame.image.load('square-button.png')
        self.resizedSquareSurf = pygame.transform.scale(squareSurf, (SQUARESIZE, SQUARESIZE))
        self.squareRect = self.resizedSquareSurf.get_rect()
        self.squareRect.topleft = (top, left)
        return self.squareRect

    @classmethod
    def squareBoardStructure(cls):
        cls.newBoard=[[EMPTY for x in range(BOARDWIDTH)] for y in range(BOARDHEIGHT)]
        return cls.newBoard # CREATE INDIPENDENT ELEMENTS.. len(board)==5, len(board[0])==5

    def __init__(self):
        self.squaresBoard = Squares.squareBoardStructure()

    def reset(self): # reset data structure to its total empty state
        self.squaresBoard = Squares.squareBoardStructure()

    def drawItAll(self):
        for x in range(len(self.squaresBoard)):
            for y in range(len(self.squaresBoard[x])):
                top, left = self.topLeftSquarePixelCoords(x,y)
                self.squareRect = self.getSquaresRect(top, left)
                WINSURF.blit(self.resizedSquareSurf, self.squareRect)

    def drawImagesSquares(self):
        for x in range(len(self.squaresBoard)):
            for y in range(len(self.squaresBoard[x])):
                top, left = self.topLeftSquarePixelCoords(x, y)

    def clickedSquare(self, mousex, mousey):
        for x in range(len(self.squaresBoard)): # 0<=x<=4
            for y in range(len(self.squaresBoard[x])): # 0<=y<=4
                top, left = self.topLeftSquarePixelCoords(x, y)
                squareRect=pygame.Rect(top, left, SQUARESIZE, SQUARESIZE)

                if squareRect.collidepoint(mousex, mousey):
                    return x, y # 0<=x<=4, 0<=y<=4
        return None, None

    def secondClickIsValid(self, clickedSquares=0): #CHECK IF TWO SQUARES CLICKED ARE DISTANCED BY MORE THAN 1 SQUARE IN X OR Y COORDS
        self.clickedSquares = clickedSquares
        for x in range(len(self.squaresBoard)): # 0<=x<=4
            for y in range(len(self.squaresBoard[x])): # 0<=y<=4
                if self.squaresBoard[x][y] == CLICKED:
                    self.clickedSquares += 1
                    if self.clickedSquares == 1:
                        self.firstSquare = [x,y]
                        continue

                    elif self.clickedSquares == 2:
                        self.secondSquare = [x,y]
                        if ((self.firstSquare[0] - self.secondSquare[0] == 1 or self.firstSquare[0] - self.secondSquare[0] == -1)
                            and self.firstSquare[1] - self.secondSquare[1] == 0) or self.firstSquare[0] - self.secondSquare[0] == 0 \
                            and (self.firstSquare[1] - self.secondSquare[1] == 1 or self.firstSquare[1] - self.secondSquare[1] == -1):

                            return self.firstSquare, self.secondSquare # [x,y]

                        else:
                            invalid = textBanner('NOT VALID MOVE', 25, RED)
                            invalid.setCenterBlit(WINDOWWIDTH/2, WINDOWHEIGHT/2-30)
                            pygame.display.update()
                            return 'INVALID'

    def topLeftSquarePixelCoords(self, squareX, squareY): # GIVEN A SQUARE CORD GIVE ME HIS TOP-LEFT PIXEL CORDS . 0<=X,Y<=4
        topX=XMARGIN
        topY=YMARGIN
        x=topX+(SQUARESIZE+XSQUAREGAP)*squareX
        y=topY+(SQUARESIZE+YSQUAREGAP)*squareY
        return x, y

    def updateAfterPlayer(self, square1Coords, square2Coords, turn):
        if turn == 'player':
            self.squaresBoard[square1Coords[0]][square1Coords[1]] = CLICKED
            self.squaresBoard[square2Coords[0]][square2Coords[1]] = CLICKED

    def colorClickedSquare(self):
        for x in range(len(self.squaresBoard)):
            for y in range(len(self.squaresBoard[x])):
                if self.squaresBoard[x][y] == CLICKED:
                    top, left = self.topLeftSquarePixelCoords(x, y)
                    squareRect = pygame.Rect((top, left), (SQUARESIZE, SQUARESIZE))
                    pygame.draw.rect(WINSURF, RED, squareRect, 3)
                    pygame.display.update()
                    pygame.time.wait(300)

# INIZIALIZE THE OBJECT WITH THE TEXT, SIZE AND COLOR (BY DEFAULT IT WILL BE DARKGREEN)
class textBanner():

    def __init__(self, text, size, color = DARKGREEN):
        self.FONTMODEL = pygame.font.Font('orange_juice.ttf', size)
        self.TEXTSURF = self.FONTMODEL.render(text, True, color)
        self.TEXTRECT = self.TEXTSURF.get_rect()

    def setCenterBlit(self, posX, posY):
        self.TEXTRECT.center = (posX, posY)
        WINSURF.blit(self.TEXTSURF, self.TEXTRECT)

    def setTopLeftBlit(self, posX, posY):
        self.TEXTRECT.topleft = (posX, posY)
        WINSURF.blit(self.TEXTSURF, self.TEXTRECT)

    def testCollision(self, mouseX, mouseY):
        return self.TEXTRECT.collidepoint(mouseX, mouseY)

    def animateSelection(self):
        pygame.draw.rect(WINSURF, DARKGREEN, self.TEXTRECT, 4)

def kill():
    pygame.quit()
    sys.exit()

startingSquareBoard = Squares()
copySquareBoard = Squares()
initialGrid = GridBoard()

if __name__=='__main__':
    main()

# TO DO

# DON'T ALLOW THE PLAYER TO MAKE THE SAME MOVE TWICE, see isSecondClickValid








