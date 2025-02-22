import pygame as pg
from constants import *
from pygame.locals import (K_w, K_s, K_d, K_a, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_RETURN, K_RSHIFT, K_LSHIFT, K_LCTRL, K_RCTRL)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SIZE)

from object import *
from bilder import *
import score_text

orders = []
spawn_timer = 0
score = 0
font = pg.font.Font(None, 36)
spawn_interval = 1000 #hvor ofte det skal komme en ny bestilling, (i frames)

thrown_food = pg.sprite.Group()
meat = pg.sprite.Group()
bread = pg.sprite.Group()
wall_list = pg.sprite.Group()
station_list = pg.sprite.Group()

# STATIONS
tomato_station = FoodStation(670, 250, 110, 60)
bread_station = FoodStation(650, 500, 60, 60)
lettuce_station = FoodStation(850, 500, 60, 60)
meat_station = FoodStation(780, 100, 60, 60)

cutting_station1 = ActionStation(510, 70, 50, 70, True, True)
cutting_station2 = ActionStation(590, 70, 50, 70, True, True)
cooking_station1 = ActionStation(965, 250, 80, 40, True, False)
cooking_station2 = ActionStation(965, 160, 80, 40, True, False)
plate_station = PlateStation(330, 500, 150, 70, False)
deliver_station = DeliverStation(240, 160, 70, 150, False)

trash_station = ActionStation(330, 70, 50, 70, False, False)

stations = [tomato_station, bread_station, meat_station, plate_station, cutting_station1, cutting_station2, 
            cooking_station1, cooking_station2, trash_station, lettuce_station, deliver_station]
for station in stations:
    station_list.add(station)

player1 = Player(400, 200, p1_d)
player2 = Player(830, 200, p2_d)

#VEGGER
topwall = Wall(215, 48, HORIZONTAL_WALL_WIDTH, HORIZONTAL_WALL_HEIGHT)
wall_list.add(topwall)
bottomwall = Wall(215, 535, HORIZONTAL_WALL_WIDTH, HORIZONTAL_WALL_HEIGHT)
wall_list.add(bottomwall)
lefttwall = Wall(215, 70, SIDEWALL_WIDTH, SIDEWALL_HEIGHT)
wall_list.add(lefttwall)
rightwall = Wall(970, 70, SIDEWALL_WIDTH, SIDEWALL_HEIGHT)
wall_list.add(rightwall)
middle_wall_v = Wall(680, 115, 75, 276)
wall_list.add(middle_wall_v)
middle_wall_h = Wall(501, 341, 254, 60)
wall_list.add(middle_wall_h)

# FUNKSJONER 
images1 = [p1_u, p1_d, p1_r, p1_l]
images2 = [p2_u, p2_d, p2_r, p2_l]


def food_from_station(station, food_class, food_img):
    if player1.rect.colliderect(station.rect) and player1.action ==True:
        tomato_station.give_food(player1, food_class, food_img)
    if player2.rect.colliderect(station.rect) and player2.action ==True:
        tomato_station.give_food(player2, food_class, food_img)

def use_station(station):
    if player1.rect.colliderect(station.rect) and player1.action and player1.held_food is not None:
        station.use_station(player1)
    if player2.rect.colliderect(station.rect) and player2.action and player2.held_food is not None:
        station.use_station(player2)

def update_station(station):
    if station.in_use:  
            station.update(player1 if not player1.can_move else player2)
    station.draw(screen) 

running = True
while running:
    keys_pressed = []
    #keys_pressed = pg.key.get_pressed()       -> for å holde taster inne isteden for å trykke 
    # Sjekker om brukeren avslutter vinduet:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            keys_pressed.append(event.key)
            
    clock.tick(FPS)

    # Tegner bakgrunnsbildet:
    screen.blit(bg_img, (0, 0))

    # Flytter og tegner spilleren:
    player1.draw(screen)
    player2.draw(screen)

    player1.update(images1, K_w, K_s, K_d, K_a, K_SPACE, K_LCTRL, player2, wall_list)
    player2.update(images2 , K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, K_RCTRL, player1, wall_list)


    wall_list.draw(screen)
    station_list.draw(screen)

    # hvis spiller vil plukke fra mat-stasjon
    food_from_station(tomato_station, Tomato, tomato_img)
    food_from_station(lettuce_station, Lettuce, lettuce_img)
    food_from_station(meat_station, RawMeat, beef_img)
    food_from_station(bread_station, Bread, burgerbread_img)

    use_station(cutting_station1)
    use_station(cutting_station2)
    use_station(cooking_station1)
    use_station(cooking_station2)
    use_station(trash_station)

    update_station(cutting_station1)
    update_station(cutting_station2)
    update_station(cooking_station1)
    update_station(cooking_station2)
    update_station(trash_station)

# plate og deliver station
    if player1.rect.colliderect(plate_station.rect) and player1.action:
        plate_station.place_ingredient(player1)

    if player2.rect.colliderect(plate_station.rect) and player2.action:
        plate_station.place_ingredient(player2)

    if player1.rect.colliderect(plate_station.rect) and player1.plateAction:
        plate_station.pick_up_burger(player1)

    if player2.rect.colliderect(plate_station.rect) and player2.plateAction:
        plate_station.pick_up_burger(player2)

    if player1.rect.colliderect(deliver_station.rect) and player1.action:
        score = deliver_station.deliver_burger(player1, orders, score)

    if player2.rect.colliderect(deliver_station.rect) and player2.action:
        score = deliver_station.deliver_burger(player2, orders, score)  


    plate_station.draw(screen)
    deliver_station.draw(screen)
    deliver_station.update()

    player1.throw(keys_pressed, K_LSHIFT, thrown_food)
    player2.throw(keys_pressed, K_RSHIFT, thrown_food)

    # hvis spillerne holder noe, tegnes det opp
    if player1.held_food:
        player1.held_food.draw(screen)
    if player2.held_food:
        player2.held_food.draw(screen)
    
    for food in thrown_food:
        food.update()
        food.draw(screen)

    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        orders.append(Order(10,10))
        spawn_timer = 0 

    for order in orders:
        order.update()
        order.draw(screen)
        score = order.check_out_of_screen(orders, score) #sjekker om bestillingen har gått av skjermen og fjerner den evt 

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    outline_text = font.render(f"Score: {score}", True, (0, 0, 0))
    for dx in [-2, 0, 2]:  
        for dy in [-2, 0, 2]:  
            if dx != 0 or dy != 0:  
                screen.blit(outline_text, (600 + dx, 10 + dy))
    screen.blit(score_text, (600, 10))
   

    pg.display.update()

pg.quit()
