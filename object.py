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
        

class Player(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image) 
        self.held_food = None   # spilleren holder ingen mat ved start
        self.can_move = True  


    def update(self, kd, ku, kr, kl, pickup, other_player):
        if not self.can_move:
            return
        
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
            #print("action true")
        else: 
            self.action = False
            #print("action false")


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
            tomato = Food(center[0]-10, center[1]-10, tomato_img)
            tomatoes.add(tomato)
            self.held_food = None       # spilleren mister maten

        # TODO: all mat må kunne kastes - kan bare kaste maten spilleren holder. 
    
    def pick_up(self, food):
        if self.held_food is None:
            print(f"Picking up: {type(food)}")  # Debug-melding
            self.held_food = food


    def put_down(self):
        self.held_food = None

class ProgressBar:
    def __init__(self, duration):
        self.duration = duration
        self.progress = 0
        self.start_time = None

    def start(self):
        self.start_time = pg.time.get_ticks()
        #print("ProgressBar startet :", self.start_time) -> brukt under debug

    def update(self):
        #print("progressjon:", self.progress) -> brukt for debug
        if self.start_time is not None:
            elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000  
            self.progress = min(elapsed_time / self.duration, 1) 

    def draw(self, screen, x, y, width, height):
        border_rect = pg.Rect(x - 2, y - 2, width + 4, height + 4)  # Litt større enn progress bar
        pg.draw.rect(screen, (255, 255, 255), border_rect, 2)  
        pg.draw.rect(screen, (255, 0, 0), (x, y, width, height)) # Rød bakgrunn
        pg.draw.rect(screen, (0, 255, 0), (x, y, width * self.progress, height)) # grønnt progress etterhvert

    def is_complete(self):
        return self.progress >= 1
    
class ActionStation(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.in_use = False
        self.progress_bar = ProgressBar(4) 
        self.food_type = None #lagrer typen mat som blir kutta/stekt 

    def use_station(self, player):
        if player.held_food and player.action and not self.in_use:  
            print(f"Started processing: {type(player.held_food)}")  # Debug-melding
            self.in_use = True
            player.can_move = False
            self.progress_bar.start()
            self.food_type = type(player.held_food)
            player.put_down()
            
    def update(self, player):
        if not self.in_use:  # Legger til en sjekk
            return

        self.progress_bar.update()
        if self.progress_bar.is_complete():
            self.in_use = False
            player.can_move = True
            print(f"Finished processing: {self.food_type}")  

            if self.food_type == Tomato:
                new_food = TomatoSlice(player.rect.x, player.rect.y, tomatoslice_img)
                print("Created a TomatoSlice!")
                player.pick_up(new_food)

            self.food_type = None
            #Evt skrive koden sånn:
            #if self.food_type == Tomato:
                #player.pick_up(TomatoSlice(player.rect.x, player.rect.y, tomatoslice_img)) 

                
                #elif self.food_type == rawPatty:
                    #player.pick_up(CookedMeat(player.rect.x, player.rect.y, beef_img))

 
                #TODO: spiller må få den kuttet versjonen av maten 
                #player.pick_up(food_type(player.rect.x, player.rect.y, food_img))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.in_use:
            self.progress_bar.draw(screen, self.rect.x, self.rect.y - 20, 50, 10)

class FoodStation(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def give_food(self, player, Food_class, food_img):
        if player.held_food is None and player.action == True:
            player.pick_up(Food_class(player.rect.x, player.rect.y, food_img)) 

    #TODO: fikse funkjsonen under for å ungå gjenngående kode i main, 
    # men får feilmeldingen at player ikke har en attributt som heter action, som er rart siden den har det
    #def use_station(player, station, food_class, food_image): 
    #    if player.rect.colliderect(station.rect) and player.action:
    #       station.give_food(player, food_class, food_image)



class Food(Object, pg.sprite.Sprite):
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

#MAT klassene

class Tomato(Food):  #Hel tomat
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Lettuce(Food):  #Helt salathode
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class LettuceLeaf(Food):  #Salat blad
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class TomatoSlice(Food):  # kutta tomato
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class RawMeat(Food):  #raw kjott
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class RawPatty(Food):  #raw burgerkjott
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class CookedPatty(Food):  #stekt burgerkjott
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


        # TODO: 
        # - må kunne plukkes opp etter kast
        # - må kunne kutte opp tomat -> tomatoslice
        # - må kunne steke kjøtt