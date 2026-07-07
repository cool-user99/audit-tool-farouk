import os
from datetime import datetime


def generate_report(config, anomalies, rules, output_dir="reports"):
    """
    Génère un rapport d'audit au format HTML.
    Retourne le chemin du fichier généré.
    """

    # Créer le dossier reports/ si inexistant
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Nom du fichier rapport
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"audit_{config['filename'].replace('.txt', '')}_{date_str}.html"
    output_path = os.path.join(output_dir, filename)

    # Calcul du score
    total = len(rules)
    nb_anomalies = len(anomalies)
    nb_ok = total - nb_anomalies
    score = int((nb_ok / total) * 100) if total > 0 else 0

    # Couleur du score
    if score >= 80:
        score_color = "#28a745"
    elif score >= 50:
        score_color = "#ffc107"
    else:
        score_color = "#dc3545"

    # Icônes et couleurs par criticité
    criticite_style = {
        "CRITIQUE": {"color": "#dc3545", "bg": "#fdf0f0", "icon": "🔴"},
        "MAJEURE":  {"color": "#fd7e14", "bg": "#fff4ec", "icon": "🟠"},
        "MOYENNE":  {"color": "#ffc107", "bg": "#fffbec", "icon": "🟡"},
        "MINEURE":  {"color": "#28a745", "bg": "#f0fdf4", "icon": "🟢"},
    }

    # Trier anomalies par criticité
    ordre = {"CRITIQUE": 1, "MAJEURE": 2, "MOYENNE": 3, "MINEURE": 4}
    anomalies_triees = sorted(
        anomalies, key=lambda x: ordre.get(x["criticite"], 5)
    )

    # Générer les lignes du tableau anomalies
    rows_html = ""
    for a in anomalies_triees:
        style = criticite_style.get(a["criticite"], {"color": "#000", "bg": "#fff", "icon": "⚪"})
        ligne_info = f"Ligne {a['ligne']}" if a["ligne"] else "-"
        rows_html += f"""
        <tr style="background-color:{style['bg']}">
            <td>{style['icon']} <strong style="color:{style['color']}">{a['criticite']}</strong></td>
            <td>{a['rule_id']}</td>
            <td>{a['rule_name']}</td>
            <td>{a['message']}</td>
            <td>{ligne_info}</td>
        </tr>"""

    # Message si aucune anomalie
    if not anomalies_triees:
        rows_html = """
        <tr>
            <td colspan="5" style="text-align:center; color:#28a745; padding:20px;">
                ✅ Aucune anomalie détectée — configuration conforme !
            </td>
        </tr>"""

    # Générer le HTML complet
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'audit — {config['filename']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0; padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background-color: #1F3864;
            color: white;
            padding: 30px;
        }}
        .header h1 {{ margin: 0 0 5px 0; font-size: 24px; }}
        .header p  {{ margin: 5px 0; opacity: 0.85; font-size: 14px; }}
        .score-box {{
            display: inline-block;
            background: white;
            color: {score_color};
            border: 3px solid {score_color};
            border-radius: 8px;
            padding: 10px 25px;
            font-size: 28px;
            font-weight: bold;
            margin-top: 15px;
        }}
        .content {{ padding: 25px; }}
        .stats {{
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
        }}
        .stat-card {{
            flex: 1;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #ddd;
        }}
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
        }}
        .stat-card .label {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th {{
            background-color: #1F3864;
            color: white;
            padding: 12px;
            text-align: left;
            font-size: 13px;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
            font-size: 13px;
        }}
        tr:hover {{ opacity: 0.9; }}
        .footer {{
            text-align: center;
            padding: 15px;
            font-size: 12px;
            color: #999;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Rapport d'Audit Réseau</h1>
        <p>Fichier analysé : <strong>{config['filename']}</strong></p>
        <p>Date d'analyse : {config['date_import']}</p>
        <p>Chemin : {config['filepath']}</p>
        <div class="score-box">{nb_ok}/{total} — {score}%</div>
    </div>

    <div class="content">
        <div class="stats">
            <div class="stat-card" style="border-color:#1F3864">
                <div class="number" style="color:#1F3864">{total}</div>
                <div class="label">Règles vérifiées</div>
            </div>
            <div class="stat-card" style="border-color:#28a745">
                <div class="number" style="color:#28a745">{nb_ok}</div>
                <div class="label">Règles respectées</div>
            </div>
            <div class="stat-card" style="border-color:#dc3545">
                <div class="number" style="color:#dc3545">{nb_anomalies}</div>
                <div class="label">Anomalies détectées</div>
            </div>
            <div class="stat-card" style="border-color:{score_color}">
                <div class="number" style="color:{score_color}">{score}%</div>
                <div class="label">Score de conformité</div>
            </div>
        </div>

        <h2>Anomalies détectées</h2>
        <table>
            <thead>
                <tr>
                    <th>Criticité</th>
                    <th>ID Règle</th>
                    <th>Règle</th>
                    <th>Message</th>
                    <th>Ligne</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>

    <div class="footer">
        audit-tool-farouk — Rapport généré le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}
    </div>
</div>
</body>
</html>"""

    # Écrire le fichier
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Rapport généré : {output_path}")
    return output_path