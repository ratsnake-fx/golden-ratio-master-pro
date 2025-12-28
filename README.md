# 💎 Golden Ratio Master Pro

**Advanced 5-Split Position Calculator for Trading**

Ein Streamlit-basiertes Tool für professionelles Positionsmanagement mit Fibonacci-Golden-Ratio Splitting.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Was ist das?

Statt einer einzelnen Position mit vollem Risiko am weitesten Stop-Loss teilt dieses Tool dein Risiko in **5 Positionen** auf, wobei jede einen engeren SL hat basierend auf dem **Golden Ratio Decay**:

| Position | Decay | Gewichtung |
|----------|-------|------------|
| P1 | 100% | 13/31 (42%) |
| P2 | 61.8% | 8/31 (26%) |
| P3 | 38.2% | 5/31 (16%) |
| P4 | 23.6% | 3/31 (10%) |
| P5 | 14.6% | 2/31 (6%) |

**Vorteil:** Höheres effektives Risk-Reward bei gleichem Gesamtrisiko.

---

## ✨ Features

- **📊 Vollständige Symbol-Unterstützung**
  - Forex Majors & Crosses (28+ Paare)
  - Futures (NQ, MNQ, ES, MES, YM, GC, CL, ...)
  - Index CFDs, Commodities, Crypto

- **🎯 Futures Kleinst-System**
  - Automatisch 1 Kontrakt pro Position
  - Multiplikator für Skalierung (1x, 2x, 3x...)
  - Detaillierte Tick/Punkt-Anzeige

- **📈 Szenario-Analyse**
  - Was passiert bei 0-5 SL getroffen?
  - Break-Even Punkt Berechnung
  - Visuelles P/L Chart

- **🎨 Dark Trading Terminal UI**
  - Professionelles Design
  - SL-Leiter Visualisierung
  - Risiko-Verteilung Pie Chart

- **📋 Export**
  - Copy-Paste Ready Order Strings
  - JSON Export für Automation

---

## 🚀 Installation

### Voraussetzungen
- Python 3.9 oder höher
- pip (Python Package Manager)

### Setup

```bash
# Repository klonen
git clone https://github.com/ratsnake-fx/golden-ratio-master-pro.git
cd golden-ratio-master-pro

# Dependencies installieren
pip install -r requirements.txt

# App starten
streamlit run golden_ratio_master_pro.py
```

### Windows Batch-Datei (Optional)

Erstelle eine `start.bat` im Projektordner:

```batch
@echo off
cd /d "%~dp0"
streamlit run golden_ratio_master_pro.py
pause
```

---

## 📖 Verwendung

### Forex/CFD Modus
1. Wähle Kategorie und Symbol
2. Gib Entry, Max SL (P1), und Take Profit ein
3. Setze Kontostand und Risiko %
4. Analysiere die 5-Split Positionen

### Futures Kleinst-System
1. Wähle "Futures" Kategorie
2. Wähle "Kleinst-System (1 Kontrakt)"
3. Setze Multiplikator (1 = 5 Kontrakte total)
4. Alle Details inkl. Ticks werden angezeigt

---

## 📸 Screenshots

*Coming soon*

---

## 🔧 Unterstützte Instrumente

### Futures
| Symbol | Tick Size | Tick Value | Punkt-Wert |
|--------|-----------|------------|------------|
| NQ | 0.25 | $5.00 | $20/Punkt |
| MNQ | 0.25 | $0.50 | $2/Punkt |
| ES | 0.25 | $12.50 | $50/Punkt |
| MES | 0.25 | $1.25 | $5/Punkt |
| YM | 1.0 | $5.00 | $5/Punkt |
| GC | 0.10 | $10.00 | $100/Punkt |
| CL | 0.01 | $10.00 | $1000/Punkt |

### Forex
EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, und 20+ Cross-Paare

### CFDs
XAUUSD (Gold), XAGUSD (Silber), US100, US500, US30, GER40, BTCUSD, ETHUSD

---

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE)

---

## 🤝 Contributing

Pull Requests sind willkommen! Für grössere Änderungen bitte zuerst ein Issue eröffnen.

---

## ⚠️ Disclaimer

Dieses Tool dient nur zu Bildungszwecken. Trading birgt erhebliche Risiken. Vergangene Performance ist kein Indikator für zukünftige Ergebnisse. Nutze dieses Tool auf eigene Verantwortung.

---

Made with 💎 and φ = 1.618...
