import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
from docopt import docopt

class BackgammonHumanPlayer: #will always see board from white perspective (moves just flipped)
	def __init__(self, bw, brd):
		self.black_or_white = bw
		self.board = brd

	def updateBoard(self, brd):
		self.board = brd

	def makeMove(self, dice_roll):
		move = raw_input("Please enter a move in the format [index1 index2 index3 index4] or [index1 index2 index3 index4 index5 index6 index7 index8] in case of doubles)\n where the sequences are in order of the checkers you want to move: ")
		move = move.split()
		move = tuple(move)
		move = map(int, move)
		return move
