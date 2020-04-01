import pygame
import random
from math import sin, cos, pi, radians
import os

ABILLITY_GEN_TIMER = 40 # how many CLOCK tiks it will take to another abillity to apper
ABILLITY_GONE_TIMER = 2000 # how much time after the abillity was appered it will disapear
EFFECT_COUNTER = 10000 # how long the abillity will be activated on the player

#effect attrebutie consts
#TODO effect others
SIZE = 5 #change size #TODO minimize
CHANGE = 4 #change diraction
SPEED = 3 #the player speed is changing #TODO0
SQURE = 2 #create squre form movment #TODO
GHOST = 1 #the player is has no path and can pass through walls #TODO

SQURE_COUNTER = 4 #limit to squre so he will not kill self

#pic for attrebuite
ATT_DICT = {SIZE:r'.\pics\hungry_omez.png',
            CHANGE:r'.\pics\cd_omez.png',
            GHOST:r'.\pics\ghost.png',
            SQURE:r'.\pics\squre_omez.png',
            SPEED:r'.\pics\speedy_omez.png'}

#picture proportion
PIC_PROP = (30,30)

# ratio between game and score board 3/4
BOARD_SIZE_WID = 700
BOARD_SIZE_HIGHT = 500
#the yellow border width
BORDER_WIDTH = 7
#the size of the winning annoucment
WINNING_SIZE = 75
#size of path radius
PATH_RAD = 3
#colors
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#
PLAYER_SPACE = 80 #how many frames of the player movment it take until a space apeepr
PLAYER_SPACE_RANGE = 10 #for how many frames the player movment will draw space

ANGEL_FACTOR = 5.5 #how much the angel gets bigger every tik of CLOCk
PACE = 3 #radius of movment

CLOCK = pygame.time.Clock()

#utilles file

