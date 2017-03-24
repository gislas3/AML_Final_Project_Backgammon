


import sys
#from tkinter import * 
#from PIL import Image, ImageTk
import numpy as np
from docopt import docopt


class BackgammonBoard():
	def __init__(self):
		self.board = np.zeros(28)
		self.board[0:12] = [2, 0, 0, 0, 0,  -5, 0, -3, 0, 0, 0, 5]
		self.board[23:11:-1] = -1*self.board[0:12]
		#for debugging
		#self.board[25] = -1
		#self.board[27] = 2
		#self.board[0] = -1
		#self.board[1] = -4
		#self.board[2] = 2
		#self.board[3] = -2
		#self.board[4] = -1
		#self.board[5] = -3
		#self.board[6] = -2
		#self.board[9] = -2
		#self.board[10] = -1
		#self.board[14] = -1
		#self.board[21] = 5
		#self.board[22] = 8
		#self.board[18] = 4
		#self.board[21] = 1
		#self.board[23] = 1
		self.bstring_generic = []
		self.bstring_generic.append(list("  12  13  14  15  16  17   18  19  20  21  22  23   24  "))
		self.bstring_generic.append(list("|   |   |   |   |   |   ||   |   |   |   |   |   ||   ||"))
		self.bstring_generic.append(list("|   |   |   |   |   |   ||   |   |   |   |   |   ||   ||"))
		self.bstring_generic.append(list("                                                        "))
		self.bstring_generic.append(list("                      26                                "))
		self.bstring_generic.append(list("                         |                              "))
		self.bstring_generic.append(list("                         |                              "))
		self.bstring_generic.append(list("                      27                                "))
		self.bstring_generic.append(list("                                                        "))
		self.bstring_generic.append(list("|   |   |   |   |   |   ||   |   |   |   |   |   ||   ||"))
		self.bstring_generic.append(list("|   |   |   |   |   |   ||   |   |   |   |   |   ||   ||"))
		self.bstring_generic.append(list("  11  10  9   8   7   6    5   4   3   2   1   0    -1  "))
		#self.update_board(self.board)

	def reset(self):
		self.board = np.zeros(28)
		self.board[0:12] = [2, 0, 0, 0, 0,  -5, 0, -3, 0, 0, 0, 5]
		self.board[23:11:-1] = -1*self.board[0:12]
		
	def update_board(self, newboard):
		self.board = newboard
		for x in (1, 5, 6, 9):
			if(x == 1): #first row
				zstart = 12
				ypos = 2
				for z in range(zstart, zstart + 13): #loop through game board
					if(self.board[z] != 0):
						if(self.board[z] < 0): #corresponds to black piece
							self.bstring_generic[x][ypos] = "B"
						else: #corresponds to white piece
							self.bstring_generic[x][ypos] = "W"
						self.bstring_generic[x+1][ypos] = int(np.mod(abs(self.board[z]), 10))
						if(abs(self.board[z]) >= 10):
							self.bstring_generic[x+1][ypos-1] =  int(abs(self.board[z])/10)
						else:
							self.bstring_generic[x+1][ypos-1] =  " "
					else:
						self.bstring_generic[x][ypos] = " "
						self.bstring_generic[x+1][ypos] = " "
						self.bstring_generic[x+1][ypos-1] = " "
					if(z in (17, 23)):
						ypos = ypos + 5
					else:
						ypos = ypos + 4

			elif(x == 9): #first row
				zstart = 11
				ypos = 2
				for z in range(zstart, zstart - 13, -1): #loop through game board
					if(z == -1):
						z = 25
					if(self.board[z] != 0):
						if(self.board[z] < 0): #corresponds to black piece
							self.bstring_generic[x][ypos] = "B"
						else: #corresponds to white piece
							self.bstring_generic[x][ypos] = "W"
						self.bstring_generic[x+1][ypos] = int(np.mod(abs(self.board[z]), 10))
						if(abs(self.board[z]) >= 10):
							self.bstring_generic[x+1][ypos-1] = int(abs(self.board[z])/10)
						else:
							self.bstring_generic[x+1][ypos-1] =  " "	
					else:
						self.bstring_generic[x][ypos] = " "
						self.bstring_generic[x+1][ypos] = " "
						self.bstring_generic[x+1][ypos-1] = " "
					if(z in (6, 0)):
						ypos = ypos + 5
					else:
						ypos = ypos + 4
			else: #game rows that correspond to middle pieces
				if (x == 5):
				 	if (self.board[26] != 0):
						self.bstring_generic[x][24] = "B"
						self.bstring_generic[x][26] = int(abs(self.board[26]))
					else:
						self.bstring_generic[x][24] = " "
						self.bstring_generic[x][26] = " "
				elif (x ==6):
					if (self.board[27] != 0):
						self.bstring_generic[x][24] = "W"
						self.bstring_generic[x][26] = int(abs(self.board[27]))
					else:
						self.bstring_generic[x][24] = " "
						self.bstring_generic[x][26] = " "	
	

	def draw_board(self):
		for x in range(0, len(self.bstring_generic)):
			for y in range(0, len(self.bstring_generic[x])):
				sys.stdout.write(str(self.bstring_generic[x][y]))
			sys.stdout.write("\n")	

			
