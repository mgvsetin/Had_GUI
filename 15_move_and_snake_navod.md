# Průvodce implementací hry Had — Studijní materiál

> **Tento dokument je vaším průvodcem, ne tahákem.** Záměrně neobsahuje hotové řešení. Obsahuje ale vše, co potřebujete k tomu, abyste si řešení napsali sami: konceptuální vysvětlení, schémata, ukázky na analogických problémech a upozornění na místa, kde se nejčastěji chybuje. Pracujte systematicky — každou fázi si nejdřív promyslete na papíře, teprve pak pište kód.

---

## Přehled projektu a pracovní postup

Máte k dispozici šablonu `15_move_and_snake_empty.py` se strukturou programu a prázdnými těly funkcí. Váš úkol je tyto funkce naplnit logikou. Šablona obsahuje globální proměnné a sekci `MAIN` — **tyto části nemodifikujte**, pokud nemáte dobrý důvod.

### Pořadí implementace (doporučené)

Implementujte funkce v tomto pořadí. Každá vyšší vrstva závisí na té nižší:

```
1. initialize_game()   →  Nastavení počátečního stavu
2. render_board()      →  Vizualizace stavu
3. place_food()        →  Generování pozice jídla
4. move_snake()        →  Herní logika, kolize, růst
5. game_loop()         →  Orchestrace herního tikání
6. get_input()         →  Asynchronní vstup z klávesnice
```

> **Proč toto pořadí?** Až napíšete `render_board()`, můžete si okamžitě vizuálně ověřit, že data v `SNAKE` a `FOOD` vypadají správně. Logiku bez vizualizace ladíte slepě.

---

## Fáze 1 — Inicializace: `initialize_game()`

### Co má tato funkce dělat?

Nastavit **počáteční herní stav** — to znamená uvést všechny globální proměnné do výchozích hodnot tak, aby bylo možné hru spustit znovu bez nutnosti restartovat celý program.

### Co konkrétně nakódovat?

- Resetovat proměnnou `SNAKE` na výchozí seznam článků (3 prvky).
- Resetovat proměnnou `FOOD` na výchozí pozici.
- Resetovat `DIRECTION` na výchozí směr.
- Resetovat `GAME_OVER` na `False`.
- Resetovat `DELAY` na výchozí rychlost.

### Klíčová syntaktická konstrukce: `global`

Funkce, která **čte** globální proměnnou, to může dělat bez deklarace. Funkce, která globální proměnnou **přepisuje** (přiřazuje jí novou hodnotu), musí na začátku deklarovat `global jméno_proměnné`. Toto platí pro všechny funkce v tomto projektu.

```python
# Analogický příklad — čítač kol
pocet_kol: int = 0

def nova_hra() -> None:
    """Resetuje čítač kol na nulu."""
    global pocet_kol
    pocet_kol = 0   # Bez 'global' by toto vytvořilo lokální proměnnou!

def pridej_kolo() -> None:
    """Zvýší čítač o jedna."""
    global pocet_kol
    pocet_kol += 1  # '+=' je přiřazení, tedy i tady je 'global' nutné
```

### Časté úskalí

- Zapomenutí na `global` způsobí, že funkce bude pracovat s lokální kopií proměnné a globální stav se nezmění. Python vás na to **neupozorní chybou** — kód poběží, ale nebude fungovat správně.

---

## Fáze 2 — Souřadnicový systém: Pozice jako `(y, x)`

Než začnete psát `render_board()`, musíte si pevně zapamatovat konvenci pro souřadnice. V celém projektu používáme formát **`(souřadnice_y, souřadnice_x)`**.

### Proč `(y, x)` a ne `(x, y)`?

Při vykreslování řádku po řádku iterujete nejdřív přes řádky (osa Y), pak přes sloupce (osa X). Toto odpovídá přirozenému pořadí indexů v matici.

```
      x=0   x=1   x=2   x=3
     +-----+-----+-----+-----+
y=0  |(0,0) (0,1) (0,2) (0,3)|  ← První řádek
y=1  |(1,0) (1,1) (1,2) (1,3)|  ← Druhý řádek
y=2  |(2,0) (2,1) (2,2) (2,3)|  ← Třetí řádek
     +-----+-----+-----+-----+
```

> **Pamatujte:** Pohyb **dolů** znamená **zvýšení y** (y+1). Pohyb **doprava** znamená **zvýšení x** (x+1). To je opačná intuice než v matematickém grafu!

Šablona uvádí:
```python
SNAKE = [(5, 5), (5, 4), (5, 3)]  # hlava je na řádku 5, sloupci 5
```
Had leží vodorovně, protože y se nemění, ale x klesá — hlava je vpravo.

---

## Fáze 3 — Vykreslování: `render_board()`

### Co má tato funkce dělat?

Projít celou hrací plochu políčko po políčku a pro každé políčko rozhodnout, jaký znak se má zobrazit. Výsledek vytisknout do terminálu.

### Algoritmus (pseudokód)

```
Pro každý řádek y od 0 do BOARD_HEIGHT-1:
    Začni s prázdným řetězcem řádku
    Pro každý sloupec x od 0 do BOARD_WIDTH-1:
        Pokud (y, x) == SNAKE[0]:       → tiskni HEAD_SYMBOL
        Jinak pokud (y, x) je v SNAKE:  → tiskni SNAKE_SYMBOL
        Jinak pokud (y, x) == FOOD:     → tiskni FOOD_SYMBOL
        Jinak:                          → tiskni EMPTY_SYMBOL
    Přidej řádek do výstupu
Vypiš celý výstup najednou
```

### Jak předejít blikání terminálu?

Každý `print()` zapíše na terminál a způsobuje překreslení. Místo volání `print()` pro každý znak sestav **celou plochu do jednoho řetězce** a vypište ji jedním voláním. Před vykreslením terminál vymažte pomocí `os.system("cls" if os.name == "nt" else "clear")`.

```python
# Analogický příklad — sestavení tabulky do řetězce
radky = []
for i in range(3):
    radek = ""
    for j in range(4):
        radek += f"[{i},{j}]"
    radky.append(radek)
print("\n".join(radky))
```

### Klíčová syntaktická konstrukce: Podmíněný výraz v řetězci

Pro přehlednost lze podmínku vložit přímo do f-stringu nebo použít ternární výraz:

```python
# Ternární výraz — přiřazení hodnoty podle podmínky
hodnota = "ANO" if 5 > 3 else "NE"
print(hodnota)  # Výstup: ANO
```

### Časté úskalí

- Podmínku pro hlavu (`SNAKE[0]`) musíte otestovat **dříve** než podmínku pro tělo (`in SNAKE`), protože hlava je také součástí seznamu `SNAKE`.
- Operátor `in` pro seznam `SNAKE` má časovou složitost O(n). Pro základní verzi to nevadí, ale u velmi dlouhého hada by mohlo zpomalovat vykreslování.

---

## Fáze 4 — Generování jídla: `place_food()`

### Co má tato funkce dělat?

Vygenerovat náhodnou pozici `(y, x)` na hrací ploše, která:
1. Leží uvnitř hranic (ne na okraji ani za ním).
2. Není obsazena hadem (žádným článkem z `SNAKE`).

### Algoritmus

Nejjednodušší přístup je **generovat opakovaně**, dokud nenajdete volné místo:

```python
# Analogický příklad — náhodná volná pozice v seznamu
obsazene = [(1, 2), (3, 4), (0, 0)]

import random

def najdi_volnou_pozici(obsazene, vyska, sirka):
    """Najde náhodnou pozici, která není v seznamu obsazených."""
    while True:
        y = random.randint(0, vyska - 1)
        x = random.randint(0, sirka - 1)
        if (y, x) not in obsazene:
            return (y, x)

volna = najdi_volnou_pozici(obsazene, 5, 5)
print(f"Volná pozice: {volna}")
```

### Časté úskalí

- `random.randint(a, b)` vrací číslo **včetně** obou krajních hodnot. Horní hranici tedy nastavte na `BOARD_HEIGHT - 1` a `BOARD_WIDTH - 1`.
- Funkce musí přiřadit výsledek do **globální** proměnné `FOOD` — nezapomeňte na `global FOOD`.
- Teoreticky může nekonečný cyklus `while True` viset, pokud je had tak dlouhý, že zaplnil celou plochu. Pro základní verzi to nevadí, ale je dobré si tohoto okrajového případu být vědom.

---

## Fáze 5 — Herní logika: `move_snake()`

Toto je **nejkomplexnější funkce** celého projektu. Obsahuje fyziku pohybu, detekci kolizí i logiku růstu hada.

### Co má tato funkce dělat?

V každém tiku hry:
1. Vypočítat novou pozici **hlavy** na základě aktuálního `DIRECTION`.
2. Zkontrolovat **kolizi se stěnou** — je nová hlava mimo hranice?
3. Zkontrolovat **kolizi s tělem** — je nová hlava na pozici, která už je v `SNAKE`?
4. Pokud kolize → nastavit `GAME_OVER = True` a vrátit se.
5. Přidat novou hlavu na **začátek** `SNAKE`.
6. Zkontrolovat, zda had **snědl jídlo** (nová hlava == `FOOD`).
7. Pokud snědl → zavolat `place_food()`, **neodstraňovat** ocas (had vyroste).
8. Pokud nesnědl → odstranit poslední článek (ocas) ze `SNAKE`.

### Schéma pohybu — vizualizace

```
PŘED pohybem (směr: vpravo):
  SNAKE = [(5, 5), (5, 4), (5, 3)]
                ↑hlava       ↑ocas

Krok 1: Nová hlava = (5, 5+1) = (5, 6)
        SNAKE.insert(0, (5, 6))
  SNAKE = [(5, 6), (5, 5), (5, 4), (5, 3)]

Krok 2a: Had NESNĚDL jídlo → odebereme ocas
        SNAKE.pop()
  SNAKE = [(5, 6), (5, 5), (5, 4)]   ← Délka zachována

Krok 2b: Had SNĚDL jídlo → ocas necháme
  SNAKE = [(5, 6), (5, 5), (5, 4), (5, 3)]  ← Had je delší o 1
```

### Jak vypočítat novou pozici hlavy?

Pro každý směr se změní buď `y` nebo `x` o ±1:

| Směr    | Změna y | Změna x |
|---------|---------|---------|
| `UP`    | -1      | 0       |
| `DOWN`  | +1      | 0       |
| `LEFT`  | 0       | -1      |
| `RIGHT` | 0       | +1      |

Elegantní způsob je uložit tyto offsety do slovníku a přistupovat k nim podle aktuálního `DIRECTION`. Nevyhnete se tak dlouhému `if/elif` bloku.

```python
# Analogický příklad — pohyb bodu na mřížce
pohyby = {
    "NAHORU": (-1, 0),
    "DOLU":   (+1, 0),
    "VLEVO":  (0, -1),
    "VPRAVO": (0, +1),
}

pozice = (3, 3)
smer = "NAHORU"

dy, dx = pohyby[smer]
nova_pozice = (pozice[0] + dy, pozice[1] + dx)
print(f"Nová pozice: {nova_pozice}")  # Výstup: Nová pozice: (2, 3)
```

### Jak detekovat kolizi se stěnou?

Zkontrolujte, zda je y mimo interval `<0, BOARD_HEIGHT-1>` nebo x mimo `<0, BOARD_WIDTH-1>`.

```python
# Analogický příklad — kontrola hranic
def je_mimo_hranice(y, x, vyska, sirka):
    """Vrátí True, pokud je pozice mimo hrací plochu."""
    return y < 0 or y >= vyska or x < 0 or x >= sirka
```

### Jak detekovat kolizi s tělem?

Použijte operátor `in` — zkontrolujte, zda je nová pozice hlavy obsažena v `SNAKE`. Pozor: v tomto okamžiku je `SNAKE` ještě v původním stavu (před vložením nové hlavy), takže testujete správně.

### Časté úskalí

- **Pořadí operací je kritické:** Nejdříve kolize, pak insert, pak pop. Pokud vložíte hlavu do `SNAKE` dříve, než zkontrolujete kolizi s tělem, bude nová hlava součástí `SNAKE` a kolizi s ní nikdy nenajdete.
- Kolize se stěnou musí kontrolovat **novou pozici**, ne aktuální hlavu.

---

## Fáze 6 — Herní smyčka: `game_loop()`

### Co má tato funkce dělat?

Řídit tempo hry v nekonečném cyklu. Opakovat tři základní operace, dokud není `GAME_OVER` nastaveno na `True`.

### Schéma herního tikání

```
Dokud GAME_OVER == False:
    1. render_board()   ← Zobraz aktuální stav
    2. move_snake()     ← Přepočítej stav (may set GAME_OVER = True)
    3. time.sleep(DELAY)← Počkej — toto určuje rychlost hry

Po cyklu:
    Zobraz zprávu o konci hry (skóre, délka hada...)
```

> **Proč nejdřív render, pak move?** Pokud by to bylo obráceně, hráč by nikdy neuviděl stav bezprostředně před kolizí — poslední frame by zobrazoval již "přepočítaný" stav po nárazu.

### Časté úskalí

- Stav `GAME_OVER` mění funkce `move_snake()`. `game_loop()` ho pouze čte. Nezapomeňte na `global GAME_OVER` v `move_snake()`.
- Po ukončení cyklu nezapomeňte uživateli vypsat výsledek (skóre, délka hada, výzva ke stisknutí klávesy).

---

## Fáze 7 — Vstup z klávesnice: `get_input()`

### Co má tato funkce dělat?

Neustále zjišťovat, zda hráč stiskl klávesu (`w`, `a`, `s`, `d`) a odpovídajícím způsobem změnit globální proměnnou `DIRECTION`. Musí přitom **zamezit otočení o 180°**.

### Proč potřebujeme vlákno?

Standardní `input()` **zablokuje** celý program — had by se nepohnul, dokud hráč nestiskne Enter. Místo toho používáme `keyboard.is_pressed()`, která **neblokuje** a okamžitě vrátí `True`/`False`. Tato funkce proto běží ve vlastním vlákně (viz sekce MAIN v šabloně).

```
Hlavní vlákno (game_loop):          Vedlejší vlákno (get_input):
  render_board()                      while GAME_OVER == False:
  move_snake()                            if keyboard.is_pressed("d"):
  time.sleep(DELAY)                           DIRECTION = "RIGHT"
  render_board()                          if keyboard.is_pressed("a"):
  move_snake()     ←── DIRECTION ────────     DIRECTION = "LEFT"
  time.sleep(DELAY)                       time.sleep(0.01)
  ...                                     ...
```

### Pravidlo protisměru

Had nesmí okamžitě změnit směr na přesně opačný. Validaci proveďte pomocí slovníku opačných směrů:

```python
# Analogický příklad — validace povolené změny stavu
povolene_prechody = {
    "STUJ":   ["DOPRAVA", "DOLEVA", "DOPREDU"],
    "DOPREDU": ["DOPRAVA", "DOLEVA", "STUJ"],
    # Nedovolíme přímé otočení z DOPREDU na DOZADU
}

aktualni_stav = "DOPREDU"
pozadovany_stav = "DOZADU"

if pozadovany_stav in povolene_prechody.get(aktualni_stav, []):
    aktualni_stav = pozadovany_stav
    print("Stav změněn.")
else:
    print("Přechod není povolen.")
```

Pro projekt je jednodušší přístup: uložit mapování `"směr": "opačný_směr"` a nový směr nastavit jen tehdy, pokud není opačný k aktuálnímu.

### Nastavení `daemon = True`

V sekci MAIN je vlákno spuštěno s `input_thread.daemon = True`. Tento atribut **musí být nastaven**, jinak po skončení `game_loop()` terminál "zamrzne" — vedlejší vlákno zůstane aktivní a čeká na klávesy, i když hra skončila. `daemon = True` zajistí automatické ukončení vedlejšího vlákna spolu s hlavním vláknem.

### Časté úskalí

- V cyklu `while` uvnitř `get_input()` **vždy přidejte** `time.sleep(0.01)`. Bez něj vlákno spotřebuje 100 % jednoho jádra procesoru.
- Podmínka ukončení cyklu: cyklus by měl skončit, jakmile je `GAME_OVER == True`, jinak vlákno bezcílně běží i po konci hry (i když `daemon = True` to nakonec ukončí).

---

## Rozšíření dle README

Až bude základní verze funkční, prostudujte `15_move_and_snake_README.md` a implementujte rozšíření. Níže jsou technické záchytné body pro nejdůležitější z nich.

### Barevný rendering (`colorama`)

Knihovna `colorama` přidává ANSI escape kódy do terminálu. Při použití přidejte ke každému barevnému řetězci na konci `Style.RESET_ALL`, jinak se barva "rozteče" na zbytek výstupu.

```python
from colorama import Fore, Style

# Ukázka obarvení textu — analogie k vykreslování hada
znaky = ["hlava", "tělo", "tělo", "ocas"]
for i, znak in enumerate(znaky):
    if i == 0:
        print(Fore.GREEN + znak + Style.RESET_ALL)
    else:
        print(Fore.LIGHTGREEN_EX + znak + Style.RESET_ALL)
```

Kde v projektu to implementovat: přímo do podmíněného bloku uvnitř `render_board()`, místo přímého přidání symbolu obalte symbol barevnými kódy.

### Zrychlování hry

Po snězení jídla v `move_snake()` snižte `DELAY` o malou konstantu. Použijte `max()` k zajištění dolní meze:

```python
# Analogický příklad — omezení hodnoty zdola
aktualni_rychlost = 0.2
minimum = 0.05
snizeni = 0.005

aktualni_rychlost = max(minimum, aktualni_rychlost - snizeni)
print(f"Nová rychlost: {aktualni_rychlost}")
```

### Ukládání stavu do JSON

Pro rekonstrukci identického herního stavu stačí uložit: `SNAKE` (seznam pozic), `FOOD` (pozice jídla), `DIRECTION` (aktuální směr), `DELAY` (aktuální rychlost/obtížnost) a případně `score`.

```python
import json

# Analogický příklad — serializace seznamu n-tic do JSON
data = {
    "had": [(5, 5), (5, 4), (5, 3)],
    "jidlo": (7, 7),
}
json_retezec = json.dumps(data)
print(json_retezec)

# Načtení zpět — pozor: JSON vrátí seznam, ne tuple!
nactena_data = json.loads(json_retezec)
# Převod zpět na tuple:
had = [tuple(pozice) for pozice in nactena_data["had"]]
print(had)
```

> **Pozor:** JSON nezná datový typ `tuple` — uloží ho jako `list`. Při načítání musíte každou pozici převést zpět pomocí `tuple()`.

---

## Standardy a požadavky na kód

Celý projekt musí dodržovat:

- **PEP 8** — odsazení 4 mezery, maximálně 79 znaků na řádek, mezery kolem operátorů.
- **Type hints** — každá funkce musí mít anotované parametry a návratový typ, např. `def place_food() -> None:`.
- **Google-style docstrings** — každá funkce musí mít dokumentační řetězec s popisem, sekcí `Args:` (pokud má parametry) a `Returns:` (pokud vrací hodnotu).

```python
def vypocitej_plochu(sirka: int, vyska: int) -> int:
    """Vypočítá plochu obdélníka.

    Args:
        sirka: Šířka obdélníka v jednotkách.
        vyska: Výška obdélníka v jednotkách.

    Returns:
        Plocha obdélníka jako celé číslo.
    """
    return sirka * vyska
```

---
