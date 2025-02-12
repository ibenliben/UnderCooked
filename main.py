import pygame as pg
from constants import *
from pygame.locals import (K_w, K_s, K_d, K_a, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_KP_ENTER, K_RSHIFT, K_LSHIFT)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SIZE)
tomatoes = pg.sprite.Group()

from object import Object, Player, Food
from bilder import *
import score_text

player1 = Player(200, 100, player1_d)
player2 = Player(400, 100, player2_d)


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
    
    player1.update(K_w, K_s, K_d, K_a)
    player2.update(K_UP, K_DOWN, K_RIGHT, K_LEFT)

    player1.throw(keys_pressed, K_LSHIFT, tomatoes)
    player2.throw(keys_pressed, K_RSHIFT, tomatoes)

    tomatoes.update()
    tomatoes.draw(screen)
    

    # Oppdater skjermen for å vise endringene:
    pg.display.update()


pg.quit()