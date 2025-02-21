import pygame as pg
from constants import *
from pygame.locals import (K_w, K_s, K_d, K_a, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_RETURN, K_RSHIFT, K_LSHIFT)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SIZE)

from object import *
from bilder import *
import score_text

thrown_food = pg.sprite.Group()
meat = pg.sprite.Group()
bread = pg.sprite.Group()
wall_list = pg.sprite.Group()
station_list = pg.sprite.Group()

# STATIONS
tomato_station = FoodStation(670, 250, 110, 60)
bread_station = FoodStation(650, 520, 60, 60)
lettuce_station = FoodStation(850, 520, 60, 60)
meat_station = FoodStation(780, 100, 60, 60)

cutting_station1 = ActionStation(510, 70, 50, 70, True)
cutting_station2 = ActionStation(590, 70, 50, 70, True)
cooking_station1 = ActionStation(965, 250, 80, 40, True)
cooking_station2 = ActionStation(965, 160, 80, 40, True)
plate_station = PlateStation(330, 520, 150, 70, False)
deliver_station = DeliverStation(240, 160, 70, 150, False)

trash_station = ActionStation(330, 70, 50, 70, False)

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
    # Sjekker om brukeren avslutter vinduet:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            keys_pressed.append(event.key)
            
    clock.tick(FPS)

    # Tegner bakgrunnsbildet:
    screen.blit(bg_img, (0, 0))

    # TODO: Skriv inn "score"/penger og tid


    # Flytter og tegner spilleren:
    player1.draw(screen)
    player2.draw(screen)

    player1.update(images1, K_w, K_s, K_d, K_a, K_SPACE, player2, wall_list)
    player2.update(images2 , K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, player1, wall_list)


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

    # Oppdater skjermen for å vise endringene:
    pg.display.update()


pg.quit()
