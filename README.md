# Trafic routier à Paris : Bd Barbes, Av. du Président Kennedy, Av. de la Grande Armée

> Projet du module Analyse et Transformation de Données (MSc DM2). Avancement : chargement (M1), nettoyage (M2) et transformation (M3) terminés ; analyse finale en cours.

## La question
Comment le trafic évolue-t-il selon l'heure et le jour (semaine / week-end) sur mes trois axes parisiens de nature différente : un boulevard urbain, un axe de transit et une entrée d'agglomération ?

## Les données
- **Source** : comptages routiers permanents de la Ville de Paris (boucles électromagnétiques, mesures horaires).
- **Axes** : Bd_Barbes (12 tronçons), Av_Pdt_Kennedy (6), Av_Grande_Armee (4).
- **Période** : du 1er mars au 31 août 2026.
- **Volume** : 95 960 lignes brutes, 22 tronçons (12 + 6 + 4), 4 416 heures attendues par tronçon..
- **Pièges rencontrés** :
  Pour l'instant ,
  - `k` (taux d'occupation) est manquant dans ~9,6 % des lignes, `q` (débit) dans ~3,6 %.
  - `etat_trafic = Inconnu` correspond exactement aux lignes où `k` est manquant (9 169 lignes) : c'est une valeur manquante déguisée en texte.
  - Fuseau horaire, doublons, valeurs aberrantes de `q` 
  - **Pièges rencontrés et traitements** :
  - **Fuseau horaire** : les dates sont en UTC (suffixe `+00:00`), ce que j'ai vérifié sur le 29 mars (23 h en heure de Paris, 24 h en UTC). Elles sont converties en heure de Paris.
  - **Valeurs manquantes** : `q` manque dans 3,6 % des lignes et `k` dans 9,6 %. Les 3 202 lignes `Invalide` ont `q` et `k` vides ; `Barré` (100 lignes) garde un débit renseigné.
  - **`Inconnu` = `k` manquant** : les 9 169 lignes `etat_trafic = Inconnu` sont exactement celles où `k` est vide.
  - **Heures absentes du fichier** : 52 heures manquent pour tous les capteurs, en 4 épisodes (24 h, 24 h, 3 h, 1 h). J'ai reconstruit une grille complète capteur × heure (97 152 lignes) avant toute interpolation.
  - **Doublons cachés** : aucune ligne dupliquée, mais le débit `q` ne compte que 13 séries différentes pour 22 tronçons (6 sur 12 pour Bd_Barbes, 3 sur 6 pour Av_Pdt_Kennedy, 4 sur 4 pour Av_Grande_Armee). Le débit semble recopié entre tronçons voisins ; `groupe_q` repère ces groupes.
  - **Capteur 5258 (Av_Grande_Armee)** : `k` est absent sur 98 % de ses heures.
  - **Interpolation** : limitée aux trous de 3 h ou moins entre deux mesures réelles ; les longues pannes restent vides. Les valeurs reconstituées sont marquées (`q_comble`, `k_comble`) et `q`, `k` d'origine sont conservés.
    - **Valeurs aberrantes de `q`** : l'IQR par capteur signale 580 valeurs sur 92 486, surtout des nuits calmes (534 trop basses, 78 % entre 3 h et 5 h), que je garde. Seules 2 valeurs à 5 421,95 véhicules/heure, physiquement incohérentes (non entières, très au-dessus du 99,9e percentile à 1 392), sont mises à `NaN`.
  - **Encodage** : `etat_trafic` est encodé en ordinal (l'occupation médiane `k` augmente de Fluide à Bloqué), avec `Inconnu` en `NaN` ; `etat_barre` est en one-hot.
  - **Variables temporelles** (heure, jour de la semaine, week-end, mois) calculées en heure de Paris.

## Résultats
On a aucune ligne dupliquée, mais le débit `q` ne compte que 13 séries différentes pour 22 capteurs (6 pour Bd_Barbes, 3 pour Av_Pdt_Kennedy, 4 pour Av_Grande_Armee). L'occupation `k` compte 20 séries pour 22 capteurs. Egalement les groupes partagés ont entre 94,6 % et 99,8 % de mesures présentes : ce ne sont pas des capteurs vides. Le plus grand groupe (4 capteurs de Bd_Barbes : 1630, 1632, 1634, 1636) est formé de tronçons consécutifs.

Conclusion: le débit semble recopié entre tronçons voisins. Une moyenne de débit par axe compterait plusieurs fois la même mesure, surtout sur Bd_Barbes. 

Sur la gestion des colonnes inutiles, on a que chaque capteur a 1 carrefour amont et au maximum 1 carrefours aval sur la période. `t_utc` et `t_paris` désignent le même instant. les colonnes de carrefours décrivent la géométrie du réseau, et `iu_ac` suffit à identifier un tronçon, je peux donc  les supprimer

Ainsi, je garde `t_paris` pour les analyses horaires et supprime `t_utc`, qui contient la même information.



## Limites
Les données ne disent pas pourquoi ce débit est partagé.
Les données ne disent pas pourquoi aussi un tronçon est `Invalide`, ni pourquoi le débit est identique sur des tronçons voisins.
Le débit étant partagé entre tronçons, une moyenne par axe risque de compter plusieurs fois la même mesure : je tiens compte de `groupe_q`.
`k` est inutilisable sur le capteur 5258.
On a trois axes seulement donc les conclusions ne se généralisent pas à tout Paris.

Le 12 avril, trois capteurs d'Av_Pdt_Kennedy partagent un débit allant jusqu'à 1 856 véhicules/heure alors que leur occupation va de 0 % à près de 97 % : la valeur est conservée (sous 2 000) mais reste incohérente. Les données ne permettent pas de dire lequel est juste, je le signale plutôt que d'inventer une règle.

## Lancer le projet
```bash
pip install -r requirements.txt
python download_data.py
```
Puis exécuter les notebooks dans l'ordre : `01_exploration.ipynb`, `02_nettoyage.ipynb` (écrit `data/processed/comptages_propres.parquet`), `03_transformation.ipynb` (écrit `data/processed/comptages_transformes.parquet`), puis l'analyse finale.


## Utilisation de l'IA
J'ai utilisé Claude pour résoudre des problèmes d'installation (Git, e-mail GitHub, kernel Jupyter), corrigé les parties de codes qui ne marchaient pas.
J'ai vérifié ses affirmations avec mes sorties : par exemple, mon texte disait que les valeurs trop hautes de l'IQR étaient « dispersées », ce que le calcul des jours les plus touchés a contredit (12 sur 46 tombent le même jour).