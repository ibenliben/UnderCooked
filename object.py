import pygame as pg
from constants import *

from bilder import *


class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image 
        self.dx = 0
        self.dy = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)



class Food(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)



class Chicken_wing(Food, pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image)
        self.dx = 5
        self.dy = -3
        self.y_start = y
       
    def update(self):
        self.dy += 0.1 # Gravitasjon
        if self.dy > 0 and abs(self.y - self.y_start) < 0.1:
            self.dx = 0
            self.dy = 0
            self.y = self.y_start

        super().update()

        # TODO: 
        # - player1 kaster til venstre og player 2 til høyre
        # - legge på tyngdekraft...
        # - self.kill() etter noen sekunder/ plukke opp
    

class Player(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image) 

    def update(self, kd, ku, kr, kl):
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
        self.rect.topleft = (self.x, self.y)

    
    def throw(self, keys_pressed, k_throw, wings):
        if k_throw in keys_pressed:
            center = self.rect.center
            wing = Chicken_wing(center[0]-10, center[1]-10, chicken_wing)
            wings.add(wing)


