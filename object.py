import pygame as pg
from constants import *
from bilder import *
import random as random
 
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
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = (0, 0)
        self.plateAction = False

    def update(self, imagelist , kd, ku, kr, kl, pickup, ctrl, other_player, wall_list):
        if not self.can_move:
            return
        speed = 6 #MIDLERTIDIG økt farten til spilleren under beta fasen grunnet raskere debuggings muligheter
        dx, dy = 0, 0  # Midlertidig bevegelse
        keys_pressed = pg.key.get_pressed()

        if keys_pressed[ku]:
            dy += speed
            self.image = imagelist[0]
            self.direction = (0, -1)

        if keys_pressed[kd]:
            dy -= speed
            self.image = imagelist[1]
            self.direction = (0, 1)

        if keys_pressed[kr]:
            dx += speed
            self.image = imagelist[2]
            self.direction = (1, 0)

        if keys_pressed[kl]:
            dx -= speed
            self.image = imagelist[3]
            self.direction = (-1, 0)

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
        
        if keys_pressed[ctrl]:
            self.plateAction = True
            print("plateAction = True")
        else:
            self.plateAction = False

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
    
    def throw(self, keys_pressed, throw_key, thrown_food_group):
        if throw_key in keys_pressed and self.held_food is not None:
            # Throw the food based on current direction
            food = ThrownFood(self.rect.centerx, self.rect.centery, self.held_food.image, self.direction)
            thrown_food_group.add(food)  # Add thrown food to the group
            self.held_food = None

    def pick_up(self, food):
        if self.held_food is None:
            print(f"Picking up: {type(food)}")  #Debug-melding
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
    def __init__(self, x, y, width, height, progress, cut):
        super().__init__(x, y, width, height)
        self.in_use = False
        self.progress_bar = ProgressBar(2)#øker hastigheten til progressbaren under beta fasen
        self.food_type = None   #lagrer typen mat som blir kutta/stekt  
        self.progress = progress
        self.cut = cut

    
    def process_food(self, player):
        if not player.held_food:
            return

        food_type = type(player.held_food)
        print(f"Started processing: {food_type}")  # Debug-melding

        if self.cut:  #Kuttestasjon
            if isinstance(player.held_food, (Tomato, Lettuce, RawMeat)):
                print(f"{food_type} is being sliced")
            else:
                print(f"{food_type} cannot be sliced")
                return
        else:  # Kokestasjon
            if isinstance(player.held_food, RawPatty):
                print(f"{food_type} is being cooked")
            else:
                print(f"{food_type} cannot be cooked")
                return

        #Start prosessen hvis mattypen er gyldig
        self.in_use = True
        self.food_type = food_type
        self.progress_bar.start()
        player.can_move = False
        player.put_down()


    def use_station(self, player):
        if player.held_food and player.action and not self.in_use:
            self.process_food(player)


    def update(self, player):
        if not self.in_use:
            return

        self.progress_bar.update()
        if self.progress_bar.is_complete():
            self.in_use = False
            player.can_move = True
            print(f"Finished processing: {self.food_type}")

            #Opprett ny mat basert på prosessen
            if self.cut:
                sliced_food_map = {
                    Tomato: (TomatoSlice, tomatoslice_img),
                    Lettuce: (LettuceLeaf, leaf_img),
                    RawMeat: (RawPatty, rawpatty_img),
                }
                if self.food_type in sliced_food_map:
                    sliced_class, image = sliced_food_map[self.food_type]
                    new_food = sliced_class(player.rect.x, player.rect.y, image)
                    print(f"Created a {sliced_class}!")
                    player.pick_up(new_food)

            else:  #stekeestasjon
                if self.food_type == RawPatty:
                    cookedpatty = CookedPatty(player.rect.x, player.rect.y, cookedpatty_img)
                    print("Created a Cooked Patty!")
                    player.pick_up(cookedpatty)

            self.food_type = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.in_use:
            self.progress_bar.draw(screen, self.rect.x, self.rect.y - 20, 50, 10)

class PlateStation(ActionStation):
    def __init__(self, x, y, width, height, in_use):
        super().__init__(x, y, width, height, in_use, cut=False)
        self.ingredients = []
        
    def place_ingredient(self, player):
        if player.held_food:
            print(f"legger  {player.held_food} til plate")
            if isinstance(player.held_food, (Bread, TomatoSlice, LettuceLeaf, CookedPatty)) and not any(isinstance(i, type(player.held_food)) for i in self.ingredients):
                self.ingredients.append(player.held_food)
                player.held_food = None  #spilleren legger fra seg maten
            print(f"nåværende ingredients: {self.ingredients}")
                
    def pick_up_burger(self, player):
        if self.ingredients:  # Ensure there are ingredients on the plate
            player.held_food = Burger(self.rect.x, self.rect.y, burger_img, self.ingredients.copy())
            print(f"plukket opp burger med ingredients: {self.ingredients}")
            self.ingredients.clear()
        else:
            print("ikkje noko ingredienser å plukke opp")

    def draw(self, screen):
        super().draw(screen)
        x_offset = -len(self.ingredients) * 10 // 2  # startpunkt for å sentrere ingrediensene
        for ingredient in self.ingredients:
            ingredient_x = self.rect.centerx - ingredient.image.get_width() // 2 + x_offset
            ingredient_y = self.rect.centery - ingredient.image.get_height() // 2
            screen.blit(ingredient.image, (ingredient_x, ingredient_y))
            x_offset += 20  # øker mellomrommet mellom ingredienser
        #if self.completed_burger:
            #screen.blit(burger_img, (self.rect.x, self.rect.y))

class DeliverStation(ActionStation):
    def __init__(self, x, y, width, height, in_use):
        super().__init__(x, y, width, height, in_use, cut=False)
        self.delivery_time = 0
        self.delivered_burger = False  #variabel for å vite om en burger er levert
        self.delivered_ingredients = []

    def deliver_burger(self, player, orders, score):
        if isinstance(player.held_food, Burger):
            self.delivered_ingredients = player.held_food.ingredients.copy()
            for order in orders:
                if order.check_order(player, self.delivered_ingredients):
                    score += 10 
                    orders.remove(order)
                    break
            self.delivered_burger = True
            player.held_food = None
            self.delivery_time = pg.time.get_ticks()

        return score  


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
        self.dx = 0
        self.dy = 0
        self.gravity = 0.2  
        self.friction = 0.95  
        self.y_start = self.rect.y
        self.cooldown_timer = 0
        self.cooldown_duration = 9000  

    def update(self):
        self.dy += self.gravity  
        self.dx *= self.friction  

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.y >= self.y_start:  
            self.dy = 0
            self.dx = 0
            self.rect.y = self.y_start  

        if self.cooldown_timer == 0:
            self.cooldown_timer = pg.time.get_ticks()
        elif pg.time.get_ticks() - self.cooldown_timer >= self.cooldown_duration:
            self.kill()  
        
        super().update()

class ThrownFood(pg.sprite.Sprite):
    def __init__(self, x, y, image, direction):
        super().__init__() 
        self.image = image 
        self.rect = self.image.get_rect(center=(x, y)) 
        self.vx = direction[0] * 6 
        self.vy = direction[1] * 5  -7
        self.gravity = 0.3  
        self.initial_y = y 
        self.time_on_ground = None 

    def update(self):
        self.vy += self.gravity 
        self.rect.x += self.vx  
        self.rect.y += self.vy  
        if self.rect.y >= self.initial_y:
            self.rect.y = self.initial_y  
            self.vy = 0  
            self.vx = 0 

        if self.time_on_ground is None:
            self.time_on_ground = pg.time.get_ticks()

        if self.time_on_ground is not None and pg.time.get_ticks() - self.time_on_ground >= 4000:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect) 

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
    def __init__(self, x, y, image, ingredients=None):  #Default til None
        super().__init__(x, y, image)
        self.ingredients = ingredients if ingredients is not None else []

#en funksjon jeg lekte meg med under litt prøving av hvordan å få ingrediensene på burgern til å stemme i lista
    #def add_ingredient(self, ingredient):
    #    print(f"legger til {ingredient} på burger")  #Debug
    #   self.ingredients.append(ingredient)

class Order:
    def __init__(self, x, y):
        self.x = x
        self.y = float(y)
        self.width = 120  
        self.height = 120
        self.ingredients = self.generate_order()
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.speed = 0.2
        self.background_color = (250, 250, 250)
        self.image = burger_img  

    def generate_order(self):
        base = ["Bread", "Patty"] 
        optional = ["Lettuce", "Tomato"]
        num_toppings = random.randint(1, len(optional))
        toppings = random.sample(optional, num_toppings) 
        return base + toppings

    def update(self):
        self.y += self.speed  
        self.rect.y = int(self.y) 
      
    def draw(self, screen):
        bg_rect = pg.Rect(self.rect.x, self.rect.y, self.width, self.height)
        pg.draw.rect(screen, self.background_color, bg_rect, border_radius=10)
        screen.blit(self.image, (self.rect.x + 10, self.rect.y + 10))  

        font = pg.font.Font(None, 24)
        for i, ingredient in enumerate(self.ingredients):
            text = font.render(ingredient, True, (0, 0, 0))  
            screen.blit(text, (self.rect.x + 50, self.rect.y + 10 + (i * 20)))

    def check_order(self, player,  delivered_ingredients):
        name_mapping = {
            "CookedPatty": "Patty",
            "RawPatty": "Patty",
            "TomatoSlice": "Tomato",
            "LettuceLeaf": "Lettuce"
        }
    
        delivered_ingredients = [
            name_mapping.get(ingredient.__class__.__name__, ingredient.__class__.__name__)  
            for ingredient in player.held_food.ingredients
        ]
        print(f"leverte ingredients: {delivered_ingredients}")
        print(f"bestillings ingredients: {self.ingredients}") #litt debugging
        

        if delivered_ingredients == self.ingredients:
            print("Correct order delivered! Score +10.")
            return True
        else:
            print("Incorrect order.")
            return False
        
    def check_out_of_screen(self, orders, score):
        if score is None:
            score = 0
        if self.rect.y > 600:  
            orders.remove(self)
            score -= 30
            print(f"the time ran out,  -30 points New score: {score}")
            return score
        return score
    
#Egt en unødvendig klasse, ble brukt under testing av kode    
#class OrderBurger:
#   def __init__(self, x, y, image, ingredients):
#        self.image = image
#        self.ingredients = ingredients #liste med hva som er på burgeren
#        self.rect = self.image.get_rect(center = (x,y))
