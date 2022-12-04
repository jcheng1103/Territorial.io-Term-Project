from cmu_112_graphics import *
from gameFuncs import *
import os

def drawStartScreen(app, canvas):
    #Background
    canvas.create_rectangle(0,0,app.width,app.height,
    fill="#303030")
    canvas.create_text(app.width/2, app.height*0.2, text='Territorial.io', 
    fill='white', font=('Comic Sans MS', 50, 'bold italic'))
    canvas.create_text(app.width/2, app.height*0.35, 
    text=f'File currently loaded: {app.loadFile}', 
    fill='white', font=('Comic Sans MS', 30, 'bold italic'))

    app.startButton.draw(canvas,"Start Game")
    app.tutorialButton.draw(canvas,"Tutorial")
    app.settingsButton.draw(canvas,"Settings")
    app.loadButton.draw(canvas,"Load Save")

def startScreenMousePressed(app, event):
    #If click is within startButton bounds
    if (app.startButton.checkBounds(event)):
        app.state = 3
        app.mouseX = event.x
        app.mouseY = event.y
        gameInit(app)
    #If click is within tutorialButton bounds
    if (app.tutorialButton.checkBounds(event)):
        app.state = 1
    #If click is within settingsButton bounds
    if (app.settingsButton.checkBounds(event)):
        app.state = 2
    
    if (app.loadButton.checkBounds(event)):
        temp = app.getUserInput("Enter save file name:")
        while (temp != None and not os.path.isfile(temp)):
            temp = app.getUserInput("""Save file doesn't exist, 
                                    please enter another name:""")
        if (temp == None):
            return
        app.loadFile = temp
    
def settingsInit(app):
    app.nameChangeButton = (app.width*0.4,app.height*0.2,
                            app.width*0.6,app.height*0.25)
    app.rSlider = (app.width*0.4,app.height*0.5,app.width*0.7,app.height*0.58)
    app.gSlider = (app.width*0.4,app.height*0.6,app.width*0.7,app.height*0.68)
    app.bSlider = (app.width*0.4,app.height*0.7,app.width*0.7,app.height*0.78)
    app.colorDisplay = (app.width*0.4-app.height*0.1,app.height*0.5,
    app.width*0.4-app.height*0.02,app.height*0.78)
    app.rVal = 0
    app.gVal = 0
    app.bVal = 255

def drawSettingsScreen(app, canvas):
    #Background
    canvas.create_rectangle(0,0,app.width,app.height,
    fill="#303030")

    #Name change
    canvas.create_text(app.width/2, app.height*0.1, fill="white", 
    font=('Comic Sans MS', 30, 'bold italic'), text="Current name")
    canvas.create_text(app.width/2, app.height*0.15, fill=app.playerColor, 
    font=('Comic Sans MS', 30, 'bold italic'), text=f'{app.playerName}')
    x0,y0,x1,y1 = app.nameChangeButton
    canvas.create_rectangle(x0,y0,x1,y1,fill="#000000",outline="white")
    canvas.create_text(app.width/2, (y0+y1)/2, fill="white", 
    font=('Comic Sans MS', 15, 'bold italic'), text=f"Click to change name")

    #Color selecting sliders
    x0,y0,x1,y1 = app.rSlider
    canvas.create_rectangle(x0,y0,x1,y1,fill="#000000",outline="white")
    canvas.create_rectangle(x0,y0,x0+(x1-x0)*app.rVal/255,y1,
    fill="#FF0000",outline="white")

    x0,y0,x1,y1 = app.gSlider
    canvas.create_rectangle(x0,y0,x1,y1,fill="#000000",outline="white")
    canvas.create_rectangle(x0,y0,x0+(x1-x0)*app.gVal/255,y1,
    fill="#00FF00",outline="white")

    x0,y0,x1,y1 = app.bSlider
    canvas.create_rectangle(x0,y0,x1,y1,fill="#000000",outline="white")
    canvas.create_rectangle(x0,y0,x0+(x1-x0)*app.bVal/255,y1,
    fill="#0000FF",outline="white")

    canvas.create_text(app.width/2, app.rSlider[1]-50, fill="white", 
    font=('Comic Sans MS', 30, 'bold italic'), text="Select color:")

    x0,y0,x1,y1 = app.colorDisplay
    canvas.create_rectangle(x0,y0,x1,y1,fill=app.playerColor,outline="white")

def settingsScreenSliderEvent(app, event):
    #If drag is within 3 sliders
    x0,y0,x1,y1 = app.rSlider
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        app.rVal = int((event.x-x0)/(x1-x0)*255)
    x0,y0,x1,y1 = app.gSlider
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        app.gVal = int((event.x-x0)/(x1-x0)*255)
    x0,y0,x1,y1 = app.bSlider
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        app.bVal = int((event.x-x0)/(x1-x0)*255)
    app.playerColor = "#"+hexRGB(app.rVal)+hexRGB(app.gVal)+hexRGB(app.bVal)

#Checks for if change name button has been clicked and updates name
def changeName(app, event):
    x0,y0,x1,y1 = app.nameChangeButton
    if (event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
        temp = app.getUserInput("Enter name:")
        while (len(temp) > 20 or len(temp) == 0):
            if (len(temp) == 0):
                temp =app.getUserInput("Name is too short, please enter again:")
            else:
                temp = app.getUserInput("Name is too long, please enter again:")
        app.playerName = temp

def drawBackButton(app, canvas):
    app.backButton.draw(canvas,"x",(0,-4))
    return

def backButtonEvent(app, event):
    if (app.gameOver):
        return
    if (app.backButton.checkBounds(event)):
        if (app.state != 3):
            app.state = 0
        else:
            app.warningWindow = True

def drawTutorialScreen(app, canvas):
    #Background
    canvas.create_rectangle(0,0,app.width,app.height,
    fill="#303030")