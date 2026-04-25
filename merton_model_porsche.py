# -*- coding: utf-8 -*-
"""
merton_model_porsche.py
=======================
Implementazione Python del Modello Strutturale di Merton (1974)
applicato al caso Porsche AG (bilancio consolidato IFRS 2025).

Il modello quantifica la Probability of Default (PD) e la Distance to Default (DD)
in due scenari:
  - Baseline:       condizioni operative normali
  - Stress logistico: shock da iper-inflazione logistica e transizione Just-in-Case

Utilizzato come supporto quantitativo alla tesi triennale:
"Supply Chain Risk Management e Revisione Legale: Il caso Porsche AG"
Università degli Studi di Padova - Corso di Laurea Triennale in Economia

Autore: Giovanni Destro
Anno:   2025

Dipendenze:
    pip install numpy scipy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import fsolve

# ==============================================================================
# 1. PARAMETRI DI MERCATO E RISOLUZIONE MODELLO DI MERTON
# ==============================================================================
E = 35.0         # Market Cap dell'Equity Porsche in Mld €
sigma_E = 0.35   # Volatilità azionaria (35%)
D = 28.0         # Default Point (soglia critica debito)
r = 0.035        # Tasso Risk-Free (3.5%)
T = 1.0          # Orizzonte temporale (1 anno)

def merton_system(vars):
    """Sistema di equazioni per estrarre il valore implicito degli asset (V0)
    e la loro volatilità (sigma_V) tramite il modello di Merton."""
    V, sigma_V = vars
    d1 = (np.log(V / D) + (r + 0.5 * sigma_V**2) * T) / (sigma_V * np.sqrt(T))
    d2 = d1 - sigma_V * np.sqrt(T)
    eq1 = V * norm.cdf(d1) - D * np.exp(-r * T) * norm.cdf(d2) - E
    eq2 = (V / E) * norm.cdf(d1) * sigma_V - sigma_E
    return [eq1, eq2]

V0, sigma_V = fsolve(merton_system, [E + D, sigma_E * (E / (E + D))])

print(f"Valore implicito degli asset (V0):  {V0:.2f} Mld €")
print(f"Volatilità implicita degli asset (sigma_V): {sigma_V:.4f} ({sigma_V*100:.2f}%)")

# ==============================================================================
# 2. GRAFICO 1 — PERCORSI DEL MOTO BROWNIANO GEOMETRICO
# ==============================================================================
np.random.seed(101)
n_paths = 100
n_steps = 252       # giorni di contrattazione in un anno
dt = T / n_steps
t = np.linspace(0, T, n_steps + 1)
mu_base = 0.02      # drift base

paths = np.zeros((n_steps + 1, n_paths))
paths[0] = V0
for i in range(1, n_steps + 1):
    z = np.random.standard_normal(n_paths)
    paths[i] = paths[i-1] * np.exp((mu_base - 0.5 * sigma_V**2) * dt + sigma_V * np.sqrt(dt) * z)

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(t, paths, color='#1f77b4', lw=1, alpha=0.3)
ax1.axhline(V0, color='#2ca02c', linestyle='-', lw=2.5,
            label=f'Valore Reale Iniziale ($V_0$): {V0:.1f} Mld €')
ax1.axhline(D, color='#d62728', linestyle='--', lw=3.5,
            label=f'Default Point ($D$): {D} Mld €')
ax1.set_title('Genesi Stocastica: Simulazione 100 Percorsi Asset Impliciti (Porsche AG)',
              fontsize=14, fontweight='bold')
ax1.set_xlabel('Orizzonte Temporale (Frazione di Anno)', fontsize=12)
ax1.set_ylabel('Valore degli Asset Reali Impliciti (Mld €)', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right', fontsize=11, framealpha=0.9)
ax1.set_xlim(0, T)
plt.tight_layout()
plt.savefig('grafico1_percorsi_stocastici.png', dpi=150, bbox_inches='tight')
plt.show()

# ==============================================================================
# 3. GRAFICO 2 — DASHBOARD DI STRESS TESTING (Baseline vs Shock Logistico)
# ==============================================================================
np.random.seed(42)
simulations = 10000

# Scenario Baseline
VT_base = V0 * np.exp((mu_base - 0.5 * sigma_V**2) * T +
                       sigma_V * np.sqrt(T) * np.random.standard_normal(simulations))
DD_base = (np.log(V0 / D) + (mu_base - 0.5 * sigma_V**2) * T) / (sigma_V * np.sqrt(T))
PD_base = norm.cdf(-DD_base) * 100

# Scenario Stress (drift negativo + volatilità raddoppiata)
mu_stress = -0.04
sigma_V_stress = sigma_V * 2.0
VT_stress = V0 * np.exp((mu_stress - 0.5 * sigma_V_stress**2) * T +
                         sigma_V_stress * np.sqrt(T) * np.random.standard_normal(simulations))
DD_stress = (np.log(V0 / D) + (mu_stress - 0.5 * sigma_V_stress**2) * T) / (sigma_V_stress * np.sqrt(T))
PD_stress = norm.cdf(-DD_stress) * 100

print(f"\nScenario Baseline  — DD: {DD_base:.2f}  |  PD: {PD_base:.2f}%")
print(f"Scenario Stress    — DD: {DD_stress:.2f}  |  PD: {PD_stress:.2f}%")

fig2, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
props = dict(boxstyle='round,pad=0.5', facecolor='#f9f9f9', edgecolor='#cccccc', alpha=0.9)

# Subplot 1 — Baseline
axes[0].hist(VT_base, bins=80, color='#1f77b4', edgecolor='white', alpha=0.8, density=True)
axes[0].axvline(D, color='#d62728', linestyle='--', lw=3, label=f'Default Point: {D} Mld €')
axes[0].axvline(V0, color='#2ca02c', linestyle=':', lw=2, label=f'Asset Reale: {V0:.1f} Mld €')
axes[0].text(0.95, 0.95, f'Baseline Metrics:\nDD: {DD_base:.2f}\nPD: {PD_base:.2f}%',
             transform=axes[0].transAxes, fontsize=12,
             verticalalignment='top', horizontalalignment='right', bbox=props)
axes[0].set_title('Scenario Baseline (Continuità Garantita)', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Valore Asset a Scadenza (Mld €)', fontsize=11)
axes[0].set_ylabel('Densità di Probabilità', fontsize=11)
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# Subplot 2 — Stress Logistico
counts, bins, patches = axes[1].hist(VT_stress, bins=80, color='#9467bd',
                                      edgecolor='white', alpha=0.8, density=True)
axes[1].axvline(D, color='#d62728', linestyle='--', lw=3, label=f'Default Point: {D} Mld €')
axes[1].axvline(V0, color='#2ca02c', linestyle=':', lw=2, label=f'Asset Reale: {V0:.1f} Mld €')
for count, bin_edge, patch in zip(counts, bins, patches):
    if bin_edge < D:
        patch.set_facecolor('#d62728')
axes[1].text(0.95, 0.95, f'Stress Metrics:\nDD: {DD_stress:.2f}\nPD: {PD_stress:.2f}%',
             transform=axes[1].transAxes, fontsize=12,
             verticalalignment='top', horizontalalignment='right', bbox=props)
axes[1].set_title('Scenario di Stress (Shock Logistico & Normativo)', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Valore Asset a Scadenza (Mld €)', fontsize=11)
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('grafico2_stress_testing.png', dpi=150, bbox_inches='tight')
plt.show()
