import math

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class country:
    def __init__(self, id, color):
        self.id = id #corresponding int on board
        self.color = color #fill color on board
        self.money = 10
        self.size = 1
        self.attackProportion = 0.3 #Must be between 0 and 1 inclusive
    
    #Logistic equation: f(x) = L/(1+e**-k(x-a))
    # x = ln(L/f(x)-1)/-k + a
    def updateMoney(self):
        #find current position on curve
        L = self.size*1000
        y = self.money
        k = 0.08
        a = 50
        x = math.log(L/y - 1) / -k + a
        #Update money
        x += 1
        self.money = roundHalfUp(L/(1+math.exp(-k*(x-a))))
