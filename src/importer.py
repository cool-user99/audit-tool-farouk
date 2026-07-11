# Module : Import des fichiers de configuration réseau
# Auteur : Farouk
# Projet : audit-tool-farouk

import os
import shutil
from datetime import datetime


def load_config(filepath):
    """
    Charge un fichier de configuration réseau.
    Retourne un dictionnaire avec les infos du fichier.
    """
    if not os.path.exists(filepath):
        print(f"[ERREUR] Fichier introuvable : {filepath}")
        return None

    if not filepath.endswith(".txt"):
        print(f"[ERREUR] Format non supporté : {filepath}")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.rstrip() for line in lines]

    config = {
        "filename"    : os.path.basename(filepath),
        "filepath"    : filepath,
        "date_import" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_lines" : len(lines),
        "lines"       : lines
    }

    print(f"[OK] Configuration chargée : {config['filename']}")
    print(f"     Lignes lues : {config['total_lines']}")
    print(f"     Date import : {config['date_import']}")

    return config


def archive_config(filepath, backup_dir="configs/backups"):
    """
    Archive automatiquement le fichier de configuration
    dans configs/backups/ avec la date et l'heure.
    """
    if not os.path.exists(filepath):
        print(f"[ERREUR] Fichier introuvable : {filepath}")
        return None

    # Créer le dossier backups/ si inexistant
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Construire le nom du fichier archivé
    date_str  = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    basename  = os.path.basename(filepath).replace(".txt", "")
    archive_name = f"{basename}_{date_str}.txt"
    archive_path = os.path.join(backup_dir, archive_name)

    # Copier le fichier dans backups/
    shutil.copy2(filepath, archive_path)

    print(f"[OK] Configuration archivée : {archive_path}")
    return archive_path


def list_configs(directory):
    """
    Liste tous les fichiers .txt dans un dossier.
    """
    if not os.path.exists(directory):
        print(f"[ERREUR] Dossier introuvable : {directory}")
        return []

    files = [f for f in os.listdir(directory) if f.endswith(".txt")]

    if not files:
        print(f"[INFO] Aucun fichier trouvé dans : {directory}")
        return []

    print(f"[OK] {len(files)} fichier(s) trouvé(s) dans {directory} :")
    for f in files:
        print(f"     - {f}")

    return files