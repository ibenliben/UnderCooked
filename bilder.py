import pygame as pg
from constants import *

bg_img = pg.image.load("assets/map.png").convert_alpha()
tomato_img = pg.image.load("assets/tomato.png").convert_alpha()
tomatoslice_img = pg.image.load("assets/tomatoslice.png").convert_alpha()
beef_img = pg.image.load("assets/beef.png").convert_alpha()
rawpatty_img = pg.image.load("assets/burgerpattyraw.png").convert_alpha()
cookedpatty_img = pg.image.load("assets/burgerpattycooked.png").convert_alpha()
lettuce_img = pg.image.load("assets/lettuce.png").convert_alpha()
leaf_img = pg.image.load("assets/lettuceleaf.png").convert_alpha()
burgerbread_img = pg.image.load("assets/burgerbread.png").convert_alpha()
burger_img = pg.image.load("assets/burger.png").convert_alpha()
station_img = pg.image.load("assets/station.png").convert_alpha()
square_img = pg.image.load("assets/square.png").convert_alpha()

#SPILLERNE
p1_d = pg.image.load("assets/player/p1back.png").convert_alpha()
p2_d = pg.image.load("assets/player/p2back.png").convert_alpha()
p1_u = pg.image.load("assets/player/p1front.png").convert_alpha()
p2_u = pg.image.load("assets/player/p2left.png").convert_alpha()
p1_r = pg.image.load("assets/player/p1right.png").convert_alpha()
p2_l = pg.image.load("assets/player/p2left.png").convert_alpha()
p1_stand_l = pg.image.load("assets/player/p1standleft.png").convert_alpha()
p2_stand_r = pg.image.load("assets/player/p2standright.png").convert_alpha()

PLAYER_HEIGHT = 40

bg_img = pg.transform.scale(bg_img, SIZE)
tomato_img = pg.transform.scale(tomato_img,(30, 30))
tomatoslice_img = pg.transform.scale(tomatoslice_img,(40, 40))
beef_img = pg.transform.scale(beef_img,(40, 40))
cookedpatty_img = pg.transform.scale(cookedpatty_img,(40, 40))
rawpatty_img = pg.transform.scale(rawpatty_img,(40, 40))
burgerbread_img = pg.transform.scale(burgerbread_img,(40, 40))
lettuce_img = pg.transform.scale(lettuce_img,(30, 30))
leaf_img = pg.transform.scale(leaf_img,(30, 30))
burger_img = pg.transform.scale(burger_img, (30, 30))
station_img = pg.transform.scale(station_img,(60, 60))
square_img = pg.transform.scale(square_img,(60, 60))

#SPILLERNE
DEFAULT_PLAYER_SIZE = (60,100)
p1_d = pg.transform.scale(p1_d, DEFAULT_PLAYER_SIZE)
p2_d = pg.transform.scale(p2_d, DEFAULT_PLAYER_SIZE)
p1_u = pg.transform.scale(p1_u, DEFAULT_PLAYER_SIZE)
p2_u = pg.transform.scale(p2_u, DEFAULT_PLAYER_SIZE)
p1_r = pg.transform.scale(p1_r, (100,90))
p2_l = pg.transform.scale(p2_l, (100,90))
p1_l = pg.transform.flip(p1_r, True, False)
p2_r = pg.transform.flip(p2_l, True, False)
