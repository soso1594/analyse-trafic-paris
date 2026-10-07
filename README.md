# Trafic routier à Paris : Bd Barbes, Av. du Président Kennedy, Av. de la Grande Armée

> Projet du module Analyse et Transformation de Données (MSc DM2). Analyse en cours : M1 terminé, M2 en cours.

## La question
Comment le trafic évolue-t-il selon l'heure et le jour (semaine / week-end) sur mes trois axes parisiens de nature différente : un boulevard urbain, un axe de transit et une entrée d'agglomération ?

## Les données
- **Source** : comptages routiers permanents de la Ville de Paris (boucles électromagnétiques, mesures horaires).
- **Axes** : Bd_Barbes (12 tronçons), Av_Pdt_Kennedy (6), Av_Grande_Armee (4).
- **Période** : du 1er mars au 31 août 2026.
- **Volume** : 95 960 lignes, 11 colonnes (~12,6 Mo).
- **Pièges rencontrés** :
  Pour l'instant ,
  - `k` (taux d'occupation) est manquant dans ~9,6 % des lignes, `q` (débit) dans ~3,6 %.
  - `etat_trafic = Inconnu` correspond exactement aux lignes où `k` est manquant (9 169 lignes) : c'est une valeur manquante déguisée en texte.
  - Fuseau horaire, doublons, valeurs aberrantes de `q` : (j'en saurais plus , à compléter après M2 et M3.)

## Résultats
3 à 5 résultats chiffrés, avec 1 ou 2 graphiques.

## Limites
Ce que les données ne permettent pas de dire.

## Lancer le projet
```bash
pip install -r requirements.txt
python download_data.py
```
Puis exécuter les notebooks dans l'ordre.

## Utilisation de l'IA
J'ai utilisé Claude pour résoudre des problèmes d'installation (Git, e-mail GitHub, kernel Jupyter), corrigé les parties de codes qui ne marchaient pas.
