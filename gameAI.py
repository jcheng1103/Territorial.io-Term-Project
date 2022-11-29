import random

def findNeighbours(app,target):
    s = set()
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if (app.board[i][j] != target,
            not i-1 < 0 and app.board[i-1][j] == id or
            not i+1 >= len(app.board) and app.board[i+1][j] == id or
            not j-1 < 0 and app.board[i][j-1] == id or
            not j+1 >= len(app.board[0]) and app.board[i][j+1] == id):
                s.add(app.board[i][j])
    return s

def runAi(app, agent):
    #Find weakest neighbour
    s = findNeighbours(app, agent)
    #If there is still empty space and agent has some threshold of money
    if (-1 in s):
        if (agent.money > random.randint(agent.size*10,agent.size*50)):
            agent.attackInit(app,-1,int(agent.money*agent.aggro))
        return

    #threshold not met
    if (agent.money/agent.size/1000 < agent.threshold):
        return
    
    #Find smallest neighbour
    smallest = None 
    for i in s:
        if (smallest == None or app.dict[i].money < app.dict[smallest].money):
            smallest = i
    
    #If the difference between the to countries isn't too big, or growth has stopped
    if (app.dict[smallest].money/(agent.money*agent.aggro) <= agent.tooBig
    or agent.money >= agent.size * 1000):
        agent.attackInit(app,smallest,int(agent.money*agent.aggro))

