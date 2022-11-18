import math, copy, random
from cmu_112_graphics import *
from gameFuncs import *

def drawStartScreen(app, canvas):
    #Background
    canvas.create_rectangle(0,0,app.width,app.height,
    fill="#303030")

    #Start button
    x0,y0,x1,y1 = app.startButton
    canvas.create_rectangle(x0,y0,x1,y1,
    fill="#32c837")
    font=('Comic Sans MS', 40, 'bold italic')
    canvas.create_text((x1+x0)/2, (y1+y0)/2, text='Start Game', 
    fill='white', font=font)

    #Tutorial button
    x0,y0,x1,y1 = app.tutorialButton
    canvas.create_rectangle(x0,y0,x1,y1,
    fill="blue")
    font=('Comic Sans MS', 20, 'bold italic')
    canvas.create_text((x1+x0)/2, (y1+y0)/2, text='Tutorial', 
    fill='white', font=font)

    #Settings button
    x0,y0,x1,y1 = app.settingsButton
    canvas.create_rectangle(x0,y0,x1,y1,
    fill="red")
    font=('Comic Sans MS', 20, 'bold italic')
    canvas.create_text((x1+x0)/2, (y1+y0)/2, text='Settings', 
    fill='white', font=font)

def startScreenMousePressed(app, event):
    x0,y0,x1,y1 = app.startButton
    #If click is within startButton bounds
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        app.state = 3
        gameInit(app)