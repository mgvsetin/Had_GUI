# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram
"""_summary_
Vytvořte grafickou verzi hry Had v Pygame — přepis projektu 16 (Tkinter)
do herní knihovny Pygame.

## Zadání úlohy
Vaším úkolem je naprogramovat hru Had jako okenní aplikaci v Pygame, která:
1. Otevře grafické okno s hrací plochou 20×20 políček.
2. Na hrací ploše zobrazí hada a jídlo jako barevné obdélníky/kruhy.
3. Had se pohybuje pomocí šipek (nebo WASD) na klávesnici.
4. Po snězení jídla se had prodlouží a jídlo se přesune.
5. Hra končí nárazem do stěny nebo vlastního těla.
6. Po konci hry se zobrazí skóre a možnost restartu (klávesa R).

## Bonusové rozšíření
* Postupné zrychlování hry (zvyšující se FPS)
* Zobrazení mřížky
* Úvodní obrazovka před startem hry
* Vlastní barevné zpracování
"""

import pygame
import sys
import random

##############################################################
# Globální konstanty (neměňte)

CELL_SIZE    = 25        # Velikost jednoho políčka v pixelech
BOARD_WIDTH  = 20        # Počet políček horizontálně
BOARD_HEIGHT = 20        # Počet políček vertikálně
FPS          = 7         # Výchozí rychlost hry (snímků za sekundu)

# Barvy jako RGB trojice (R, G, B)
COLOR_BG    = (15,  15,  15)
COLOR_HEAD  = (50,  220,  50)
COLOR_BODY  = (0,   160,   0)
COLOR_FOOD  = (220,  50,  50)
COLOR_GRID  = (30,   30,  30)
COLOR_TEXT  = (255, 255, 255)
COLOR_SCORE = (255, 220,   0)

##############################################################
# Globální herní proměnné

SNAKE:     list  = [(10, 10), (10, 9), (10, 8)]  # [(y,x), ...] hlava první
FOOD:      tuple = (5, 5)                         # (y, x)
DIRECTION: str   = "RIGHT"
SCORE:     int   = 0
GAME_OVER: bool  = False

##############################################################
# Globální reference na pygame objekty (vytvoří se v MAIN)

screen:     pygame.Surface    = None  # type: ignore
clock:      pygame.time.Clock = None  # type: ignore
font_score: pygame.font.Font  = None  # type: ignore
font_end:   pygame.font.Font  = None  # type: ignore

##############################################################
# Funkce pro inicializaci (reset) herního stavu
# initialize_game()

##############################################################
# Funkce pro vykreslení stavu hry na screen
# render_board()
# Nápověda: screen.fill(), pygame.draw.rect(), pygame.draw.circle(),
#            font.render(), screen.blit(), pygame.display.flip()

##############################################################
# Funkce pro umístění jídla na náhodné volné políčko
# place_food()

##############################################################
# Funkce pro pohyb hada, kontrolu kolizí a růst
# move_snake()

##############################################################
# Funkce pro zpracování konstanty stisknuté klávesy
# change_direction(key: int)
# Nápověda: pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT

##############################################################
# Hlavní herní smyčka — obsahuje while running:
# game_loop()
# Struktura: for event in pygame.event.get() → logika → render → clock.tick(FPS)

##############################################################
### Spuštění programu - MAIN

if __name__ == "__main__":
    pygame.init()
    initialize_game()

    # Vytvoření okna
    screen = pygame.display.set_mode((BOARD_WIDTH * CELL_SIZE,
                                      BOARD_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Had — Pygame")

    # Hodiny pro řízení FPS
    clock = pygame.time.Clock()

    # Fonty — vytvořte jednou zde, nikoli uvnitř herní smyčky!
    font_score = pygame.font.SysFont("Arial", 16)
    font_end   = pygame.font.SysFont("Arial", 30, bold=True)

    # Spuštění herní smyčky
    game_loop()
