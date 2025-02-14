import pygame as pg
from constants import *
from pygame.locals import (K_w, K_s, K_d, K_a, K_UP,K_LCTRL, K_RCTRL, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_KP_ENTER, K_RSHIFT, K_LSHIFT)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SIZE)

from object import Player, Food, FoodStation
from bilder import *
import score_text

tomatoes = pg.sprite.Group()
tomato_station = FoodStation(715, 210, square_img)
bread = pg.sprite.Group()
bread_station = FoodStation(460, 480, square_img)
tomatoes = pg.sprite.Group()
meat_station = FoodStation(800, 100, square_img)
meat = pg.sprite.Group()



player1 = Player(500, 100, p1_d)
player2 = Player(400, 100, p2_d)


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

    tomato_station.draw(screen)
    bread_station.draw(screen)
    meat_station.draw(screen)
    # Flytter og tegner spilleren:
    player1.draw(screen)
    player2.draw(screen)

    
    player1.update(K_w, K_s, K_d, K_a, K_LCTRL, player2)
    player2.update(K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RCTRL, player1)

    #TODO: Komprimer funksjonen under

    # hvis spillere prøver å plukke opp tomat
    if player1.rect.colliderect(tomato_station.rect) and player1.action ==True:
        tomato_station.give_food(player1, Food, tomato_img)
    if player2.rect.colliderect(tomato_station.rect) and player2.action ==True:
        tomato_station.give_food(player2, Food, tomato_img)

    if player1.rect.colliderect(bread_station.rect) and player1.action ==True:
        bread_station.give_food(player1, Food, burgerbread_img)
    if player2.rect.colliderect(bread_station.rect) and player2.action ==True:
        bread_station.give_food(player2, Food, burgerbread_img)

    if player1.rect.colliderect(meat_station.rect) and player1.action ==True:
        meat_station.give_food(player1, Food, beef_img)
    if player2.rect.colliderect(meat_station.rect) and player2.action ==True:
        meat_station.give_food(player2, Food, beef_img)

    player1.throw(keys_pressed, K_LSHIFT, tomatoes)
    player2.throw(keys_pressed, K_RSHIFT, tomatoes)

    # hvis spillerne holder noe, tegnes det opp
    if player1.held_food:
        player1.held_food.draw(screen)
    if player2.held_food:
        player2.held_food.draw(screen)

    tomatoes.update()
    tomatoes.draw(screen)
    

    # Oppdater skjermen for å vise endringene:
    pg.display.update()


pg.quit()