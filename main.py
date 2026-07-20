# Point d'entrée principal - audit-tool-farouk
# Auteur : Farouk
# Usage  : python main.py <fichier_config>
#  python main.py <fichier_v1> <fichier_v2>

import sys
import os
from src.importer import load_config, archive_config
from src.analyzer import load_rules, analyze_config, afficher_resultats
from src.reporter import generate_report
from src.comparator import compare_configs, afficher_comparaison
from src.db_manager import init_db, save_audit


RULES_FILE = "rules/audit_rules.yaml"


def main():
    print("\n=== NetAudit Pro (audit-tool-farouk) ===\n")

    # Initialiser la base de données
    init_db()

    if len(sys.argv) < 2:
        print("[USAGE] python main.py <fichier_config>")
        print("[USAGE] python main.py <fichier_v1> <fichier_v2>")
        sys.exit(1)

    # Mode comparaison — 2 fichiers
    if len(sys.argv) == 3:
        print(">>> Mode comparaison de deux configurations...\n")
        resultat = compare_configs(sys.argv[1], sys.argv[2])
        afficher_comparaison(resultat)
        return

    # Mode audit — 1 fichier
    config_path = sys.argv[1]

    # Étape 1 — Charger la configuration
    print(">>> Étape 1 : Chargement de la configuration...")
    config = load_config(config_path)
    if config is None:
        sys.exit(1)

    # Étape 2 — Archiver automatiquement
    print("\n>>> Étape 2 : Archivage automatique...")
    archive_config(config_path)

    # Étape 3 — Charger les règles
    print("\n>>> Étape 3 : Chargement des règles d'audit...")
    rules = load_rules(RULES_FILE)
    if not rules:
        sys.exit(1)

    # Étape 4 — Analyser
    print("\n>>> Étape 4 : Analyse en cours...")
    anomalies = analyze_config(config, rules)

    # Étape 5 — Afficher dans le terminal
    afficher_resultats(config, anomalies, rules)

    # Étape 6 — Générer le rapport HTML
    print(">>> Étape 6 : Génération du rapport HTML...")
    rapport_path = generate_report(config, anomalies, rules)

    # Étape 7 — Sauvegarder dans SQLite
    print(">>> Étape 7 : Sauvegarde dans la base de données...")
    save_audit(config, anomalies, rules, rapport_path)

    print(f"\n[OK] Rapport disponible ici :")
    print(f"     {os.path.abspath(rapport_path)}\n")


if __name__ == "__main__":
    main()