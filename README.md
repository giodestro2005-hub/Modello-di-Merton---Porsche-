# Merton Model – Porsche AG

Implementazione Python del **Modello Strutturale di Merton (1974)** applicato al caso **Dr. Ing. h.c. F. Porsche AG**, sviluppata come supporto quantitativo alla tesi triennale:

> *"OLTRE L’EFFICIENZA LOGISTICA: LA TRANSIZIONE STRATEGICA AL JUST-IN-CASE E GLI IMPATTI SUL VALORE D’IMPRESA NEL CASO PORSCHE AG"*  
> Giovanni Destro — Università degli Studi di Padova, 2025

---

## Descrizione

Il modello concettualizza il capitale netto (Equity) di Porsche AG come un'opzione call europea sul valore degli asset aziendali, quantificando la **Probability of Default (PD)** e la **Distance to Default (DD)** in due scenari:

- **Baseline**: condizioni operative normali
- **Stress logistico**: shock da iper-inflazione logistica e transizione Just-in-Case (volatilità raddoppiata, drift negativo)

Il codice genera due grafici:
1. Simulazione di 100 percorsi stocastici del valore degli asset (Moto Browniano Geometrico)
2. Dashboard di stress testing con distribuzione del valore degli asset a scadenza nei due scenari

---

## Requisiti

```bash
pip install -r requirements.txt
```

Oppure manualmente:

```bash
pip install numpy scipy matplotlib
```

---

## Esecuzione

```bash
python merton_model_porsche.py
```

I grafici vengono salvati automaticamente come:
- `grafico1_percorsi_stocastici.png`
- `grafico2_stress_testing.png`

---

## Parametri principali

| Parametro | Valore | Descrizione |
|-----------|--------|-------------|
| E | 35 Mld € | Market Cap Equity Porsche AG |
| σ_E | 35% | Volatilità azionaria |
| D | 28 Mld € | Default Point (soglia critica debito) |
| r | 3.5% | Tasso risk-free |
| T | 1 anno | Orizzonte temporale |

---

## Struttura del codice

### 1. Importazione delle librerie
Lo script utilizza tre moduli scientifici:
- **numpy** — operazioni vettoriali, radici quadrate e logaritmi naturali per le equazioni di pricing
- **scipy.stats.norm** — funzione di ripartizione della normale standardizzata (Φ), essenziale nel framework Black-Scholes
- **scipy.optimize.fsolve** — algoritmo numerico per trovare le radici del sistema di equazioni non lineari

### 2. `merton_model_solver` — Il core del modello
Cuore computazionale dell'analisi. Riceve in input i dati di bilancio e di mercato (Equity, Debito, Tempo, Tasso risk-free e Volatilità dell'Equity) e imposta il sistema di due equazioni di Merton. Poiché il sistema non ammette soluzione algebrica diretta, fornisce a `fsolve` una stima iniziale ragionevole: assume che il valore degli asset sia pari alla somma di Equity e Debito, e che la loro volatilità sia proporzionale a quella dell'Equity. A partire da questi seed, il solver itera fino a convergere sui valori reali di V (Valore degli Asset) e σᵥ (Volatilità degli Asset).

### 3. `calculate_default_metrics` — Metriche di rischio
Una volta estratti i parametri impliciti, questa funzione applica la formula della Distance to Default (DD), misurando quante deviazioni standard separano il valore degli asset dal punto di insolvenza. Successivamente mappa la DD sulla distribuzione normale standardizzata per ottenere la Probability of Default (PD).

### 4. Applicazione e Stress Testing
Lo script calcola due scenari:
- **Scenario Baseline** — riflette la normale operatività e l'attuale capitalizzazione di mercato
- **Scenario di Stress Logistico** — simula la transizione al Just-in-Case aumentando il debito aziendale (per finanziare l'iper-inflazione del magazzino, stimata in 6 miliardi €) e incrementando la volatilità azionaria per riflettere l'incertezza della supply chain

---

## Autore

**Giovanni Destro**  
Università degli Studi di Padova  
Corso di Laurea Triennale in Economia  
2025
