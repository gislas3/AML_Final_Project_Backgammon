import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
from docopt import docopt

class BackgammonTestPlayer: #will always see board from white perspective (moves just flipped)
    def __init__(self, brd, bw):
        self.black_or_white = bw
        self.board = np.zeros(len(brd))
        self.board = np.copy(brd)
        if(self.black_or_white == "Black"):
            self.updateBoard(self.board)
        self.inds = np.where(self.board > 0)[0]    
        self.listmoves1 = []
        self.listmoves2 = []
        self.maxlen = 0
        self.maxroll = 0
        self.typ = "Test"
        self.setstates = set()
        self.rep = True #added

    def reset(self, brd):
        self.board = np.zeros(len(brd))
        self.board = np.copy(brd)
        if(self.black_or_white == "Black"):
            self.updateBoard(self.board)
        self.inds = np.where(self.board > 0)[0]    
        self.listmoves1 = []
        self.listmoves2 = []
        self.maxlen = 0
        self.maxroll = 0
        self.setstates = {}
        self.rep = True #added

    def updateBoard(self, brd):
        if(self.black_or_white == "Black"):
            self.board[0:24] = brd[23::-1]
            self.board[24:26] = brd[25:23:-1]
            self.board[26:28] = brd[27:25:-1]
            self.board = -1*self.board
        else:
            self.board = brd    
        self.inds = np.where(self.board > 0)[0]
        self.maxlen = 0

        #self.bearoff = (np.argmax(self.inds) <= 5 or np.argmax(self.inds) == 25)  and np.argmin(self.inds) >= 0    


    def removeMoves1(self, thelen):
        for x in self.listmoves1:
            if(len(x) <= thelen):
                self.listmoves1.remove(x)
            else:
                break

    def removeMoves2(self, thelen):
        for x in self.listmoves2:
            if(len(x) <= thelen):
                self.listmoves2.remove(x)
            else:
                break

    def makeMove(self):
        
    
    
    
    def recur_moves1(self, dice_roll, boardcopy, indscopy, cand, it):
        #print "board copy is: " +  str(boardcopy)
        #print "indscopy is: " + str(indscopy)
        #print "cand is: " + str(cand)
        #print "dice_roll is: " + str(dice_roll)
        if(len(dice_roll) == 0 or len(indscopy) == 0): #finished recursion for one move
            if(len(cand) != 0 and len(cand) >= self.maxlen):
                if(len(cand) == 2 and x[1] - x[0] > self.maxroll): #changed abs(x[0] - x[1]) to x[1] - x[0]
                    self.maxroll = x[1] - x[0]
                    if(self.maxroll != 0):
                       self.removeMinVals1()
                #if(boardcopy not in self.setstates): #this makes program much slower
                
                self.listmoves1.append(cand)
                self.dictstates[cand] = str(boardcopy)

                if(len(cand) > self.maxlen): #only add moves that use maximal amt of dice
                    #print cand
                    if(self.maxlen != 0):
                        self.removeMoves1(self.maxlen) 
                    self.maxlen = len(cand) #track the length of the candidate moves
                #print "ADDED TO LIST"
            #boardcopy = np.copy(self.boardarray)
            #indscopy = np.copy(self.inds)                    
            return
        if(boardcopy[27] != 0): #first check if have a piece in the middle of the board
            d1 = dice_roll[0]
            bc = np.empty_like(boardcopy)
            bc[:] = boardcopy[:]
            candadd = ()
            if(bc[d1-1] >= -1):
                #cand = cand + (27, d1)
                candadd = (27, d1-1)
                bc[27] -= 1
                if(bc[d1-1] == -1): #move results in hitting a piece off the board
                    bc[d1-1] += 1
                    bc[26] -= 1
                bc[d1-1] += 1
                indscopy2 = np.where(bc > 0)[0] #changed - added two indents
                self.recur_moves1(dice_roll[1:], bc, indscopy2, cand + candadd) #changed - added two indents
            else: #added
                if(len(dice_roll) == 2): #added - check starting from smalle
                    if(it == 1): #added - if on 2nd iteration and lower dice blocked, just exit, because already tried higher dice
                        return
                    self.recur_moves1(dice_roll[::-1], boardcopy, indscopy, cand) #added
                    self.rep = False #added
                else: #should only reach here if had two pieces inside, got one out, then couldnt get second one out
                    self.recur_moves1(dice_roll[1:], boardcopy, indscopy, cand) #added
                    self.rep = False #added
        else:
            d1 = dice_roll[0]
            temparray = np.where(boardcopy > 0)[0]
            tempminind = np.min(temparray)
            tempmaxind = np.max(temparray)
            #print "tempminind is: " + str(tempminind)
            #print "tempmaxind is:" + str(tempmaxind)
            tempbear = tempmaxind <= 24  and tempminind >= 18
            #print "tempbear is: " + str(tempbear)
            bc = np.empty_like(boardcopy)
            bc[:] = boardcopy[:]
            if(indscopy[0] < 24 and tempbear and (indscopy[0] + d1 == 24 or (indscopy[0] == tempminind and tempminind + d1 > 24))):
                #cand = cand + (indscopy[0], 24)
                #print "HERE"
                candadd = (indscopy[0], 24)
                bc[indscopy[0]] -= 1
                bc[24] += 1
                indscopy2 = np.where(bc > 0)[0]
                self.recur_moves1(dice_roll[1:], bc, indscopy2, cand + candadd)
                self.recur_moves1(dice_roll[1:], bc, indscopy2[1:], cand)
            elif(indscopy[0] + d1 < 24 and bc[indscopy[0] + d1] >= -1):
                #candadd = cand + (indscopy[0], indscopy[0] + d1 )
                candadd = (indscopy[0], indscopy[0] + d1 )
                bc[indscopy[0]] -= 1
                if(bc[indscopy[0] + d1] == -1): #move results in hitting a piece off the board
                    bc[indscopy[0] + d1] += 1
                    bc[26] -=1
                bc[indscopy[0] + d1] += 1
                indscopy2 = np.where(bc > 0)[0]
                self.recur_moves1(dice_roll[1:], bc, indscopy2, cand + candadd)
                self.recur_moves1(dice_roll[1:], bc, indscopy2[1:], cand)        
            self.recur_moves1(dice_roll, boardcopy, indscopy[1:], cand)            

    def removeMinVals1(self):
        for x in self.listmoves1:
            if(x[1] - x[0] < self.maxroll): #changed abs(x[0] - x[1]) to x[1] - x[0]
                self.listmoves1.remove(x)
            else:
                break

    def removeDuplicates(self): #added
        tempstates = set()
        for x in self.listmoves1:
            if x in tempstates:
                self.listmoves1.remove(x)
            tempstates.add(x)

    def findreverses(self, dice_roll, boardcopy, indscopy, cand): #added - method to avoid separate actions resulting in same state
        if(boardcopy[27] != 0): #added -
            self.recur_moves1(dice_roll, boardcopy, indscopy, cand, 1) #start with minimum roll (look at all possible moves from there)
            if(self.boardarray[dice_roll[0]-1] >= -1 and self.boardarray[dice_roll[1]-1] != -1): #lower wasnt blocked and first couldnt have been a hit and run
                self.listmoves1.remove((27, dice_roll[0] - 1, dice_roll[0]-1, dice_roll[0]-1+dice_roll[1])) #remove
                del self.dictstates[(27, dice_roll[0] - 1, dice_roll[0]-1, dice_roll[0]-1+dice_roll[1])]
        elif(self.maxlen == 2): #must try moving the second dice first to see if can use both dice
            self.recur_moves1(dice_roll, boardcopy, indscopy, cand, 1) #start with minimum roll (look at all possible moves from there)
            if(self.maxlen == 2): #maxlength is still 2, might have duplicates
                self.removeDuplicates() #hopefully this rarely gets called
        else:
            minind = np.min(indscopy)
            minind2 = np.min(indscopy[np.where(indscopy != minind)])
            if(minind < 18 and minind2 >= 18 and self.boardarray[minind] == 1 and (self.boardarray[minind + dice_roll[0]] >= 18 or self.boardarray[minind + dice_roll[1]] >= 18)): #possiblity of bearing off; was too complicated to do by hand
                self.recur_moves1(dice_roll, boardcopy, indscopy, cand)
            else:
                for x in range(0, len(indscopy)):
                    if(indscopy[x] + dice_roll[0] + dice_roll[1] < 24 and (boardarray[indscopy[x] + dice_roll[0]] == -1 or boardarray[indscopy[x] + dice_roll[0]] <= -2) and boardarray[indscopy[x] + dice_roll[0] + dice_roll[1]] >= -1): #should only add same piece moves where one piece is blocked or can do a hit and run
                        self.listmoves1.append(indscopy[x], indscopy[x] + dice_roll[0], indscopy[x]+dice_roll[0], indscopy[x]+dice_roll[0]+dice_roll[1])
    
    def getpossibleMoves1(self, dice_roll):
        tempboard = np.copy(self.board)
        tempinds = np.copy(self.inds)
        self.listmoves1 = []
        self.dictstates = {}
        self.maxlen = 0
        self.maxroll = 0
        self.rep = True
        cand = ()
        #print self.board
        self.recur_moves1(dice_roll, tempboard, tempinds, cand, 0)
        if(dice_roll[0] != dice_roll[1] and self.rep): #added the self.rep part
            cand = ()
            tempboard = np.copy(self.board)
        #self.recur_moves(dice_roll[1::-1], tempboard, tempinds, cand) #changed- commented out
            self.findreverses(dice_roll[::-1], tempboard, tempinds, cand) #added
        return self.listmoves1
            



        def recur_moves2(self, dice_roll, boardcopy, indscopy, cand, it):
        #print "board copy is: " +  str(boardcopy)
        #print "indscopy is: " + str(indscopy)
        #print "cand is: " + str(cand)
        #print "dice_roll is: " + str(dice_roll)
        if(len(dice_roll) == 0 or len(indscopy) == 0): #finished recursion for one move
            if(len(cand) != 0 and len(cand) >= self.maxlen):
                if(len(cand) == 2 and x[1] - x[0] > self.maxroll): #changed abs(x[0] - x[1]) to x[1] - x[0]
                    self.maxroll = x[1] - x[0]
                    if(self.maxroll != 0):
                       self.removeMinVals2()
                #if(boardcopy not in self.setstates): #this makes program much slower
                
                self.listmoves2.append(cand)
                #    self.setstates.add(boardcopy)

                if(len(cand) > self.maxlen): #only add moves that use maximal amt of dice
                    #print cand
                    if(self.maxlen != 0):
                        self.removeMoves2(self.maxlen) 
                    self.maxlen = len(cand) #track the length of the candidate moves
                #print "ADDED TO LIST"
            #boardcopy = np.copy(self.boardarray)
            #indscopy = np.copy(self.inds)                    
            return
        if(boardcopy[27] != 0): #first check if have a piece in the middle of the board
            d1 = dice_roll[0]
            bc = np.empty_like(boardcopy)
            bc[:] = boardcopy[:]
            candadd = ()
            if(bc[d1-1] >= -1):
                #cand = cand + (27, d1)
                candadd = (27, d1-1)
                bc[27] -= 1
                if(bc[d1-1] == -1): #move results in hitting a piece off the board
                    bc[d1-1] += 1
                    bc[26] -= 1
                bc[d1-1] += 1
                indscopy2 = np.where(bc > 0)[0] #changed - added two indents
                self.recur_moves2(dice_roll[1:], bc, indscopy2, cand + candadd) #changed - added two indents
            else: #added
                if(len(dice_roll) == 2): #added - check starting from smalle
                    if(it == 1): #added - if on 2nd iteration and lower dice blocked, just exit, because already tried higher dice
                        return
                    self.recur_moves2(dice_roll[::-1], boardcopy, indscopy, cand) #added
                    self.rep = False #added
                else: #should only reach here if had two pieces inside, got one out, then couldnt get second one out
                    self.recur_moves2(dice_roll[1:], boardcopy, indscopy, cand) #added
                    self.rep = False #added
        else:
            d1 = dice_roll[0]
            temparray = np.where(boardcopy > 0)[0]
            tempminind = np.min(temparray)
            tempmaxind = np.max(temparray)
            #print "tempminind is: " + str(tempminind)
            #print "tempmaxind is:" + str(tempmaxind)
            tempbear = tempmaxind <= 24  and tempminind >= 18
            #print "tempbear is: " + str(tempbear)
            bc = np.empty_like(boardcopy)
            bc[:] = boardcopy[:]
            if(indscopy[0] < 24 and tempbear and (indscopy[0] + d1 == 24 or (indscopy[0] == tempminind and tempminind + d1 > 24))):
                #cand = cand + (indscopy[0], 24)
                #print "HERE"
                candadd = (indscopy[0], 24)
                bc[indscopy[0]] -= 1
                bc[24] += 1
                indscopy2 = np.where(bc > 0)[0]
                self.recur_moves2(dice_roll[1:], bc, indscopy2, cand + candadd)
                self.recur_moves2(dice_roll[1:], bc, indscopy2[1:], cand)
            elif(indscopy[0] + d1 < 24 and bc[indscopy[0] + d1] >= -1):
                #candadd = cand + (indscopy[0], indscopy[0] + d1 )
                candadd = (indscopy[0], indscopy[0] + d1 )
                bc[indscopy[0]] -= 1
                if(bc[indscopy[0] + d1] == -1): #move results in hitting a piece off the board
                    bc[indscopy[0] + d1] += 1
                    bc[26] -=1
                bc[indscopy[0] + d1] += 1
                indscopy2 = np.where(bc > 0)[0]
                self.recur_moves2(dice_roll[1:], bc, indscopy2, cand + candadd)
                self.recur_moves2(dice_roll[1:], bc, indscopy2[1:], cand)        
            self.recur_moves2(dice_roll, boardcopy, indscopy[1:], cand)   

    def getpossibleMoves2(self, dice_roll):
        tempboard = np.copy(self.board)
        tempinds = np.copy(self.inds)
        self.listmoves2 = []
        #self.maxlen = 0
        #self.maxroll = 0
        #self.rep = True
        cand = ()
        #print self.board
        self.recur_moves2(dice_roll, tempboard, tempinds, cand, 0)
        if(dice_roll[0] != dice_roll[1]): #added the self.rep part
            cand = ()
            self.recur_moves2(dice_roll, tempboard, tempinds, cand, 0)
        return self.listmoves2
            
    
