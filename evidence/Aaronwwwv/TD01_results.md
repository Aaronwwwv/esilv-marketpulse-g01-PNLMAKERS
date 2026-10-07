# TD01 - Bootstrap + Linux - Résultats

**Étudiant :** Aaron [Nom] (@Aaronwwwv)
**Équipe :** PNL Makers - G01
**Dépôt :** `esilv-marketpulse-g01-PNLMAKERS`
**Environnement :** Windows + Git Bash

---

## Partie 2-3 - Dépôt d'équipe et TEAM.md

- Groupe de TD : G01
- Équipe : PNL Makers
- Dépôt : `esilv-marketpulse-g01-PNLMAKERS`
- Collaborateurs : @Aaronwwwv, @Justglz, @FlorianDubreu, @KillianCalais
- TEAM.md créé et mergé via Pull Request.


## Partie 5 - Navigation Linux

### 5.1 Dossier courant

```bash
pwd
```
```
/c/Users/aaron/esilv-marketpulse-g01-PNLMAKERS
```
`pwd` affiche le chemin absolu du dossier dans lequel le terminal travaille.

### 5.2 Lister les fichiers

```bash
ls
```
```
config/          evidence/   README.md         TEAM.md
CONTRIBUTING.md  labs/       requirements.txt  TEAM_TEMPLATE.md
data/            readiness/  src/
```

```bash
ls -la
```
```
drwxr-xr-x 1 aaron 197609     0 Oct  7 15:57 ./
drwxr-xr-x 1 aaron 197609     0 Oct  7 16:24 ../
drwxr-xr-x 1 aaron 197609     0 Oct  7 16:25 .git/
-rw-r--r-- 1 aaron 197609   199 Oct  7 14:46 .gitignore
drwxr-xr-x 1 aaron 197609     0 Oct  7 14:46 config/
-rw-r--r-- 1 aaron 197609  3126 Oct  7 14:46 CONTRIBUTING.md
drwxr-xr-x 1 aaron 197609     0 Oct  7 14:46 data/
drwxr-xr-x 1 aaron 197609     0 Oct  7 16:12 evidence/
drwxr-xr-x 1 aaron 197609     0 Oct  7 14:46 labs/
drwxr-xr-x 1 aaron 197609     0 Oct  7 14:46 readiness/
-rw-r--r-- 1 aaron 197609 10747 Oct  7 14:46 README.md
-rw-r--r-- 1 aaron 197609   135 Oct  7 14:46 requirements.txt
drwxr-xr-x 1 aaron 197609     0 Oct  7 14:46 src/
-rw-r--r-- 1 aaron 197609  1528 Oct  7 15:57 TEAM.md
-rw-r--r-- 1 aaron 197609  1508 Oct  7 14:46 TEAM_TEMPLATE.md
```
`ls` liste le contenu du dossier. `-l` affiche les détails (droits, taille, date) et `-a` inclut les fichiers cachés comme `.gitignore` et `.git`.

### 5.3 Naviguer vers les données

```bash
cd data
pwd
ls
cd sample
pwd
ls
cd ../..
pwd
```
```
/c/Users/aaron/esilv-marketpulse-g01-PNLMAKERS/data
sample/
/c/Users/aaron/esilv-marketpulse-g01-PNLMAKERS/data/sample
bloomberg_reference_expected.json  instruments.json
bloomberg_reference_sample.json    prices.csv
/c/Users/aaron/esilv-marketpulse-g01-PNLMAKERS
```
`cd` change de dossier. `cd ../..` remonte de deux niveaux, ce qui ramène à la racine du dépôt.

---

## Partie 6 - Inspection des données

### 6.1 Métadonnées JSON

```bash
cat data/sample/instruments.json
```
```json
{
  "instrument": {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "currency": "USD",
    "market": "NASDAQ"
  },
  "benchmark": {
    "ticker": "SP500",
    "name": "S&P 500",
    "currency": "USD",
    "market": "US"
  }
}
```

1. **Instrument :** AAPL - Apple Inc. (USD, NASDAQ)
2. **Benchmark :** SP500 - S&P 500 (USD, US)
3. **Où sont stockés noms et tickers :** dans `data/sample/instruments.json`, sous les clés `instrument` et `benchmark`, dans les champs `ticker` et `name`.

### 6.2 Observations CSV

```bash
head data/sample/prices.csv
```
```
date,ticker,open,high,low,close,volume
2026-09-01,AAPL,249.20,251.50,248.00,250.00,38000000
2026-09-01,SP500,6592.00,6615.00,6580.00,6600.00,0
2026-09-02,AAPL,250.80,252.80,249.60,251.30,39500000
2026-09-02,SP500,6607.00,6627.00,6595.00,6612.00,0
2026-09-03,AAPL,249.60,251.30,248.40,249.80,41000000
2026-09-03,SP500,6596.00,6613.00,6584.00,6598.00,0
2026-09-04,AAPL,251.30,253.60,250.10,252.10,42500000
2026-09-04,SP500,6612.00,6635.00,6600.00,6620.00,0
2026-09-08,AAPL,251.90,253.90,250.70,252.40,44000000
```
`head` affiche les 10 premières lignes. Colonnes : date, ticker, open, high, low, close, volume.

```bash
grep AAPL data/sample/prices.csv
```
```
2026-09-14,AAPL,256.60,258.30,255.40,256.80,42500000
2026-09-15,AAPL,257.20,259.50,256.00,258.00,44000000
2026-09-16,AAPL,256.70,258.70,255.50,257.20,38000000
2026-09-17,AAPL,259.20,260.90,258.00,259.40,39500000
2026-09-18,AAPL,259.30,261.60,258.10,260.10,41000000
2026-09-21,AAPL,259.10,261.10,257.90,259.60,42500000
2026-09-22,AAPL,261.10,262.80,259.90,261.30,44000000
2026-09-23,AAPL,261.20,263.50,260.00,262.00,38000000
2026-09-24,AAPL,263.00,265.00,261.80,263.50,39500000
2026-09-25,AAPL,262.60,264.30,261.40,262.80,41000000
2026-09-28,AAPL,263.30,265.60,262.10,264.10,42500000
2026-09-29,AAPL,264.50,266.50,263.30,265.00,44000000
2026-09-30,AAPL,266.00,267.70,264.80,266.20,38000000
```

```bash
grep SP500 data/sample/prices.csv
```
```
2026-09-01,SP500,6592.00,6615.00,6580.00,6600.00,0
2026-09-02,SP500,6607.00,6627.00,6595.00,6612.00,0
2026-09-03,SP500,6596.00,6613.00,6584.00,6598.00,0
2026-09-04,SP500,6612.00,6635.00,6600.00,6620.00,0
2026-09-08,SP500,6623.00,6643.00,6611.00,6628.00,0
2026-09-09,SP500,6640.00,6657.00,6628.00,6642.00,0
2026-09-10,SP500,6642.00,6665.00,6630.00,6650.00,0
2026-09-11,SP500,6642.00,6662.00,6630.00,6647.00,0
2026-09-14,SP500,6663.00,6680.00,6651.00,6665.00,0
2026-09-15,SP500,6664.00,6687.00,6652.00,6672.00,0
2026-09-16,SP500,6663.00,6683.00,6651.00,6668.00,0
2026-09-17,SP500,6683.00,6700.00,6671.00,6685.00,0
2026-09-18,SP500,6684.00,6707.00,6672.00,6692.00,0
2026-09-21,SP500,6683.00,6703.00,6671.00,6688.00,0
2026-09-22,SP500,6703.00,6720.00,6691.00,6705.00,0
2026-09-23,SP500,6704.00,6727.00,6692.00,6712.00,0
2026-09-24,SP500,6715.00,6735.00,6703.00,6720.00,0
2026-09-25,SP500,6713.00,6730.00,6701.00,6715.00,0
2026-09-28,SP500,6720.00,6743.00,6708.00,6728.00,0
2026-09-29,SP500,6729.00,6749.00,6717.00,6734.00,0
2026-09-30,SP500,6740.00,6757.00,6728.00,6742.00,0
```
`grep` filtre les lignes qui contiennent un texte. Le même CSV contient donc les observations de l'instrument et du benchmark.

---

## Partie 7 - Vérification de l'environnement

```bash
python --version
git --version
```
```
Python 3.12.10
git version 2.53.0.windows.2
```

```bash
python src/main.py
```
```
=== MarketPulse ===

Instrument
AAPL - Apple Inc.
Last price: 266.20 USD

Benchmark
SP500 - S&P 500
Last level: 6742.00

Period: 1 month
Interval: Daily

Observations
AAPL: 21
SP500: 21
```

| Élément | Emplacement |
|---|---|
| Programme | `src/main.py` |
| Métadonnées | `data/sample/instruments.json` |
| Prix journaliers | `data/sample/prices.csv` |
| Instrument | AAPL |
| Benchmark | SP500 / S&P 500 |

---

## Partie 8 - Validation CORE

- [ ] Accès au dépôt d'équipe
- [ ] Nom du dépôt connu
- [ ] pwd, ls, cd, cat, head, grep utilisés
- [ ] Fichier JSON de métadonnées identifié
- [ ] Fichier CSV de prix identifié
- [ ] Versions de Python et Git vérifiées
- [ ] `python src/main.py` fonctionne
- [ ] Instrument et benchmark identifiés