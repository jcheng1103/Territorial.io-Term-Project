"""Run this file to start the game"""

from cmu_112_graphics import *
from countryClass import *
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
    app.startButton = button((app.width/2-120,app.height/2-50,
                        app.width/2+120,app.height/2+50),"#32c837",None,
                        ('Comic Sans MS', 40, 'bold italic'))
    font=('Comic Sans MS', 20, 'bold italic')
    app.tutorialButton = button((app.width/2-120,app.height/2+60,
                        app.width/2-5,app.height/2+110),"blue",None,font)
    app.settingsButton = button((app.width/2+5,app.height/2+60,
                        app.width/2+120,app.height/2+110),"red",None,font)
    app.warningWindow = False
    app.backButton= button((5,5,30,30),"#FF0000","white",
    ('Comic Sans MS', 30, 'bold italic'))
    settingsInit(app)
    app.playerColor = "#0000FF"
    app.playerName = "Player"

def mousePressed(app, event):
    app.mouseX, app.mouseY = event.x, event.y
    app.mousePressedX, app.mousePressedY = event.x, event.y

    if (app.state != 0):
        backButtonEvent(app,event)
    
    if (app.state == 0):
        startScreenMousePressed(app, event)  
    elif (app.state == 2):
        settingsScreenSliderEvent(app, event)
        changeName(app, event)
    elif (app.state == 3):
        gameMousePressed(app, event)

def mouseReleased(app, event):
    if (app.state == 3):
        gameMouseReleased(app, event)

def mouseDragged(app, event):
    if (app.state == 2):
        settingsScreenSliderEvent(app, event)
    elif (app.state == 3):
        gameMouseDragged(app, event)

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def keyPressed(app, event):
    if (event.key == "Escape"):
        if (app.state == 1 or app.state == 2):
            app.state = 0
        elif (app.state == 3):
            app.warningWindow = True
    if (app.state == 3):
        gameKeyPressed(app,event)

def timerFired(app):
    if (app.state == 3 and not app.warningWindow):
        gameTimerFired(app)

def redrawAll(app, canvas):
    if (app.state == 0):
        drawStartScreen(app, canvas)
    elif(app.state == 1):
        drawTutorialScreen(app,canvas)
    elif(app.state == 2):
        drawSettingsScreen(app,canvas)
    elif (app.state == 3):
        canvas.create_rectangle(0,0,800,800,fill="black")
        drawBoard(app, canvas)
        drawHud(app, canvas)
        drawLeaderBoard(app, canvas)
    
    if (app.warningWindow):
        drawWarningWindow(app,canvas)

    if (app.state != 0):
        drawBackButton(app,canvas)

def main():
    width, height = dimensions()
    runApp(width=width, height=height)

main()
