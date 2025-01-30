from bilder import *
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)

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

    def move(self):
        self.dx = 3
        self.dy = 3
        keys_pressed = pg.key.get_pressed()
        # TODO: Flytt spilleren ut i fra hvilke taster som er trykket
        if keys_pressed[K_UP]:
            self.y -= self.dy
            #self.image = 
        if keys_pressed[K_DOWN]:
            self.y += self.dy
            #self.image = 
        if keys_pressed[K_RIGHT]:
            self.x += self.dx
            #self.image = 
        if keys_pressed[K_LEFT]:
            self.x -= self.dx
            #self.image =   

class Mat(Object):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)

