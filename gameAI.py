import random

#target = id of country that the function is finding neighbours for
def findNeighbours(app,target):
    d = dict()
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if (app.board[i][j] != target and
            not i-1 < 0 and app.board[i-1][j] == target or
            not i+1 >= len(app.board) and app.board[i+1][j] == target or
            not j-1 < 0 and app.board[i][j-1] == target or
            not j+1 >= len(app.board[0]) and app.board[i][j+1] == target):
                d[app.board[i][j]] = d.get(app.board[i][j],0) + 1
    return d

def runAi(app, agent):
    #Find weakest neighbour
    d = findNeighbours(app, agent.id)
    #If there is still empty space and agent has some threshold of money
    if (-1 in d):
        commit = int(5.0*d[-1])+1
        if (agent.money > random.randint(agent.size*10,agent.size*30) and
            agent.money > commit):
            agent.attackInit(app,-1,commit) #Exact amount for one layer
        return
    
    #Find smallest neighbour
    smallest = None 
    for i in d:
        if (smallest == None or app.dict[i].money < app.dict[smallest].money):
            smallest = i
    
    #If the smallest neighbour is signifcantly smaller
    density = app.dict[smallest].money/app.dict[smallest].size
    if (app.dict[smallest].money < agent.money*agent.aggro and
        int(d[smallest]*density)+1 <= agent.money):
        agent.attackInit(app,smallest,int(d[smallest]*density)+1)
        return

    # if attack threshold not met
    if (agent.money/agent.size/1000 < agent.threshold):
        return
    
    #If the difference between the to countries isn't too big, or growth has stopped
    if (app.dict[smallest].money/(agent.money*agent.aggro) <= agent.tooBig
    or agent.money >= agent.size * 1000):
        agent.attackInit(app,smallest,agent.money*agent.aggro)

