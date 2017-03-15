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

created by Gregory Islas and Olivier Saluan  
            
Usage: backgammon [-d <flag>] [-n <int>] [-e <int>]

Options:
-h --help      Show the description of the program
-d <flag> --display <flag>  a flag for activating the display [default: True]
-n <int> --n_humans <int>  an integer for the number of human players [default: 1]
-e <int> --max_n_iteration <int>  the maximum number of iterations [default: 1000]
"""


import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
from time import sleep
from docopt import docopt
import backgammonboard
import backgammonhumanplayer
import backgammonaiplayer

class Environment():
	def __init__(self, player1type, player2type, vb):
		self.board = backgammonboard.BackgammonBoard()
		self.boardarray = self.board.board
		if(player1type == "Comp"):
			self.player1 = backgammonaiplayer.BackgammonAIPlayer(self.boardarray, "White")
		else:
			self.player1 = backgammonhumanplayer.BackgammonHumanPlayer(self.boardarray, "White")
		if(player2type == "Comp"):
			self.player2 = backgammonaiplayer.BackgammonAIPlayer(self.boardarray, "Black")
		else:
			self.player2 = backgammonhumanplayer.BackgammonHumanPlayer(self.boardarray, "Black")	
		self.white_inds = np.where(self.boardarray > 0)[0]
		self.black_inds = np.where(self.boardarray < 0)[0]
		self.white_bearoff = False
		self.black_bearoff = False	
		self.d1 = -1
		self.d2 = -1
		sd1 = 1#np.random.randint(1, 7)
		sd2 = 6#np.random.randint(1, 7)
		while(sd1 == sd2):
			sd1 = np.random.randint(1, 7)
			sd2 = np.random.randint(1, 7)
		firststr = ""	
		if(sd1 > sd2): #white goes first	
			self.turn = 0
			firststr = "White goes first!"
		else: #black goes first
			self.turn = 1
			firststr = "Black goes first!"	
		self.verbose = vb
		if(self.verbose):
			self.board.draw_board()
			print "The result of the dice roll is: " + str(sd1) + ", " + str(sd2)
			print firststr
		self.possiblemovelist = []	
	
	def rolldice(self):
		temp = np.random.randint(1, 7, size = 2)
		self.d1 = np.max(temp)
		self.d2 = np.min(temp)
		#if(self.d1 == self.d2): #simplifying assumption of no doubles
		#	print "The dice roll is: " + str(self.d1) + ", " + str(self.d2) + ", " + str(self.d1) + ", " + str(self.d2)
		#else:
		if(self.verbose):
			if(self.turn == 0):
				print "White's roll is: " + str(self.d1) + ", " + str(self.d2)
			else:
				print "Black's roll is: " + str(self.d1) + ", " + str(self.d2)	
				
	def legal_move(self, move):
		if(self.turn == 0):
			return move in self.player1.getpossibleMoves()
		else:
			return move in self.player2.getpossibleMoves()

		#if(len(move) != 2): #wrong length
		#	return False
		#if(max(move) > 24 or min(move) < -1): #wrong indices
		#	return False	
		#if((self.turn == 0 and self.boardarray[27] != 0) or(self.turn == 1 and self.boardarray[26] != 0)): #one of the board members is in jail
	
	def check_possiblemoves(self, dice_list): #just checks to see if there is at least one legal move
		if(self.turn == 0 and self.boardarray[27] != 0):	
			for d in dice_list:
				if self.boardarray[d-1] >= -1: #either white pieces, no pieces, or only one black piece
					return True
		elif(self.turn == 1 and self.boardarray[26] != 0):
			for d in dice_list:
				if self.boardarray[24-d] <=1: #either black pieces, no pieces, or only one white piece
					return True
		else:
			if(self.turn == 0): #white player
				minind = np.min(self.white_inds)
				for x in self.white_inds:
					for d in dice_list:
						if(self.white_bearoff and (x + d == 24 or d > 24 - minind)): # can bear off
							return True
						else:
							if(self.boardarray[x+d] >= -1): #either white pieces, no pieces, or only one black piece
								return True
			else: #black player
				maxind = np.max(self.black_inds)
				if maxind == 25:
					maxind = np.max(self.black_inds[np.where(self.black_inds != 25)])
				for x in self.black_inds:
					for d in dice_list:
						if(self.black_bearoff and (x - d == -1 or d > maxind)): # can bear off
							return True
						else:
							if(self.boardarray[x-d] <= 1): #either black pieces, no pieces, or only one white piece
								return True					
		return False	
				

	def updateboard(self, move):
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
		self.possiblemovelist = []			


	def makeMove(self):
		#if(self.d1 == self.d2):
		#	list_dice = [self.d1, self.d2, self.d1, self.d2]
		#else:
		list_dice = [max(self.d1, self.d2), min(self.d1, self.d2)]
		if(self.check_possiblemoves(list_dice) == False): #no possible moves
			self.board.update_board(self.boardarray)
			if(self.verbose):
				print "Sorry, you have no available moves"
				self.board.draw_board()
			self.turn = np.mod(self.turn + 1, 2)
			return
		if(len(self.possiblemovelist) ==0):
			if(self.turn == 0):
				self.possiblemovelist = self.player1.getpossibleMoves(list_dice)
			else:
				self.possiblemovelist = self.player2.getpossibleMoves(list_dice)	
		print self.possiblemovelist		
		if(self.turn == 0):
			move = self.player1.makeMove((self.d1, self.d2))
		else:
			move = self.player2.makeMove((self.d1, self.d2))
		move2 = move
		if(self.turn == 1):
			move2 = ()
			for x in move: #flip the move to correspond with expected table input
				if(x == -1):
					move2 = move2 + (24, )
				elif(x >= 0 and x <= 23):
					move2 = move2 + (23-x, )
				elif(x == 26):
					move2 = move2 + (27, )
				elif(x == 24):
					move2 = move2 + (100, )
				else:
					move2 = move2 + (x, )			

		print move2	
		if(move2 in (self.possiblemovelist)):
			self.updateboard(move)
			self.board.update_board(self.boardarray)
			if(self.verbose):
				self.board.draw_board()
			if(not self.getTerminalState()):
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

	def getTerminalState(self):
		if(abs(self.boardarray[24]) == 15 or abs(self.boardarray[25]) == 15):
			return True
		else:
			return False	


if __name__ == "__main__":

    # Retrieve the arguments from the command-line
    my_args = docopt(__doc__)
    print my_args
    disp = my_args["--display"]
    p1 = "Comp"
    p2 = "Human"
    if(my_args["--n_humans"] == "0"):
    	p2 = "Comp"
    elif(my_args["--n_humans"] == "2"):
    	#print "HERE!!!"
    	p1 = "Human"
    env = Environment(p1, p2, disp)
    while(not env.getTerminalState()):
    	env.rolldice()
    	env.makeMove()
    if(env.turn == 0):
    	if(disp):
    		print "White wins!"
    	#env.player1.reward()	

    else:
    	if(disp):
    		print "Black Wins wins!"			




