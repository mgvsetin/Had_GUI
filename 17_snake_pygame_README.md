\# Had\_Pygame

Projekt — had s pomocí Pygame



\# Hra Had v Pygame



\## Shrnutí

Vytvořte grafickou verzi hry \*\*Had\*\* v Pythonu s využitím herní knihovny `pygame`. Navazujete na předchozí projekt (lekce 16 — Had v Tkinteru): herní logiku pohybu, kolizí a generování potravy \*\*již znáte\*\* a přenášíte ji beze změny. Nová věc je způsob, jakým hru zobrazujete a řídíte — místo Tkinter `Canvas` a `.after()` použijete explicitní herní smyčku `while running:` a `pygame.time.Clock`.



Cílem hry je ovládat hada po hrací ploše, sbírat potravu, prodlužovat jeho tělo a vyhýbat se nárazu do stěny nebo do vlastního těla.



> \*\*Instalace:\*\* Pygame není součástí standardní knihovny Pythonu.

> Nainstalujte ho příkazem: `pip install pygame`



\---



\## Zadání úlohy

Vaším úkolem je naprogramovat hru \*\*Had\*\* jako grafickou aplikaci v Pygame.



Program bude obsahovat:

1\. \*\*Hlavní okno aplikace\*\* vytvořené pomocí `pygame.display.set\_mode()`.

2\. \*\*Hrací plochu\*\* vykreslenou na `pygame.Surface` (objekt `screen`).

3\. \*\*Hada\*\*, který se pohybuje po hrací ploše.

4\. \*\*Potravu\*\*, kterou had sbírá.

5\. \*\*Ovládání šipkami\*\* na klávesnici (volitelně i WASD).

6\. \*\*Podmínky pro konec hry\*\* s zobrazením výsledku.



\---



\## Požadovaná funkčnost



\### 1. Hrací plocha

\- Hrací plocha bude mít rozměr \*\*20 × 20 políček\*\*.

\- Každé políčko bude mít stejnou velikost v pixelech (doporučeno \*\*25 pixelů\*\*).

\- Plocha bude zobrazena graficky jako okno aplikace.



\### 2. Had

\- Had se skládá z \*\*hlavy\*\* a \*\*těla\*\*.

\- Na začátku hry bude mít had délku alespoň \*\*3 dílky\*\*.

\- Každý dílek hada bude zobrazen jako barevný obdélník (`pygame.draw.rect()`).

\- Hlava musí být odlišena od těla jinou barvou.



\### 3. Potrava

\- Na hrací ploše se vždy nachází právě \*\*jedna potrava\*\*.

\- Potrava se zobrazí na \*\*náhodně vybraném volném políčku\*\* (nesmí být na hadovi).

\- Pokud had potravu sní:

&#x20; - zvětší se jeho délka o jeden dílek,

&#x20; - objeví se nová potrava na jiném volném místě.



\### 4. Pohyb hada

\- Had se pohybuje vždy o \*\*jedno políčko\*\* v aktuálním směru.

\- Podporované směry pohybu: nahoru, dolů, doleva, doprava.

\- Směr pohybu mění hráč pomocí klávesnice.

\- Had \*\*nesmí provést okamžitý obrat o 180°\*\* (např. jde-li doprava, nesmí se otočit doleva).



\### 5. Ovládání

\- Hru ovládejte pomocí kláves:

&#x20; - šipka nahoru — pohyb nahoru,

&#x20; - šipka dolů — pohyb dolů,

&#x20; - šipka doleva — pohyb doleva,

&#x20; - šipka doprava — pohyb doprava.

\- Volitelně přidejte podporu kláves `W`, `A`, `S`, `D`.



\### 6. Konec hry

\- Hra končí, pokud:

&#x20; - had narazí do stěny hrací plochy,

&#x20; - had narazí do svého vlastního těla.

\- Po konci hry se v okně zobrazí zpráva \*\*Konec hry\*\* a dosažené skóre.

\- Volitelně: klávesa `R` restartuje hru bez nutnosti zavřít okno.



\---



\## Technické požadavky



Program musí obsahovat alespoň tyto části:



\- inicializaci Pygame (`pygame.init()`) a správné ukončení (`pygame.quit()`),

\- zpracování fronty událostí (`pygame.event.get()`) včetně `pygame.QUIT`,

\- detekci stisku kláves pomocí události `pygame.KEYDOWN`,

\- řízení rychlosti hry pomocí `pygame.time.Clock` a `clock.tick(FPS)`,

\- vykreslení aktuálního stavu na `screen` a zobrazení snímku pomocí `pygame.display.flip()`,

\- generování nové potravy na volné políčko,

\- kontrolu kolize se stěnou a vlastním tělem.



Doporučuje se rozdělit program do samostatných funkcí:



| Funkce | Účel |

| :-- | :-- |

| `initialize\_game()` | Reset herního stavu (had, jídlo, směr, skóre) |

| `render\_board()` | Vykreslení celé scény na `screen` + `display.flip()` |

| `place\_food()` | Generování náhodné volné pozice pro potravu |

| `move\_snake()` | Pohyb hada, kontrola kolizí, růst po snězení |

| `change\_direction(key)` | Změna směru na základě Pygame konstanty klávesy |

| `game\_loop()` | Hlavní smyčka `while running:` se třemi fázemi |



\### Kostra hlavního programu



```python

if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   pygame.init()

&#x20;   initialize\_game()



&#x20;   screen = pygame.display.set\_mode((BOARD\_WIDTH \* CELL\_SIZE,

&#x20;                                     BOARD\_HEIGHT \* CELL\_SIZE))

&#x20;   pygame.display.set\_caption("Had — Pygame")

&#x20;   clock = pygame.time.Clock()



&#x20;   game\_loop()   # Obsahuje while running: a na konci volá pygame.quit()

```



\---



\## Minimální verze

Aby byla úloha splněna, program musí umět:

\- otevřít okno s hrací plochou a správně ho zavřít křížkem,

\- zobrazit hada (hlava odlišena barvou) a potravu,

\- pohybovat hadem podle vstupu hráče pomocí šipek,

\- zvětšit hada a přemístit potravu po snězení,

\- ukončit hru při kolizi a zobrazit zprávu v okně.



\---



\## Rozšiřující úkoly

Pokud budete mít základní verzi hotovou, můžete doplnit:

\- zobrazení skóre a délky hada přímo v okně během hry,

\- restart hry klávesou `R` bez zavření okna,

\- úvodní obrazovku před startem hry (s návodem na ovládání),

\- postupné zrychlování hry — zvyšujte `FPS` po každém snězení potravy,

\- zobrazení mřížky (tenké čáry mezi políčky),

\- překážky na hrací ploše, které had musí obcházet,

\- zvukové efekty pomocí `pygame.mixer` při snězení potravy nebo konci hry.



\---



\## Doporučení k návrhu programu

Před samotným programováním si promyslete:

\- jak se liší herní smyčka `while running:` od Tkinter `.after()` z předchozí lekce,

\- proč se `pygame.display.flip()` musí volat na konci každého snímku,

\- jak Pygame zpracovává vstup z klávesnice (fronta událostí vs. polling),

\- jak převést políčkové souřadnice `(y, x)` na pixelové souřadnice pro `pygame.draw.rect()`,

\- jak oddělovat herní logiku od vykreslování.



Nejdřív vytvořte jednoduchou funkční verzi, teprve poté přidávejte rozšíření.



V kódu dbejte na:

\- srozumitelné názvy proměnných a funkcí,

\- přehlednou strukturu — tři fáze herní smyčky (události / logika / vykreslení),

\- type hints a Google-style docstringy u každé funkce,

\- dodržování standardu PEP 8.



\---



\## Kontrolní otázky

\- Jaký je rozdíl mezi `pygame.KEYDOWN` a `pygame.key.get\_pressed()`? Který z nich použijete pro ovládání hada a proč?

\- Proč je nutné volat `pygame.quit()` na konci programu?

\- Co přesně dělá `clock.tick(FPS)` a jak tím řídíte rychlost hada?

\- Jak se liší zpracování vstupu z klávesnice v Pygame oproti Tkinteru z předchozí lekce?

\- Proč musíte `pygame.font.SysFont()` volat mimo herní smyčku, nikoli uvnitř ní?

\- Jak byste implementovali „průchod zdí" — had vyjde z pravého okraje a objeví se vlevo?

\- Co by bylo potřeba změnit, kdybyste chtěli přidat druhého hada ovládaného klávesami WASD?

