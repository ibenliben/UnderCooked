import pygame as pg
from constants import *

bg_img = pg.image.load("assets/map.png").convert_alpha()
player1_d = pg.image.load("assets/player1.png").convert_alpha()
player2_d = pg.image.load("assets/player2.png").convert_alpha()
tomato_img = pg.image.load("assets/tomato.png").convert_alpha()
tomatoslice_img = pg.image.load("assets/tomatoslice.png").convert_alpha()
beef_img = pg.image.load("assets/beef.png").convert_alpha()
cabbage_img = pg.image.load("assets/cabbage.png").convert_alpha()
leaf_img = pg.image.load("assets/leaf.png").convert_alpha()
burgerbread_img = pg.image.load("assets/burgerbread.png").convert_alpha()
station_img = pg.image.load("assets/station.png").convert_alpha()
square_img = pg.image.load("assets/square.png").convert_alpha()

PLAYER_HEIGHT = 70

bg_img = pg.transform.scale(bg_img, SIZE)
player1_d = pg.transform.scale(player1_d, (PLAYER_HEIGHT, 1200/(975/PLAYER_HEIGHT)))
player2_d = pg.transform.scale(player2_d, (PLAYER_HEIGHT, 1200/(975/PLAYER_HEIGHT)))
tomato_img = pg.transform.scale(tomato_img,(30, 30))
tomatoslice_img = pg.transform.scale(tomatoslice_img,(30, 30))
beef_img = pg.transform.scale(beef_img,(30, 10))
burgerbread_img = pg.transform.scale(burgerbread_img,(40, 40))
cabbage_img = pg.transform.scale(cabbage_img,(30, 30))
leaf_img = pg.transform.scale(leaf_img,(30, 30))
station_img = pg.transform.scale(station_img,(60, 60))
square_img = pg.transform.scale(square_img,(60, 60))

#player1_r = pg.transform.flip(player1_l, True, False)
#player2_r = pg.transform.flip(player2_l, True, False)