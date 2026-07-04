# Module : Import des fichiers de configuration réseau
# Auteur : Farouk
# Projet : audit-tool-farouk

import os
from datetime import datetime


def load_config(filepath):
    """
    Charge un fichier de configuration réseau.
    Retourne un dictionnaire avec les infos du fichier.
    """
    # Vérifier si le fichier existe
    if not os.path.exists(filepath):
        print(f"[ERREUR] Fichier introuvable : {filepath}")
        return None

    # Vérifier si c'est bien un fichier texte
    if not filepath.endswith(".txt"):
        print(f"[ERREUR] Format non supporté : {filepath}")
        return None

    # Lire le fichier ligne par ligne
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Nettoyer les lignes (supprimer espaces inutiles)
    lines = [line.rstrip() for line in lines]

    # Construire le résultat
    config = {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "date_import": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_lines": len(lines),
        "lines": lines
    }

    print(f"[OK] Configuration chargée : {config['filename']}")
    print(f"     Lignes lues : {config['total_lines']}")
    print(f"     Date import : {config['date_import']}")

    return config


def list_configs(directory):
    """
    Liste tous les fichiers .txt dans un dossier.
    """
    if not os.path.exists(directory):
        print(f"[ERREUR] Dossier introuvable : {directory}")
        return []

    files = [f for f in os.listdir(directory) if f.endswith(".txt")]

    if not files:
        print(f"[INFO] Aucun fichier de configuration trouvé dans : {directory}")
        return []

    print(f"[OK] {len(files)} fichier(s) trouvé(s) dans {directory} :")
    for f in files:
        print(f"     - {f}")

    return files