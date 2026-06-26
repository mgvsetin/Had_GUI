# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram
"""_summary_
Vytvořte jednoduchou verzi hry "Had" v terminálu.  
Cílem hry je pohybovat hadem po hrací ploše, sbírat jídlo a vyhýbat se 
překážkám (stěnám a vlastnímu tělu).  

## Zadání úlohy  
Vaším úkolem je naprogramovat hru "Had", která:  
1. Zobrazí hrací plochu (mřížka) o rozměrech 20x10 (šířka x výška) v terminálu.  
2. Na této ploše bude:  
   - **Had** reprezentovaný znakem `O` (hlava) a `o` (tělo).  
   - **Jídlo** reprezentované znakem `*`.  
3. Had se pohybuje v jednom ze čtyř směrů:  
   - `W`: nahoru.  
   - `S`: dolů.  
   - `A`: doleva.  
   - `D`: doprava.  
4. Pokud had sní jídlo (`*`):  
   - Jeho délka se zvětší o jeden dílek.  
   - Jídlo se přemístí na náhodné VOLNÉ místo na hrací ploše.  
5. Hra končí, pokud:  
   - Had narazí do stěny (hranic hrací plochy).  
   - Had narazí do svého vlastního těla.  
6. Program běží nepřetržitě, dokud hra neskončí nebo hráč manuálně 
neukončí program (např. `Ctrl+C`).  

## Funkčnost  
1. **Hrací plocha**:  
   - Hrací plocha bude dvourozměrná mřížka s rozměry 20x10.  
   - Každé pole na ploše obsahuje jeden ze znaků:  
     - `O`: hlava hada.  
     - `o`: tělo hada.  
     - `*`: jídlo.  
     - ` `: prázdné pole.  

2. **Pohyb hada**:  
   - Had se pohybuje o jedno políčko v aktuálním směru.  
   - Směr se mění podle vstupu uživatele (`w`, `a`, `s`, `d`).  

3. **Jídlo**:  
   - Jídlo se objeví na náhodné volné pozici na hrací ploše.  
   - Pokud had sní jídlo, jeho délka se zvětší o jeden dílek.  

4. **Konec hry**:  
   - Hra končí, pokud:  
     - Had narazí do stěny (pozice mimo hrací plochu).  
     - Had narazí do svého vlastního těla (pozice hlavy hada se překrývá s tělem).  

## Uživatelské vstupy  
- Hráč ovládá hada pomocí kláves:  
  - `W`: pohyb nahoru.  
  - `S`: pohyb dolů.  
  - `A`: pohyb doleva.  
  - `D`: pohyb doprava.  

"""

import os
import random
import time
import threading
import keyboard


##############################################################
# Globální proměnné

BOARD_WIDTH = 20  # Šířka hrací plochy
BOARD_HEIGHT = 20  # Výška hrací plochy
SNAKE_SYMBOL = "x" 
HEAD_SYMBOL =  "O"
FOOD_SYMBOL = "+"
EMPTY_SYMBOL = " "
DIRECTION = "RIGHT"  # Výchozí směr
SNAKE = [(5, 5), (5, 4), (5, 3)]  # Výchozí pozice hada (hlava -> ocas)
FOOD = (7, 7)  # Výchozí pozice jídla
DELAY = 0.2
GAME_OVER = False


##############################################################
# Funkce pro inicializaci hry
# initialize_game()


##############################################################
# Funkce pro vykreslení aktuálního stavu hrací plochy
# render_board()


##############################################################
# Funkce pro umístění potravy
# place_food()


##############################################################
# Funkce, která posune hada dle kláves, ověří kolizi, prodlouží
# move_snake()


##############################################################
# Hlavní herní smyčka
# game_loop()


##############################################################
# Načtení klávesy od uživatele, knihovna keyboard
# Do smyčky je vhodné přidat time.sleep(0.01)
# funkce pro paralelní zpracování vstupu od uživatele - viz závěrečná část kódu
# get_input()


##############################################################
### Spuštění programu - MAIN

if __name__ == "__main__":
    initialize_game()

    # Vytvoření vlákna pro detekci vstupu
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()

    # Spuštění herní smyčky
    game_loop()