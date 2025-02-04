import pygame as pg
#from constants import *
from bilder import *
from pygame.locals import (K_w, K_s, K_d, K_a, K_UP, K_DOWN, K_RIGHT, K_LEFT)

class Object:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img  # lage liste med bilder? lettere å bytte bilde når player beveger seg
        self.dx = 0
        self.dy = 0

    def draw(self, screen):
        screen.blit(self.img,(self.x, self.y))

    def move(self):
        self.x += self.dx
        self.y += self.dy


class Player(Object):
    def __init__(self, x, y, img):
        super().__init__(x, y, img) 

    def move(self, kd, ku, kr, kl):
        self.dx = 3
        self.dy = 3
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[ku]:
            self.y += self.dy
            #self.image = 
        if keys_pressed[kd]:
            self.y -= self.dy
            #self.image = 
        if keys_pressed[kr]:
            self.x += self.dx
            #self.image = 
        if keys_pressed[kl]:
            self.x -= self.dx
            #self.image =   

class Food(Object):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)

