# Pohyb objektu a sbírání předmětů na hrací ploše (terminálová minihra)

Tentokrát si vyzkoušíte **tvorbu jednoduché minihry**: budete ovládat hráčovu kostičku na ploše, sbírat předměty a udržovat výsledné skóre. Lekce upevňuje znalosti práce s cykly, podmínkami, funkcemi, detekcí vstupu z klávesnice a tvorbou interaktivních aplikací.

K dispozici máte:

- **`move_empty.py`** – zde vytvoříte vlastní kód,


## 1. Zadání a princip hry

### Herní pravidla a cíle

- Hrací plocha je **mřížka** 20x10 (šířka × výška).
- Hráč ovládá **kostičku O** pomocí kláves W, A, S, D (nahoru, doleva, dolů, doprava).
- Na náhodné pozici je **hvězdička (*)**, kterou hráč "sní" při kontaktu, a tím získá bod.
- Po "snězení" se hvězdička objeví jinde na volné pozici.
- Hra běží stále, dokud hráč nestiskne Ctrl+C (neukončí ručně).
- (Bonus) Přidávají se **okraje**, **počítadlo pohybů**, **barevné efekty**.


## 2. Klíčové prvky a návrh programu

### a) Vykreslení hrací plochy s okraji

- Okraje jsou tvořeny například znakem `#` nebo jiným Vámi zvoleným.
- Vnitřek plochy tvoří pole bodů – hráč (O), hvězdička (*), zbytek např. tečkami.
- V poli přečtěte po řádcích a v každé buňce určete, co se má zobrazit.


### b) Ovládání pohybu hráče

- Čtení vstupu využívá knihovnu `keyboard` (je potřeba mít nainstalovanou).
- Při stisku klávesy se posune hráč v daném směru, ale nesmí překročit okraj.
- Po každém pohybu se aktualizuje počet pohybů a překreslí obrazovka.


### c) Generování hvězdičky

- Hvězdička (*) se objeví vždy **na volné pozici** (nesmí být na hráči ani na okraji).
- Je-li hráč na pozici hvězdičky, skóre se zvýší a hvězdička se přesune.


### d) Sledování skóre a počtu tahů

- Na obrazovce se neustále zobrazuje aktuální skóre a počet pohybů (tahů).
- Skóre se zobrazuje v horní části nebo pod polem.


### e) Barevné efekty a vylepšení

- Pro zvýraznění hráče, hvězdičky a okrajů lze použít knihovnu `colorama`.
- Zajistěte, aby hráč i hvězdička byly lépe rozeznatelné.


## 3. Struktura a kostra programu

Každou základní část doporučujeme řešit samostatnou funkcí:


| Funkce | Účel |
| :-- | :-- |
| `render_board()` | Vykreslí aktuální stav (pole, hráč, hvězdička, okraje) |
| `place_food()` | Najde náhodnou volnou pozici pro hvězdičku |
| `move_player(direction)` | Posune hráče požadovaným směrem |
| `game_loop()` | Řídí celou hru, detekuje vstup, aktualizuje výpisy |

### Kostra hlavního programu

```python
if __name__ == "__main__":
    print("Použijte klávesy W, A, S, D pro pohyb. Stiskněte Ctrl+C pro ukončení.")
    
    FOOD_POS = place_food()
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nHra ukončena. Děkujeme za hraní!")
```


## 4. Postup při implementaci

Od všech implementovaných funkcí se očekává dodržování standardu PEP 8, anotace typů (type hints) a výstižné Google-style docstringy.

---

### Architektura terminálové hry: Krok za krokem

Tvorba hry v terminálu vyžaduje pochopení několika základních konceptů: jak uchovávat informace o hře (stav), jak tyto informace zobrazit (vykreslování), jak je měnit na základě uživatelského vstupu (pohyb) a jak to celé udržet v chodu (herní smyčka).

#### 1. Správa stavu hry (Zápis do globálních proměnných)

Vaše hra si musí pamatovat, kde je hráč, kde je hvězdička a jaké je skóre. Tyto hodnoty se v čase mění. V naší základní šabloně využíváme globální proměnné.

Pokud funkce pouze *čte* globální proměnnou (např. potřebuje znát šířku plochy), stačí její název přímo použít. Pokud ale funkce potřebuje globální proměnnou *přepsat* (např. změnit pozici hráče nebo zvýšit skóre), musíte Pythonu explicitně říct, že neměníte lokální proměnnou, ale tu globální. K tomu slouží klíčové slovo `global`.

**Pomocný příklad:**

```python
skore: int = 0

def pridej_bod() -> None:
    """Zvýší globální počítadlo skóre o jedna."""
    global skore  # Bez tohoto řádku by Python vytvořil lokální proměnnou
    skore += 1

```

#### 2. Vykreslování plochy (Souřadnicový systém a cykly)

Terminál funguje jako mřížka znaků. Počátek souřadnicového systému `(0, 0)` je vždy v **levém horním rohu**. Osa X roste doprava, osa Y roste **dolů**.

Pro vykreslení 2D plochy potřebujete dva vnořené cykly. Vnější cyklus obvykle prochází řádky (osa Y) a vnitřní sloupce (osa X). Uvnitř vnitřního cyklu se rozhodujete, jaký znak pro danou souřadnici vytisknete.

**Pomocný koncept (Vykreslení 3x3 mřížky s jedním cílem):**

```python
CIL_POZICE = (1, 1)

def ukaz_mrizku() -> None:
    """Vykreslí ukázkovou mřížku 3x3 s jedním specifickým bodem."""
    for y in range(3):
        radek = ""
        for x in range(3):
            if (x, y) == CIL_POZICE:
                radek += "X"  # Zde je cíl
            else:
                radek += "."  # Prázdné místo
        print(radek)

```

*Tip k implementaci:* Ve vaší funkci `render_board()` nezapomeňte před začátkem cyklů smazat obsah terminálu pomocí `os.system('clear' if os.name == 'posix' else 'cls')` a vypsat aktuální skóre.

#### 3. Náhodnost a prevence kolizí (Generování hvězdičky)

Když hvězdička zmizí, musí se objevit nová. K určení její pozice využijete `random.randint(min, max)`. Musíte si ale dát pozor na to, aby se nová hvězdička neobjevila přesně tam, kde právě stojí hráč.

K vyřešení tohoto problému se typicky používá cyklus `while True:`, který neustále generuje nové souřadnice, dokud nepadne taková, která je volná. Jakmile je nalezena, cyklus přerušíme návratem hodnoty.

**Pomocný koncept (Házení kostkou, dokud nepadne sudé číslo):**

```python
import random

def hod_sudou() -> int:
    """Hází šestistěnnou kostkou, dokud nepadne sudé číslo."""
    while True:
        hod = random.randint(1, 6)
        if hod % 2 == 0:
            return hod  # Vrací hodnotu a tím okamžitě ukončuje cyklus

```

#### 4. Logika pohybu a kontrola hranic

Funkce `move_player(direction: str)` má za úkol vzít aktuální pozici hráče, rozdělit ji na `x` a `y`, provést výpočet nového kroku a výsledek uložit zpět.

Klíčové je ošetřit hranice. Hráč nesmí "vypadnout" z plochy. Podmínka pro pohyb nahoru tedy není jen stisk klávesy "w", ale také fakt, že `y` je větší než nula (horní okraj).

**Pomocný koncept (Pohyb po 1D ose s ochranou):**

```python
pozice_x: int = 5
MAX_X: int = 10

def posun_vpravo() -> None:
    """Posune objekt o krok vpravo, pokud nenarazí na hranici."""
    global pozice_x
    
    # Podmínka kontroluje, zda nejsme na pravém okraji (indexujeme od 0)
    if pozice_x < MAX_X - 1:
        pozice_x += 1

```

*Nezapomeňte:* Na konci vaší funkce pro pohyb musíte ověřit, zda nová pozice hráče `PLAYER_POS` není náhodou stejná jako pozice hvězdičky `FOOD_POS`. Pokud ano, musíte adekvátně reagovat (skóre, nová hvězdička).

#### 5. Herní smyčka (Game Loop) a čtení vstupu

Herní smyčka je srdcem aplikace. Jde o cyklus `while not GAME_OVER:`, který se opakuje několikrát za sekundu. V každém průchodu musí zjistit, jakou klávesu uživatel drží. K tomu využíváme neblokující čtení z modulu `keyboard`.

Na konci každého cyklu je nutné smyčku na zlomek vteřiny pozastavit, jinak by program spotřeboval veškerý výkon procesoru.

**Pomocný koncept (Základní čtení z klávesnice):**

```python
import keyboard
import time

def demo_smycka() -> None:
    """Ukázková smyčka pro detekci kláves."""
    bezi = True
    while bezi:
        if keyboard.is_pressed('mezernik'):
            print("Byl stisknut mezerník!")
            bezi = False  # Ukončení cyklu
            
        time.sleep(0.1)  # Odpočinek procesoru na 100 ms

```

#### 6. Spouštěcí blok MAIN

Již máte předpřipravený blok `if __name__ == "__main__":`. Tento blok zaručuje, že se kód spustí pouze tehdy, když skript spustíte napřímo (nikoliv pokud byste jej importovali jako modul do jiného skriptu).

Zde se definují úvodní akce. Před vstupem do hlavní herní smyčky je logické vygenerovat první náhodnou pozici hvězdičky. Blok `try...except KeyboardInterrupt` je tam proto, aby aplikace po stisku `Ctrl+C` nezkolabovala s nevzhledným výpisem chyb (Traceback), ale aby se elegantně ukončila vypsáním závěrečné zprávy. Vaším úkolem je zajistit, aby funkce `game_loop()` a `place_food()` byly před zavoláním v tomto bloku korektně naimplementovány.

---

## 5. Doporučené rozšíření a experimenty

- **Barevné efekty:** použijte knihovnu `colorama` pro zvýraznění. Obarvěte hráče zeleně, hvězdičku žlutě, okraje červeně atp.
- **Omezení pole:** umožněte změnu velikosti pole nebo vkládání překážek.
- **Vypsání high-score:** zaznamenávejte nejlepší skóre mezi jednotlivými sezeními (uložte do souboru).
- **Zrychlení hry:** postupně s rychlostí přibývajících bodů snižujte DELAY.
- **Přidání více hvězdiček najednou:** pro vyšší obtížnost.


## Kontrolní otázky

- Jak zajistíte, aby hráč nikdy nemohl překročit okraj herní plochy?
- Jak se generuje náhodná pozice pro hvězdičku bez kolize s hráčem?
- Jak upravit hru, aby počítala a zvýrazňovala součet tahů?
- Jaká vylepšení by šlo přidat pro vyšší hratelnost nebo efekt?
- Odkud a jak čtete stisk klávesnice a co by bylo potřeba pro ovládání šipkami?
- Jak by bylo možné hru rozšířit o další prvky (překážky, více hráčů, časový limit...)?
- Proč programová smyčka (`game_loop`) nemá konec, ale běží, dokud ji neukončí uživatel?
- Jak zajistit, aby bylo možné hrací pole zmenšovat, zvětšovat nebo přidávat nové typy objektů?
