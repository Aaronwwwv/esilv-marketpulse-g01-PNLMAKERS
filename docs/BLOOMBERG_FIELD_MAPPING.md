# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source : data/sample/bloomberg_reference_sample.json
- Référence attendue : data/sample/bloomberg_reference_expected.json
- Connectivité Bloomberg live : non démontrée
- Le fichier docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md n'est pas présent dans le dépôt. Le mapping suit l'énoncé TD09 et le champ schema_note du fichier source.
- Les valeurs sont pédagogiques, reprises de prices.csv. Ce ne sont pas des observations Bloomberg certifiées.

## Market instruments

| Role | Ticker canonique | Identifiant Bloomberg |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| Champ MarketPulse | Champ source | Statut / notes |
|---|---|---|
| date | observation_date | clé d'enveloppe pédagogique, format YYYY-MM-DD |
| ticker | mapping applicatif | AAPL ou SP500 |
| open | open_value | clé d'enveloppe pédagogique |
| high | high_value | clé d'enveloppe pédagogique |
| low | low_value | clé d'enveloppe pédagogique |
| close | close_value | clé d'enveloppe pédagogique |
| volume | volume_value | 0 pour le benchmark (un indice n'a pas de volume) |

Les clés observation_date, open_value, high_value, low_value, close_value et volume_value sont des clés d'enveloppe pédagogiques. Ce ne sont pas des mnémoniques Bloomberg.

## Inspection

- Instrument AAPL US Equity : 21 observations, du 2026-09-01 au 2026-09-30.
- Benchmark SPX Index : 21 observations, mêmes dates, volume à 0.
- Aucun champ manquant dans l'échantillon.

## TD10 handoff

- Access mode : APPROVED_SAMPLE
- Identifiant instrument : AAPL US Equity
- Identifiant benchmark : SPX Index
- Représentation des dates : chaîne YYYY-MM-DD dans observation_date
- Structure d'entrée : liste series, avec role, canonical_ticker, provider_identifier, observations
- Champs manquants : aucun dans l'échantillon
- Notes de normalisation : garder SP500 comme ticker canonique, SPX Index reste à la frontière du fournisseur. Résultat attendu : data/sample/bloomberg_reference_expected.json