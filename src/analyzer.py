# Module : Moteur d'analyse et application des règles d'audit
# Auteur : Farouk
# Projet : audit-tool-farouk

import re
import yaml


def load_rules(rules_file):
    """
    Charge les règles d'audit depuis le fichier YAML.
    """
    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print(f"[OK] {len(data['rules'])} règles chargées depuis {rules_file}")
        return data["rules"]
    except FileNotFoundError:
        print(f"[ERREUR] Fichier de règles introuvable : {rules_file}")
        return []
    except Exception as e:
        print(f"[ERREUR] Impossible de lire les règles : {e}")
        return []


def analyze_config(config, rules):
    """
    Applique les règles sur la configuration.
    Retourne la liste des anomalies détectées.
    """
    anomalies = []
    lines = config["lines"]
    full_text = "\n".join(lines)

    for rule in rules:
        rule_id    = rule.get("id", "???")
        rule_name  = rule.get("name", "???")
        criticite  = rule.get("criticite", "MINEURE")
        pattern    = rule.get("pattern", "")
        message    = rule.get("message_echec", "Anomalie détectée")
        inverse    = rule.get("inverse", False)

        # Chercher le pattern dans tout le texte
        match = re.search(pattern, full_text, re.MULTILINE)

        # inverse=False : le pattern DOIT être présent
        # inverse=True  : le pattern NE DOIT PAS être présent
        anomalie_detectee = (not match and not inverse) or (match and inverse)

        if anomalie_detectee:
            # Trouver le numéro de ligne
            ligne_num = None
            if match:
                ligne_num = full_text[:match.start()].count("\n") + 1

            anomalies.append({
                "rule_id"  : rule_id,
                "rule_name": rule_name,
                "criticite": criticite,
                "message"  : message,
                "ligne"    : ligne_num
            })

    return anomalies


def afficher_resultats(config, anomalies, rules):
    """
    Affiche les résultats de l'audit dans le terminal.
    """
    print("\n" + "="*55)
    print(f"  RAPPORT D'AUDIT — {config['filename']}")
    print(f"  Date : {config['date_import']}")
    print("="*55)

    if not anomalies:
        print("\n Aucune anomalie détectée — configuration conforme !\n")
    else:
        print(f"\n {len(anomalies)} anomalie(s) détectée(s) :\n")

        # Ordre d'affichage par criticité
        ordre = {"CRITIQUE": 1, "MAJEURE": 2, "MOYENNE": 3, "MINEURE": 4}
        anomalies_triees = sorted(anomalies, key=lambda x: ordre.get(x["criticite"], 5))

        for a in anomalies_triees:
            icon = {
                "CRITIQUE": "🔴",
                "MAJEURE" : "🟠",
                "MOYENNE" : "🟡",
                "MINEURE" : "🟢"
            }.get(a["criticite"], "⚪")

            ligne_info = f" (ligne {a['ligne']})" if a["ligne"] else ""
            print(f"  {icon} [{a['criticite']}] {a['message']}{ligne_info}")

    # Score de conformité
    total = len(rules)
    ok = total - len(anomalies)
    score = int((ok / total) * 100) if total > 0 else 0

    print("\n" + "-"*55)
    print(f"  Score de conformité : {ok}/{total} règles OK ({score}%)")
    print("="*55 + "\n")