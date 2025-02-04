import pygame as pg
from constants import *

bg_img = pg.image.load("assets/bg1.jpg").convert_alpha()
player1_d = pg.image.load("assets/player1.png").convert_alpha()
player2_d = pg.image.load("assets/player2.png").convert_alpha()
chicken_wing = pg.image.load("assets/chicken_wing.png").convert_alpha()

PLAYER_HEIGHT = 70

bg_img = pg.transform.scale(bg_img, SIZE)
player1_d = pg.transform.scale(player1_d, (PLAYER_HEIGHT, 1200/(975/PLAYER_HEIGHT)))
player2_d = pg.transform.scale(player2_d, (PLAYER_HEIGHT, 1200/(975/PLAYER_HEIGHT)))
chicken_wing = pg.transform.scale(chicken_wing,(40, 20))


#player1_r = pg.transform.flip(player1_l, True, False)
#player2_r = pg.transform.flip(player2_l, True, False)