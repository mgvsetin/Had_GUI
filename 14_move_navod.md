# Průvodce implementací terminálové minihry — Pohyb a sbírání předmětů

> **Tento dokument je váš průvodce, ne tahák.** Záměrně neobsahuje hotové řešení. Obsahuje vysvětlení konceptů, schémata, ukázky na analogických problémech a upozornění na místa, kde se nejčastěji chybuje. Pracujte systematicky — každou fázi si nejdřív promyslete, teprve pak pište kód.
>
> Projekt `14` je přímým předchůdcem projektu `15` (hra Had). Koncepty, které se naučíte zde — vykreslování, souřadnicový systém, herní smyčka — v příštím projektu rovnou rozšíříte.

---

## Přehled projektu a pracovní postup

Máte k dispozici šablonu `14_move_empty.py` s globálními proměnnými a prázdnými těly funkcí. Sekci `MAIN` **nemodifikujte** — je již funkční a volá vaše funkce ve správném pořadí.

### Pořadí implementace (doporučené)

```
1. render_board()      →  Vizualizace stavu hry
2. place_food()        →  Generování náhodné pozice hvězdičky
3. move_player()       →  Pohyb hráče, kontrola hranic, sbírání
4. game_loop()         →  Orchestrace celé hry
```

> **Proč toto pořadí?** Po napsání `render_board()` si okamžitě můžete vizuálně ověřit, že globální proměnné `PLAYER_POS` a `FOOD_POS` obsahují správná data. Debugovat logiku bez vizualizace je výrazně těžší.

---

## Fáze 0 — Souřadnicový systém a globální stav

Než napíšete jediný řádek kódu, musíte si ujasnit dvě věci, které prostupují celým projektem.

### Souřadnicový systém: `(x, y)` vs `(y, x)`

V šabloně jsou pozice uloženy jako `(x, y)` — tedy nejdřív sloupec, pak řádek:

```python
PLAYER_POS = (5, 5)  # (x=5, y=5) → sloupec 5, řádek 5
FOOD_POS   = (7, 7)  # (x=7, y=7)
```

Při vykreslování naopak iterujete vnějším cyklem přes **řádky** (y) a vnitřním přes **sloupce** (x). Mějte na paměti, co je co:

```
      x=0  x=1  x=2  x=3  x=4
     +----+----+----+----+----+
y=0  |    |    |    |    |    |
y=1  |    |    |    |    |    |
y=2  |    |    | O  |    |    |  ← Hráč na (x=2, y=2)
y=3  |    |    |    |    |    |
     +----+----+----+----+----+
```

> **Pohyb dolů** = zvýšení `y`. **Pohyb doprava** = zvýšení `x`. Osa Y tedy roste směrem dolů — opačně než v matematickém grafu.

### Klíčové slovo `global`

Každá funkce, která globální proměnnou **přepisuje**, musí na začátku deklarovat `global jméno_proměnné`. Funkce, která proměnnou pouze **čte**, to nepotřebuje.

```python
# Analogický příklad
skore: int = 0

def pridej_bod() -> None:
    """Zvýší globální skóre o jedna."""
    global skore          # Bez tohoto by Python vytvořil lokální proměnnou
    skore += 1            # '+=' je přiřazení → global je nutné

def zobraz_skore() -> None:
    """Vypíše aktuální skóre — pouze čte, global není potřeba."""
    print(f"Skóre: {skore}")
```

> **Záludnost:** Zapomenuté `global` nevyvolá vždy chybu. Kód poběží, ale globální stav se nezmění — hra se bude chovat nesprávně a odhalit příčinu může být obtížné.

---

## Fáze 1 — Vykreslování: `render_board()`

### Co má tato funkce dělat?

Projít celou hrací plochu políčko po políčku, pro každé políčko rozhodnout, jaký znak zobrazit, a výsledek vytisknout do terminálu.

### Algoritmus (pseudokód)

```
Smazat terminál
Sestavit řetězec s horním okrajem
Pro každý řádek y od 0 do BOARD_HEIGHT-1:
    Přidat levý okraj
    Pro každý sloupec x od 0 do BOARD_WIDTH-1:
        Pokud (x, y) == PLAYER_POS  → přidat PLAYER_SYMBOL
        Jinak pokud (x, y) == FOOD_POS → přidat FOOD_SYMBOL
        Jinak                         → přidat EMPTY_SYMBOL
    Přidat pravý okraj + odřádkování
Přidat dolní okraj
Vytisknout celý sestavený řetězec + skóre/statistiky
```

### Jak předejít blikání terminálu?

Nevolat `print()` pro každý znak zvlášť. Místo toho sestavit **celou plochu do jednoho řetězce** a vytisknout ji jedním voláním. Před výpisem terminál vymažte:

```python
import os
os.system('cls' if os.name == 'nt' else 'clear')
```

```python
# Analogický příklad — sestavení tabulky do jednoho řetězce
radky = []
for i in range(3):
    radek = "|"
    for j in range(4):
        radek += f" {i},{j} |"
    radky.append(radek)
print("\n".join(radky))
```

### Jak vykreslit okraje?

Okraj je jen řetězec opakujícího se znaku. Horní a dolní okraj mají délku `BOARD_WIDTH + 2` (plocha + dva rohové znaky). Levý a pravý okraj jsou jednotlivé znaky přidané na začátek a konec každého řádku.

```python
# Analogický příklad — ohraničení řetězce
sirka = 5
znak = "#"
horni_okraj = znak * (sirka + 2)
radek_obsahu = znak + " abc " + znak
dolni_okraj = znak * (sirka + 2)
print(horni_okraj)
print(radek_obsahu)
print(dolni_okraj)
# Výstup:
# #######
# # abc #
# #######
```

### Časté úskalí

- Podmínku pro hráče testujte **dříve** než pro jídlo — obě pozice jsou obecně různé, ale pokud by byly stejné, hráč má vizuální prioritu.
- Skóre a počet pohybů vypisujte **pod** hrací plochou, nikoliv jako součást plochy.
- Souřadnice `(x, y)` — nezaměňte pořadí při porovnání s `PLAYER_POS` a `FOOD_POS`.

---

## Fáze 2 — Generování hvězdičky: `place_food()`

### Co má tato funkce dělat?

Vygenerovat náhodnou pozici `(x, y)` uvnitř hrací plochy, která **není obsazena hráčem**, a tuto pozici vrátit.

### Algoritmus

Nejjednodušší přístup je generovat opakovaně, dokud nenajdete volné místo:

```python
# Analogický příklad — náhodná pozice, která není na hráči
import random

hrac = (3, 3)
sirka, vyska = 10, 10

def najdi_volnou_pozici(hrac, sirka, vyska):
    """Vrátí náhodnou pozici, která není obsazena hráčem."""
    while True:
        x = random.randint(0, sirka - 1)
        y = random.randint(0, vyska - 1)
        if (x, y) != hrac:
            return (x, y)

print(najdi_volnou_pozici(hrac, sirka, vyska))
```

### Návratová hodnota vs. globální proměnná

Funkce `place_food()` **vrací** novou pozici (pomocí `return`) — nenastavuje `FOOD_POS` sama. Volající kód (sekce `MAIN` a funkce `move_player()`) výsledek přiřadí do `FOOD_POS`. Toto je záměrný design šablony — zachovejte ho.

```python
# Správné volání (již je v MAIN):
FOOD_POS = place_food()
```

### Časté úskalí

- `random.randint(a, b)` vrací číslo **včetně** obou krajních hodnot. Horní mez tedy nastavte na `BOARD_WIDTH - 1` resp. `BOARD_HEIGHT - 1`.
- Funkce nesmí generovat pozici na okraji, pokud máte okraje jako součást hrací plochy — v tomto projektu jsou okraje pouze vizuální, hrací plocha je stále `BOARD_WIDTH × BOARD_HEIGHT` vnitřních buněk.

---

## Fáze 3 — Pohyb hráče: `move_player(direction)`

### Co má tato funkce dělat?

Na základě parametru `direction` (řetězec `"UP"`, `"DOWN"`, `"LEFT"`, `"RIGHT"`) vypočítat novou pozici hráče, ověřit, že nová pozice je uvnitř hrací plochy, a pozici uložit. Pokud hráč stojí na hvězdičce, zvýšit skóre a vygenerovat novou hvězdičku.

### Schéma logiky

```
Funkce dostane: direction = "RIGHT"

1. Rozbalit PLAYER_POS na x, y
2. Vypočítat nové souřadnice:
     "UP"    → y_nové = y - 1,  x_nové = x
     "DOWN"  → y_nové = y + 1,  x_nové = x
     "LEFT"  → x_nové = x - 1,  y_nové = y
     "RIGHT" → x_nové = x + 1,  y_nové = y
3. Zkontrolovat hranice:
     x_nové >= 0 AND x_nové < BOARD_WIDTH
     y_nové >= 0 AND y_nové < BOARD_HEIGHT
4. Pokud je pozice platná → PLAYER_POS = (x_nové, y_nové)
5. Pokud PLAYER_POS == FOOD_POS:
     SCORE += 1
     FOOD_POS = place_food()
```

### Elegantní výpočet kroku pomocí slovníku

Místo dlouhého `if/elif` bloku lze offsety pohybu uložit do slovníku:

```python
# Analogický příklad — pohyb bodu na mřížce
kroky = {
    "UP":    (0, -1),
    "DOWN":  (0, +1),
    "LEFT":  (-1, 0),
    "RIGHT": (+1, 0),
}

pozice = (5, 5)
smer = "RIGHT"

dx, dy = kroky[smer]
nova_pozice = (pozice[0] + dx, pozice[1] + dy)
print(f"Nová pozice: {nova_pozice}")  # Výstup: Nová pozice: (6, 5)
```

### Kontrola hranic — jednoduchá podmínka

```python
# Analogický příklad — kontrola platnosti pozice
def je_platna(x, y, sirka, vyska):
    """Vrátí True, pokud je pozice uvnitř hrací plochy."""
    return 0 <= x < sirka and 0 <= y < vyska
```

> Pokud nová pozice **není platná**, funkce jednoduše **nic neudělá** — hráč zůstane stát na místě. Nejedná se o chybu, ale o záměrné chování (narážení do stěny).

### Časté úskalí

- Nezapomeňte na `global PLAYER_POS, FOOD_POS, SCORE` — funkce přepisuje všechny tři.
- Sbírání hvězdičky testujte **po** přesunutí hráče na novou pozici, nikoliv před ním.
- Počítadlo pohybů (pokud ho implementujete jako bonus) zvyšujte pouze tehdy, když se hráč skutečně pohnul (nová pozice se liší od staré).

---

## Fáze 4 — Herní smyčka: `game_loop()`

### Co má tato funkce dělat?

Neustále zjišťovat, které klávesy jsou stisknuty, volat `move_player()` se správným směrem, překreslit plochu a na konci každého průchodu na krátko počkat.

### Schéma průchodu smyčkou

```
Dokud GAME_OVER == False:
    1. render_board()              ← Zobraz aktuální stav
    2. Detekuj stisknuté klávesy:
         keyboard.is_pressed("w") → move_player("UP")
         keyboard.is_pressed("s") → move_player("DOWN")
         keyboard.is_pressed("a") → move_player("LEFT")
         keyboard.is_pressed("d") → move_player("RIGHT")
    3. time.sleep(DELAY)           ← Odpočinek procesoru
```

### Proč `keyboard.is_pressed()` a ne `input()`?

Funkce `input()` **zablokuje** celý program — hra by čekala na stisk Enteru. `keyboard.is_pressed()` okamžitě vrátí `True` nebo `False` a program pokračuje dál. Hra tak reaguje plynule a `DELAY` určuje, jak rychle se hráč pohybuje.

```python
# Analogický příklad — neblokující čtení klávesy
import keyboard
import time

def demo() -> None:
    """Ukázka neblokující detekce klávesy v cyklu."""
    for _ in range(50):           # 50 průchodů místo nekonečna
        if keyboard.is_pressed("mezernik"):
            print("Mezerník stisknut!")
        time.sleep(0.05)          # 20 průchodů za sekundu
```

### Na co nezapomenout v `game_loop()`

- Funkce v tomto projektu **nečte** `GAME_OVER` aktivně (hra se ukončuje přes `Ctrl+C`, které zachytí `try/except` v `MAIN`). Přesto je `GAME_OVER` v šabloně připravena pro případné rozšíření (kolize s překážkou apod.).
- `time.sleep(DELAY)` patří **na konec** průchodu cyklem, nikoliv na začátek.
- Pořadí: nejdřív `render_board()`, pak detekce vstupu. Hráč tak vždy vidí stav před svým tahem.

---

## Bonusová rozšíření dle README

### Počítadlo pohybů

Přidejte globální proměnnou `MOVES: int = 0` a v `move_player()` ji zvyšujte o 1 při každém platném pohybu. Zobrazujte ji v `render_board()` spolu se skóre.

### Barevné efekty (`colorama`)

Každý znak v `render_board()` obalte barevným kódem. Nezapomeňte na `Style.RESET_ALL` za každým obarveným řetězcem:

```python
from colorama import Fore, Style

# Analogický příklad — obarvení různých objektů
objekty = [("hráč", "O"), ("hvězdička", "*"), ("okraj", "#")]
barvy = {
    "hráč":     Fore.GREEN,
    "hvězdička": Fore.YELLOW,
    "okraj":    Fore.RED,
}

for nazev, symbol in objekty:
    barva = barvy.get(nazev, "")
    print(barva + symbol + Style.RESET_ALL + f"  ← {nazev}")
```

### High-score (ukládání do souboru)

Při ukončení hry porovnejte aktuální `SCORE` s hodnotou načtenou ze souboru. Pokud je aktuální skóre vyšší, soubor přepište.

```python
# Analogický příklad — čtení a zápis jednoho čísla ze souboru
def nacti_rekord(soubor: str) -> int:
    """Načte rekordní skóre ze souboru, nebo vrátí 0."""
    try:
        with open(soubor, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def uloz_rekord(soubor: str, skore: int) -> None:
    """Uloží skóre do souboru."""
    with open(soubor, "w") as f:
        f.write(str(skore))
```

---

## Standardy a požadavky na kód

Celý projekt musí dodržovat:

- **PEP 8** — odsazení 4 mezery, max. 79 znaků na řádek.
- **Type hints** — každá funkce musí mít anotované parametry a návratový typ.
- **Google-style docstrings** — každá funkce musí mít dokumentační řetězec.

```python
def move_player(direction: str) -> None:
    """Posune hráče v zadaném směru, pokud pohyb nepřekračuje hranice.

    Args:
        direction: Směr pohybu. Povolené hodnoty: 'UP', 'DOWN', 'LEFT', 'RIGHT'.
    """
    ...
```

---

## Kontrolní otázky pro sebehodnocení

Než projekt odevzdáte, ověřte, že dokážete odpovědět:

- Proč používáme `keyboard.is_pressed()` místo `input()`? Co by se stalo, kdybychom `input()` použili?
- Co přesně dělá `time.sleep(DELAY)` uvnitř herní smyčky a co se stane, pokud tento řádek vymažete?
- Proč `place_food()` hodnotu **vrací** (`return`) místo toho, aby ji přímo zapsala do `FOOD_POS`?
- Jak byste upravili `move_player()`, aby had mohl „projít" skrz stěnu a objevit se na druhé straně (tzv. wrap-around)?
- Co je `try/except KeyboardInterrupt` v bloku `MAIN` a proč je tam?
- Jak byste přidali překážky na hrací plochu? Co by se muselo změnit ve funkcích `render_board()`, `place_food()` a `move_player()`?

---

*Konzistentní s: `14_move_empty.py`, `14_move_README.md`*  
*Navazující projekt: `15_move_and_snake_empty.py`*
