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


class FoodStation(Object):
<<<<<<< Updated upstream
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
=======
    def __init__(self, x, y):
        super().__init__(x, y)
>>>>>>> Stashed changes

    def give_food(self, player, Food_class, food_img):
        if player.held_food is None:
            player.pick_up(Food_class(player.rect.x, player.rect.y, food_img)) # spilleren får en tomat

    # TODO: skille mellom give_tomato, give_salad osv.

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
        # - må kunne kutte opp tomat -> tomatoslice
        # - må kunne steke kjøtt
<<<<<<< Updated upstream
    
=======
    



>>>>>>> Stashed changes
