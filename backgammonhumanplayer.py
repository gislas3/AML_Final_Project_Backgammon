import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
from docopt import docopt

class BackgammonHumanPlayer: #will always see board from white perspective (moves just flipped prior to interaction with main class)
	def __init__(self, brd, bw):
		self.black_or_white = bw
		self.board = np.zeros(len(brd))
		self.board = np.copy(brd)
		if(self.black_or_white == "Black"):
			self.board[0:24] = -1*self.board[23::-1]
		self.inds = np.where(self.board > 0)[0]	
		self.listmoves = []
		self.maxlen = 0
		self.maxroll = 0

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


	def makeMove(self, dice_roll):
		move = raw_input("Please enter a move in the format [index1 index2 index3 index4] or [index1 index2 index3 index4 index5 index6 index7 index8] in case of doubles)\n where the sequences are in order of the checkers you want to move: ")
		move = move.split()
		move = tuple(move)
		move = map(int, move)
		move = tuple(move)
		return move

	def recur_moves(self, dice_roll, boardcopy, indscopy, cand):
		#print "board copy is: " +  str(boardcopy)
		#print "indscopy is: " + str(indscopy)
		#print "cand is: " + str(cand)
		#print "dice_roll is: " + str(dice_roll)
		if(len(dice_roll) == 0 or len(indscopy) == 0): #finished recursion for one move
			if(len(cand) != 0 and len(cand) >= self.maxlen):
				self.listmoves.append(cand)
				if(len(cand) > self.maxlen):
					#print cand
					self.maxlen = len(cand) #track the length of the candidate moves
				#print "ADDED TO LIST"
			#boardcopy = np.copy(self.boardarray)
			#indscopy = np.copy(self.inds)					
			return
		if(boardcopy[27] != 0): #first check if have a piece in the middle of the board
			d1 = dice_roll[0]
			bc = np.empty_like(boardcopy)
			bc[:] = boardcopy[:]
			if(bc[d1] >= -1):
				#cand = cand + (27, d1)
				candadd = (27, d1)
				bc[27] -= 1
				if(bc[d1] == -1): #move results in hitting a piece off the board
					bc[d1] += 1
					bc[26] -= 1
				bc[d1] += 1
			indscopy2 = np.where(bc > 0)[0]
			self.recur_moves(dice_roll[1:], bc, indscopy2, cand + (27, d1))	
		else:
			d1 = dice_roll[0]
			tempminind = np.argmin(indscopy)
			tempmaxind = np.argmax(indscopy)
			tempbear = tempmaxind <= 24  and tempminind >= 18
			bc = np.empty_like(boardcopy)
			bc[:] = boardcopy[:]
			if(tempbear and (indscopy[0] + d1 == 24 or d1 > 24 - tempmaxind)):
				#cand = cand + (indscopy[0], 24)
				candadd = (indscopy[0], 24)
				bc[indscopy[0]] -= 1
				bc[24] += 1
				indscopy2 = np.where(bc > 0)[0]
				self.recur_moves(dice_roll[1:], bc, indscopy2, cand + candadd)
				self.recur_moves(dice_roll[1:], bc, indscopy2[1:], cand)
			elif(indscopy[0] + d1 < 24 and bc[indscopy[0] + d1] >= -1):
				#candadd = cand + (indscopy[0], indscopy[0] + d1 )
				candadd = (indscopy[0], indscopy[0] + d1 )
				bc[indscopy[0]] -= 1
				if(bc[indscopy[0] + d1] == -1): #move results in hitting a piece off the board
					bc[indscopy[0] + d1] += 1
					bc[26] -=1
				bc[indscopy[0] + d1] += 1
				indscopy2 = np.where(bc > 0)[0]
				self.recur_moves(dice_roll[1:], bc, indscopy2, cand + candadd)
				self.recur_moves(dice_roll[1:], bc, indscopy2[1:], cand)		
			self.recur_moves(dice_roll, boardcopy, indscopy[1:], cand)			


	def getpossibleMoves(self, dice_roll):
		tempboard = np.copy(self.board)
		tempinds = np.copy(self.inds)
		self.listmoves = []
		self.maxlen = 2
		cand = ()
		self.recur_moves(dice_roll, tempboard, tempinds, cand)
		if(dice_roll[0] != dice_roll[1]):
			cand = ()
			tempboard = np.copy(self.board)
			self.recur_moves(dice_roll[1::-1], tempboard, tempinds, cand)
		return self.listmoves


		 
