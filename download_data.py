"""Télécharge votre tranche des comptages routiers permanents de la Ville de Paris.

1. Remplacez ROUTES par vos 3 axes (noms exacts de la colonne `axe` de liste_des_axes.csv).
2. Lancez : python download_data.py
3. Les données arrivent dans data/raw/comptages.csv (dossier ignoré par Git).

Source : https://opendata.paris.fr/explore/dataset/comptages-routiers-permanents/
"""
from pathlib import Path

import requests

ROUTES = []  # ex. ["Pyrenees", "Av_de_Clichy", "Voie_Mazas"]
DATE_DEBUT = "2026-03-01"
DATE_FIN = "2026-09-01"  # exclue

URL = ("https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/"
       "comptages-routiers-permanents/exports/csv")
COLONNES = ("iu_ac,libelle,t_1h,q,k,etat_trafic,iu_nd_amont,libelle_nd_amont,"
            "iu_nd_aval,libelle_nd_aval,etat_barre")
SORTIE = Path("data/raw/comptages.csv")


def main():
    if len(ROUTES) != 3:
        raise SystemExit("Renseignez vos 3 axes dans ROUTES avant de lancer le script.")
    axes = ",".join(f"'{r}'" for r in ROUTES)
    params = {
        "select": COLONNES,
        "where": f"libelle in ({axes}) and t_1h >= date'{DATE_DEBUT}' and t_1h < date'{DATE_FIN}'",
    }
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    print("Téléchargement en cours (1 à 3 minutes)...")
    with requests.get(URL, params=params, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(SORTIE, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    taille = SORTIE.stat().st_size / 1e6
    if taille < 0.01:
        raise SystemExit("Fichier vide : vérifiez l'orthographe de vos axes dans ROUTES.")
    print(f"{SORTIE} : {taille:.1f} Mo")


if __name__ == "__main__":
    main()
