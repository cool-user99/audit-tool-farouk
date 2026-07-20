# Guide d'installation — NetAudit Pro
## Prérequis

| Outil | Version | Vérification |
|-------|---------|--------------|
| Python | 3.x | `python --version` |
| Git | 2.x | `git --version` |
| VS Code | dernière | — |

---

## Étape 1 — Cloner le dépôt

```bash
git clone https://github.com/cool-user99/audit-tool-farouk.git
cd audit-tool-farouk
```

---

## Étape 2 — Installer les dépendances

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient :

## Étape 3 — Vérifier la structure

```bash
tree
```

### Mode 2 — Comparaison entre deux versions

```bash
python main.py <fichier_v1> <fichier_v2>
```

**Exemple :**
```bash
python main.py configs/tests/ROUTER-CONFORME.txt configs/tests/ROUTER-ERREURS.txt
```

**Ce que l'outil fait :**
1. Charge les deux fichiers
2. Compare ligne par ligne
3. Affiche les différences


---

## Les 8 règles d'audit

| ID | Règle | Criticité |
|----|-------|-----------|
| R1 | Hostname présent | MAJEURE |
| R2 | Pas de mot de passe en clair | CRITIQUE |
| R3 | Interfaces avec description | MOYENNE |
| R4 | VLAN déclarés | MOYENNE |
| R5 | Adresses IP présentes | MAJEURE |
| R6 | Routes statiques documentées | MOYENNE |
| R7 | SSH configuré | CRITIQUE |
| R8 | NTP configuré | MINEURE |

---

## Lire le rapport HTML

Après chaque audit, un rapport HTML est généré dans `reports/` :

```bash
# Ouvrir dans le navigateur (Windows)
start reports\audit_ROUTER-ERREURS_2026-07-05.html
```

---

## Ajouter un nouveau fichier de configuration

1. Copie ton fichier `.txt` dans `configs/tests/`
2. Lance l'audit :
```bash
python main.py configs/tests/MON-ROUTEUR.txt
```
3. Le rapport est généré automatiquement dans `reports/`