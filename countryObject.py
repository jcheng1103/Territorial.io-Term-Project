import math
import decimal
from collections import deque
import copy
import random

def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class country:
    def __init__(self, id, color, name):
        self.id = id #corresponding int on board
        self.color = color #fill color on board
        self.name = name
        self.money = 100
        self.size = 1
        self.attackProportion = 0.3 #Must be between 0 and 1 inclusive
        self.growthRate = 0.0
        self.attacks = [] #(queue, who is being attacked, money, original money)

        #For the bots
        self.threshold = random.randint(30,100)/100 #What threshold bots attack at
        self.tooBig = random.randint(3,10) #Bots won't attack if the difference is too big
        self.aggro = random.randint(10,30)/100 #How much bots attack with

    
    #Logistic equation: f(x) = L/(1+e**-k(x-a))
    # x = ln(L/f(x)-1)/-k + a
    def updateMoney(self):
        #find current position on curve
        L = self.size*1000
        y = self.money
        k = 0.05
        a = 100
        x = 0
        if (y < L):
            x = math.log(L/y - 1) / -k + a
            x += 1
            self.growthRate = L/(1+math.exp(-k*(x-a)))/self.money
            self.money = roundHalfUp(L/(1+math.exp(-k*(x-a))))
        else:
            self.growthRate = 1.0
        self.money += self.size
        self.money = min(self.size*1500, self.money)
    
    def isNeighbour(self, app, id, i, j):
        if (app.board[i][j] == id and
        not i-1 < 0 and app.board[i-1][j] == self.id or
        not i+1 >= len(app.board) and app.board[i+1][j] == self.id or
        not j-1 < 0 and app.board[i][j-1] == self.id or
        not j+1 >= len(app.board[0]) and app.board[i][j+1] == self.id):
            return True
        return False

    #initializing queue for dfs
    def attackInit(self, app, id, committed):
        #If the country is already being attacked
        for i in range(len(self.attacks)):
            if (self.attacks[i][1] == id):
                temp = self.attacks[i]
                self.attacks[i] = (temp[0],temp[1],temp[2]+committed,
                temp[3]+committed)
                return

        self.money -= committed
        searchQueue = deque()
        neighbours = 0
        density = 1.0
        if (id != -1):
            density = app.dict[id].money/app.dict[id].size
        for i in range(len(app.board)):
            for j in range(len(app.board[0])):
                #If current tile == id and borders the attacking country
                if (app.board[i][j] == id and self.isNeighbour(app,id,i,j)):
                    neighbours += 1
                    app.board[i][j] = -2
        #If committed troops are insufficient for conquering
        if (neighbours * density > committed):
            #Reset game board to original state
            for i in range(len(app.board)):
                for j in range(len(app.board[0])):
                    if (app.board[i][j] == -2):
                        app.board[i][j] = id
            if (id != -1):
                    app.dict[id].money -= committed
            return
        for i in range(len(app.board)):
            for j in range(len(app.board[0])):
                #If current tile == id and borders the attacking country
                if (app.board[i][j] == -2):
                    app.board[i][j] = self.id
                    searchQueue.append((i,j))
        self.size += len(searchQueue)
        if (id != -1):
            app.dict[id].size -= len(searchQueue)
            app.dict[id].money -= roundHalfUp(len(searchQueue)*density)
        self.attacks.append((searchQueue, id,
                committed-roundHalfUp(len(searchQueue)*density), committed))
        
    def incrementAttacks(self, app):
        j = 0
        for i in self.attacks:
            id = i[1]
            if (id != -1 and (id not in app.dict or app.dict[id].size <= 0)):
                self.attacks.pop(j)
                continue
            #Search for next depth
            searchQueue = copy.copy(i[0])
            density = 1.0
            if (id != -1):
                density = app.dict[id].money/app.dict[id].size
            newlyAdded = []
            money = i[2]
            #Find neighbours to all tiles in searchQueue
            while (len(searchQueue) > 0):
                front = searchQueue.popleft()
                if (not front[0]-1 < 0 and app.board[front[0]-1][front[1]]==id):
                    app.board[front[0]-1][front[1]] = self.id
                    newlyAdded.append((front[0]-1,front[1]))
                if (not front[0]+1 >= len(app.board) and
                app.board[front[0]+1][front[1]] == id):
                    app.board[front[0]+1][front[1]] = self.id
                    newlyAdded.append((front[0]+1,front[1]))
                if (not front[1]-1 < 0 and app.board[front[0]][front[1]-1]==id):
                    app.board[front[0]][front[1]-1] = self.id
                    newlyAdded.append((front[0],front[1]-1))
                if (not front[1]+1 >= len(app.board[0]) and
                app.board[front[0]][front[1]+1] == id):
                    app.board[front[0]][front[1]+1] = self.id
                    newlyAdded.append((front[0],front[1]+1))
                #If the attack has run out of money
                if (len(newlyAdded)*density>money):
                    break
            #If the attack has run out of money
            if (len(newlyAdded)*density>money):
                #Replace modified tiles
                for i in newlyAdded:
                    app.board[i[0]][i[1]] = id
                self.attacks.pop(j)
                if (id != -1):
                    app.dict[id].money -= money
            elif (len(newlyAdded) == 0):
                #Attack has terminated because there is no land to conquer
                #Remaining money is refunded
                self.money += i[2]
                self.attacks.pop(j)
            else:
                #Update queue
                self.attacks[j] = (deque(newlyAdded), id,
                money-roundHalfUp(len(newlyAdded)*density), i[3])
                self.size += len(newlyAdded)
                if (id != -1):
                    app.dict[id].size -= len(newlyAdded)
                    app.dict[id].money -= roundHalfUp(len(newlyAdded)*density)
            j += 1


