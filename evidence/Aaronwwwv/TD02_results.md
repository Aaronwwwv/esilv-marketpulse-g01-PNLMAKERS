# TD02 - Python + CSV / JSON - Résultats

**Étudiant :** Aaron Dinguirard (@Aaronwwwv)
**Équipe :** PNL Makers - G01
**Environnement :** Windows + Git Bash, Python 3.12.10

---

## Partie 1 - Revue du starter

| Question | Réponse |
|---|---|
| Fonction qui lit le JSON | `load_instruments()` |
| Fonction qui lit le CSV | `load_prices()` |
| Fonction qui sélectionne un ticker | `filter_prices()` |
| Fonction qui coordonne l'exécution | `main()` |
| Emplacement des fichiers d'entrée | `data/sample/` (variable `DATA_DIR`) |

---

## Partie 2 - JSON et dictionnaires

```python
import sys
sys.path.insert(0, "src")
from main import load_instruments

instruments = load_instruments()
print(type(instruments))
print(instruments.keys())

instrument = instruments["instrument"]
benchmark = instruments["benchmark"]
print(instrument["ticker"])
print(instrument["name"])
print(instrument["currency"])
print(benchmark["ticker"])
print(benchmark["name"])
```
```
<class 'dict'>
dict_keys(['instrument', 'benchmark'])
AAPL
Apple Inc.
USD
SP500
S&P 500
```

- `instruments` est un dictionnaire qui contient deux objets métier : `instrument` et `benchmark`.
- `instrument` est un dictionnaire qui décrit l'instrument principal (AAPL).
- `benchmark` est un dictionnaire qui décrit l'indice de référence (S&P 500).

---

## Partie 3 - CSV et liste de dictionnaires

```python
import sys
sys.path.insert(0, "src")
from main import load_prices

prices = load_prices()
print(type(prices))
print(type(prices[0]))
print(prices[0])

print(prices[0]["close"])
print(type(prices[0]["close"]))
print(float(prices[0]["close"]))
```
```
<class 'list'>
<class 'dict'>
{'date': '2026-09-01', 'ticker': 'AAPL', 'open': '249.20', 'high': '251.50', 'low': '248.00', 'close': '250.00', 'volume': '38000000'}
250.00
<class 'str'>
250.0
```

- `prices` est une **liste**, et chaque élément `prices[0]` est un **dictionnaire** (une ligne du CSV).
- `csv.DictReader` lit chaque valeur comme du **texte** (`str`), même les prix.
- Il faut donc convertir avec `float()` avant tout calcul.

---

## Partie 4 - Filtrage instrument / benchmark

```python
import sys
sys.path.insert(0, "src")
from main import load_instruments, load_prices, filter_prices

instruments = load_instruments()
prices = load_prices()

instrument_prices = filter_prices(prices, instruments["instrument"]["ticker"])
benchmark_prices = filter_prices(prices, instruments["benchmark"]["ticker"])

print(len(instrument_prices))
print(len(benchmark_prices))
```
```
21
21
```

`filter_prices` parcourt toutes les lignes et garde celles dont le ticker correspond : boucle + condition + ajout = filtrage.

---

## Parties 5 à 7 - Nouvelles fonctions

```python
def get_first_close(prices):
    first_row = prices[0]
    return float(first_row["close"])


def get_last_close(prices):
    last_row = prices[-1]
    return float(last_row["close"])


def display_market_summary(asset, prices, show_currency=True):
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    if show_currency:
        currency = f" {asset['currency']}"
    else:
        currency = ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close  : {first_close:.2f}{currency}")
    print(f"Last close   : {last_close:.2f}{currency}")
```

- `get_first_close` et `get_last_close` lisent le prix de clôture de la première et de la dernière observation, et le convertissent en `float`.
- `display_market_summary` est une seule fonction réutilisée pour AAPL et pour le S&P 500 : même opération, données différentes.
- `show_currency=False` pour le S&P 500, car un indice s'exprime en points et pas en dollars.
- `main()` reste lisible : il charge, filtre, puis appelle les fonctions d'affichage.

---

## Partie 8 - Résultat final

```bash
python src/main.py
```
```
=== MarketPulse ===

Market configuration
Period   : 1 month
Interval : Daily

Instrument
AAPL - Apple Inc.
Observations : 21
First close  : 250.00 USD
Last close   : 266.20 USD

Benchmark
SP500 - S&P 500
Observations : 21
First close  : 6600.00
Last close   : 6742.00
```

---

## Validation CORE

- [x] MarketPulse tourne toujours avec `python src/main.py`
- [x] `instruments.json` chargé
- [x] `prices.csv` chargé
- [x] Lignes AAPL et SP500 séparées
- [x] 21 observations pour chaque série
- [x] Premier close affiché pour chaque série
- [x] Dernier close affiché pour chaque série
- [x] Conversion numérique des close avant utilisation
- [x] Logique de résumé réutilisable
- [x] Modifications Python prêtes pour le TD03