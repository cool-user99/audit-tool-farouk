# Module : Génération des rapports d'audit au format HTML
# Auteur : Farouk
# Projet : NetAudit Pro

import os
from datetime import datetime


def generate_report(config, anomalies, rules, output_dir="reports"):
    """
    Génère un rapport d'audit professionnel au format HTML.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    date_str  = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename  = f"audit_{config['filename'].replace('.txt', '')}_{date_str}.html"
    output_path = os.path.join(output_dir, filename)

    # Calcul du score
    total        = len(rules)
    nb_anomalies = len(anomalies)
    nb_ok        = total - nb_anomalies
    score        = int((nb_ok / total) * 100) if total > 0 else 0

    # Couleur du score
    if score >= 80:
        score_color  = "#16a34a"
        score_label  = "Conforme"
        score_bg     = "#f0fdf4"
    elif score >= 50:
        score_color  = "#ca8a04"
        score_label  = "Partiellement conforme"
        score_bg     = "#fefce8"
    else:
        score_color  = "#dc2626"
        score_label  = "Non conforme"
        score_bg     = "#fef2f2"

    # Recommandations par règle
    recommandations = {
        "password_cleartext"  : "Utiliser 'enable secret' au lieu de 'enable password' pour chiffrer le mot de passe.",
        "ssh_check"           : "Configurer 'transport input ssh' sur les lignes VTY et activer SSH version 2.",
        "hostname_check"      : "Définir un hostname explicite avec la commande 'hostname <nom>'.",
        "interface_description": "Ajouter une description sur chaque interface avec 'description <texte>'.",
        "vlan_check"          : "Déclarer les VLANs nécessaires avec 'vlan <id>' et 'name <nom>'.",
        "ip_address_check"    : "Configurer une adresse IP sur chaque interface active.",
        "static_route_check"  : "Documenter les routes statiques avec des commentaires '!'.",
        "ntp_check"           : "Configurer un serveur NTP avec 'ntp server <ip>'.",
    }

    # Styles criticité
    criticite_style = {
        "CRITIQUE": {"color": "#dc2626", "bg": "#fef2f2", "border": "#fecaca", "icon": "CRITIQUE"},
        "MAJEURE" : {"color": "#ea580c", "bg": "#fff7ed", "border": "#fed7aa", "icon": "MAJEURE"},
        "MOYENNE" : {"color": "#ca8a04", "bg": "#fefce8", "border": "#fef08a", "icon": "MOYENNE"},
        "MINEURE" : {"color": "#16a34a", "bg": "#f0fdf4", "border": "#bbf7d0", "icon": "MINEURE"},
    }

    # Compter par criticité
    count_critique = len([a for a in anomalies if a["criticite"] == "CRITIQUE"])
    count_majeure  = len([a for a in anomalies if a["criticite"] == "MAJEURE"])
    count_moyenne  = len([a for a in anomalies if a["criticite"] == "MOYENNE"])
    count_mineure  = len([a for a in anomalies if a["criticite"] == "MINEURE"])

    # Trier anomalies
    ordre = {"CRITIQUE": 1, "MAJEURE": 2, "MOYENNE": 3, "MINEURE": 4}
    anomalies_triees = sorted(anomalies, key=lambda x: ordre.get(x["criticite"], 5))

    # Générer tableau anomalies
    rows_html = ""
    for a in anomalies_triees:
        style = criticite_style.get(a["criticite"], {"color": "#000", "bg": "#fff", "border": "#ddd", "icon": "INFO"})
        ligne_info = f"Ligne {a['ligne']}" if a["ligne"] else "—"
        recommandation = recommandations.get(a["rule_name"], "Vérifier la configuration manuellement.")

        rows_html += f"""
        <tr>
            <td>
                <span style="background:{style['bg']};color:{style['color']};
                border:1px solid {style['border']};padding:4px 10px;
                border-radius:20px;font-size:12px;font-weight:700;">
                    {style['icon']}
                </span>
            </td>
            <td><strong>{a['rule_id']}</strong></td>
            <td style="color:#64748b;font-size:13px;">{a['rule_name']}</td>
            <td>{a['message']}</td>
            <td style="color:#94a3b8;font-size:13px;">{ligne_info}</td>
            <td style="color:#64748b;font-size:12px;font-style:italic;">{recommandation}</td>
        </tr>"""

    # Générer tableau toutes les règles
    rules_ko_names = [a["rule_name"] for a in anomalies]
    all_rules_html = ""
    for rule in rules:
        is_ok = rule.get("name") not in rules_ko_names
        status_color = "#16a34a" if is_ok else "#dc2626"
        status_bg    = "#f0fdf4" if is_ok else "#fef2f2"
        status_border= "#bbf7d0" if is_ok else "#fecaca"
        status_text  = "Conforme" if is_ok else "Non conforme"

        all_rules_html += f"""
        <tr>
            <td><strong>{rule.get('id', '')}</strong></td>
            <td>{rule.get('name', '')}</td>
            <td style="color:#64748b;font-size:13px;">{rule.get('criticite', '')}</td>
            <td>
                <span style="background:{status_bg};color:{status_color};
                border:1px solid {status_border};padding:4px 12px;
                border-radius:20px;font-size:12px;font-weight:700;">
                    {status_text}
                </span>
            </td>
        </tr>"""

    # Barre de progression
    progress_width = score

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'audit — {config['filename']} — NetAudit Pro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Inter',Arial,sans-serif; background:#f8fafc; color:#1e293b; }}

        .header {{
            background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 100%);            
            color: white;
            padding: 40px;
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 30px;
        }}
        .brand {{ font-size: 14px; opacity: 0.7; margin-bottom: 8px; }}
        .header h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 8px; }}
        .header-meta {{ font-size: 13px; opacity: 0.7; }}
        .header-meta span {{ margin-right: 20px; }}

        .score-badge {{
            background: {score_bg};
            color: {score_color};
            border: 2px solid {score_color};
            border-radius: 12px;
            padding: 16px 28px;
            text-align: center;
            min-width: 140px;
        }}
        .score-badge .score-num {{
            font-size: 36px;
            font-weight: 800;
            line-height: 1;
        }}
        .score-badge .score-lbl {{
            font-size: 12px;
            font-weight: 600;
            margin-top: 4px;
        }}

        .progress-bar {{
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            width: {progress_width}%;
            background: {score_color};
            border-radius: 10px;
            transition: width 1s ease;
        }}
        .progress-label {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            opacity: 0.7;
            margin-top: 6px;
        }}

        .container {{ max-width: 1100px; margin: 30px auto; padding: 0 24px; }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid #f1f5f9;
        }}
        .stat-num {{ font-size: 32px; font-weight: 800; margin-bottom: 4px; }}
        .stat-lbl {{ font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; }}

        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid #f1f5f9;
            margin-bottom: 20px;
        }}
        .card h2 {{
            font-size: 16px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid #f1f5f9;
        }}

        table {{ width: 100%; border-collapse: collapse; }}
        th {{
            background: #f8fafc;
            color: #64748b;
            padding: 12px 14px;
            text-align: left;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-bottom: 2px solid #f1f5f9;
        }}
        td {{
            padding: 12px 14px;
            border-bottom: 1px solid #f8fafc;
            font-size: 13px;
        }}
        tr:hover td {{ background: #f8fafc; }}
        tr:last-child td {{ border-bottom: none; }}

        .empty-msg {{
            text-align: center;
            padding: 40px;
            color: #16a34a;
            font-weight: 600;
            font-size: 15px;
        }}

        .footer {{
            text-align: center;
            padding: 24px;
            font-size: 12px;
            color: #94a3b8;
            border-top: 1px solid #f1f5f9;
            margin-top: 20px;
        }}
    </style>
</head>
<body>

<div class="header">
    <div class="header-top">
        <div>
            <div class="brand">NetAudit Pro — Rapport d'audit automatisé</div>
            <h1>{config['filename']}</h1>
            <div class="header-meta">
                <span>Date : {config['date_import']}</span>
                <span>Chemin : {config['filepath']}</span>
                <span>Lignes : {config['total_lines']}</span>
            </div>
        </div>
        <div class="score-badge">
            <div class="score-num">{score}%</div>
            <div class="score-lbl">{score_label}</div>
        </div>
    </div>
    <div class="progress-bar">
        <div class="progress-fill"></div>
    </div>
    <div class="progress-label">
        <span>0%</span>
        <span>Score de conformité : {nb_ok}/{total} règles respectées</span>
        <span>100%</span>
    </div>
</div>

<div class="container">

    <!-- Statistiques -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-num" style="color:#0f172a">{total}</div>
            <div class="stat-lbl">Règles vérifiées</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#dc2626">{count_critique}</div>
            <div class="stat-lbl">Critiques</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#ea580c">{count_majeure}</div>
            <div class="stat-lbl">Majeures</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#ca8a04">{count_moyenne}</div>
            <div class="stat-lbl">Moyennes</div>
        </div>
    </div>

    <!-- Anomalies -->
    <div class="card">
        <h2>Anomalies détectées ({nb_anomalies})</h2>
        {"<table><thead><tr><th>Criticité</th><th>ID</th><th>Règle</th><th>Message</th><th>Ligne</th><th>Recommandation</th></tr></thead><tbody>" + rows_html + "</tbody></table>" if anomalies else '<div class="empty-msg">Aucune anomalie détectée — Configuration conforme !</div>'}
    </div>

    <!-- Toutes les règles -->
    <div class="card">
        <h2>Détail de toutes les règles ({total})</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Règle</th>
                    <th>Criticité</th>
                    <th>Statut</th>
                </tr>
            </thead>
            <tbody>
                {all_rules_html}
            </tbody>
        </table>
    </div>

</div>

<div class="footer">
    NetAudit Pro — Rapport généré le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}
</div>

</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Rapport généré : {output_path}")
    return output_path