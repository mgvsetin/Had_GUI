# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram
"""_summary_
Vytvořte jednoduchou terminálovou aplikaci, která umožní hráči ovládat pohybující se 
kostičku (O) po hrací ploše. Cílem je sebrat co nejvíce hvězdiček (*) umístěných 
na hrací ploše.

Zadání úlohy
Vaším úkolem je vytvořit program, který:
Zobrazí hrací plochu (mřížka) o rozměrech 20x10 (šířka x výška) v terminálu.

Na této ploše bude:
Hráč reprezentovaný symbolem O, který se pohybuje pomocí kláves:
W pro pohyb nahoru.
S pro pohyb dolů.
A pro pohyb doleva.
D pro pohyb doprava.
Hvězdička (*), která se náhodně umístí na volné políčko hrací plochy.
Hráč začne na výchozí pozici (5, 5). Pohyb je omezen hranicemi plochy. 
Hráč se nemůže dostat mimo hrací plochu.

Pokud hráč dojde k hvězdičce (*), jeho skóre se zvýší o 1 
a hvězdička se přemístí na nové náhodné volné políčko.
Hrací plocha se bude v reálném čase aktualizovat, 
aby bylo vidět aktuální pozici hráče i hvězdičky.

Hra bude pokračovat neomezeně dlouho, dokud ji hráč 
manuálně neukončí (např. stiskem Ctrl+C).

* doplňte okraje herní plochy
* doplňte počítadlo pohybu hráče
* barevné kreace


"""

import os
import random
import time
import keyboard


##############################################################
# Globální proměnné

BOARD_WIDTH = 20  # Šířka hrací plochy
BOARD_HEIGHT = 10  # Výška hrací plochy
PLAYER_SYMBOL = "O"
FOOD_SYMBOL = "X"
EMPTY_SYMBOL = "."
PLAYER_POS = (5, 5)  # Výchozí pozice hráče
FOOD_POS = (7, 7)  # Výchozí pozice hvězdičky
SCORE = 0
DELAY = 0.1
GAME_OVER = False


##############################################################
# Funkce pro vykreslení hrací plochy
# render_board()


##############################################################
# Funkce pro umístění hvězdičky
# place_food()


##############################################################
# Funkce pro pohyb hráče
# move_player(direction)


##############################################################
# Hlavní herní smyčka
# game_loop()


##############################################################
### Spuštění programu - MAIN

if __name__ == "__main__":
    print("Použijte klávesy W, A, S, D pro pohyb. Stiskněte Ctrl+C pro ukončení.")
    
    FOOD_POS = place_food()
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nHra ukončena. Děkujeme za hraní!")