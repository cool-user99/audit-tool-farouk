# Module : Comparaison entre deux versions de configuration
# Auteur : Farouk
# Projet : NetAudit Pro

import os
import difflib
from datetime import datetime


def compare_configs(config1_path, config2_path):
    """
    Compare deux fichiers de configuration.
    Retourne un dictionnaire avec les différences détaillées.
    """

    if not os.path.exists(config1_path):
        print(f"[ERREUR] Fichier introuvable : {config1_path}")
        return None

    if not os.path.exists(config2_path):
        print(f"[ERREUR] Fichier introuvable : {config2_path}")
        return None

    with open(config1_path, "r", encoding="utf-8") as f:
        lignes_v1 = [line.rstrip() for line in f.readlines()]

    with open(config2_path, "r", encoding="utf-8") as f:
        lignes_v2 = [line.rstrip() for line in f.readlines()]

    # Comparaison avec difflib
    diff = list(difflib.unified_diff(
        lignes_v1,
        lignes_v2,
        fromfile=os.path.basename(config1_path),
        tofile=os.path.basename(config2_path),
        lineterm=""
    ))

    # Classer les lignes
    ajoutees   = [l[1:] for l in diff if l.startswith("+") and not l.startswith("+++")]
    supprimees = [l[1:] for l in diff if l.startswith("-") and not l.startswith("---")]

    set_v1 = set(lignes_v1)
    set_v2 = set(lignes_v2)
    inchangees = [l for l in lignes_v1 if l in set_v2]

    resultat = {
        "fichier_v1"  : os.path.basename(config1_path),
        "fichier_v2"  : os.path.basename(config2_path),
        "date_compare": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ajoutees"    : ajoutees,
        "supprimees"  : supprimees,
        "inchangees"  : inchangees,
        "total_v1"    : len(lignes_v1),
        "total_v2"    : len(lignes_v2),
        "diff"        : diff,
    }

    return resultat


def afficher_comparaison(resultat):
    """
    Affiche les différences de façon claire et structurée.
    """
    if resultat is None:
        return

    print("\n" + "="*60)
    print(f"  COMPARAISON DE CONFIGURATIONS — NetAudit Pro")
    print("="*60)
    print(f"  V1 : {resultat['fichier_v1']} ({resultat['total_v1']} lignes)")
    print(f"  V2 : {resultat['fichier_v2']} ({resultat['total_v2']} lignes)")
    print(f"  Date : {resultat['date_compare']}")
    print("="*60)

    # Résumé
    print(f"\n  RÉSUMÉ :")
    print(f"  ➕ Lignes ajoutées   : {len(resultat['ajoutees'])}")
    print(f"  ➖ Lignes supprimées : {len(resultat['supprimees'])}")
    print(f"  ✅ Lignes inchangées : {len(resultat['inchangees'])}")

    # Lignes ajoutées
    if resultat["ajoutees"]:
        print(f"\n{'='*60}")
        print(f"  ➕ AJOUTÉES dans V2 ({len(resultat['ajoutees'])}) :")
        print(f"{'='*60}")
        for ligne in resultat["ajoutees"]:
            if ligne.strip():
                print(f"  + {ligne}")

    # Lignes supprimées
    if resultat["supprimees"]:
        print(f"\n{'='*60}")
        print(f"  ➖ SUPPRIMÉES de V1 ({len(resultat['supprimees'])}) :")
        print(f"{'='*60}")
        for ligne in resultat["supprimees"]:
            if ligne.strip():
                print(f"  - {ligne}")

    # Conclusion
    print(f"\n{'='*60}")
    if not resultat["ajoutees"] and not resultat["supprimees"]:
        print("  Les deux configurations sont IDENTIQUES.")
    else:
        print(f"  {len(resultat['ajoutees']) + len(resultat['supprimees'])} différence(s) détectée(s) entre V1 et V2.")
    print("="*60 + "\n")


def generate_diff_report(resultat, output_dir="reports"):
    """
    Génère un rapport HTML de comparaison.
    """
    if resultat is None:
        return None

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    date_str  = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename  = f"diff_{resultat['fichier_v1'].replace('.txt','')}_{resultat['fichier_v2'].replace('.txt','')}_{date_str}.html"
    output_path = os.path.join(output_dir, filename)

    # Générer les lignes du diff
    diff_html = ""
    for ligne in resultat["diff"]:
        if ligne.startswith("+++") or ligne.startswith("---"):
            diff_html += f'<tr><td colspan="2" style="background:#f1f5f9;color:#64748b;font-size:12px;padding:6px 12px;">{ligne}</td></tr>'
        elif ligne.startswith("+"):
            diff_html += f'<tr><td style="background:#f0fdf4;color:#16a34a;padding:8px 12px;font-family:monospace;font-size:13px;width:50px;text-align:center;font-weight:700;">+</td><td style="background:#f0fdf4;color:#166534;padding:8px 12px;font-family:monospace;font-size:13px;">{ligne[1:]}</td></tr>'
        elif ligne.startswith("-"):
            diff_html += f'<tr><td style="background:#fef2f2;color:#dc2626;padding:8px 12px;font-family:monospace;font-size:13px;width:50px;text-align:center;font-weight:700;">-</td><td style="background:#fef2f2;color:#991b1b;padding:8px 12px;font-family:monospace;font-size:13px;">{ligne[1:]}</td></tr>'
        elif ligne.startswith("@@"):
            diff_html += f'<tr><td colspan="2" style="background:#eff6ff;color:#3b82f6;padding:6px 12px;font-size:12px;font-family:monospace;">{ligne}</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Comparaison — NetAudit Pro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Inter',sans-serif; background:#f8fafc; color:#1e293b; }}
        .header {{
            background: linear-gradient(135deg, #7f1d1d, #dc2626);
            color: white; 
            padding: 40px;
        }}
        .brand {{ font-size:13px; opacity:0.7; margin-bottom:8px; }}
        .header h1 {{ font-size:24px; font-weight:700; margin-bottom:8px; }}
        .header-meta {{ font-size:13px; opacity:0.7; }}
        .container {{ max-width:1100px; margin:30px auto; padding:0 24px; }}
        .stats-grid {{
            display:grid; grid-template-columns:repeat(3,1fr);
            gap:16px; margin-bottom:24px;
        }}
        .stat-card {{
            background:white; border-radius:12px; padding:20px;
            text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.06);
            border:1px solid #f1f5f9;
        }}
        .stat-num {{ font-size:32px; font-weight:800; margin-bottom:4px; }}
        .stat-lbl {{ font-size:11px; font-weight:600; color:#94a3b8; text-transform:uppercase; }}
        .card {{
            background:white; border-radius:12px; padding:24px;
            box-shadow:0 1px 3px rgba(0,0,0,0.06);
            border:1px solid #f1f5f9; margin-bottom:20px;
        }}
        .card h2 {{ font-size:16px; font-weight:700; margin-bottom:16px;
            padding-bottom:12px; border-bottom:1px solid #f1f5f9; }}
        table {{ width:100%; border-collapse:collapse; }}
        .footer {{ text-align:center; padding:24px; font-size:12px; color:#94a3b8; }}
    </style>
</head>
<body>
<div class="header">
    <div class="brand">NetAudit Pro — Rapport de comparaison</div>
    <h1>Comparaison de configurations</h1>
    <div class="header-meta">
        V1 : {resultat['fichier_v1']} ({resultat['total_v1']} lignes) &nbsp;|&nbsp;
        V2 : {resultat['fichier_v2']} ({resultat['total_v2']} lignes) &nbsp;|&nbsp;
        Date : {resultat['date_compare']}
    </div>
</div>

<div class="container">
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-num" style="color:#16a34a">+{len(resultat['ajoutees'])}</div>
            <div class="stat-lbl">Lignes ajoutées</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#dc2626">-{len(resultat['supprimees'])}</div>
            <div class="stat-lbl">Lignes supprimées</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#3b82f6">{len(resultat['inchangees'])}</div>
            <div class="stat-lbl">Lignes inchangées</div>
        </div>
    </div>

    <div class="card">
        <h2>Différences détaillées</h2>
        <table>{diff_html}</table>
    </div>
</div>

<div class="footer">
    NetAudit Pro — Rapport généré le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Rapport de comparaison généré : {output_path}")
    return output_path