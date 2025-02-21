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

    def update(self, imagelist , kd, ku, kr, kl, pickup, other_player, wall_list):
        if not self.can_move:
            return
        speed = 3.5
        dx, dy = 0, 0  # Midlertidig bevegelse
        keys_pressed = pg.key.get_pressed()

        if keys_pressed[ku]:
            dy += speed
            self.image = imagelist[0]

        if keys_pressed[kd]:
            dy -= speed
            self.image = imagelist[1]

        if keys_pressed[kr]:
            dx += speed
            self.image = imagelist[2]

        if keys_pressed[kl]:
            dx -= speed
            self.image = imagelist[3]

        # sjekker kollisjon før vi oppdaterer posisjon
        new_rect = self.rect.move(dx, dy)
        if not self.check_collision(new_rect, other_player, wall_list):
            self.rect = new_rect  # bare oppdater hvis det ikke er kollisjon

        if keys_pressed[pickup]:
            self.action = True
            #print("action true")
        else: 
            self.action = False
            #print("action false")

        self.rect.topleft = (self.rect.x, self.rect.y)

        if self.held_food:
            self.held_food.rect.center = self.rect.center   # tomaten føger etter spiller

    def check_collision(self, new_rect, other_player, wall_list):
        if new_rect.colliderect(other_player.rect):
            return True
        for wall in wall_list:
            if new_rect.colliderect(wall):
                return True
        return False

    def throw(self, keys_pressed, k_throw, thrown_food):
        # kan bare kaste mat hvis spilleren har mat
        if k_throw in keys_pressed and self.held_food:      
            thrown_food.add(self.held_food)
            self.held_food = None       # spilleren mister maten

    
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
        if self.start_time is None:  #dersom progressbaren ikke er starta skal den ikke tegnes heller
            return
        border_rect = pg.Rect(x - 2, y - 2, width + 4, height + 4)  # Litt større enn progress bar
        pg.draw.rect(screen, (255, 255, 255), border_rect, 2)  
        pg.draw.rect(screen, (255, 0, 0), (x, y, width, height)) # Rød bakgrunn
        pg.draw.rect(screen, (0, 255, 0), (x, y, width * self.progress, height)) # grønnt progress etterhvert

    def is_complete(self):
        return self.progress >= 1

class Station(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height], pg.SRCALPHA)   # aktiverer alfakanal for å kunne få gjennomsktig bokser
        self.image.fill((0,0,0,0))  # fyller med gjennomsiktig
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ActionStation(Station):
    def __init__(self, x, y, width, height, progress):
        super().__init__(x, y, width, height)
        self.in_use = False
        self.progress_bar = ProgressBar(4) 
        self.food_type = None   #lagrer typen mat som blir kutta/stekt  
        self.progress = progress

    def use_station(self, player):
        if player.held_food and player.action and not self.in_use:  
            print(f"Started processing: {type(player.held_food)}")  # Debug-melding
            self.in_use = True
            self.food_type = type(player.held_food)

            if self.progress:  # Only run the progress bar if progress is enabled
                self.progress_bar.start()
                player.can_move = False
            
            player.put_down()  

    def update(self, player):
        if not self.in_use:  # Legger til en sjekk
            return

        self.progress_bar.update()
        if self.progress_bar.is_complete():
            self.in_use = False
            player.can_move = True
            print(f"Finished processing: {self.food_type}")

            def food_slice(food_class, sliced_food_class, food_img):
                if self.food_type == food_class:
                            new_food = sliced_food_class(player.rect.x, player.rect.y, food_img)
                            print(f"Created a {sliced_food_class}!")
                            player.pick_up(new_food)                            
            food_slice(Tomato, TomatoSlice, tomatoslice_img)
            food_slice(Lettuce, LettuceLeaf, leaf_img)
            food_slice(RawMeat, RawPatty, rawpatty_img)

            def cook_meat():
                if self.food_type == RawPatty:
                    cookedpatty = CookedPatty(player.rect.x, player.rect.y, cookedpatty_img)
                    print("Created a Cooked Patty!")
                    player.pick_up(cookedpatty)
            cook_meat()

            self.food_type = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.in_use:
            self.progress_bar.draw(screen, self.rect.x, self.rect.y - 20, 50, 10)
class PlateStation(ActionStation):
    def __init__(self, x, y, width, height, in_use):
        super().__init__(x, y, width, height, in_use)
        self.ingredients = []
        self.completed_burger = False
        
    def place_ingredient(self, player):
        if player.held_food:
            if isinstance(player.held_food, (Bread, TomatoSlice, LettuceLeaf, CookedPatty)) and not any(isinstance(i, type(player.held_food)) for i in self.ingredients):
                self.ingredients.append(player.held_food)
                player.held_food = None  # spilleren legger fra seg maten
                
            # sjekker om alle ingrediensene er der
            if {Bread, TomatoSlice, LettuceLeaf, CookedPatty} == {type(i) for i in self.ingredients}:
                self.completed_burger = True
                self.ingredients.clear()  # fjerner ingrediensene, de blir til en burger
                
    def pick_up_burger(self, player):
        if self.completed_burger and not player.held_food:
            player.held_food = Burger(self.rect.x, self.rect.y, burger_img)
            self.completed_burger = False  # fjerner burgeren fra tallerkenen
    
    def draw(self, screen):
        super().draw(screen)
        x_offset = -len(self.ingredients) * 10 // 2  # startpunkt for å sentrere ingrediensene
        for ingredient in self.ingredients:
            ingredient_x = self.rect.centerx - ingredient.image.get_width() // 2 + x_offset
            ingredient_y = self.rect.centery - ingredient.image.get_height() // 2
            screen.blit(ingredient.image, (ingredient_x, ingredient_y))
            x_offset += 20  # øker mellomrommet mellom ingredienser
        if self.completed_burger:
            screen.blit(burger_img, (self.rect.x, self.rect.y))

class DeliverStation(ActionStation):
    def __init__(self, x, y, width, height, in_use):
        super().__init__(x, y, width, height, in_use)
        self.delivery_time = 0
        self.delivered_burger = False  # variabel for å vite om en burger er levert

    def deliver_burger(self, player):
        if isinstance(player.held_food, Burger):
            player.held_food = None  # spilleren leverer burgeren
            self.delivery_time = pg.time.get_ticks()  # starter timer
            self.delivered_burger = True  # burger er levert

    def update(self):
        if self.delivery_time and pg.time.get_ticks() - self.delivery_time > 3000:
            self.delivery_time = 0  # resetter etter 3 sekunder
            self.delivered_burger = False     # fjerner burger etter 3 sek

    def draw(self, screen):
        super().draw(screen)
        if self.delivered_burger:
            burger_x = self.rect.centerx - burger_img.get_width() // 2
            burger_y = self.rect.centery - burger_img.get_height() // 2
            screen.blit(burger_img, (burger_x, burger_y))  # tegner burgeren på midten

class TrashStation(ActionStation):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

class FoodStation(Station):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def give_food(self, player, Food_class, food_img):
        if player.held_food is None and player.action == True:
            player.pick_up(Food_class(player.rect.x, player.rect.y, food_img)) 

class Wall(Station):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    
class Food(Object, pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image)
        self.dx = 3
        self.dy = -2
        self.y_start = self.rect.y
        self.cooldown_timer = 0
        self.cooldown_duration = 9000 
        
    def update(self):
        self.dy += 0.1
        # oppdaterer posisjonen basert på hastigheten
        self.rect.x += self.dx
        self.rect.y += self.dy

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
class Tomato(Food):  
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class TomatoSlice(Food): 
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Lettuce(Food):  
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class LettuceLeaf(Food): 
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class RawMeat(Food):  
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class RawPatty(Food):  
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class CookedPatty(Food):   
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Bread(Food):      
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Burger(Food):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


# TODO: 
# - må kunne plukkes opp etter kast/ bare fjerne kasting
# - må IKKE kunne bruke sliced food i kuttestasjon aka ingenting skjer om du pøver å kutte noe som allerede er kutta