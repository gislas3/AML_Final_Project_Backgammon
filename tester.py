
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

b = np.zeros(28)
#b[0:12] = [2, 0, 0, 0, 0,  -5, 0, -3, 0, 0, 0, 5]
#b[23:11:-1] = -1*b[0:12]
#for debugging
b[27] = 2
#b[26] = -2
b[0] = -1
#b[1] = -4
#b[2] = 2
#b[3] = -1
#b[4] = -1
b[5] = -5
b[7] = -2
b[11] = 4
b[12] = -5
b[14] = 1
b[16] = 3
b[18] = 5
b[23] = -2

c = backgammonaiplayer.BackgammonAIPlayer(b, "White")
print c.getpossibleMoves((6, 1))
print (6, 1) in (6, 1, 5, 1)