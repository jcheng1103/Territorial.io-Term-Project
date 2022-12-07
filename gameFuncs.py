import math, copy, random
from cmu_112_graphics import *
from countryClass import *
from gameAI import *
from buttonClass import *
import os

def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def gameInit(app):
    app.timerDelay = 500
    app.cellSize = 10
    app.drawnCellSize = 10 #To account for zooming
    app.rows = 80
    app.cols = 80
    #Which section of board will be displayed (top left and bottom right bound)
    app.boardTopLeft = (0,0)
    app.boardBottomRight = (app.width,app.width)
    app.mouseWasDragged = True
    app.hudHeight = app.height-app.cols*app.cellSize
    app.showLeaderBoard = False
        #sliderBox is the coordinates for the bounding box of the attack slider
    app.sliderBox = (app.width*0.35,
                    app.cols*app.cellSize+app.hudHeight/2-app.hudHeight*0.3,
                    app.width*7/8,
                    app.cols*app.cellSize+app.hudHeight/2+app.hudHeight*0.3)
    x0,y0,x1,y1 = app.sliderBox
    app.minusButton = button((x0-(y1-y0),y0,x0,y1),fill="#303030",
    outline="#A0A0A0",font=('Comic Sans MS', 40, 'bold italic'))
    app.plusButton = button((x1,y0,x1+(y1-y0),y1,),fill="#303030",
    outline="#A0A0A0",font=('Comic Sans MS', 40, 'bold italic'))
    app.warningWindowDims = (app.width/2-250,app.width/2-150,
                        app.width/2+250,app.width/2+150)
    x0,y0,x1,y1 = app.warningWindowDims
    font=('Comic Sans MS', 20, 'bold italic')
    app.yesButton = button((x0+(x1-x0)*0.1,y0+(y1-y0)*0.7,
                    x0+(x1-x0)*0.3,y0+(y1-y0)*0.85),"#00FF00","white",font)
    app.noButton = button((x0+(x1-x0)*0.7,y0+(y1-y0)*0.7,
                    x0+(x1-x0)*0.9,y0+(y1-y0)*0.85),"#FF0000","white",font)
    app.returnToGameButton = button((x0+(x1-x0)*0.4,y0+(y1-y0)*0.7,
                    x0+(x1-x0)*0.6,y0+(y1-y0)*0.85),"#606060","white",font)
    app.returnToMenuButton = button((x0+(x1-x0)*0.3,y0+(y1-y0)*0.7,
                    x0+(x1-x0)*0.7,y0+(y1-y0)*0.85),"#0000FF","white",font)
    app.defaultFill = "#1A1A1A"

    if (app.loadFile == None):
        newGameInit(app)
    else:
        loadGame(app)
    
    app.loadFile = None
    

def newGameInit(app):
    app.players = 8
    app.countryColors = [app.playerColor,"#ffff00","#00ff00","#00ffff",
                        "#ff0000","#A0A0A0","#ff00ff","#fc9105"]
    app.names = [app.playerName, "Bot 1", "Bot 2", "Bot 3", "Bot 4", "Bot 5", 
                "Bot 6", "Bot 7"]
    #Dictionary that supports using a country's integer id to find the
    #corrsponding country object
    app.dict = {}

    #Initialize the board with -1s. The -1s show the current tile is empty.
    app.board = []
    for i in range(app.rows):
        app.board.append([-1]*app.cols)

    for i in range(app.players):
        row = random.randint(0,app.rows-1)
        col = random.randint(0,app.cols-1)
        #If the tile is already occupied, keep rolling random
        while (app.board[row][col] == 0):
            row = random.randint(0,app.rows-1)
            col = random.randint(0,app.cols-1)
        temp = dict()
        app.dict[i] = country(i,app.countryColors[i],app.names[i],attacks=temp)
        app.board[row][col] = i

splitStr = "🤯🤓@🤮🙃"
def loadGame(app):
    with open(app.loadFile) as f:
        line = f.readline()
        app.players = int(line)

        #Reading in data for each country
        app.dict = {}
        for i in range(app.players):
            data = f.readline().split(splitStr)
            data[0] = int(data[0])
            data[3] = int(data[3])
            data[4] = int(data[4])
            data[5] = float(data[5])
            attacks = dict()
            for i in range(7,len(data)-3,3):
                dict[data[i]] = (data[i+1],data[i+2])
            app.dict[data[0]] = country(data[0],data[1],data[2],data[3],data[4],
            data[5],attacks)
        
        #Reading in data for the board
        bData = f.readline()
        app.board = []
        while (bData != ""):
            temp = []
            for i in bData.split(splitStr):
                if (i == "\n"):
                    break
                temp.append(int(i))
            app.board.append(temp)
            bData = f.readline()
        f.close()

def saveGame(app):
    #Open file
    temp = app.getUserInput("Enter save file name:")
    while (temp != None and os.path.isfile(temp)):
        temp = app.getUserInput("""Save file already exists, 
                                please enter another name:""")
    if (temp == None):
        return
    
    f = open(temp, "w")


    f.write(str(app.players)+"\n")

    #Saving data for each country
    for i in app.dict:
        c = app.dict[i]
        temp = [i,c.color,c.name,c.money,c.size,c.attackProportion]
        for key in c.attacks:
            temp.append(key)
            temp.append(c.attacks[key][0])
            temp.append(c.attacks[key][1])
        temp.append("\n")
        f.write(splitStr.join(map(str, temp)))
    
    #Saving data for the board
    for row in app.board:
        temp = []
        for i in row:
            temp.append(str(i))
        temp.append("\n")
        f.write(splitStr.join(temp))
    f.close()


#Finds the position to draw something on canvas based on position in game board
def boardToDisplay(app,row,col):
    width = app.boardBottomRight[0] - app.boardTopLeft[0]
    x = app.boardTopLeft[0] + col * width / app.cols
    y = app.boardTopLeft[1] + row * width / app.rows
    return x,y

def onScreen(app,x0,y0,x1,y1):
    return not(x1<0 or x0>app.width or y1<0 or y0>app.width)

def drawBoard(app,canvas):
    x0, y0 = app.boardTopLeft
    x1, y1 = app.boardBottomRight
    cSize = (app.boardBottomRight[0]-app.boardTopLeft[0])/app.cols
    canvas.create_rectangle(x0-cSize,y0-cSize,x1+cSize,y1+cSize,fill='white') #Map border
    canvas.create_rectangle(x0,y0,x1,y1,fill=app.defaultFill,width=0)
    for i in range(app.rows):
        for j in range(app.cols):
            id = app.board[i][j]
            if (id != -1):
                x0,y0=boardToDisplay(app,i,j)
                x1,y1=boardToDisplay(app,i+1,j+1)
                if (not onScreen(app,x0,y0,x1,y1)):
                    continue #Offscreen cells aren't drawn to improver performance
                fill = app.defaultFill
                if (id in app.dict):
                    fill = app.dict[id].color
                canvas.create_rectangle(x0,y0,x1,y1,fill=fill,outline=fill)
    drawNames(app,canvas)

def getCountrySize(a):
        return a.size

def drawLeaderBoard(app, canvas):
    x0,y0,x1,y1=app.width*0.92,app.width*0.02,app.width*0.98,app.width*0.08
    app.mouseX
    #Only draw leaderboard if mouse is in the top left corner
    if (not (app.mouseX>x0 and app.mouseX>y0 
        and app.mouseX<x1 and app.mouseY<y1)):
        canvas.create_rectangle(x0,y0,x1,y1,fill="black",outline="white")
        return
    
    w = app.width
    x0,y0,x1,y1=w*0.7,w*0.02,w*0.98,y0+(len(app.dict)+1)*25
    canvas.create_rectangle(x0,y0,x1,y1,fill="black",outline="white")

    #Make a list of all countries sorted by size
    tempL = []
    for key in app.dict:
        tempL.append(app.dict[key])
    tempL.sort(key = getCountrySize,reverse = True)

    #Draw leaderboard
    x, y = app.width*0.84, app.width*0.02+10
    canvas.create_text(x, y, fill='white', 
    font=('Comic Sans MS', 20, 'bold italic'), text="Leaderboard")
    canvas.create_line(x0,y0+20,x1,y0+20, fill = "white",width = 1)
    y = app.width*0.02+30
    font=('Comic Sans MS', 15, 'italic')
    for i in range(len(app.dict)):
        canvas.create_text(x-app.width*0.1, y, fill='white', font=font,
        text=f'{i+1}.')
        canvas.create_text(x, y, fill=tempL[i].color, font=font,
        text=f'{tempL[i].name}')
        canvas.create_text(x+app.width*0.1, y, fill='white', font=font,
        text=f'{tempL[i].size}')
        y += 20


#Function to conver color int to hex value
def hexRGB(n):
    hexList = "0123456789ABCDEF"
    return hexList[n//16] + hexList[n%16] 

def sliderColor(player):
    """when proportion is 0.0, slider is green, when proportion is 1.0,
    the slider is red. The color ranges from green to red depending
    on the proportion selected"""
    r = int(255*player.attackProportion)
    g = int(255*(1-player.attackProportion))
    b = int(100*(1-player.attackProportion))
    return "#"+hexRGB(r)+hexRGB(g)+hexRGB(b)

def drawHud(app,canvas):
    #Hud background
    canvas.create_rectangle(0,app.width,app.width,app.height,fill="#FFFFFF")
    #Hud border with game board
    canvas.create_line(0,app.cellSize*app.cols,app.width,app.cellSize*app.cols,
    fill = "red",width = 3)

    #Displaying player money
    #The id of the player is always 0
    player = app.dict[0]
    font=('Comic Sans MS', 20, 'bold italic')
    x, y = app.width/8, app.cellSize*app.cols+app.hudHeight*0.3
    canvas.create_text(x, y, text=f'{player.money}', fill='green', font=font)

    #Displaying growth rate
    font=('Comic Sans MS', 15, 'bold italic')
    y = app.cellSize*app.cols+app.hudHeight*0.6
    canvas.create_text(x, y, fill='black', font=font,
    text=f'Interest rate: {str(round((player.growthRate-1)*100,2))}%')
    font=('Comic Sans MS', 15, 'bold italic')
    y = app.cellSize*app.cols+app.hudHeight*0.75
    canvas.create_text(x, y, fill='black', font=font,
    text=f'Income: {player.size}')

    #Displaying slider
    x0,y0,x1,y1 = app.sliderBox
    canvas.create_rectangle(x0,y0,x1,y1,outline="#A0A0A0",fill="#303030")
    canvas.create_rectangle(x0,y0,x0+(x1-x0)*player.attackProportion,y1,
    fill=sliderColor(player),outline="#A0A0A0")
    attackMon = int(player.money*player.attackProportion)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'{attackMon}', 
    fill='white', font=font)

    #Slider buttons
    app.minusButton.draw(canvas,"-")
    app.plusButton.draw(canvas,"+")

def drawWarningWindow(app, canvas):
    x0,y0,x1,y1 = app.warningWindowDims
    canvas.create_rectangle(x0,y0,x1,y1,fill="#000000",outline="white")
    canvas.create_text((x0+x1)/2, y0+(y1-y0)*0.2, fill='white', 
    font=('Comic Sans MS', 20, 'bold italic'),
    text= "Your progress won't be automatically saved.")
    canvas.create_text((x0+x1)/2, y0+(y1-y0)*0.3, fill='white', 
    font=('Comic Sans MS', 20, 'bold italic'),
    text= "Would you like to save your progress?")

    app.yesButton.draw(canvas,"Yes")
    app.noButton.draw(canvas,"No")
    app.returnToGameButton.draw(canvas,"Resume")

def drawNames(app, canvas):
    #Calculating the prefix sum of borders
    for key in app.dict:
        app.dict[key].maxWidth = 0
        app.dict[key].row = -1
        app.dict[key].col = -1
    borders = []
    for i in range(len(app.board)):
        borders.append([0]*len(app.board[0]))

    for i in range(len(app.board)):
        for j in range(1,len(app.board[0])):
            borders[i][j] += borders[i][j-1]
            if (app.board[i][j] != app.board[i][j-1]):
                borders[i][j] += 1
    
    for i in range(len(app.board[0])):
        for j in range(len(app.board)):
            borders[j][i] += borders[j-1][i]
            if (app.board[j][i] != app.board[j-1][i]):
                borders[j][i] += 1

    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            #For each top left corner what is the biggest possible text box?
            if (app.board[i][j] == -1):
                continue #To avoid evaluating empty space
            current = app.dict[app.board[i][j]]
            #Bottom right coordinates
            i1, j1=int(i+current.maxWidth*current.ratio),int(j+current.maxWidth)
            if (current.row == -1):
                current.row = i
                current.col = j
            #While maxWidth can be expanded, keep expanding maxWidth
            # and update row,col accordingly
            while (i1 < len(app.board) and j1 < len(app.board[0]) and 
            app.board[i][j] == app.board[i1][j1] and
            borders[i1][j1]-borders[i1][j]-borders[i][j1]+borders[i][j] == 0):
                current.maxWidth += 1
                current.row = i
                current.col = j
                i1 = int(i+current.maxWidth*current.ratio)
                j1 = int(j+current.maxWidth)
    
    for key in app.dict:
        drawName(app,app.dict[key],canvas)

def drawName(app,current,canvas):
    x,y = boardToDisplay(app,current.row+0.5,current.col+current.maxWidth/2)
    textLength = max(len(current.name),len(str(current.money)))
    widthPerLetter = current.maxWidth / textLength
    fontSize = roundHalfUp(widthPerLetter * 0.01 * 
                            (app.boardBottomRight[0] - app.boardTopLeft[0]))
    if (fontSize < 6):
        return
    fill = "white"
    color = current.color #Color of the country
    brightness = (int(color[1:3],base=16)+int(color[3:5],base=16)+
                                                    int(color[5:],base=16))/3
    if (brightness > 80):
        fill = "black" #adjusts text color if white text will be too difficult to see
    canvas.create_text(x, y+fontSize*0.5, fill=fill, 
    font=('Comic Sans MS', fontSize, 'bold italic'), text=current.name)
    canvas.create_text(x, y+fontSize*1.5, fill=fill, text=f"{current.money}",
    font=('Comic Sans MS', fontSize, 'bold italic'))

def drawAttacks(app, canvas):
    player = app.dict[0]
    x0,x1 = app.width/2-75,app.width/2+75
    y0,y1 = 10, 40
    for i in player.attacks:
        if (y1 > app.width/2):
            break
        if (i == -1):
            drawBackgroundAttack(app,canvas,app.width/2-75,y0,app.width/2+75,y1)
        elif (i in app.dict):
            x0 = app.width/2-75
            x1 = x0 + len(app.dict[i].name)*20
            drawAttack(app, canvas,x0,y0,x1,y1,i)
        y0 += 40
        y1 += 40

#Draws attack progression meter for conquering into background
def drawBackgroundAttack(app, canvas,x0,y0,x1,y1):
    player = app.dict[0]
    canvas.create_rectangle(x0,y0,x1,y1,fill="#818181",outline="white")
    canvas.create_text((x0+x1)/2, (y0+y1)/2, fill="white", 
    text=f"{player.attacks[-1][0]}",
    font=('Comic Sans MS', 20, 'bold italic'))
    proportion = player.attacks[-1][0]/player.attacks[-1][1]
    canvas.create_line(x0,y1,x0+(x1-x0)*proportion,y1,fill="white",width=3)

def drawAttack(app, canvas,x0,y0,x1,y1,id):
    player = app.dict[0]
    canvas.create_rectangle(x0,y0,x1+150,y1,fill="#818181",outline="white")
    
    #Left part (name)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, fill="white", 
    text=f"{app.dict[id].name}",
    font=('Comic Sans MS', 20, 'bold italic'))
    canvas.create_line(x1,y0,x1,y1,fill="white",width=1)

    #Right part (troops)
    canvas.create_text(x1+75, (y0+y1)/2, fill="white", 
    text=f"{player.attacks[id][0]}",
    font=('Comic Sans MS', 20, 'bold italic'))
    proportion = player.attacks[id][0]/player.attacks[id][1]
    canvas.create_line(x1,y1,x1+150*proportion,y1,fill="white",width=3)
    
def drawGameOverWindow(app, canvas):
    x0,y0,x1,y1 = app.warningWindowDims
    canvas.create_rectangle(x0,y0,x1,y1,fill="#000000",outline="white")
    if (app.dict[0].size > 0):
        canvas.create_text((x0+x1)/2, y0+(y1-y0)*0.2, fill='white', 
        font=('Comic Sans MS', 20, 'bold italic'),
        text= "You won!")
    else:
        canvas.create_text((x0+x1)/2, y0+(y1-y0)*0.2, fill='white', 
        font=('Comic Sans MS', 20, 'bold italic'),
        text= "You lost!")

    app.returnToMenuButton.draw(canvas,"Return to menu")

def unScale(app, event):
    width = (app.boardBottomRight[0]-app.boardTopLeft[0])
    j = int((event.x-app.boardTopLeft[0])/width*app.cols)
    i = int((event.y-app.boardTopLeft[1])/width*app.rows)
    if (i>=0 and i<=app.rows and j>=0 and j<=app.cols):
        return app.board[i][j]
    return None

def gameMousePressed(app, event):
    app.mouseWasDragged = False
    if (app.warningWindow):
        app.mouseWasDragged = True

    #When warning window is open
    if (app.warningWindow):
        if (app.yesButton.checkBounds(event)):
            app.state = 0
            saveGame(app)
            app.warningWindow = False
        if (app.noButton.checkBounds(event)):
            app.state = 0
            app.warningWindow = False
        if (app.returnToGameButton.checkBounds(event)):
            app.warningWindow = False
        return
    
    if (app.gameOver):
        if (app.returnToMenuButton.checkBounds(event)):
            app.state = 0
            app.gameOver = False
        return
    #For when the game is continuing
    #The id of the player is always 0
    player = app.dict[0]

    #When slider is clicked
    x0,y0,x1,y1 = app.sliderBox
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        player.attackProportion = (event.x-x0)/(x1-x0)
    #When slider buttons are clicked
    if (app.minusButton.checkBounds(event)):
        player.attackProportion -= 0.05
    if (app.plusButton.checkBounds(event)):
        player.attackProportion += 0.05
    #Restrict proportion to between 0 and 1
    player.attackProportion = min(player.attackProportion,1.0)
    player.attackProportion = max(player.attackProportion,0)

def gameMouseReleased(app, event):
    #Checking if an attack is taking place
    #If statement checks to see if the mouse was being dragged
    if (app.mouseWasDragged or app.warningWindow or app.gameOver):
        return
    
    player = app.dict[0]
    if (event.y < app.height-app.hudHeight):
        id = unScale(app,event)
        if (id != None and id != player.id):
            player.attackInit(app,id,int(player.attackProportion*player.money))

def gameMouseDragged(app, event):
    player = app.dict[0]
    app.mouseWasDragged = True
    #When player drags mouse across slider
    x0,y0,x1,y1 = app.sliderBox
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        player.attackProportion = (event.x-x0)/(x1-x0)
        
    #When player drags mouse across board
    if (event.y < app.width):
        xShift = event.x-app.mouseX
        yShift = event.y-app.mouseY
        app.boardTopLeft = (app.boardTopLeft[0]+xShift,
                            app.boardTopLeft[1]+yShift)
        app.boardBottomRight = (app.boardBottomRight[0]+xShift,
                            app.boardBottomRight[1]+yShift)
    app.mouseX = event.x
    app.mouseY = event.y

#Scales the location of top right and bottom right bound
#sf = scale factor
def scale(app, sf):
    topLeftVec = ((app.boardTopLeft[0]-app.mouseX)*sf,
                (app.boardTopLeft[1]-app.mouseY)*sf)
    bottomRightVec = ((app.boardBottomRight[0]-app.mouseX)*sf,
                    (app.boardBottomRight[1]-app.mouseY)*sf)
    return ((topLeftVec[0]+app.mouseX,topLeftVec[1]+app.mouseY),
            (bottomRightVec[0]+app.mouseX, bottomRightVec[1]+app.mouseY))

def gameKeyPressed(app,event):
    #Zooming in and out, change cell size and bounds of board to be drawn
    #Keep the point the mouse is on invariant

    #Zoom limit = 10x, for both in and out
    if(event.key == "w" and 
    (app.boardBottomRight[0]-app.boardTopLeft[0])*1.1 <= app.width*10):
        app.boardTopLeft, app.boardBottomRight = scale(app,1.1)
    if (event.key == "s"and 
    (app.boardBottomRight[0]-app.boardTopLeft[0])*0.9 >= app.width*0.1):
        app.boardTopLeft, app.boardBottomRight = scale(app,0.9)

def gameTimerFired(app):
    L = []
    for key in app.dict:
        L.append(key)
    for key in L:
        if (app.dict[key].size <= 0):
            if (key == 0):
                app.gameOver = True
                break
            del app.dict[key]
            continue
        app.dict[key].updateMoney()
        if (key != 0):
            runAi(app,app.dict[key])
        app.dict[key].incrementAttacks(app)

    if (0 not in app.dict or len(app.dict) == 1):
        app.gameOver = True