import pygame as pg
from constants import *

from bilder import *


class Object:
    def __init__(self, x, y, image):
        self.image = image 
        self.dx = 0
        self.dy = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        #self.rect.topleft = (self.x, self.y)


class Food(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)



class Tomato(Food, pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image)
        self.dx = 5
        self.dy = -3
        self.y_start = self.rect.y
       
    def update(self):
        self.dy += 0.1 # Gravitasjon
        if self.dy > 0 and abs(self.rect.y - self.y_start) < 0.1:
            self.dx = 0
            self.dy = 0
            self.rect.y = self.y_start

        super().update()

        # TODO: 
        # - player1 kaster til venstre og player 2 til høyre
        # - må kunne plukkes opp
    

class Player(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image) 

    def update(self, kd, ku, kr, kl):
        self.dx = 3
        self.dy = 3
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[ku]:
            self.rect.y += self.dy
            #self.image = 
        if keys_pressed[kd]:
            self.rect.y -= self.dy
            #self.image = 
        if keys_pressed[kr]:
            self.rect.x += self.dx
            #self.image = 
        if keys_pressed[kl]:
            self.rect.x -= self.dx
            #self.image =   
        self.rect.topleft = (self.rect.x, self.rect.y)

    
    def throw(self, keys_pressed, k_throw, tomatoes):
        if k_throw in keys_pressed:
            center = self.rect.center
            tomato = Tomato(center[0]-10, center[1]-10, tomato_img)
            tomatoes.add(tomato)


