# ⚡ TRIPLE-ZONE WEATHER ORDER ENGINE

A localized, high-frequency alpha terminal engineered to map live meteorological feeds against structured prediction market ladders. The system tracks real-time temperature vectors, calculates delta velocities, and generates execution signals for complex multi-zone target contracts (e.g., Polymarket brackets).

## 📌 Core Features

* **Multi-Zone Pipeline Tracking:** Real-time monitoring across three primary geopolitical target regions[cite: 6]:
* 📍 **Zone 1:** Lucknow Airport Area (IST)[cite: 6]
* 📍 **Zone 2:** Seoul Incheon International Airport (KST)[cite: 6]
* 📍 **Zone 3:** Hong Kong Observatory Hill (HKT)[cite: 6]


* **Dynamic Vector Engine:** Quantifies real-time temperature velocity changes ($\Delta^{\circ}\text{C}/\text{hr}$) using micro-timestamp differences to predict late-stage market pushes[cite: 6].
* **Automated Bracket States:** Maps current data points, peak market windows, and maximum daily parameters to dynamically shift bracket indicators (`Reached`[cite: 6], `Closed`[cite: 6], `Buy Yes`[cite: 6], `Scalp Spread`[cite: 6]).
* **Asynchronous Execution Architecture:** Powered by background thread routines to preserve UI state responsiveness while querying Open-Meteo core data layers[cite: 6].

---

## 🛠️ System Architecture

The trading application isolates network execution states from rendering loops to guarantee zero UI layout blocking[cite: 6].

```
  [Open-Meteo Core API]
           │
           ▼ (Asynchronous Data Fetch - Every 15 Mins)
┌──────────────────────────────────────┐
│       Background Worker Loop         │ ──► Compute Vector Acceleration
└──────────────────────────────────────┘
           │
           ▼ (Thread-Safe payload synchronization)
┌──────────────────────────────────────┐
│         Tkinter Main UI Loop         │ ──► Dynamic Predictive Output Matrix
└──────────────────────────────────────┘

```

---

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have Python 3.8+ along with the `requests` library deployed in your environment:

```bash
pip install requests

```

### 2. Deployment Execution

Run the production script from your terminal:

```bash
python luck3.py

```

---

## 📊 Matrix Signal Logic Matrix

The engine processes signals through a specific evaluation priority rule set[cite: 6]:

| Bracket Status Flag | UI Tag Style | Logical Trigger Condition |
| --- | --- | --- |
| `[-] OUT: Reached` | Neutral Gray | Current or daily max temperature meets/exceeds target threshold[cite: 6]. |
| `[🚫] CLOSED: Unreached` | Neutral Gray | Market time windows expire without cross-over targets reached[cite: 6]. |
| `[⚡] BUY YES` | Success Green | Inside peak hour window, short delta target distance, positive velocity[cite: 6]. |
| `[🔄] SCALP SPREAD` | Warning Yellow | Stagnant momentum detected near threshold boundaries[cite: 6]. |
| `[🛑] BUY NO / SELL YES` | Failure Red | High distance delta with negative acceleration vectors[cite: 6]. |

---

## 🔧 Target Configurations

Modifications to structural data brackets can be configured directly within the class constructor inside `luck3.py`[cite: 6]:

```python
# Modifying contract target tracking boundaries
self.lko_brackets = [39, 40, 41, 42, 43] # Lucknow Brackets
self.sel_brackets = [25, 26, 27, 28, 29] # Seoul Brackets
self.hkg_brackets = [29, 30, 31, 32, 33] # Hong Kong Brackets

```

---

