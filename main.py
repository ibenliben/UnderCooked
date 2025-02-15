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

tomato_station = FoodStation(700, 250, square_img)
bread_station = FoodStation(650, 530, square_img)
lettuce_station = FoodStation(850, 530, square_img)
meat_station = FoodStation(780, 100, square_img)
plate_station = ActionStation(360, 530, square_img)
trash_station = ActionStation(330, 70, square_img)
cutting_station1 = ActionStation(510, 70,square_img)
cutting_station2 = ActionStation(590, 70,square_img)
cooking_station1 = ActionStation(970, 250,square_img)
cooking_station2 = ActionStation(970, 160,square_img)
deliver_station = ActionStation(240, 160,square_img)


player1 = Player(500, 100, p1_d)
player2 = Player(400, 100, p2_d)


# FUNKSJONER 

images1 = [p1_u, p1_d, p1_r, p1_l]
images2 = [p2_u, p2_d, p2_r, p2_l]
stations = [tomato_station, bread_station, meat_station, plate_station, cutting_station1, cutting_station2, 
            cooking_station1, cooking_station2, trash_station, lettuce_station, deliver_station]

def draw_stations(stations):
    for station in stations:
        station.draw(screen)

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

    draw_stations(stations)

    # Flytter og tegner spilleren:
    player1.draw(screen)
    player2.draw(screen)

    
    player1.update(images1, K_w, K_s, K_d, K_a, K_SPACE, player2)
    player2.update(images2 , K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, player1)
    #cutting_station1.update(player1)
    #cutting_station1.update(player2)

    # hvis spiller vil plukke fra mat-stasjon
    food_from_station(tomato_station, Tomato, tomato_img)
    food_from_station(lettuce_station, Lettuce, lettuce_img)
    food_from_station(meat_station, RawMeat, beef_img)
    food_from_station(bread_station, Bread, burgerbread_img)


    #tomato_station.use_station(player1, Tomato, tomato_img)    Kommenterer disse linjene vekk midlertidig, 
    #tomato_station.use_station(player2, Tomato, tomato_img)

    use_station(cutting_station1)
    use_station(cutting_station2)
    use_station(trash_station)
    use_station(cooking_station1)
    use_station(cooking_station2)

    update_station(cutting_station1)
    update_station(cutting_station2)
    update_station(cooking_station1)
    update_station(cooking_station2)

    player1.throw(keys_pressed, K_LSHIFT, thrown_food)
    player2.throw(keys_pressed, K_RSHIFT, thrown_food)

    # hvis spillerne holder noe, tegnes det opp
    if player1.held_food:
        player1.held_food.draw(screen)
    if player2.held_food:
        player2.held_food.draw(screen)

    thrown_food.update()
    thrown_food.draw(screen)
    

    # Oppdater skjermen for å vise endringene:
    pg.display.update()


pg.quit()
