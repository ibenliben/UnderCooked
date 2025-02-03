import pygame as pg
from constants import *

bg_img = pg.image.load("assets/bg1.jpg").convert_alpha()
player1_r = pg.image.load("assets/player1.png").convert_alpha()
player2_r = pg.image.load("assets/player2.png").convert_alpha()

PLAYER_HEIGHT = 70

bg_img = pg.transform.scale(bg_img, SIZE)
player1_r = pg.transform.scale(player1_r, (PLAYER_HEIGHT, WIDTH/(HEIGHT/PLAYER_HEIGHT)))
player2_r = pg.transform.scale(player2_r, (PLAYER_HEIGHT, WIDTH/(HEIGHT/PLAYER_HEIGHT)))


player1_l = pg.transform.flip(player1_r, True, False)
player2_l = pg.transform.flip(player2_r, True, False)