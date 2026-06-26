# Had_GUI
Projekt - had s pomocí TkInter

# Hra Had v Tkinteru

## Shrnutí
Vytvořte jednoduchou grafickou verzi hry **Had** v Pythonu s využitím knihovny `tkinter`. Můžete využít tiny.school rádce.

Cílem hry je ovládat hada po hrací ploše, sbírat potravu, prodlužovat jeho tělo a vyhýbat se nárazu do stěny nebo do vlastního těla.

---

## Zadání úlohy
Vaším úkolem je naprogramovat hru **Had** jako **okenní aplikaci**.

Program bude obsahovat:
1. **Hlavní okno aplikace** vytvořené pomocí `tkinter`.
2. **Hrací plochu** zobrazenou graficky, například pomocí widgetu `Canvas`.
3. **Hada**, který se pohybuje po hrací ploše.
4. **Potravu**, kterou had sbírá.
5. **Ovládání klávesnicí**.
6. **Podmínky pro konec hry**.

---

## Požadovaná funkčnost

### 1. Hrací plocha
- Hrací plocha bude mít rozměr **20 × 20 políček**.
- Každé políčko bude mít stejnou velikost.
- Plocha bude zobrazena graficky v okně aplikace.
- Vhodné je zvolit například velikost jednoho políčka **20 až 40 pixelů**.

### 2. Had
- Had se skládá z **hlavy** a **těla**.
- Na začátku hry bude mít had délku alespoň **3 dílky**.
- Každý dílek hada bude zobrazen graficky jako tvar na hrací ploše, například obdélník.
- Hlava by měla být odlišena od těla, například jinou barvou.

### 3. Potrava
- Na hrací ploše se vždy nachází právě **jedna potrava**.
- Potrava se zobrazí na **náhodně vybraném volném políčku**.
- Pokud had potravu sní:
  - zvětší se jeho délka o jeden dílek,
  - objeví se nová potrava na jiném volném místě.

### 4. Pohyb hada
- Had se pohybuje vždy o **jedno políčko** v aktuálním směru.
- Podporované směry pohybu:
  - nahoru,
  - dolů,
  - doleva,
  - doprava.
- Směr pohybu mění hráč pomocí klávesnice.

### 5. Ovládání
- Hru ovládejte pomocí kláves:
  - šipka nahoru – pohyb nahoru,
  - šipka dolů – pohyb dolů,
  - šipka doleva – pohyb doleva,
  - šipka doprava – pohyb doprava.
- Volitelně můžete přidat i podporu kláves `W`, `A`, `S`, `D`.

### 6. Konec hry
- Hra končí, pokud:
  - had narazí do stěny hrací plochy,
  - had narazí do svého vlastního těla.
- Po konci hry se v okně zobrazí informace **Konec hry**.
- Volitelně můžete zobrazit i dosažené skóre.

---

## Technické požadavky

Program by měl obsahovat alespoň tyto části:
- vytvoření hlavního okna,
- vytvoření hrací plochy,
- zpracování stisku kláves,
- pravidelnou aktualizaci hry,
- vykreslení aktuálního stavu,
- generování nové potravy,
- kontrolu kolizí.

Doporučuje se rozdělit program do menších funkcí, například:
- funkce pro vykreslení,
- funkce pro posun hada,
- funkce pro kontrolu kolize,
- funkce pro vytvoření nové potravy,
- funkce pro zpracování vstupu z klávesnice.

---

## Minimální verze
Aby byla úloha splněna, program musí umět:
- otevřít okno s hrací plochou,
- zobrazit hada a potravu,
- pohybovat hadem podle vstupu hráče,
- zvětšit hada po sebrání potravy,
- ukončit hru při kolizi.

---

## Rozšiřující úkoly
Pokud budete mít základní verzi hotovou, můžete doplnit některé z následujících vylepšení:
- zobrazení skóre,
- tlačítko nebo klávesu pro restart hry,
- úvodní obrazovku,
- postupné zrychlování hry,
- vlastní barevné zpracování,
- zobrazení mřížky,
- překážky na mapě.

---

## Doporučení k návrhu programu
Před samotným programováním si promyslete:
- jak budete ukládat pozice jednotlivých částí hada,
- jak budete určovat novou pozici hlavy,
- jak poznáte, že had snědl potravu,
- jak poznáte kolizi,
- jak budete oddělovat herní logiku od vykreslování.

Nejdříve vytvořte jednoduchou funkční verzi a teprve potom přidávejte další vylepšení.

V kódu dbejte na:
- srozumitelné názvy proměnných a funkcí,
- přehlednou strukturu,
- rozumné rozdělení programu na menší části,
- komentáře u důležitých míst programu.
