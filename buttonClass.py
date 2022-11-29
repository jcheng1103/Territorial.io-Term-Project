class button:
    def __init__(self,bounds,fill,outline,font):
        self.bounds = bounds #Tuple of the bounds of the button
        self.fill = fill
        self.outline = outline
        self.font = font
    
    def checkBounds(self, event):
        x0,y0,x1,y1 = self.bounds
        return (event.x > x0 and event.x < x1
        and event.y > y0 and event.y < y1)

    def draw(self,canvas,text="",textOffset=(0,0)):
        x0,y0,x1,y1 = self.bounds
        canvas.create_rectangle(x0,y0,x1,y1,
        outline=self.outline,fill=self.fill)
        canvas.create_text((x0+x1)/2+textOffset[0],(y0+y1)/2+textOffset[1], 
        text=text, fill='white', font=self.font)