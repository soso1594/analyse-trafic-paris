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
On a aucune ligne dupliquée, mais le débit `q` ne compte que 13 séries différentes pour 22 capteurs (6 pour Bd_Barbes, 3 pour Av_Pdt_Kennedy, 4 pour Av_Grande_Armee). L'occupation `k` compte 20 séries pour 22 capteurs. Egalement les groupes partagés ont entre 94,6 % et 99,8 % de mesures présentes : ce ne sont pas des capteurs vides. Le plus grand groupe (4 capteurs de Bd_Barbes : 1630, 1632, 1634, 1636) est formé de tronçons consécutifs.

Conclusion: le débit semble recopié entre tronçons voisins. Une moyenne de débit par axe compterait plusieurs fois la même mesure, surtout sur Bd_Barbes. 

Sur la gestion des colonnes inutiles, on a que chaque capteur a 1 carrefour amont et au maximum 1 carrefours aval sur la période. `t_utc` et `t_paris` désignent le même instant. les colonnes de carrefours décrivent la géométrie du réseau, et `iu_ac` suffit à identifier un tronçon, je peux donc  les supprimer

Ainsi, je garde `t_paris` pour les analyses horaires et supprime `t_utc`, qui contient la même information.

## Limites
Les données ne disent pas pourquoi ce débit est partagé.

## Lancer le projet
```bash
pip install -r requirements.txt
python download_data.py
```
Puis exécuter les notebooks dans l'ordre.

## Utilisation de l'IA
J'ai utilisé Claude pour résoudre des problèmes d'installation (Git, e-mail GitHub, kernel Jupyter), corrigé les parties de codes qui ne marchaient pas.
