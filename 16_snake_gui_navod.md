# Průvodce implementací hry Had v grafickém okně (Tkinter)

> **Tento dokument je váš průvodce, ne tahák.** Záměrně neobsahuje hotové řešení. Obsahuje vysvětlení konceptů Tkinteru, schémata, ukázky na analogických problémech a upozornění na místa, kde se nejčastěji chybuje.
>
> Pokud jste prošli projekty `14` (Move) a `15` (Snake terminál), herní logiku — pohyb hada, kolize, generování jídla — **již znáte**. Nová věc je pouze to, kde se výsledek zobrazuje: místo textu v terminálu kreslíme barevné tvary do grafického okna.

---

## Co je Tkinter a jak funguje

Tkinter je grafická knihovna, která je **přímo součástí Pythonu** — není potřeba nic instalovat. Umožňuje vytvářet okna, tlačítka, textová pole a plátna pro kreslení.

Každá Tkinter aplikace stojí na jednom základním principu: **hlavní smyčka událostí** (`mainloop`). Program neskončí po posledním řádku kódu — místo toho vstoupí do smyčky, která neustále čeká na události (klik myší, stisk klávesy, uplynutí časovače) a reaguje na ně voláním funkcí, které jste předem zaregistrovali.

```
Váš kód:                    Tkinter mainloop:
  Vytvoř okno                  ┌─────────────────────────┐
  Vytvoř Canvas         →      │  Čekám na událost...    │
  Zaregistruj klávesy          │  → Stisknuta šipka vpravo│
  Naplánuj první tik           │    → Zavolám change_dir()│
  window.mainloop()            │  → Uběhlo 200 ms         │
                               │    → Zavolám game_step() │
                               │  → Stisknuta šipka dolů  │
                               │    → Zavolám change_dir()│
                               └─────────────────────────┘
```

Celá hra se tedy skládá ze dvou typů funkcí:
- **Funkce herní logiky** (pohyb, kolize, jídlo) — znáte je z projektu 15.
- **Funkce Tkinteru** (vytvoření okna, kreslení na Canvas, registrace kláves, časovač).

---

## Přehled projektu a pracovní postup

### Doporučené pořadí implementace

```
1. Vytvoření okna a Canvas          →  Vidíte prázdné okno (ověření, že vše funguje)
2. render_board()                   →  Vykreslení hada a jídla na Canvas
3. place_food()                     →  Generování náhodné pozice jídla
4. move_snake()                     →  Herní logika pohybu, kolize, růst
5. change_direction()               →  Zpracování vstupu z klávesnice
6. game_step()                      →  Jeden tik hry (orchestrace)
7. Registrace kláves + spuštění     →  Propojení všeho dohromady
```

### Klíčové konstanty, které budete potřebovat

```python
CELL_SIZE   = 25      # Velikost jednoho políčka v pixelech
BOARD_WIDTH = 20      # Počet políček horizontálně
BOARD_HEIGHT= 20      # Počet políček vertikálně
DELAY       = 200     # Prodleva mezi tiky v milisekundách
```

Velikost okna v pixelech je pak `BOARD_WIDTH * CELL_SIZE` × `BOARD_HEIGHT * CELL_SIZE` = 500 × 500 px.

---

## Fáze 1 — Vytvoření okna a Canvas

### Co je Canvas?

`Canvas` je widget Tkinteru, který funguje jako **kreslicí plátno**. Kreslíte na něj geometrické tvary — obdélníky, kruhy, čáry — pomocí metod jako `.create_rectangle()` nebo `.create_oval()`. Každý nakreslený tvar dostane unikátní ID, pomocí kterého ho lze později přesunout nebo smazat.

### Minimální funkční Tkinter okno

Toto je nejmenší možný kód, který otevře okno s plátnem. Studujte ho řádek po řádku:

```python
import tkinter as tk

# 1. Vytvoření hlavního okna
window = tk.Tk()
window.title("Had")                   # Titulek okna

# 2. Vytvoření Canvas a jeho vložení do okna
canvas = tk.Canvas(
    window,                           # Rodičovský widget (okno)
    width=500,                        # Šířka v pixelech
    height=500,                       # Výška v pixelech
    bg="black"                        # Barva pozadí
)
canvas.pack()                         # Zobrazení widgetu v okně

# 3. Spuštění hlavní smyčky — BEZ TOHOTO okno okamžitě zavře
window.mainloop()
```

> **Spusťte tento kód jako první krok.** Pokud se okno otevře a zůstane otevřené, máte základ. Teprve poté pokračujte dál.

### Jak kreslit na Canvas — souřadnice v pixelech

Na Canvasu se pracuje v **pixelech**, ne v políčkách. Levý horní roh je `(0, 0)`. Převod z políčkových souřadnic `(gx, gy)` na pixelové je jednoduchý:

```
pixel_x = gx * CELL_SIZE
pixel_y = gy * CELL_SIZE
```

Obdélník jednoho políčka na pozici `(gx, gy)` tedy zabírá oblast od `(gx*CELL_SIZE, gy*CELL_SIZE)` do `((gx+1)*CELL_SIZE, (gy+1)*CELL_SIZE)`.

```python
# Analogický příklad — nakreslení jednoho zeleného čtverce na pozici (3, 2)
CELL_SIZE = 25
gx, gy = 3, 2

x1 = gx * CELL_SIZE         # = 75
y1 = gy * CELL_SIZE         # = 50
x2 = (gx + 1) * CELL_SIZE  # = 100
y2 = (gy + 1) * CELL_SIZE  # = 75

canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
```

### Vymazání Canvas před překreslením

Před každým překreslením scény smažte vše, co je na Canvasu nakresleno:

```python
canvas.delete("all")    # Smaže všechny nakreslené objekty
```

---

## Fáze 2 — Vykreslování: `render_board()`

### Co má tato funkce dělat?

Smazat Canvas a znovu nakreslit:
1. Tělo hada (článek po článku jako obdélníky).
2. Hlavu hada (odlišnou barvou).
3. Jídlo (jinou barvou nebo tvarem).
4. Skóre nebo statistiky jako text.

### Algoritmus

```
canvas.delete("all")

Pro každý článek v SNAKE (kromě prvního):
    Nakresli obdélník na canvas (barva těla)

Nakresli obdélník pro SNAKE[0] (barva hlavy — odlišná)

Nakresli obdélník/oval pro FOOD (barva jídla)

Nakresli text se skóre
```

### Jak kreslit text na Canvas

```python
# Analogický příklad — text uprostřed nahoře
canvas.create_text(
    250,                    # x souřadnice středu textu
    10,                     # y souřadnice středu textu
    text=f"Skóre: {SCORE}",
    fill="white",           # Barva textu
    font=("Arial", 14)      # Font a velikost
)
```

### Jak nakreslit oval místo obdélníku (pro jídlo)

```python
# create_oval kreslí elipsu/kruh do ohraničujícího obdélníku
canvas.create_oval(x1, y1, x2, y2, fill="red", outline="")
# outline="" = bez ohraničení
```

### Časté úskalí

- Pořadí kreslení záleží — co nakreslíte jako poslední, bude navrchu. Jídlo kreslete před hadem, hlavu hada kreslete jako poslední, aby byl vždy viditelný.
- Souřadnice v `SNAKE` jsou stále v políčkách `(y, x)` — při volání `create_rectangle` je nutno převést na pixely.
- Nezapomeňte na malý vnitřní offset (např. 1–2 px) pro `outline` nebo mezeru mezi políčky — hra pak vizuálně vypadá lépe.

---

## Fáze 3 — Generování jídla: `place_food()`

Tato funkce je identická s projektem 15. Vygenerujte náhodnou pozici `(y, x)`, která **neleží** v žádném článku `SNAKE`, a přiřaďte ji do globální proměnné `FOOD`.

```python
# Připomenutí — analogický příklad ze projektu 15
import random

while True:
    y = random.randint(0, BOARD_HEIGHT - 1)
    x = random.randint(0, BOARD_WIDTH - 1)
    if (y, x) not in SNAKE:
        FOOD = (y, x)
        break
```

Oproti projektu 15 zde není žádná změna logiky. Rozdíl je pouze v tom, že výsledek uvidíte jako červený kruh na Canvas, ne jako `+` v terminálu.

---

## Fáze 4 — Herní logika: `move_snake()`

Tato funkce je opět téměř totožná s projektem 15. Zkopírujte logiku a upravte pouze reference na globální proměnné (název okna, Canvas apod. se zde nemění — `move_snake()` s nimi nepracuje).

### Připomenutí schématu pohybu

```
PŘED:  SNAKE = [(5,5), (5,4), (5,3)]   DIRECTION = "RIGHT"

1. Nová hlava: (5, 5+1) = (5, 6)
2. Kolize se stěnou? → y<0 nebo y>=20 nebo x<0 nebo x>=20 → GAME_OVER
3. Kolize s tělem?   → (5,6) in SNAKE → GAME_OVER
4. SNAKE.insert(0, (5, 6))
5. Snědl jídlo?      → SNAKE[0] == FOOD → place_food(), SCORE+=1
   Jinak             → SNAKE.pop()

PO:    SNAKE = [(5,6), (5,5), (5,4)]
```

### Co je v GUI verzi jinak

- `GAME_OVER` se nastavuje stejně jako v projektu 15.
- Funkce **neřídí zpomalení** (`time.sleep` se zde nepoužívá) — tempo hry zajišťuje `.after()` v herní smyčce.
- Po nastavení `GAME_OVER = True` funkce vrátí řízení zpět do `game_step()`, která pak zobrazí zprávu o konci.

---

## Fáze 5 — Zpracování vstupu: `change_direction()`

### Jak registrovat klávesy v Tkinteru

Tkinter používá systém **bindování** — přiřazení funkce k události. Událost klávesy má formát `"<KeyPress-název>"` nebo zkráceně `"<název>"`.

```python
# Analogický příklad — reakce na různé klávesy
def po_stisku(event):
    """Zavolá se při stisku libovolné registrované klávesy."""
    print(f"Stisknuto: {event.keysym}")   # keysym = název klávesy jako řetězec

# Registrace kláves na okno (window musí existovat)
window.bind("<Up>",    po_stisku)    # Šipka nahoru
window.bind("<Down>",  po_stisku)    # Šipka dolů
window.bind("<Left>",  po_stisku)    # Šipka vlevo
window.bind("<Right>", po_stisku)    # Šipka vpravo
window.bind("<w>",     po_stisku)    # Klávesa W (malé)
window.bind("<W>",     po_stisku)    # Klávesa W (velké)
```

> `event.keysym` je řetězec s názvem klávesy: `"Up"`, `"Down"`, `"Left"`, `"Right"`, `"w"`, `"s"` atd.

### Jak napsat `change_direction()`

Funkce dostane objekt `event` a podle `event.keysym` nastaví nový směr. Musí přitom kontrolovat pravidlo **zákazu obratu o 180°** — stejně jako v projektu 15.

```python
# Analogický příklad — zpracování šipek a validace protisměru
OPACNE_SMERY = {
    "UP": "DOWN", "DOWN": "UP",
    "LEFT": "RIGHT", "RIGHT": "LEFT"
}

def ukazka_zmeny_smeru(event) -> None:
    """Ukázka: změna směru na základě stisknuté klávesy."""
    global DIRECTION

    mapovani = {
        "Up": "UP", "Down": "DOWN",
        "Left": "LEFT", "Right": "RIGHT",
        "w": "UP", "s": "DOWN",
        "a": "LEFT", "d": "RIGHT",
    }
    novy_smer = mapovani.get(event.keysym)   # None, pokud klávesa není v mapě

    if novy_smer and novy_smer != OPACNE_SMERY[DIRECTION]:
        DIRECTION = novy_smer
```

### Kde zaregistrovat klávesy?

V části `MAIN`, **před** spuštěním `window.mainloop()`:

```python
window.bind("<Up>",    change_direction)
window.bind("<Down>",  change_direction)
window.bind("<Left>",  change_direction)
window.bind("<Right>", change_direction)
```

---

## Fáze 6 — Herní tik: `game_step()`

Toto je **klíčová funkce GUI verze** a nahrazuje `game_loop()` z projektu 15. Místo nekonečné smyčky `while True` se tato funkce zavolá vždy po uplynutí `DELAY` milisekund, provede jeden herní tik a pak **naplánuje své vlastní další zavolání**.

### Mechanismus `.after()`

```python
# Analogický příklad — odpočítávání pomocí .after()
import tkinter as tk

window = tk.Tk()
label = tk.Label(window, text="Čekám...", font=("Arial", 20))
label.pack()

pocitadlo = [5]    # Použijeme seznam kvůli mutabilitě uvnitř funkce

def odpocitej():
    """Sníží počítadlo a naplánuje se znovu, dokud nedosáhne nuly."""
    pocitadlo[0] -= 1
    label.config(text=str(pocitadlo[0]))
    if pocitadlo[0] > 0:
        window.after(1000, odpocitej)   # Zavolej se znovu za 1000 ms
    else:
        label.config(text="Start!")

window.after(1000, odpocitej)           # První naplánování
window.mainloop()
```

> **Princip je vždy stejný:** Funkce na konci zavolá `window.after(DELAY, game_step)` — tím naplánuje sebe samu na příště. Pokud se hra skončí (GAME_OVER), přeplánování se neprovede a hra se zastaví.

### Schéma `game_step()`

```
def game_step():
    Pokud GAME_OVER == True:
        Zobraz "Konec hry" na Canvas
        Vrať se (nepřeplánuj)    ← Tím se hra zastaví

    move_snake()      ← Přepočítej stav (může nastavit GAME_OVER)
    render_board()    ← Překresli Canvas

    window.after(DELAY, game_step)   ← Naplánuj příští tik
```

### Proč je pořadí `move_snake()` před `render_board()` správné?

Nejdříve přepočítáme stav (posun hada, kontrola kolize), pak zobrazíme výsledný stav. Hráč tak vidí vždy **aktuální** pozici, ne pozici z minulého tiku.

### Jak zobrazit "Konec hry" na Canvas

```python
# Analogický příklad — overlay text přes hrací plochu
canvas.create_rectangle(
    100, 180, 400, 280,      # Oblast pro text (x1,y1,x2,y2)
    fill="black",
    outline="white",
    width=2
)
canvas.create_text(
    250, 220,                # Střed oblasti
    text="KONEC HRY",
    fill="white",
    font=("Arial", 28, "bold")
)
canvas.create_text(
    250, 255,
    text=f"Skóre: {SCORE}",
    fill="yellow",
    font=("Arial", 16)
)
```

---

## Fáze 7 — Propojení v sekci MAIN

Toto je struktura spouštěcího bloku. Pořadí kroků je závazné:

```python
if __name__ == "__main__":
    # 1. Inicializace herního stavu
    initialize_game()        # Reset SNAKE, FOOD, DIRECTION, SCORE, GAME_OVER

    # 2. Vytvoření okna
    window = tk.Tk()
    window.title("Had")
    window.resizable(False, False)   # Zakáže změnu velikosti okna

    # 3. Vytvoření Canvas
    canvas = tk.Canvas(
        window,
        width=BOARD_WIDTH * CELL_SIZE,
        height=BOARD_HEIGHT * CELL_SIZE,
        bg="black"
    )
    canvas.pack()

    # 4. Registrace kláves
    window.bind("<Up>",    change_direction)
    window.bind("<Down>",  change_direction)
    window.bind("<Left>",  change_direction)
    window.bind("<Right>", change_direction)

    # 5. První naplánování herního tiku
    window.after(DELAY, game_step)

    # 6. Spuštění hlavní smyčky (blokující — vrátí se až po zavření okna)
    window.mainloop()
```

> **Pozor:** `window` a `canvas` jsou zde globální proměnné (vytvořené v `MAIN`). Vaše funkce jako `render_board()` a `game_step()` je budou potřebovat. Deklarujte je tedy jako globální konstanty na úrovni modulu — nebo je vytvořte v `MAIN` a předávejte jako parametry. Konzistentní přístup je důležitý.

---

## Rozšíření dle README

### Restart hry

Po konci hry navažte na stisk klávesy (např. `R`) a zavolejte `initialize_game()`, pak znovu `window.after(DELAY, game_step)`:

```python
def restart(event) -> None:
    """Restartuje hru po stisku R."""
    global GAME_OVER
    if GAME_OVER:
        initialize_game()
        window.after(DELAY, game_step)

window.bind("<r>", restart)
window.bind("<R>", restart)
```

### Postupné zrychlování

V `move_snake()`, po snězení jídla, snižte `DELAY` s dolní mezí — stejný princip jako v projektu 15:

```python
global DELAY
DELAY = max(60, DELAY - 5)   # Minimum 60 ms = ~16 tahů za sekundu
```

### Zobrazení mřížky

Mřížku nakreslete v `render_board()` **před** vykreslením hada a jídla, aby byla vždy pod herními objekty:

```python
# Analogický příklad — vertikální čáry mřížky
for col in range(BOARD_WIDTH + 1):
    x = col * CELL_SIZE
    canvas.create_line(x, 0, x, BOARD_HEIGHT * CELL_SIZE, fill="#222222")
# Analogicky horizontální čáry pro řádky...
```

---

## Souhrn nových konceptů Tkinteru

| Koncept | Metoda / Funkce | Kdy se používá |
|---|---|---|
| Vytvoření okna | `tk.Tk()` | Jednou na začátku v MAIN |
| Vytvoření plátna | `tk.Canvas(...)` | Jednou na začátku v MAIN |
| Zobrazení widgetu | `.pack()` | Hned po vytvoření widgetu |
| Kreslení obdélníku | `canvas.create_rectangle(x1,y1,x2,y2, fill=...)` | V `render_board()` |
| Kreslení kruhu | `canvas.create_oval(x1,y1,x2,y2, fill=...)` | V `render_board()` |
| Kreslení textu | `canvas.create_text(x,y, text=..., fill=...)` | V `render_board()` |
| Smazání plátna | `canvas.delete("all")` | Na začátku `render_board()` |
| Registrace klávesy | `window.bind("<název>", funkce)` | V MAIN před `mainloop()` |
| Časovač | `window.after(ms, funkce)` | V `game_step()` a MAIN |
| Spuštění smyčky | `window.mainloop()` | Poslední řádek v MAIN |

---

## Standardy a požadavky na kód

Stejně jako v projektech 14 a 15:

- **PEP 8** — odsazení 4 mezery, max. 79 znaků na řádek.
- **Type hints** — každá funkce musí mít anotované parametry a návratový typ.
- **Google-style docstrings** — každá funkce musí mít dokumentační řetězec.

```python
def render_board() -> None:
    """Smaže Canvas a vykreslí aktuální stav hry.

    Vykresluje v pořadí: pozadí/mřížka, tělo hada, hlava hada, jídlo,
    skóre. Při GAME_OVER přidá overlay s výsledkem.
    """
    canvas.delete("all")
    # ... implementace ...
```

---

## Kontrolní otázky pro sebehodnocení

- Proč se v GUI verzi nepoužívá `while True` ani `time.sleep()`? Co je nahrazuje?
- Co přesně dělá `window.mainloop()` a co se stane, když tento řádek vynecháte?
- Jaký je rozdíl mezi souřadnicemi políčka `(gy, gx)` a souřadnicemi pixelů na Canvas? Jak provedete převod?
- Proč musí být `canvas.delete("all")` voláno na začátku každého překreslení?
- Co se stane, když v `game_step()` zapomenete na podmínku `if GAME_OVER` a nepřerušíte plánování?
- Jak byste přidali tlačítko "Restart" jako widget Tkinteru (nikoliv klávesu)? Kde byste ho umístili?
- Proč je `window.bind("<Up>", change_direction)` a ne `window.bind("<Up>", change_direction())`? Jaký je rozdíl mezi těmito dvěma zápisy?

---

*Konzistentní s: `README.md` (Had GUI), `14_move_empty.py`, `15_move_and_snake_empty.py`*  
*Předchozí projekt: `15_move_and_snake` (Had v terminálu)*
