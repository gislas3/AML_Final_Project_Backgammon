#!/usr/bin/env python
# -*- coding: utf-8 -*-

# README !!!
# This version doesn't use a graphical interface and was tested under Python 2.7.13; since the code uses the python 2 print function, it will likely not work in python 3
# You need to install numpy and docopt for the program to work
# This can be done with the following commands (in a terminal in a Linux OS):
#   If running Python 2:
#    pip install numpy
#    pip install docopt
# Upon startup, the game will ask whether you want to play two human players (for debugging the environment), one human and once computer, or two computer players()
# For this, 'pip' (or pip3) needs to be installed (which is usually already the case). If not, you can do it by installing classically python-dev (for pip) or python3-pip (for pip3), with your usual OS library management tool (yum, aptitude, apt-get, synaptic, ...).

"""
A simple backgammon interface for developing an intelligent AI backgammon playing agent

created by Gregory ISLAS and Olivier SALAUN  
            
Usage: backgammon [-d <flag>] [-n <int>] [-e <int>]

Options:
-h --help      Show the description of the program
-d <flag> --display <flag>  a flag for activating the display [default: 1]
-n <int> --n_humans <int>  an integer for the number of human players [default: 1]
-e <int> --max_n_iteration <int>  the maximum number of iterations [default: 1000]
"""


import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
import time
from docopt import docopt
import backgammonboard
import backgammonhumanplayer
import backgammonaiplayer
import montecarlotreenested

class Environment():
    def __init__(self, player1type, player2type, vb):
        self.board = backgammonboard.BackgammonBoard()
        self.boardarray = self.board.board
        self.mct = None
        if(player1type == "Comp"):
            self.player1 = backgammonaiplayer.BackgammonAIPlayer(self.boardarray, "White")
        else:
            self.player1 = backgammonhumanplayer.BackgammonHumanPlayer(self.boardarray, "White")
        if(player2type == "Comp"):
            self.player2 = backgammonaiplayer.BackgammonAIPlayer(self.boardarray, "Black")
        else:
            self.player2 = backgammonhumanplayer.BackgammonHumanPlayer(self.boardarray, "Black")
        #initialize the MCT structure if playing with a computer
        self.white_inds = np.where(self.boardarray > 0)[0]
        self.black_inds = np.where(self.boardarray < 0)[0]
        self.white_bearoff = False
        self.black_bearoff = False    
        self.d1 = -1
        self.d2 = -1
        sd1  = np.random.randint(1, 7)
        sd2 = np.random.randint(1, 7)
        #sd1 = 6 #for debugging
        #sd2 = 3 #for debugging
        self.fst = -1
        while(sd1 == sd2):
            sd1 = np.random.randint(1, 7)
            sd2 = np.random.randint(1, 7)
        firststr = ""    
        if(sd1 > sd2): #white goes first    
            self.turn = 0
            self.fst = 1
            firststr = "White goes first!"
            if("Comp" in (player1type, player2type)): #for debugging
                self.mct = montecarlotreenested.MonteCarloTreeNested(self.player1.board, np.sqrt(2), 1) #for debugging
                #self.player1.setTurn(1)
                #self.player2.setTurn(-1)
        else: #black goes first
            self.turn = 1
            self.fst = 2
            firststr = "Black goes first!"
            if("Comp" in (player1type, player2type)): #for debugging
                self.mct = montecarlotreenested.MonteCarloTreeNested(self.player2.board, np.sqrt(2), 1) #for debugging
                #self.player2.setTurn(1)
                #self.player1.setTurn(-1)
        self.verbose = vb
        self.its = 0
        if(self.verbose == 1):
            self.board.update_board(self.boardarray)
            self.board.draw_board()
            print "The result of the dice roll is: " + str(sd1) + ", " + str(sd2)
            print firststr
        self.possiblemovelist = []
        self.d1 = sd1
        self.d2 = sd2   
#print "self.verbose is " + str(self.verbose)
    
    def reset(self):
        self.board.reset()
        self.boardarray = self.board.board
        self.player1.reset(self.boardarray)
        self.player2.reset(self.boardarray)
        self.white_inds = np.where(self.boardarray > 0)[0]
        self.black_inds = np.where(self.boardarray < 0)[0]
        self.white_bearoff = False
        self.black_bearoff = False    
        self.d1 = -1
        self.d2 = -1
        sd1  = np.random.randint(1, 7)
        sd2 = np.random.randint(1, 7)
        self.fst = -1
        while(sd1 == sd2):
            sd1 = np.random.randint(1, 7)
            sd2 = np.random.randint(1, 7)
        firststr = ""    
        if(sd1 > sd2): #white goes first    
            self.turn = 0
            self.fst = 1
            firststr = "White goes first!"
            if("Comp" in (self.player1.typ, self.player2.typ)):
                self.mct.reset(self.player1.board)
                #self.player1.setTurn(1)
                #self.player2.setTurn(-1)
        else: #black goes first
            self.turn = 1
            self.fst = 2
            firststr = "Black goes first!"
            if("Comp" in (self.player1.typ, self.player2.typ)):
                self.mct.reset(self.player2.board)
                #self.player2.setTurn(1)
                #self.player1.setTurn(-1)
        self.its = 0    
        self.possiblemovelist = []
        if(self.verbose == 1):
            self.board.update_board(self.boardarray)
            self.board.draw_board()
            print "The result of the dice roll is: " + str(sd1) + ", " + str(sd2)
            print firststr
        self.d1 = sd1
        self.d2 = sd2     

    def rolldice(self):
        if(self.its != 0):
            temp = np.random.randint(1, 7, size = 2)
            self.d1 = np.max(temp)
            self.d2 = np.min(temp)
            #self.d1 = 4 #for debugging
            #self.d2 = 1 #for debugging
        #else: #for debugging
         #   self.d1 = 6
          #  self.d2 = 6    
        #if(self.d1 == self.d2): #simplifying assumption of no doubles
        #    print "The dice roll is: " + str(self.d1) + ", " + str(self.d2) + ", " + str(self.d1) + ", " + str(self.d2)
        #else:
        if(self.verbose == 1):
            if(self.turn == 0):
                print "White's roll is: " + str(self.d1) + ", " + str(self.d2)
            else:
                print "Black's roll is: " + str(self.d1) + ", " + str(self.d2)           
        self.its += 1



    def legal_move(self, move):
        if(self.turn == 0):
            return move in self.player1.getpossibleMoves()
        else:
            return move in self.player2.getpossibleMoves()

        #if(len(move) != 2): #wrong length
        #    return False
        #if(max(move) > 24 or min(move) < -1): #wrong indices
        #    return False    
        #if((self.turn == 0 and self.boardarray[27] != 0) or(self.turn == 1 and self.boardarray[26] != 0)): #one of the board members is in jail
    
    def check_possiblemoves(self, dice_list): #just checks to see if there is at least one legal move
        if(self.turn == 0 and self.boardarray[27] != 0):    
            for d in dice_list:
                if self.boardarray[d-1] >= -1: #either white pieces, no pieces, or only one black piece
                    # print "T1"
                    return True
        elif(self.turn == 1 and self.boardarray[26] != 0):
            for d in dice_list:
                if self.boardarray[24-d] <=1: #either black pieces, no pieces, or only one white piece
                    #print "T2"
                    return True
        else:
            if(self.turn == 0): #white player
                minind = np.min(self.white_inds)
                for x in self.white_inds:
                    for d in dice_list:
                        if(self.white_bearoff and (x + d == 24 or d > 24 - minind)): # can bear off
                            #print "T3"
                            return True
                        else:
                            if(x+d < 24 and self.boardarray[x+d] >= -1): #either white pieces, no pieces, or only one black piece
                                #print "x is " + str(x)
                                #print "d is " + str(d)
                                #print "self.boardarray is " + str(self.boardarray)
                                # print "T4"
                                return True
            else: #black player
                maxind = np.max(self.black_inds)
                if maxind == 25:
                    maxind = np.max(self.black_inds[np.where(self.black_inds != 25)])
                for x in self.black_inds:
                    for d in dice_list:
                        if(self.black_bearoff and (x - d == -1 or d > maxind)): # can bear off
                            #print "T5"
                            return True
                        else:
                            if(x != 25 and x-d > -1 and self.boardarray[x-d] <= 1): #either black pieces, no pieces, or only one white piece
                                #print "T6"
                                return True        
        #print "T7"                                    
        return False    
                

    def updateboard(self, move, move2=(), legal = True):
        #print "Legal is: " + str(legal)
        if(legal):
            for x in range(0, len(move), 2):
                ind1 = move[x]
                ind2 = move[x+1]
                if(ind2 == -1):
                    ind2 = 25    
                if(self.turn == 0):
                    if(self.boardarray[ind2] < 0):
                        self.boardarray[ind2] = self.boardarray[ind2] + 2
                        self.boardarray[26] = self.boardarray[26]-1
                    else:
                        self.boardarray[ind2] = self.boardarray[ind2] + 1
                    self.boardarray[ind1] = self.boardarray[ind1] - 1
                else:
                    if(self.boardarray[ind2] > 0):
                        self.boardarray[ind2] = self.boardarray[ind2] - 2
                        self.boardarray[27] = self.boardarray[27] + 1
                    else:
                        self.boardarray[ind2] = self.boardarray[ind2] - 1    
                    self.boardarray[ind1] = self.boardarray[ind1] + 1
            self.player1.updateBoard(self.boardarray)
            self.player2.updateBoard(self.boardarray)
        if(not self.mct is None):
            #print "IN ILLEGAL MOVE SECTION"
            if(self.fst == 1): #if computer always white, will always be a computer move here
                if(self.turn == 1 and self.player2.typ == "Human"):  #must pass in the human's move if playing human vs comp
                    self.mct.nextstate(self.player1.board, legal, (max(self.d1, self.d2), min(self.d1, self.d2)), move2)
                else:
                    self.mct.nextstate(self.player1.board, legal, (max(self.d1, self.d2), min(self.d1, self.d2)))
                    #advance the tree into the next state
            else:
                if(self.turn == 1 and self.player2.typ == "Human"):    #must pass in the human's move if playing human vs comp
                    self.mct.nextstate(self.player2.board, legal, (max(self.d1, self.d2), min(self.d1, self.d2)), move2) 
                else:
                    self.mct.nextstate(self.player2.board, legal, (max(self.d1, self.d2), min(self.d1, self.d2)))        
        self.possiblemovelist = []            


    def makeMove(self):
        #if(self.d1 == self.d2):
         #   list_dice = [self.d1, self.d2, self.d1, self.d2]
        #else:
        list_dice = (max(self.d1, self.d2), min(self.d1, self.d2))
        if(self.check_possiblemoves(list_dice) == False): #no possible moves
            #add here for making dummy state for monte carlo tree
            if(self.verbose == 1):
                print "Sorry, you have no available moves"
                self.board.draw_board()
                self.board.update_board(self.boardarray)    
            self.updateboard((), (), False)
            self.turn = np.mod(self.turn + 1, 2)
            return
        if(len(self.possiblemovelist) ==0):
            if(self.turn == 0):
                self.possiblemovelist = self.player1.getpossibleMoves(list_dice)
            else:
                self.possiblemovelist = self.player2.getpossibleMoves(list_dice)    
        #print self.possiblemovelist #for debugging

        if(self.turn == 0):
            if(self.player1.typ == "Human"):
                move = self.player1.makeMove(list_dice)
            else:
                move = self.mct.makeMove(self.possiblemovelist, list_dice)
        else:
            if(self.player2.typ == "Human"):
                move = self.player2.makeMove(list_dice)
            else:
                move = self.mct.makeMove(self.possiblemovelist, list_dice)
        move2 = move
        if(self.turn == 1 and self.player2.typ == "Human"):
            move2 = ()
            for x in move: #flip the move to correspond with expected table input
                if(x == -1):
                    move2 = move2 + (24, )
                elif(x >= 0 and x <= 23):
                    move2 = move2 + (23-x, )
                elif(x == 26):
                    move2 = move2 + (27, )
                elif(x == 24 or x == 27):
                    move2 = move2 + (100, )
                else:
                    move2 = move2 + (x, )            
        elif(self.turn == 1 and self.player2.typ == "Comp"):
            move = ()
            for x in move2: #flip the move to correspond with expected table input
                if(x == 24):
                    move = move + (25, )
                elif(x >= 0 and x <= 23):
                    move = move + (23-x, )
                elif(x == 27):
                    move = move + (26, )
                else:
                    print "ERROR!!"                
    #print "Move is " + str(move2)
        if(((self.player1.typ == "Comp" and self.turn == 0) or (self.player2.typ == "Comp" and self.turn == 1)) or move2 in self.possiblemovelist):
            self.updateboard(move, move2, True)
            
            if(self.verbose == 1):
                self.board.update_board(self.boardarray)
                self.board.draw_board()
            if(not self.getTerminalState(True)):
                self.turn = np.mod(self.turn + 1, 2)
                self.black_inds = np.where(self.boardarray < 0)[0]
                self.white_inds = np.where(self.boardarray > 0)[0]
                self.white_bearoff = np.max(self.white_inds) <= 24 and np.min(self.white_inds) >= 18
                tempmaxind = np.max(self.black_inds)
                if tempmaxind == 25: #very bad coding but at this point it was too late to change everything
                    tempmaxind = np.max(self.black_inds[np.where(self.black_inds != 25)])
                self.black_bearoff = tempmaxind <= 5  and np.min(self.black_inds) >= 0
        else:
            print "Sorry, you entered an invalid move"
            self.makeMove()

    def getTerminalState(self, update = False):
        #if(abs(self.boardarray[24]) == 15 or abs(self.boardarray[25]) == 15):
        #    return True
        #else:
        #    return False    
        if(abs(self.boardarray[24]) == 15):
            if(not self.mct is None and update and "Human" not in (self.player1.typ, self.player2.typ)):
                if(self.fst == 1): #player 1 went first and won
                    self.mct.backprop(1, self.player1.board, (max(self.d1, self.d2), min(self.d1, self.d2)))
                else:
                    self.mct.backprop(0, self.player1.board, (max(self.d1, self.d2), min(self.d1, self.d2))) #player 1 went first and lost            
            return True
        elif(abs(self.boardarray[25]) == 15):
            if(not self.mct is None and update and "Human" not in (self.player1.typ, self.player2.typ)):
                if(self.fst == 2): #player 2 went first and won
                    self.mct.backprop(1, self.player2.board, (max(self.d1, self.d2), min(self.d1, self.d2)))
                else:
                    self.mct.backprop(0, self.player2.board, (max(self.d1, self.d2), min(self.d1, self.d2)))    
            return True
        return False    
                

if __name__ == "__main__":
    # Retrieve the arguments from the command-line
    progst = time.time()
    my_args = docopt(__doc__)
    print my_args
    disp = int(my_args["--display"])
    p1 = "Comp"
    p2 = "Human"
    if(my_args["--n_humans"] == "0"):
        p2 = "Comp"
    elif(my_args["--n_humans"] == "2"):
        #print "HERE!!!"
        p1 = "Human"
    env = Environment(p1, p2, disp)
    total_iterations = int(my_args["--max_n_iteration"])
    for x in range(0, total_iterations):
        start_time = time.time()
        while(not env.getTerminalState()):
            env.rolldice()
            #raw_input("Press enter to make move") #for debugging
            env.makeMove()
        if(env.turn == 0):
            if(disp):
                print "White wins!"
            #env.player1.reward()    
        else:
            if(disp):
                print "Black wins!" 
        print "Runtime for iteration: " + str(x) + " is: " + str(time.time() - start_time)         
        env.reset()
        if("Human" not in (p1, p2) and x > 0 and x%5000 == 0):
            env.mct.savedict()
            #print "The dictionary was saved!"
    if("Human" not in (p1, p2)):
        env.mct.savedict()     

    print "Total runtime was " + str(time.time() - progst)



