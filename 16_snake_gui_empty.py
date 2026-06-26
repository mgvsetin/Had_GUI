# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram
"""_summary_
Vytvořte grafickou verzi hry Had v okně pomocí knihovny tkinter.

## Zadání úlohy
Vaším úkolem je naprogramovat hru Had jako okenní aplikaci, která:
1. Otevře grafické okno s hrací plochou 20x20 políček.
2. Na hrací ploše (Canvas) zobrazí:
   - Hada složeného z dílků (hlava odlišena barvou od těla).
   - Jídlo na náhodném volném políčku.
3. Had se pohybuje pomocí šipek na klávesnici.
4. Po snězení jídla:
   - Had se prodlouží o jeden dílek.
   - Jídlo se přemístí na nové náhodné volné políčko.
5. Hra končí, pokud:
   - Had narazí do stěny (hranice hrací plochy).
   - Had narazí do vlastního těla.
6. Po konci hry se zobrazí zpráva s dosaženým skóre.

## Bonusové rozšíření
* Zobrazení skóre během hry
* Restart hry klávesou R
* Postupné zrychlování hry
* Zobrazení mřížky
* Barevné přizpůsobení
"""

import tkinter as tk
import random

##############################################################
# Globální konstanty (neměňte)

CELL_SIZE    = 25        # Velikost jednoho políčka v pixelech
BOARD_WIDTH  = 20        # Počet políček horizontálně
BOARD_HEIGHT = 20        # Počet políček vertikálně

# Barvy
COLOR_BG         = "black"
COLOR_HEAD       = "lime green"
COLOR_BODY       = "green"
COLOR_FOOD       = "red"
COLOR_TEXT       = "white"
COLOR_GRID       = "#1a1a1a"

##############################################################
# Globální herní proměnné

SNAKE:     list  = [(10, 10), (10, 9), (10, 8)]  # [(y,x), ...] hlava první
FOOD:      tuple = (5, 5)                         # (y, x)
DIRECTION: str   = "RIGHT"                        # Výchozí směr pohybu
SCORE:     int   = 0
DELAY:     int   = 200                            # ms mezi tiky
GAME_OVER: bool  = False

##############################################################
# Globální reference na okno a Canvas (vytvoří se v MAIN)

window: tk.Tk     = None   # type: ignore
canvas: tk.Canvas = None   # type: ignore

##############################################################
# Funkce pro inicializaci (reset) herního stavu
# initialize_game()

##############################################################
# Funkce pro vykreslení stavu hry na Canvas
# render_board()
# Nápověda: canvas.delete("all"), canvas.create_rectangle(), canvas.create_oval(), canvas.create_text()

##############################################################
# Funkce pro umístění jídla na náhodné volné políčko
# place_food()

##############################################################
# Funkce pro pohyb hada, kontrolu kolizí a růst
# move_snake()

##############################################################
# Funkce pro zpracování stisku klávesy (event handler)
# change_direction(event)
# Nápověda: event.keysym obsahuje název klávesy ("Up", "Down", "Left", "Right")

##############################################################
# Jeden herní tik — orchestrace (volá se přes window.after)
# game_step()
# Nápověda: window.after(DELAY, game_step)

##############################################################
### Spuštění programu - MAIN

if __name__ == "__main__":
    initialize_game()

    # Vytvoření okna
    window = tk.Tk()
    window.title("Had — GUI")
    window.resizable(False, False)

    # Vytvoření hrací plochy
    canvas = tk.Canvas(
        window,
        width=BOARD_WIDTH * CELL_SIZE,
        height=BOARD_HEIGHT * CELL_SIZE,
        bg=COLOR_BG,
    )
    canvas.pack()

    # Registrace kláves — doplňte zbývající šipky
    window.bind("<Up>",    change_direction)
    window.bind("<Down>",  change_direction)
    window.bind("<Left>",  change_direction)
    window.bind("<Right>", change_direction)

    # První naplánování herního tiku
    window.after(DELAY, game_step)

    # Spuštění hlavní smyčky Tkinteru
    window.mainloop()
