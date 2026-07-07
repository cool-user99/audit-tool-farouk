# Point d'entrée principal - audit-tool-farouk
# Auteur : Farouk
# Usage  : python main.py <fichier_config>

import sys
import os
from src.importer import load_config
from src.analyzer import load_rules, analyze_config, afficher_resultats
from src.reporter import generate_report

RULES_FILE = "rules/audit_rules.yaml"


def main():
    print("\n=== Audit Tool Farouk ===\n")

    if len(sys.argv) < 2:
        print("[USAGE] python main.py <fichier_config>")
        print("[EXEMPLE] python main.py configs/tests/ROUTER-ERREURS.txt")
        sys.exit(1)

    config_path = sys.argv[1]

    # Étape 1 — Charger la configuration
    print(">>> Étape 1 : Chargement de la configuration...")
    config = load_config(config_path)
    if config is None:
        sys.exit(1)

    # Étape 2 — Charger les règles
    print("\n>>> Étape 2 : Chargement des règles d'audit...")
    rules = load_rules(RULES_FILE)
    if not rules:
        sys.exit(1)

    # Étape 3 — Analyser
    print("\n>>> Étape 3 : Analyse en cours...")
    anomalies = analyze_config(config, rules)

    # Étape 4 — Afficher dans le terminal
    afficher_resultats(config, anomalies, rules)

    # Étape 5 — Générer le rapport HTML
    print(">>> Étape 5 : Génération du rapport HTML...")
    rapport_path = generate_report(config, anomalies, rules)
    print(f"\n[OK] Ouvre le rapport dans ton navigateur :")
    print(f"     {os.path.abspath(rapport_path)}\n")


if __name__ == "__main__":
    main()