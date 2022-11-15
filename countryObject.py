
class country:
    def __init__(self, id, color):
        self.id = id #corresponding int on board
        self.color = color #fill color on board
        self.money = 10
        self.size = 1
        self.attackProportion = 0.3 #Must be between 0 and 1 inclusive
    
    def __str__(self):
        return str(self.id)+' '+str(self.color)
