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
    app.width, app.height = dimensions()
    app.cellSize = 10
    app.drawnCellSize = 10 #To account for zooming
    app.rows = 80
    app.cols = 80
    #Which section of board will be displayed (top left bound)
    app.boardDrawX = 0
    app.boardDrawY = 0
    app.mouseX = 0
    app.mouseY = 0
    app.hudHeight = app.height-app.cols*app.cellSize
    #sliderBox is the coordinates for the bounding box of the attack slider
    app.sliderBox = (app.width*0.35,
                    app.cols*app.cellSize+app.hudHeight/2-app.hudHeight*0.3,
                    app.width*7/8,
                    app.cols*app.cellSize+app.hudHeight/2+app.hudHeight*0.3)
    app.players = 1
    app.defaultFill = "#1A1A1A"
    app.countryColors = ["blue"] #To be expanded in the future
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
        app.dict[i] = country(i,app.countryColors[i])
        app.board[row][col] = i

def drawBoard(app,canvas):
    #Drawing all cells
    #cSize = app.drawnCellSize
    cSize = app.cellSize
    for i in range(app.rows):
        for j in range(app.cols):
            x0, y0 = i*cSize-app.boardDrawX, j*cSize-app.boardDrawY
            x1, y1 = x0+cSize-app.boardDrawX, y0+cSize-app.boardDrawY
            id = app.board[i][j]
            fill = app.defaultFill
            if (id != -1):
                fill = app.dict[id].color
            canvas.create_rectangle(x0,y0,x1,y1,fill=fill,outline=fill)

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
    x, y = app.width/8, app.cellSize*app.cols+app.hudHeight/2
    canvas.create_text(x, y, text=f'{player.money}', fill='green', font=font)

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

def mouseDragged(app, event):
    player = app.dict[0]

    #When player drags mouse across slider
    x0,y0,x1,y1 = app.sliderBox
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        player.attackProportion = (event.x-x0)/(x1-x0)

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def keyPressed(app, event):
    #Zooming in and out, change cell size and bounds of board to be drawn
    #Keep the point the mouse is on invariant
    """
    if(event.key == "w" and app.drawnCellSize < app.cellSize*10):
        app.drawnCellSize += 1
        app.boardDrawX += app.drawnCellSize
        app.boardDrawY += app.drawnCellSize
    if (event.key == "s" and app.drawnCellSize > app.cellSize):
        app.drawnCellSize -= 1
        app.boardDrawX -= app.drawnCellSize
        app.boardDrawY -= app.drawnCellSize
    """

def timerFired(app):
    return

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawHud(app, canvas)

def runGame():
    width, height = dimensions()
    runApp(width=width, height=height)


def main():
    runGame()

main()
