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
        self.action = False

    def update(self, kd, ku, kr, kl, pickup, other_player):
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

        if keys_pressed[pickup]:
            self.action = True
        else: 
            self.action = False
        
        self.rect.topleft = (self.rect.x, self.rect.y)

        if self.held_food:
            self.held_food.rect.center = self.rect.center   # tomaten føger etter spiller

    def check_collision(self, new_rect, other_player):
        if new_rect.colliderect(other_player.rect):
            return True
        #TODO: kollisjon med vegger
        #for wall in walls:
        #   if new_rect.colliderect(wall):
        #       return True
        return False

    def throw(self, keys_pressed, k_throw, tomatoes):
        # kan bare kaste mat hvis spilleren har mat
        if k_throw in keys_pressed and self.held_food:      
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
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

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
        self.cooldown_timer = 0
        self.cooldown_duration = 4000 
        
       
    def update(self):
        self.dy += 0.1

        # stopper når den treffer bakken
        if self.dy > 0 and abs(self.rect.y - self.y_start) < 0.1:
            self.dx = 0
            self.dy = 0
            self.rect.y = self.y_start

        #lager en cooldown timer
        if self.cooldown_timer == 0:
                self.cooldown_timer = pg.time.get_ticks()
        elif pg.time.get_ticks() - self.cooldown_timer >= self.cooldown_duration:
                self.kill() #fjerner tomaten fra alle sprites
        super().update()

class Bread(Food, pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image)
        self.dx = 5
        self.dy = -3
        self.y_start = self.rect.y
        self.cooldown_timer = 0
        self.cooldown_duration = 4000  # Duration in milliseconds

    def update(self):
        self.dy += 0.1

        # Stop when it hits the ground
        if self.dy > 0 and abs(self.rect.y - self.y_start) < 0.1:
            self.dx = 0
            self.dy = 0
            self.rect.y = self.y_start

        # Create a cooldown timer
        if self.cooldown_timer == 0:
            self.cooldown_timer = pg.time.get_ticks()
        elif pg.time.get_ticks() - self.cooldown_timer >= self.cooldown_duration:
            self.kill()  # Remove the bread from all sprites
        super().update()
        # TODO: 
        # - må kunne plukkes opp etter kast
        # - må kunne kutte opp tomat -> tomatoslice
        # - må kunne steke kjøtt