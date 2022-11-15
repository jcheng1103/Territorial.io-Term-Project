
class country:
    def __init__(self, id, color):
        self.id = id #corresponding int on board
        self.color = color #fill color on board
        self.money = 0
        self.size = 0
    
    def __str__(self):
        return str(self.id)+' '+str(self.color)
