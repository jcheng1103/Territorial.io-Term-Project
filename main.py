import math, copy, random
from cmu_112_graphics import *
from countryObject import *
from gameFuncs import *
from menuFuncs import *

#returns width, hight
#There isn't support for changing the window size yet
def dimensions():
    width = 800
    height = 900
    return width,height

def appStarted(app):
    app.width, app.height = dimensions()
    app.state = 0 #0 = start screen, 1 = tutorial, 2 = settings, 3 = game
    app.startButton = (app.width/2-120,app.height/2-50,
                        app.width/2+120,app.height/2+50)
    app.tutorialButton = (app.width/2-120,app.height/2+60,
                        app.width/2-5,app.height/2+110)
    app.settingsButton = (app.width/2+5,app.height/2+60,
                        app.width/2+120,app.height/2+110)
    #gameInit(app)

def mousePressed(app, event):
    if (app.state == 0):
        startScreenMousePressed(app, event)    
    elif (app.state == 3):
        gameMousePressed(app, event)

def mouseDragged(app, event):
    if (app.state == 3):
        gameMouseDragged(app, event)

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def keyPressed(app, event):
    if (app.state == 3):
        gameKeyPressed(app,event)

def timerFired(app):
    if (app.state == 3):
        gameTimerFired(app)

def redrawAll(app, canvas):
    #MVC violation?
    if (app.state == 0):
        drawStartScreen(app, canvas)
    elif (app.state == 3):
        canvas.create_rectangle(0,0,800,800,fill="black")
        drawBoard(app, canvas)
        drawHud(app, canvas)
        drawLeaderBoard(app, canvas)

def main():
    width, height = dimensions()
    runApp(width=width, height=height)

main()
