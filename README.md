# Had_GUI

Připraveno pro Projektové dny na MGV - Python, Válek

Repozitář obsahuje čtyři na sebe navazující projekty, které studenty provedou
od jednoduché terminálové minihry až po grafickou hru Had v knihovně Pygame.

Každý projekt obsahuje tři soubory: zadání (README), studijní průvodce (navod)
a šablonu se strukturou kódu (empty.py), kterou studenti doplňují.

---

## Struktura repozitáře

```
Had_GUI/
├── 14_move_empty.py              # Šablona projektu 14
├── 14_move_README.md             # Zadání projektu 14
├── 14_move_navod.md              # Studijní průvodce projektu 14
│
├── 15_move_and_snake_empty.py    # Šablona projektu 15
├── 15_move_and_snake_README.md   # Zadání projektu 15
├── 15_move_and_snake_navod.md    # Studijní průvodce projektu 15
│
├── 16_snake_gui_empty.py         # Šablona projektu 16
├── 16_snake_gui_README.md        # Zadání projektu 16
├── 16_snake_gui_navod.md         # Studijní průvodce projektu 16
│
├── 17_snake_pygame_empty.py      # Šablona projektu 17
├── 17_snake_pygame_README.md     # Zadání projektu 17
├── 17_snake_pygame_navod.md      # Studijní průvodce projektu 17
│
└── README.md                     # Tento soubor
```

---

## Přehled projektů

### 14 — Move: Pohyb a sbírání předmětů (terminál)

Úvodní projekt série. Student vytvoří jednoduchou terminálovou hru, ve které
ovládá hráče pohybujícího se po mřížce 20x10 a sbírá hvězdičky.

Klíčové koncepty: globální proměnné a `global`, souřadnicový systém `(x, y)`,
vykreslování plochy do terminálu, neblokující vstup pomocí `keyboard.is_pressed()`,
herní smyčka s `time.sleep()`.

Použité knihovny: `os`, `random`, `time`, `keyboard`

---

### 15 — Move and Snake: Had v terminálu

Navazuje přímo na projekt 14. Student přepracuje jednoduché pohybování bodu
na plnohodnotnou hru Had — dynamický seznam článků, růst hada, vlákno pro vstup.

Klíčové koncepty: had jako seznam n-tic `[(y,x), ...]`, manipulace se seznamem
(`insert`, `pop`), konvence souřadnic `(y, x)`, detekce kolizí, paralelní
zpracování vstupu pomocí `threading`.

Použité knihovny: `os`, `random`, `time`, `threading`, `keyboard`

---

### 16 — Snake GUI: Had v Tkinteru

Přesun hry Had do grafického okna. Herní logika zůstává stejná jako v projektu 15,
novou vrstvou je knihovna Tkinter — Canvas, registrace kláves a callback-based
herní smyčka přes `.after()`.

Klíčové koncepty: `tk.Tk()`, `tk.Canvas`, `canvas.create_rectangle()`,
`window.bind()`, `window.after()`, `window.mainloop()`, převod políčkových
souřadnic na pixely.

Použité knihovny: `tkinter`, `random`

---

### 17 — Snake Pygame: Had v Pygame

Přepsání hry Had do knihovny Pygame. Studenti srovnávají dva přístupy ke grafické
hře: callback model Tkinteru vs. explicitní herní smyčku `while running:` v Pygame.

Klíčové koncepty: `pygame.init()` / `pygame.quit()`, `pygame.display.set_mode()`,
`pygame.time.Clock` a `clock.tick(FPS)`, fronta událostí `pygame.event.get()`,
`pygame.KEYDOWN`, `pygame.draw.rect()`, `pygame.display.flip()`, font a `blit`.

Použité knihovny: `pygame`, `random`, `sys`

---

## Doporučené pořadí studia

Projekty jsou navrženy jako lineární série — každý staví na znalostech
z předchozího. Doporučené pořadí:

```
14 (terminál, pohyb)  →  15 (terminál, had)  →  16 (Tkinter GUI)  →  17 (Pygame)
```

---

## Požadavky na prostředí

Python 3.10 nebo novější.

Instalace externích knihoven:

```bash
pip install keyboard    # Projekty 14 a 15
pip install pygame      # Projekt 17
```

Tkinter (projekt 16) je součástí standardní instalace Pythonu — žádná
další instalace není potřeba.

---

## Standardy kódu

Ve všech projektech se vyžaduje:

- dodržování stylu **PEP 8**,
- **typové anotace** (type hints) u všech funkcí,
- **Google-style docstringy** u všech funkcí,
- smysluplné anglické názvy proměnných, funkcí a tříd,
- výstup do terminálu a komentáře v češtině.
