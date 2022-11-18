import math, copy, random
from cmu_112_graphics import *
from countryObject import *

#returns width, hight
#Don't change this
def dimensions():
    width = 800
    height = 900
    return width,height

def appStarted(app):
    app.timerDelay = 500
    app.width, app.height = dimensions()
    app.cellSize = 10
    app.drawnCellSize = 10 #To account for zooming
    app.rows = 80
    app.cols = 80
    #Which section of board will be displayed (top left and bottom right bound)
    app.boardTopLeft = (0,0)
    app.boardBottomRight = (app.width,app.width)
    app.mouseX = 0
    app.mouseY = 0
    app.hudHeight = app.height-app.cols*app.cellSize
    app.showLeaderBoard = False
    #sliderBox is the coordinates for the bounding box of the attack slider
    app.sliderBox = (app.width*0.35,
                    app.cols*app.cellSize+app.hudHeight/2-app.hudHeight*0.3,
                    app.width*7/8,
                    app.cols*app.cellSize+app.hudHeight/2+app.hudHeight*0.3)
    app.players = 5
    app.defaultFill = "#1A1A1A"
    app.countryColors = ["blue","#ffff00","#00ff00","#00ffff","#ff0000"]
    app.names = ["Player", "Bot 1", "Bot 2", "Bot 3", "Bot 4"]
    #Dictionary that supports using a country's integer id to find the
    #corrsponding country object
    app.dict = {}

    #Initialize the board with -1s. The -1s show the current tile is empty.
    app.board = []
    for i in range(app.rows):
        app.board.append([-1]*app.cols)

    #Add countries in at random positions (1 for now)
    for i in range(app.players):
        row = random.randint(0,app.rows-1)
        col = random.randint(0,app.cols-1)
        #If the tile is already occupied, keep rolling random
        while (app.board[row][col] == 0):
            row = random.randint(0,app.rows-1)
            col = random.randint(0,app.cols-1)
        app.dict[i] = country(i,app.countryColors[i],app.names[i])
        app.board[row][col] = i

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
                x0,y0=i*cSize+app.boardTopLeft[0],j*cSize+app.boardTopLeft[1]
                x1,y1=x0+cSize,y0+cSize
                fill = app.dict[id].color
                canvas.create_rectangle(x0,y0,x1,y1,fill=fill,outline=fill)

def getCountrySize(a):
        return a.size

def drawLeaderBoard(app, canvas):
    x0,y0,x1,y1=app.width*0.92,app.width*0.02,app.width*0.98,app.width*0.08
    app.mouseX
    if (not (app.mouseX>x0 and app.mouseX>y0 
        and app.mouseX<x1 and app.mouseY<y1)):
        canvas.create_rectangle(x0,y0,x1,y1,fill="black",outline="white")
        return
    x0,y0,x1,y1=app.width*0.7,app.width*0.02,app.width*0.98,app.width*0.4
    canvas.create_rectangle(x0,y0,x1,y1,fill="black",outline="white")

    tempL = []
    for key in app.dict:
        tempL.append(app.dict[key])
    tempL.sort(key = getCountrySize)
    x, y = app.width*0.84, app.width*0.02+10
    font=('Comic Sans MS', 15, 'bold italic')
    for i in range(app.players):
        canvas.create_text(x-app.width*0.1, y, fill='white', font=font,
        text=f'{i+1}.')
        canvas.create_text(x, y, fill='white', font=font,
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
    font=('Comic Sans MS', 40, 'bold italic')
    canvas.create_rectangle(x0-(y1-y0),y0,x0,y1,
    outline="#A0A0A0",fill="#303030")
    canvas.create_text(x0-(y1-y0)/2, (y0+y1)/2, text='-', 
    fill='white', font=font)
    canvas.create_rectangle(x1,y0,x1+(y1-y0),y1,
    outline="#A0A0A0",fill="#303030")
    canvas.create_text(x1+(y1-y0)/2, (y0+y1)/2, text='+', 
    fill='white', font=font)

def mousePressed(app, event):
    #The id of the player is always 0
    player = app.dict[0]

    #When slider is clicked
    x0,y0,x1,y1 = app.sliderBox
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        player.attackProportion = (event.x-x0)/(x1-x0)
    #When slider buttons are clicked
    if (event.x > x0-(y1-y0) and event.x < x0 and 
    event.y > y0 and event.y < y1):
        player.attackProportion -= 0.05
    if (event.x > x1 and event.x < x1+(y1-y0) and 
    event.y > y0 and event.y < y1):
        player.attackProportion += 0.05
    #Restrict proportion to between 0 and 1
    player.attackProportion = min(player.attackProportion,1.0)
    player.attackProportion = max(player.attackProportion,0)

def mouseDragged(app, event):
    player = app.dict[0]

    #When player drags mouse across slider
    x0,y0,x1,y1 = app.sliderBox
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        player.attackProportion = (event.x-x0)/(x1-x0)
    #When player drags mouse across slider
    if (event.y < app.width):
        xShift = event.x-app.mouseX
        yShift = event.y-app.mouseY
        app.boardTopLeft = (app.boardTopLeft[0]+xShift,
                            app.boardTopLeft[1]+yShift)
        app.boardBottomRight = (app.boardBottomRight[0]+xShift,
                            app.boardBottomRight[1]+yShift)
        app.mouseX = event.x
        app.mouseY = event.y

def mouseMoved(app, event):
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

def keyPressed(app, event):
    #Zooming in and out, change cell size and bounds of board to be drawn
    #Keep the point the mouse is on invariant

    #Zoom limit = 10x, for both in and out
    if(event.key == "w" and 
    (app.boardBottomRight[0]-app.boardTopLeft[0])*1.1 <= app.width*10):
        app.boardTopLeft, app.boardBottomRight = scale(app,1.1)
    if (event.key == "s"and 
    (app.boardBottomRight[0]-app.boardTopLeft[0])*0.9 >= app.width*0.1):
        app.boardTopLeft, app.boardBottomRight = scale(app,0.9)

def timerFired(app):
    for key in app.dict:
        app.dict[key].updateMoney()

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,800,800,fill="black")
    drawBoard(app, canvas)
    drawHud(app, canvas)
    drawLeaderBoard(app, canvas)

def runGame():
    width, height = dimensions()
    runApp(width=width, height=height)


def main():
    runGame()

main()
