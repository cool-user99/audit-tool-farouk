# Module : Gestion de la base de données SQLite
# Auteur : Farouk
# Projet : audit-tool-farouk

import sqlite3
import os
from datetime import datetime


DB_PATH = "audit_tool.db"


def init_db():
    """
    Initialise la base de données et crée les tables.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table des équipements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipements (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nom       TEXT NOT NULL,
            ip        TEXT,
            type      TEXT,
            categorie TEXT,
            localisation TEXT
        )
    """)

    # Table des audits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            equipement    TEXT NOT NULL,
            fichier       TEXT NOT NULL,
            date_audit    TEXT NOT NULL,
            total_regles  INTEGER,
            nb_anomalies  INTEGER,
            score         INTEGER,
            rapport_path  TEXT
        )
    """)

    # Table des anomalies
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id    INTEGER,
            rule_id     TEXT,
            rule_name   TEXT,
            criticite   TEXT,
            message     TEXT,
            ligne       INTEGER,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] Base de données initialisée : audit_tool.db")


def save_audit(config, anomalies, rules, rapport_path):
    """
    Sauvegarde les résultats d'un audit dans la base de données.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    total    = len(rules)
    nb_anomalies = len(anomalies)
    score    = int(((total - nb_anomalies) / total) * 100) if total > 0 else 0

    # Insérer l'audit
    cursor.execute("""
        INSERT INTO audits (equipement, fichier, date_audit, total_regles, nb_anomalies, score, rapport_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        config["filename"].replace(".txt", ""),
        config["filepath"],
        config["date_import"],
        total,
        nb_anomalies,
        score,
        rapport_path
    ))

    audit_id = cursor.lastrowid

    # Insérer les anomalies
    for a in anomalies:
        cursor.execute("""
            INSERT INTO anomalies (audit_id, rule_id, rule_name, criticite, message, ligne)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            audit_id,
            a["rule_id"],
            a["rule_name"],
            a["criticite"],
            a["message"],
            a["ligne"]
        ))

    conn.commit()
    conn.close()
    print(f"[OK] Audit sauvegardé dans la base de données (ID: {audit_id})")
    return audit_id


def get_all_audits():
    """
    Retourne tous les audits enregistrés.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audits ORDER BY date_audit DESC")
    audits = cursor.fetchall()
    conn.close()
    return audits


def get_anomalies_by_audit(audit_id):
    """
    Retourne toutes les anomalies d'un audit.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anomalies WHERE audit_id = ?", (audit_id,))
    anomalies = cursor.fetchall()
    conn.close()
    return anomalies