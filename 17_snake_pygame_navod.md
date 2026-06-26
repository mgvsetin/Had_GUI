# Průvodce implementací hry Had v Pygame

> **Tento dokument je váš průvodce, ne tahák.** Záměrně neobsahuje hotové řešení. Obsahuje vysvětlení nových konceptů Pygame, srovnání s Tkinter verzí (lekce 16) a ukázky na analogických problémech.
>
> Herní logiku — pohyb hada, kolize, generování jídla — **znáte z projektů 15 a 16**. Soustřeďte se proto výhradně na to, co je v Pygame nové: inicializace, herní smyčka s `Clock`, systém událostí a kreslení na povrch (`Surface`).

---

## Proč Pygame místo Tkinteru?

Tkinter je výborný pro formuláře a jednoduchá GUI. Pygame je navržen **výhradně pro hry a interaktivní grafiku** — nabízí přesnější kontrolu nad časováním, jednodušší práci s barvami jako RGB trojicemi a standardní vzor herní smyčky používaný v celém herním průmyslu.

### Srovnání přístupu Tkinter vs. Pygame

| Aspekt | Tkinter (lekce 16) | Pygame (tato lekce) |
|---|---|---|
| Herní smyčka | `.after(ms, funkce)` — callback | `while running:` — explicitní nekonečný cyklus |
| Časování | Tkinter plánuje volání funkce | `clock.tick(FPS)` — aktivní čekání |
| Vstup z klávesnice | `window.bind("<Up>", fce)` — registrace | `pygame.event.get()` — fronta událostí |
| Kreslení | `canvas.create_rectangle(...)` | `pygame.draw.rect(screen, barva, rect)` |
| Smazání obrazovky | `canvas.delete("all")` | `screen.fill(barva)` |
| Zobrazení výsledku | Automaticky | `pygame.display.flip()` — nutno volat ručně |
| Barvy | Řetězce: `"green"`, `"red"` | RGB n-tice: `(0, 255, 0)`, `(255, 0, 0)` |

---

## Fáze 0 — Instalace a ověření Pygame

Pygame **není součástí standardní knihovny** Pythonu — je nutno ho nainstalovat:

```bash
pip install pygame
```

Ověření, že instalace proběhla správně:

```python
import pygame
print(pygame.version.ver)   # Vypíše verzi, např. "2.5.2"
```

---

## Fáze 1 — Inicializace a základní okno

### Životní cyklus Pygame aplikace

Každá Pygame aplikace musí projít třemi kroky:

```
1. pygame.init()            ← Inicializace všech pygame modulů
   ...vytvoření okna, herní logika...
2. while running:           ← Herní smyčka
       ...
3. pygame.quit()            ← Uvolnění zdrojů (nutné!)
```

Pokud `pygame.quit()` nezavoláte, okno se nemusí správně zavřít nebo program zamrzne.

### Minimální funkční Pygame okno

Toto je nejmenší kód, který otevře okno a reaguje na křížek (zavření). Spusťte ho jako první krok:

```python
import pygame
import sys

pygame.init()                                    # Inicializace všech modulů

screen = pygame.display.set_mode((500, 500))     # Vytvoření okna 500×500 px
pygame.display.set_caption("Had — Pygame")       # Titulek okna

clock = pygame.time.Clock()                      # Objekt pro řízení FPS
running = True

while running:
    # 1. FÁZE: Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:            # Klik na křížek
            running = False

    # 2. FÁZE: Herní logika (zatím prázdná)

    # 3. FÁZE: Vykreslení
    screen.fill((0, 0, 0))                       # Černé pozadí (R, G, B)
    pygame.display.flip()                        # Zobrazení nakresleného snímku

    clock.tick(10)                               # Max. 10 snímků za sekundu

pygame.quit()
sys.exit()
```

> **Spusťte tento kód jako první krok.** Otevře se černé okno, které zavřete křížkem. Teprve poté pokračujte.

---

## Fáze 2 — Herní smyčka a časování: `clock.tick()`

### Jak funguje `clock.tick(FPS)`

`clock.tick(FPS)` je volání, které Pygame **pozastaví** na takovou dobu, aby celý průchod smyčkou trval právě `1000/FPS` milisekund. Pro hada s FPS=5 to znamená, že had se pohne každých 200 ms.

```
Průchod smyčkou bez tick():   Průchod smyčkou s clock.tick(5):
  events (0.1 ms)               events (0.1 ms)
  logic  (0.2 ms)               logic  (0.2 ms)
  render (1.0 ms)               render (1.0 ms)
  → celkem ~1.3 ms              sleep  (~198.7 ms)
  → had by letěl ~700×/s        → celkem přesně 200 ms = 5 FPS
```

> Pro hada používejte nízké FPS (5–10) — tím řídíte rychlost hry. Pro plynulou animaci (budoucí projekty) používejte 30–60 FPS.

### Srovnání s Tkinter `.after()`

V Tkinteru jste naplánovali příští tik pomocí `window.after(DELAY, game_step)` — Tkinter sám zavolal funkci po uplynutí doby. V Pygame je smyčka **vaše** — explicitní `while running:`. Vy sami rozhodujete, co se v každém průchodu stane, a `clock.tick()` pouze zajistí správnou rychlost.

---

## Fáze 3 — Systém událostí: `pygame.event.get()`

### Co je fronta událostí?

Pygame ukládá všechny vstupní události (stisky kláves, pohyb myši, zavření okna) do **fronty**. Voláním `pygame.event.get()` tuto frontu vyprázdníte a dostanete seznam událostí od posledního průchodu smyčkou.

```python
# Analogický příklad — zpracování různých typů událostí
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    elif event.type == pygame.KEYDOWN:       # Klávesa stisknuta
        if event.key == pygame.K_UP:
            print("Šipka nahoru")
        elif event.key == pygame.K_DOWN:
            print("Šipka dolů")
        elif event.key == pygame.K_LEFT:
            print("Šipka vlevo")
        elif event.key == pygame.K_RIGHT:
            print("Šipka vpravo")
        elif event.key == pygame.K_ESCAPE:
            running = False
```

### `KEYDOWN` vs. `key.get_pressed()`

Pygame nabízí dva způsoby detekce vstupu — pro hada je důležité pochopit rozdíl:

| Metoda | Chování | Vhodné pro |
|---|---|---|
| `pygame.KEYDOWN` event | Zavolá se **jednou** při každém stisku | Změna směru hada ✓ |
| `pygame.key.get_pressed()` | Vrátí stav **všech kláves v daný okamžik** | Plynulý pohyb (střílečky) |

Pro hada chceme `KEYDOWN` — stisk klávesy změní směr jednou, had pak jede tím směrem až do dalšího stisku.

### Konstanty kláves

```python
pygame.K_UP      # Šipka nahoru
pygame.K_DOWN    # Šipka dolů
pygame.K_LEFT    # Šipka vlevo
pygame.K_RIGHT   # Šipka vpravo
pygame.K_w       # Klávesa W
pygame.K_s       # Klávesa S
pygame.K_a       # Klávesa A
pygame.K_d       # Klávesa D
pygame.K_r       # Klávesa R (restart)
pygame.K_ESCAPE  # Escape
```

---

## Fáze 4 — Kreslení: `pygame.draw` a `pygame.Rect`

### Co je `Surface`?

`screen` (vrácený z `pygame.display.set_mode()`) je objekt typu `Surface` — v podstatě 2D pole pixelů. Kreslíte na něj pomocí funkcí z modulu `pygame.draw`. Na konci každého snímku zavoláte `pygame.display.flip()`, který obsah `screen` zobrazí v okně.

### Jak kreslit obdélník

```python
# Analogický příklad — nakreslení jednoho zeleného čtverce
CELL_SIZE = 25
gx, gy = 3, 2     # Políčkové souřadnice (x, y) — v pygame konvenčně (x, y)!

x = gx * CELL_SIZE      # = 75
y = gy * CELL_SIZE      # = 50

pygame.draw.rect(
    screen,                          # Povrch, na který kreslíme
    (0, 200, 0),                     # Barva jako (R, G, B)
    (x, y, CELL_SIZE, CELL_SIZE)     # Obdélník jako (x, y, šířka, výška)
)
```

Alternativně lze použít `pygame.Rect`:

```python
# pygame.Rect je objekt reprezentující obdélník
rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
pygame.draw.rect(screen, (0, 200, 0), rect)

# Výhoda: Rect má užitečné atributy
print(rect.centerx)    # Střed X
print(rect.width)      # Šířka
```

### Jak kreslit text

Kreslení textu v Pygame vyžaduje **font objekt**, který musíte nejdřív vytvořit:

```python
# Vytvoření fontu — jednou mimo herní smyčku (globální proměnná)
font = pygame.font.SysFont("Arial", 20)

# Vykreslení textu — uvnitř herní smyčky
text_surface = font.render(f"Skóre: {SCORE}", True, (255, 255, 255))
screen.blit(text_surface, (10, 10))    # blit = nakreslení Surface na Surface
```

> `font.render()` vrátí **nový Surface** s textem. Ten pak pomocí `screen.blit()` "přilepíte" na hlavní obrazovku na zadané souřadnice.

### Konvence souřadnic v Pygame

Pozor na **změnu konvence** oproti projektu 15 a 16! V pygame je standardem `(x, y)`:

```
Projekt 15 terminal:  SNAKE = [(y=5, x=5), ...]   →  (row, col)
Projekt 16 Tkinter:   SNAKE = [(y=5, x=5), ...]   →  (row, col)  ← stejné
Projekt 17 Pygame:    Souřadnice políček → sami si zvolíte konvenci
```

Doporučení: zachovejte `(y, x)` i v Pygame pro konzistenci s předchozími projekty. Při kreslení pak pozor na pořadí:

```python
# SNAKE uložen jako (y, x) — při kreslení rozbalíme správně:
gy, gx = SNAKE[0]              # hlava
x_px = gx * CELL_SIZE          # pixel X = sloupcová souřadnice × velikost
y_px = gy * CELL_SIZE          # pixel Y = řádková souřadnice × velikost
pygame.draw.rect(screen, BARVA_HLAVY, (x_px, y_px, CELL_SIZE, CELL_SIZE))
```

---

## Fáze 5 — Funkce `render_board()`

### Algoritmus

```
screen.fill(BARVA_POZADI)         ← Smaže předchozí snímek

Volitelně: nakresli mřížku (tenké čáry)

Pro každý článek v SNAKE[1:] (tělo bez hlavy):
    Rozbal (gy, gx)
    pygame.draw.rect(screen, BARVA_TELA, (gx*CS, gy*CS, CS, CS))

Rozbal SNAKE[0] (hlava):
    pygame.draw.rect(screen, BARVA_HLAVY, (gx*CS, gy*CS, CS, CS))

Rozbal FOOD:
    pygame.draw.rect(screen, BARVA_JIDLA, (gx*CS, gy*CS, CS, CS))
    # nebo: pygame.draw.circle(screen, BARVA_JIDLA, střed, poloměr)

Nakresli text se skóre pomocí screen.blit(font.render(...), (x, y))

pygame.display.flip()             ← Zobraz hotový snímek
```

### Jak nakreslit kruh pro jídlo

```python
# Analogický příklad — kruh na střed políčka
gy, gx = FOOD
cx = gx * CELL_SIZE + CELL_SIZE // 2   # Střed X v pixelech
cy = gy * CELL_SIZE + CELL_SIZE // 2   # Střed Y v pixelech
r  = CELL_SIZE // 2 - 2                # Poloměr s malým odsazením

pygame.draw.circle(screen, (220, 50, 50), (cx, cy), r)
```

### Jak zobrazit "Konec hry" přes hrací plochu

```python
# Analogický příklad — poloprůhledný overlay + text
# 1. Nakreslit tmavý obdélník jako pozadí textu
pygame.draw.rect(screen, (20, 20, 20), (100, 180, 300, 120))

# 2. Nakreslit ohraničení
pygame.draw.rect(screen, (200, 200, 200), (100, 180, 300, 120), width=2)

# 3. Text "Konec hry"
big_font = pygame.font.SysFont("Arial", 32, bold=True)
text = big_font.render("KONEC HRY", True, (255, 255, 255))
screen.blit(text, (250 - text.get_width() // 2, 205))

# 4. Skóre pod textem
small_font = pygame.font.SysFont("Arial", 18)
score_text = small_font.render(f"Skóre: {SCORE}", True, (255, 220, 0))
screen.blit(score_text, (250 - score_text.get_width() // 2, 255))
```

---

## Fáze 6 — Struktura herní smyčky: `game_loop()`

Zde je klíčový rozdíl oproti Tkinteru. Místo callback funkce `game_step()` máte **jeden velký `while` cyklus** se třemi jasnými fázemi:

```python
# Schéma herní smyčky — 3 fáze v každém průchodu

clock = pygame.time.Clock()
running = True

while running:

    # ── FÁZE 1: UDÁLOSTI ──────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            change_direction(event.key)    # Předáme konstantu klávesy

    # ── FÁZE 2: HERNÍ LOGIKA ──────────────────────────
    if not GAME_OVER:
        move_snake()

    # ── FÁZE 3: VYKRESLENÍ ────────────────────────────
    render_board()                         # Volá pygame.display.flip() uvnitř

    # ── ŘÍZENÍ RYCHLOSTI ──────────────────────────────
    clock.tick(FPS)                        # Omezení na FPS snímků za sekundu

pygame.quit()
sys.exit()
```

### Jak předat klávesu do `change_direction()`

V Tkinteru dostávala funkce celý `event` objekt s atributem `event.keysym` (řetězec). V Pygame předáváme přímo **konstantu klávesy** jako celé číslo (`event.key`):

```python
# Analogický příklad — mapování Pygame konstant na herní směry
def ukazka_zmeny_smeru(key: int) -> None:
    """Ukázka: změna směru na základě Pygame konstanty klávesy."""
    global DIRECTION

    mapovani = {
        pygame.K_UP:    "UP",
        pygame.K_DOWN:  "DOWN",
        pygame.K_LEFT:  "LEFT",
        pygame.K_RIGHT: "RIGHT",
        pygame.K_w:     "UP",
        pygame.K_s:     "DOWN",
        pygame.K_a:     "LEFT",
        pygame.K_d:     "RIGHT",
    }
    opacne = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

    novy_smer = mapovani.get(key)            # None, pokud klávesa není v mapě
    if novy_smer and novy_smer != opacne[DIRECTION]:
        DIRECTION = novy_smer
```

---

## Fáze 7 — Propojení v sekci MAIN

```python
if __name__ == "__main__":
    # 1. Inicializace Pygame a herního stavu
    pygame.init()
    initialize_game()

    # 2. Vytvoření okna a hodin
    screen = pygame.display.set_mode((BOARD_WIDTH * CELL_SIZE,
                                      BOARD_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Had — Pygame")
    clock = pygame.time.Clock()

    # 3. Vytvoření font objektů (jednou zde, ne v každém snímku!)
    font_score = pygame.font.SysFont("Arial", 16)
    font_end   = pygame.font.SysFont("Arial", 32, bold=True)

    # 4. Spuštění herní smyčky
    game_loop()      # Funkce obsahuje while running: a volá pygame.quit()
```

> **Fonty vytvářejte vždy mimo smyčku.** `pygame.font.SysFont()` je relativně pomalá operace — pokud ji zavoláte uvnitř `while running:`, hra se může výrazně zpomalit.

---

## Rozšíření dle README

### Restart hry

Detekujte stisk `R` uvnitř smyčky událostí, ale **pouze tehdy, když je hra skončená**:

```python
elif event.type == pygame.KEYDOWN:
    if event.key == pygame.K_r and GAME_OVER:
        initialize_game()
```

### Postupné zrychlování

V `move_snake()` po snězení jídla snižte `FPS` (nebo `DELAY`):

```python
global FPS
FPS = min(15, FPS + 1)     # Max. 15 snímků za sekundu
```

### Mřížka

Nakreslete ji v `render_board()` po `screen.fill()`, ale před vykreslením hada:

```python
# Vertikální čáry
for col in range(BOARD_WIDTH + 1):
    x = col * CELL_SIZE
    pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, BOARD_HEIGHT * CELL_SIZE))
# Horizontální čáry
for row in range(BOARD_HEIGHT + 1):
    y = row * CELL_SIZE
    pygame.draw.line(screen, (30, 30, 30), (0, y), (BOARD_WIDTH * CELL_SIZE, y))
```

---

## Souhrn nových konceptů Pygame

| Koncept | Funkce / Metoda | Kdy se používá |
|---|---|---|
| Inicializace | `pygame.init()` | Jednou na začátku MAIN |
| Vytvoření okna | `pygame.display.set_mode((w, h))` | Jednou v MAIN |
| Titulek okna | `pygame.display.set_caption("text")` | Jednou v MAIN |
| Hodiny | `pygame.time.Clock()` | Jednou v MAIN |
| Limit FPS | `clock.tick(FPS)` | Na konci každého průchodu smyčkou |
| Fronta událostí | `pygame.event.get()` | Na začátku každého průchodu smyčkou |
| Zavření okna | `event.type == pygame.QUIT` | V cyklu přes události |
| Stisk klávesy | `event.type == pygame.KEYDOWN` + `event.key` | V cyklu přes události |
| Smazání obrazovky | `screen.fill((R, G, B))` | Na začátku každého snímku |
| Kreslení obdélníku | `pygame.draw.rect(screen, barva, rect)` | V `render_board()` |
| Kreslení kruhu | `pygame.draw.circle(screen, barva, střed, r)` | V `render_board()` |
| Kreslení čáry | `pygame.draw.line(screen, barva, start, end)` | V `render_board()` |
| Font | `pygame.font.SysFont("Arial", 20)` | Jednou mimo smyčku |
| Vykreslení textu | `font.render(text, True, barva)` → `screen.blit(...)` | V `render_board()` |
| Zobrazení snímku | `pygame.display.flip()` | Na konci každého snímku |
| Ukončení | `pygame.quit()` + `sys.exit()` | Po opuštění `while running:` |

---

## Standardy a požadavky na kód

Stejně jako v projektech 14, 15 a 16:

- **PEP 8** — odsazení 4 mezery, max. 79 znaků na řádek.
- **Type hints** — každá funkce musí mít anotované parametry a návratový typ.
- **Google-style docstrings** — každá funkce musí mít dokumentační řetězec.

```python
def change_direction(key: int) -> None:
    """Změní směr pohybu hada na základě stisknuté klávesy.

    Ignoruje klávesy, které by způsobily okamžitý obrat o 180°.

    Args:
        key: Pygame konstanta stisknuté klávesy (event.key).
    """
    ...
```

---

## Kontrolní otázky pro sebehodnocení

- Proč se v Pygame musí volat `pygame.display.flip()` na konci každého snímku? Co se stane, když ho vynecháte?
- Jaký je rozdíl mezi `pygame.KEYDOWN` eventem a `pygame.key.get_pressed()`? Který z nich je vhodný pro ovládání hada a proč?
- Kde a proč se vytváří `pygame.font.SysFont()` — proč ho nelze volat uvnitř herní smyčky v každém průchodu?
- Co přesně dělá `clock.tick(FPS)` a co se stane, pokud toto volání z kódu odstraníte?
- Proč je nutné na konci programu zavolat `pygame.quit()`? Co se stane, pokud ho vynecháte?
- V jaké fázi herní smyčky (události / logika / vykreslení) se má volat `move_snake()` a proč?
- Jak byste pomocí `pygame.draw.rect()` nakreslili hada s 2px mezerou mezi články, aniž byste změnili velikost políčka `CELL_SIZE`?

---

*Konzistentní s: `README.md` (Had GUI), `14_move_empty.py`, `15_move_and_snake_empty.py`, `16_snake_gui_empty.py`*  
*Předchozí projekt: `16_snake_gui` (Had v Tkinteru)*
