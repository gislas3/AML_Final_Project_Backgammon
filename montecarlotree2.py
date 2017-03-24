from __future__ import division
import numpy as np
import cPickle as pickle

class MonteCarloTree2:

    def __init__(self, start_state, C, ta, turn):
        self.global_C = C
        btemp = np.empty_like(start_state) #sigh....
    	btemp = np.copy(start_state)
    	btemp[btemp == 0] = 0
        bstring = str(btemp)
        #bstring = "+" + bstring
        try:
            with open("backgammon_mct3.p", "rb") as f:
                self.statedict = pickle.load(f)
    
        except pickle.UnpicklingError as e:
        # normal, somewhat expected
            print(traceback.format_exc(e))
            #return
        except Exception as e:
               # everything else, possibly fatal
            #print(traceback.format_exc(e))
            #return
            print "Dictionary not read"
            self.statedict = {bstring: {"total_visits": 0}}#corresponds to reward, visit, turn
            #continue
        self.visited = []
        self.added = 0
        self.its = 0
        self.toadd = ta #number of nodes to add at each iteration
        self.prevstate = bstring
        self.currturn = turn#self.statedict[bstring]["turn"] #n
        self.move = ()
        self.currstate = bstring#keep track of current state
        self.dlist = ()#keep track of the dice roll
        #self.turn = 1 #1 for own turn
    

    def reset(self, brd, turn):
    	btemp = np.empty_like(brd) #sigh....
    	btemp = np.copy(brd)
    	btemp[btemp == 0] = 0
        bstring = "+" + str(btemp) #should start from beginning - if change that, change this
        self.visited = []
        self.added = 0
        self.its = 0
        self.prevstate = bstring
        self.currturn = turn#self.statedict[bstring]["turn"]
        self.move = ()
        self.currstate = bstring
        self.dlist = ()

    def makeMove(self, listmoves, setfutstates, dicelist):
        self.dlist = dicelist
        if(self.statedict.has_key(self.currstate)): #state is in table of states
            #print self.statedict[self.currstate]
            #turn = self.statedict[self.currstate]["turn"]
            #totalvisits = self.statedict[self.currstate]["total_visits"]
            maxmove = ()
            if(self.statedict[self.currstate].has_key(dicelist)): #have seen dice roll before
                if(len(setfutstates) == len(self.statedict[self.currstate][dicelist])): #have tried every possible move from state and dice combination
                    maxval = -100000
                    maxmove = ()
                    for x in self.statedict[self.currstate][dicelist].keys(): #UCT step
                        templist = self.statedict[self.currstate][dicelist][x]
                        rewards = templist[0]
                        visits = templist[1]
                        tempval = rewards/visits + turn*self.global_C*np.sqrt(np.log(totalvisits)/visits)
                        if( abs(tempval) > maxval): #best seen so far
                            maxval = tempval
                            maxmove = x
                        # print "Max val: " + str(maxval)
                        #print "Vistis " + str(visits)
                        #print "total visits " + str(totalvisits)
                        #print "turn is " + str(turn)
                        #print "reward is " + str(rewards)
                else: #havent tried every possible move; select one have not tried before
                    thekeys = self.statedict[self.currstate][dicelist].keys()
                    for x in listmoves:
                        if(x not in thekeys): #choose first move seen that havent tried yet
                            maxmove = x
                            break
                    if(self.added < self.toadd): #havent added anything to the list yet; add this node
                        self.statedict[self.currstate][dicelist][x] = [0, 0]
    #self.added += 1 #increment number added
            else: #have not seen diceroll from current state previously
                ch = np.random.choice(len(listmoves))
                maxmove = listmoves[ch]
                if(self.added < self.toadd): #add the dice roll to the list
                    self.statedict[self.currstate][dicelist] = {maxmove : [0, 0]}
            #self.added += 1 #increment self.added
            self.move = maxmove        
            return maxmove
        else: #state is not in table (ie adding a new node)
            ch = np.random.choice(len(listmoves))
            maxmove = listmoves[ch]
            if(self.added < self.toadd): #havent added anything to table this iteration
                self.statedict[self.currstate] = {"total_visits": 0, "turn" : self.currturn} #add the new state to the dictionary
                self.statedict[self.currstate][dicelist] = {maxmove : [0, 0]} 
                self.added += 1 #increment added
            self.move = maxmove    
            return maxmove    
                
            

    # def makeMove(self, listmoves, dicelist):     #selection
    #     self.dlist = dicelist
    #     if(self.added >= 1): #return a randmoly chosen move (simluation)
    #         #print "T1"
    #         ch = np.random.choice(len(listmoves))
    #         move = listmoves[ch]
    #         return move
    #     elif(self.curr[4].has_key(dicelist)): #if contains the key, 
    #         #print "T2"
    #         parentvis = self.curr[2]
    #         parentturn = self.curr[3] 
    #         if(len(self.curr[4][dicelist]) == len(listmoves)): #has an edge with all the possible moves 
    #             maxval = -900 #should never be this small since minimum reward is -2
    #             maxmove = ()
    #             for x in self.curr[4][dicelist].keys():
    #                 tempdic = self.curr[4][dicelist][x].values()
    #                 rew = tempdic[0]
    #                 vis = tempdic[1]
    #                 trn = tempdic[2]
    #                 temp = trn*(rew/vis + self.globalC*np.sqrt(np.log(parentvis)/vis))
    #                 if(temp > maxval):
    #                     maxval = temp
    #                     maxmove = x            
    #         else:
    #             for x in listmoves:
    #                 if(x not in self.curr[4][dicelist]): #pick an action haven't tried yet
    #                     self.curr[4][dicelist][x] = ["", 0, 0, -parentturn, {}] #initialize empty for next state
    #                     maxmove = x
    #                     self.added += 1
    #                     break
    #         self.curr = self.curr[4][self.dlist][maxmove] #change curr to point to the next state
    #         self.prevmove = maxmove            
    #         return maxmove    
    #     else:
    #         #print "T3"
    #         ch = np.random.choice(len(listmoves))
    #         move = listmoves[ch]
    #         parentturn = self.curr[3]
    #         self.curr[4][dicelist] = {}
    #         self.curr[4][dicelist][move] = ["", 0, 0, -parentturn, {}]
    #         #print "INCREMENTING ADDED"
    #         #print "SELF.ADDED IS " + str(self.added)
    #         self.added += 1
    #         #print "SELF.ADDED IS NOW " + str(self.added) 
    #         self.curr = self.curr[4][self.dlist][move] #change curr to point to the next state
    #         self.prevmove = move
    #         return move


    # def nextstate(self, pbrd, legal): #expansion 
    #     if(self.its == 0):
    #         self.visited.append(self.prev)   
    #     if(self.added <= 1):
    #         if(not legal): #makeMove didnt get called because there were no available moves
    #             parentturn = self.prev[3]
    #             self.curr[4][self.dlist][self.prevmove] = [str(pbrd), 0, 0, -parentturn, {}]
    #         else:
    #             self.prev[4][self.dlist][self.prevmove][0] = str(pbrd)
    #         self.visited.append(self.curr)
    #         if(self.added == 1):
    #             self.added += 1

    #         self.prev = self.curr    
    #     self.its += 1 

    def nextstate(self, pbrd, legal):
    	btemp = np.empty_like(pbrd) #sigh....
    	btemp = np.copy(pbrd)
    	btemp[btemp == 0] = 0
    	bstring = str(btemp)
        if(self.statedict.has_key(self.currstate) and self.statedict[self.currstate].has_key(self.dlist) and self.statedict[self.currstate][self.dlist].has_key(self.move)): #add this to the list of moves to update when backpropagating
            self.visited.append((self.currstate, self.dlist, self.move)) #append a tuple so know what to update
            if(self.added == self.toadd): #added all nodes to be added for this simulation
                self.added += 1
        self.prevstate = self.currstate
        if(self.currturn == 1):
            self.currstate = "-" + bstring
        else:
            self.currstate = "+" + bstring
        self.currturn = -self.currturn
        self.move = ()
        self.dlist = ()
        self.its += 1


    def backprop(self, reward): #backpropagation
        for x in range(len(self.visited)-1, -1, -1):
            if(self.visited[x][2] != ()): #dont count for where you had no possible moves
                self.statedict[self.visited[x][0]]["total_visits"] += 1
            
                self.statedict[self.visited[x][0]][self.visited[x][1]][self.visited[x][2]][0] += reward #increment the reward
                self.statedict[self.visited[x][0]][self.visited[x][1]][self.visited[x][2]][1] += 1 #incremen the number of times the node was chosen
             
             #print "self.dict is: " + str(self.statedict)
        print "self.its is: " + str(self.its)

    def savedict(self):
        pickle.dump( self.statedict, open( "backgammon_mct3.p", "wb" ) )

