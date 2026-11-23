"""Script de téléchargement et de vérification du jeu de données IRVE.

Source : transport.data.gouv.fr / data.gouv.fr
Jeu de données : Base Nationale des Points de Recharge pour Véhicules Électriques (IRVE - statique)
"""

import os
import sys
import urllib.request
import json

DATASET_API_URL = "https://www.data.gouv.fr/api/1/datasets/base-nationale-des-points-de-recharge-pour-vehicules-electriques-en-france-irve/"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "irve_statique.csv")


def get_latest_csv_url() -> str:
    """Récupère l'URL directe du fichier CSV consolidé statique via l'API data.gouv.fr."""
    print("Interrogation de l'API data.gouv.fr...")
    req = urllib.request.Request(DATASET_API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        for res in data.get("resources", []):
            title = res.get("title", "").lower()
            fmt = res.get("format", "").lower()
            url = res.get("url", "")
            # Chercher le fichier statique consolidé CSV
            if "statique" in title and "non" not in title and ("csv" in fmt or url.endswith(".csv")):
                return url
        # Fallback première ressource CSV
        for res in data.get("resources", []):
            if res.get("format", "").lower() == "csv":
                return res.get("url", "")
    raise RuntimeError("Impossible de trouver la ressource CSV dans le jeu de données.")


def download_dataset():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 1000:
        print(f"[OK] Le fichier existe déjà : {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} Mo)")
        return

    try:
        csv_url = get_latest_csv_url()
        print(f"Téléchargement depuis : {csv_url}")
        print(f"Destination : {OUTPUT_FILE}")
        req = urllib.request.Request(csv_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response, open(OUTPUT_FILE, "wb") as out_file:
            data = response.read()
            out_file.write(data)
        print(f"[SUCCÈS] Téléchargement terminé : {os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} Mo")
    except Exception as e:
        print(f"[ERREUR] Échec du téléchargement automatique : {e}")
        print("Vous pouvez télécharger le fichier manuellement depuis :")
        print("https://transport.data.gouv.fr/datasets/base-nationale-des-points-de-recharge-pour-vehicules-electriques-en-france-irve")
        print(f"et le placer sous : {OUTPUT_FILE}")


if __name__ == "__main__":
    download_dataset()
