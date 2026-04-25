# Merton Model – Porsche AG

Implementazione Python del **Modello Strutturale di Merton (1974)** applicato al caso **Dr. Ing. h.c. F. Porsche AG**, sviluppata come supporto quantitativo alla tesi triennale:

> *"Supply Chain Risk Management e Revisione Legale: Il caso Porsche AG"*  
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

## Autore

**Giovanni Destro**  
Università degli Studi di Padova  
Corso di Laurea Triennale in Economia  
2025
