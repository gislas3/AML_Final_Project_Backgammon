import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
from docopt import docopt

class BackgammonAIPlayer: #will always see board from white perspective (moves just flipped)
	def __init__(self, bw, brd):
		self.black_or_white = bw
		self.board = brd

	def updateBoard(self, brd):
		self.board = brd

	def getPossibleMoves(self, dice_roll):
		return (0, 0)

	def makeMove(self, dice_roll):
		possible_moves = self.getPossibleMoves(dice_roll)
		return [5, 6]#possible_moves[np.random.randint(0, len(possible_moves))]

	
