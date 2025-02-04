import pygame as pg
from constants import *
screen = pg.display.set_mode(SIZE)
from bilder import *
from pygame.locals import (K_w, K_s, K_d, K_a, K_UP, K_DOWN, K_RIGHT, K_LEFT)

class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image  # lage liste med bilder? lettere å bytte bilde når player beveger seg
        self.dx = 0
        self.dy = 0

    def draw(self, screen):
        screen.blit(self.image,(self.x, self.y))

    def move(self):
        self.x += self.dx
        self.y += self.dy


class Food(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def move(self):
        # TODO: finne retning basert på hvilken side av kartet player er
        pass


class Chicken_wing(Food, pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image)
        self.rect = self.image.get_rect()
        # self.rect.center = (x, y)

    def update(self):
        self.rect.move_ip(5,0)
        # TODO: self.kill() etter noen sekunder
    

class Player(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image) 

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
    
    def throw(self, k_throw):
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[k_throw]:
            wing = Chicken_wing(self.x, self.y, chicken_wing)
            wings = pg.sprite.Group()
            wings.add(wing)

            wings.update()
            wings.draw(screen)
            print(wings)


