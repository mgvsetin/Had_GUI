# Rozšíření hry „Had“ – pokročilé funkce a vylepšení

Navazujeme na předchozí lekci, kde jste vytvořili základní verzi hry „Had“ v terminálu. Tentokrát se zaměříme na její rozšíření a vylepšení, která posunou hratelnost, uživatelský komfort i celkový zážitek na vyšší úroveň. V této lekci zpracujete nové funkce pro hladší ovládání, zobrazování skóre, lepší správu herní logiky a případně i nové herní mechaniky.

## 1. Kontrola směru pohybu a zabránění rychlému obratu

Aby hra byla férová a nedocházelo k náhlému kolizi, zavádíme omezení, že had nemůže jít opačným směrem než tím, kterým zrovna jde. Například když jde doprava, nemůže se okamžitě otočit doleva.

- Ověřujte vstupní směr a změňte jej pouze pokud není opačný.
- Pomůže tomu porovnání aktuálního a nového směru.

```python
def change_direction(new_direction):
    global DIRECTION
    opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if new_direction != opposites[DIRECTION]:
        DIRECTION = new_direction
```


## 2. Zlepšení vykreslování – barevné zvýraznění

Pro lepší orientaci hráče ve hře doporučujeme:

- Použití knihovny `colorama` k barevnému zobrazení hlavy hada, těla, jídla a hranic.
- Barevné odlišení výrazně zlepší čitelnost.
- Barvy nastavujte kolem vykreslování jednotlivých znaků.

```python
from colorama import Fore, Style
# Příklad použití v cyklu vykreslování
if (x, y) == SNAKE[^0]:
    row += Fore.GREEN + HEAD_SYMBOL + Style.RESET_ALL
elif (x, y) in SNAKE:
    row += Fore.LIGHTGREEN_EX + SNAKE_SYMBOL + Style.RESET_ALL
elif (x, y) == FOOD:
    row += Fore.RED + FOOD_SYMBOL + Style.RESET_ALL
else:
    row += EMPTY_SYMBOL
```


## 3. Implementace skóre a zobrazení statistik

- Přidejte proměnnou `score`, která se bude zvyšovat při snězení jídla.
- Vykreslete skóre a další statistiky (např. počet tahů) nad nebo pod hrací plochu.
- Umožněte restart hry po skončení.

```python
def render_score():
    print(f"Score: {score} | Délka hada: {len(SNAKE)}")
```


## 4. Zrychlení hry a obtížnost

- Po každém snědeném jídle můžete mírně snížit čas `DELAY`, čímž hra zrychlí.
- Nastavte minimální hranici zrychlení, aby hra nezrychlovala nekontrolovatelně.
- Případně přidejte volbu obtížnosti na začátku.


## 5. Vyhýbání se překážkám a rozšíření hrací plochy

- Přidejte možnost nastavit překážky na hrací plochě, které had musí obejít.
- Překážky mohou být statické nebo se časem měnit (pohyb přes kód).
- Upravit generování jídla tak, aby nepadalo na překážky ani na hada.


## 6. Ukládání a načítání hry

- Umožněte uživateli uložit si pozici hada, skóre a jídlo do souboru.
- Načtěte tyto údaje při startu hry a pokračujte ve hře.
- Za tímto účelem využijte zápis do jednoduchého textového souboru ve formátu CSV nebo JSON.


## 7. Vylepšené ovládání

- Zavedení rozpoznání více než 4 směrů pohybu (např. diagonály) – volitelné.
- Možnost ovládání šipkami na klávesnici místo pouze WASD.
- Plynulejší reakce na klávesy (s rychlejším čtením vstupu).


## 8. Bonus: Přidání herních efektů a vizuálních prvků

- Zvuky pomocí externích knihoven (např. `playsound`) při snězení jídla nebo konci hry.
- Animované efekty jako blikání hada při kolizi.
- Přechodné "power-upy" (např. zrychlení, obrana proti kolizi na několik tahů).


## Kontrolní otázky

- Jak zakážete instantní otočení hada o 180° a proč je to důležité pro hratelnost?
- Jak udržet vysoký FPS/plynulost hry, když pracujete s terminálem a Pythonem?
- Jak implementujete bezpečné a opakované generování jídla na volné pozice?
- Jak přidání barev vylepšuje zážitek z hraní a jak se s tím pracuje v terminálu?
- Jak byste přidali funkci ukládání a načítání stavu hry?
- Co by bylo potřeba změnit, kdyby se hra měla přesunout z terminálu do grafického uživatelského rozhraní?
- Jak můžete zajistit, že hra bude fungovat správně i po delším hraní (např. bez paměťových úniků)?
- Jak optimalizovat vykreslování, aby nedocházelo k blikání obrazovky při rychlých aktualizacích?
