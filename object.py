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


class Player(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image) 
        self.held_food = None   # spilleren holder ingen mat ved start

<<<<<<< Updated upstream
    def update(self, kd, ku, kr, kl, other_player):
        self.dx = 3
        self.dy = 3
        keys_pressed = pg.key.get_pressed()
        new_rect = self.rect.copy()

        if keys_pressed[ku]:
            new_rect.y += self.dy
            if not self.check_collision(new_rect, other_player):
                self.rect.y += self.dy

        if keys_pressed[kd]:
            new_rect.y -= self.dy
            if not self.check_collision(new_rect, other_player):
                self.rect.y -= self.dy

        if keys_pressed[kr]:
            new_rect.x += self.dx
            if not self.check_collision(new_rect, other_player):
                self.rect.x += self.dx

        if keys_pressed[kl]:
            new_rect.x -= self.dx
            if not self.check_collision(new_rect, other_player):
                self.rect.x -= self.dx
                 
        self.rect.topleft = (self.rect.x, self.rect.y)

    def check_collision(self, new_rect, other_player):
        if new_rect.colliderect(other_player.rect):
            return True
        #TODO: kollisjon med vegger
        #for wall in walls:
        #   if new_rect.colliderect(wall):
        #       return True
        return False

=======
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

    
>>>>>>> Stashed changes
    def throw(self, keys_pressed, k_throw, tomatoes):
        if k_throw in keys_pressed and self.held_food:      # kan bare kaste mat hvis spilleren har mat
            center = self.rect.center
            tomato = Tomato(center[0]-10, center[1]-10, tomato_img)
            tomatoes.add(tomato)
            self.held_food = None       # spilleren mister maten

        # TODO: all mat må kunne kastes - kan bare kaste maten spilleren holder. 
    
    def pick_up(self, food):
        if self.held_food is None:
            self.held_food = food


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
