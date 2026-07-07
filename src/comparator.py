import os
from datetime import datetime


def compare_configs(config1_path, config2_path):
    """
    Compare deux fichiers de configuration.
    Retourne un dictionnaire avec les lignes ajoutées,
    supprimées et modifiées.
    """

    # Vérifier les deux fichiers
    if not os.path.exists(config1_path):
        print(f"[ERREUR] Fichier introuvable : {config1_path}")
        return None

    if not os.path.exists(config2_path):
        print(f"[ERREUR] Fichier introuvable : {config2_path}")
        return None

    # Lire les deux fichiers
    with open(config1_path, "r", encoding="utf-8") as f:
        lignes_v1 = [line.rstrip() for line in f.readlines()]

    with open(config2_path, "r", encoding="utf-8") as f:
        lignes_v2 = [line.rstrip() for line in f.readlines()]

    # Comparer les lignes
    ajoutees   = []
    supprimees = []
    inchangees = []

    set_v1 = set(lignes_v1)
    set_v2 = set(lignes_v2)

    for ligne in lignes_v2:
        if ligne not in set_v1:
            ajoutees.append(ligne)

    for ligne in lignes_v1:
        if ligne not in set_v2:
            supprimees.append(ligne)

    for ligne in lignes_v1:
        if ligne in set_v2:
            inchangees.append(ligne)

    # Résultat
    resultat = {
        "fichier_v1"  : os.path.basename(config1_path),
        "fichier_v2"  : os.path.basename(config2_path),
        "date_compare": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ajoutees"    : ajoutees,
        "supprimees"  : supprimees,
        "inchangees"  : inchangees,
        "total_v1"    : len(lignes_v1),
        "total_v2"    : len(lignes_v2),
    }

    return resultat


def afficher_comparaison(resultat):
    """
    Affiche les différences entre deux configs dans le terminal.
    """
    if resultat is None:
        return

    print("\n" + "="*55)
    print(f"  COMPARAISON DE CONFIGURATIONS")
    print(f"  V1 : {resultat['fichier_v1']} ({resultat['total_v1']} lignes)")
    print(f"  V2 : {resultat['fichier_v2']} ({resultat['total_v2']} lignes)")
    print(f"  Date : {resultat['date_compare']}")
    print("="*55)

    # Lignes ajoutées
    if resultat["ajoutees"]:
        print(f"\n➕ Lignes ajoutées dans V2 ({len(resultat['ajoutees'])}) :")
        for ligne in resultat["ajoutees"]:
            if ligne.strip():
                print(f"   + {ligne}")
    else:
        print("\n➕ Aucune ligne ajoutée")

    # Lignes supprimées
    if resultat["supprimees"]:
        print(f"\n➖ Lignes supprimées de V1 ({len(resultat['supprimees'])}) :")
        for ligne in resultat["supprimees"]:
            if ligne.strip():
                print(f"   - {ligne}")
    else:
        print("\n➖ Aucune ligne supprimée")

    print("\n" + "-"*55)
    print(f"  Lignes inchangées : {len(resultat['inchangees'])}")
    print(f"  Lignes ajoutées   : {len(resultat['ajoutees'])}")
    print(f"  Lignes supprimées : {len(resultat['supprimees'])}")
    print("="*55 + "\n")