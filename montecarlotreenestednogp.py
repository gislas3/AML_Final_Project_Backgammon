from __future__ import division
import numpy as np
import cPickle as pickle

class MonteCarloTreeNestedNoGP:

    def __init__(self, start_state, C, ta):
        self.global_C = C
        btemp = np.empty_like(start_state) #sigh....
    	btemp = np.copy(start_state)
    	btemp[btemp == 0] = 0
        #btemp[btemp < -2] = -2 # should i do this....
        bstring = str(btemp)
        try:
            with open("backgammon_mct_nest_nogp.p", "rb") as f:
                self.root = pickle.load(f)
    
        except pickle.UnpicklingError as e:
        # normal, somewhat expected
            print(traceback.format_exc(e))
            #return
        except Exception as e:
               # everything else, possibly fatal
            #print(traceback.format_exc(e))
            #return
            print "Dictionary not read"
            self.root = {bstring: {"total_visits": 0, "turn" : 1}}#corresponds to reward, visit, turn
            #continue
        self.visited = []
        self.added = 0
        self.its = 0
        self.toadd = ta #number of nodes to add at each iteration
        self.prev = None
        #self.prev_prev = None
        self.currstate = bstring
        self.prevstate = ""
        #self.prev_prev_state = ""
        self.currturn = self.root[bstring]["turn"] #n
        self.move = ()
        self.curr = self.root
        self.dlist = ()#keep track of the dice roll
        #self.turn = 1 #1 for own turn
    

    def reset(self, brd):
    	btemp = np.empty_like(brd) #sigh....
    	btemp = np.copy(brd)
    	btemp[btemp == 0] = 0
        bstring = str(btemp) #should start from beginning - if change that, change this
        self.visited = []
        self.added = 0
        self.its = 0
        #self.prev_prev = None
        self.currstate = bstring
        self.prevstate = ""
        #self.prev_prev_state = ""
        self.currturn =self.root[bstring]["turn"]
        self.move = ()
        self.curr = self.root
        self.prev = None
        self.dlist = ()
            

    def makeMove(self, listmoves, dicelist):     #selection
        self.dlist = dicelist
        if(self.added >= self.toadd): #return a randmoly chosen move (simulation)
           # print "In Random Section"
            ch = np.random.choice(len(listmoves))
            move = listmoves[ch]
            return move   
        elif(self.curr[self.currstate].has_key(self.dlist)): #if have seen the dice roll before 
           # print "Current State has the diceroll"
            parentvis = self.curr[self.currstate][self.dlist]["d_visits"]
            parentturn = self.curr[self.currstate]["turn"] 
            maxmove = ()
            if(parentvis >= len(listmoves)): #have seen all possible moves 
               # print "Have tried all moves from current dice roll"
                maxval = -900 #should never be this small since minimum reward is 0
                maxmove = ()
                for x in self.curr[self.currstate][self.dlist].keys():
                    if(x != "d_visits"):
                        temp = self.curr[self.currstate][self.dlist][x]
                        k = temp.keys()[0] #need this to access the value of the state of the node
                        rew = temp[k]["val"]
                        vis = temp[k]["visits"]
                        val = parentturn* (rew/vis + self.global_C*np.sqrt(np.log(parentvis)/vis))
                       # print "Move is " + str(x)
                       # print "Reward is " + str(rew)
                        #print "Val is " + str(val)
                        if(val > maxval):
                            maxval = val
                            maxmove = x       
            else: #have not seen all possible moves from this dice roll
                for x in listmoves: #pick a node have not visited yet
                    if (not self.curr[self.currstate][self.dlist].has_key(x)):
                        maxmove = x
                        break 
            if(maxmove == ()):
                print "WHAT THE FUCK"
                sys.exit(1)                      
            self.move = maxmove    
            return maxmove    
        else: #havent seen dice roll before - choose a random node from the list of possible moves
            ch = np.random.choice(len(listmoves)) #choose a node at random
            maxmove = listmoves[ch]
            self.move = maxmove
            return maxmove


    def nextstate(self, pbrd, legal, d2, m=()): #expansion - need to add part about race, maybe about opp 2... initialize current node as previous node
        if(self.added < self.toadd): #can add a node
            #print self.currstate
            #print self.move
            #print self.dlist
            btemp = np.empty_like(pbrd) #sigh....
            btemp = np.copy(pbrd)
            btemp[btemp == 0] = 0
            bstring = str(btemp) #should start from beginning - if change that, change this
            #print bstring
            if(not legal):
            	self.dlist = d2
            	self.move = (-1, -1) #dummy move to next state
            elif(m != ()):
                self.dlist = d2
                self.move = m
            if(self.curr[self.currstate].has_key(self.dlist)): #has seen dice roll before
                if(not self.curr[self.currstate][self.dlist].has_key(self.move)): #have not performed move before - add node
                    self.curr[self.currstate][self.dlist][self.move] = {bstring : {"visits" : 0, "turn" : -self.currturn, "val":0}} #add the node
                    self.added += 1
                if(self.curr[self.currstate][self.dlist].has_key(self.move) and self.curr[self.currstate][self.dlist][self.move].keys()[0] != bstring): #error check     
                    print "ERROR"
                    print self.currstate
                    print self.move
                    print self.curr[self.currstate][self.dlist][self.move].keys()[0]
                    print bstring
                    for z in self.visited:
                        print "State: " + str(z[1])
                        print "Prev: " + str(z[3])
                        print "Roll: " + str(z[4])
                        print " "
            else: #have not seen dice roll before - add dice roll, add move node
                self.curr[self.currstate][self.dlist] = {"d_visits" : 0}
                self.curr[self.currstate][self.dlist][self.move] = {bstring : {"visits" : 0, "turn": -self.currturn, "val":0}}
                self.added += 1    
            #if(self.its > 0):         
             #   self.prev_prev = self.prev
              #  self.prev_prev_state = self.prevstate
            self.prev = self.curr
            self.prevstate = self.currstate
            self.curr = self.curr[self.currstate][self.dlist][self.move]
            self.currstate = bstring
            self.visited.append([self.curr, self.currstate, self.prev, self.prevstate, self.dlist])
        self.currturn = -self.currturn
        self.its += 1        




    def backprop(self, reward, brd, d2): #backpropagation
        if(self.added < self.toadd): #reached terminal state without adding a node - add this node if doesnt exist
            self.dlist = d2
            self.nextstate(brd, True)
        for x in range(len(self.visited)-1, -1, -1):
            tempd  = self.visited[x][0]
            tempk = self.visited[x][1]
            tempd[tempk]["visits"] += 1
            tempd[tempk]["val"] += reward
            tempp = self.visited[x][2]
            tempp[self.visited[x][3]][self.visited[x][4]]["d_visits"] += 1
        #print "self.root is: " + str(self.root)
        print "self.its is: " + str(self.its)

    def savedict(self):
        pickle.dump( self.root, open( "backgammon_mct_nest_nogp150000.p", "wb" ) )
        print "Dictionary saved!"

