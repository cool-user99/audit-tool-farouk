# Interface web Flask - audit-tool-farouk
# Auteur : Farouk
# Usage  : python app.py

import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from src.db_manager import init_db, get_all_audits, get_anomalies_by_audit

app = Flask(__name__)
app.config['APPLICATION_NAME'] = 'NetAudit Pro'
# Initialiser la base de données
init_db()


@app.route("/")
def index():
    """Page d'accueil — liste de tous les audits."""
    audits = get_all_audits()
    return render_template("index.html", audits=audits)


@app.route("/audit", methods=["GET", "POST"])
def audit():
    """Page pour lancer un nouvel audit."""
    # Lister les fichiers de configuration disponibles
    configs_dir = "configs/tests"
    fichiers = [f for f in os.listdir(configs_dir) if f.endswith(".txt")]

    message = None

    if request.method == "POST":
        fichier = request.form.get("fichier")
        if fichier:
            filepath = os.path.join(configs_dir, fichier)
            # Lancer l'audit via main.py
            result = subprocess.run(
                ["python", "main.py", filepath],
                capture_output=True, text=True
            )
            message = f"Audit de {fichier} terminé avec succès !"

    return render_template("audit.html", fichiers=fichiers, message=message)


@app.route("/rapport/<int:audit_id>")
def rapport(audit_id):
    """Page de détail d'un audit."""
    audits = get_all_audits()
    audit = next((a for a in audits if a[0] == audit_id), None)

    if audit is None:
        return "Audit introuvable", 404

    anomalies = get_anomalies_by_audit(audit_id)
    return render_template("rapport.html", audit=audit, anomalies=anomalies)


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/matrice")
def matrice():
    """Page matrice de conformité."""
    from src.db_manager import get_all_audits, get_anomalies_by_audit

    audits = get_all_audits()
    rules = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"]

    matrice_data = []
    for audit in audits:
        anomalies = get_anomalies_by_audit(audit[0])
        rules_ko = [a[3] for a in anomalies]

        row = {
            "equipement": audit[1],
            "score"     : audit[6],
            "rules"     : {}
        }
        for r in rules:
            rule_name = {
                "R1": "hostname_check",
                "R2": "password_cleartext",
                "R3": "interface_description",
                "R4": "vlan_check",
                "R5": "ip_address_check",
                "R6": "static_route_check",
                "R7": "ssh_check",
                "R8": "ntp_check"
            }.get(r)
            row["rules"][r] = "NO" if rule_name in rules_ko else "OK"

        matrice_data.append(row)

    return render_template("matrice.html", matrice=matrice_data, rules=rules)