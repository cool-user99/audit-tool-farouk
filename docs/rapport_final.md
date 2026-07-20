# Rapport Final — NetAudit Pro (audit-tool-farouk)
## Informations générales

| Élément | Détail |
|---------|--------|
| Stagiaire | Farouk |
| Projet | audit-tool-farouk |
| Dépôt GitHub | github.com/cool-user99/audit-tool-farouk |
| Durée | 4 semaines |
| Langage | Python 3.x |

---

## 1. Objectif du projet

Concevoir et développer un outil Python permettant d'automatiser 
l'audit des fichiers de configuration réseau de type Cisco. 
L'outil détecte les anomalies, les classe par criticité et 
génère un rapport HTML.

---

## 2. Réalisations

### 2.1 Modules développés

| Module | Rôle |
|--------|------|
| `importer.py` | Chargement des fichiers de configuration |
| `analyzer.py` | Application des 8 règles d'audit |
| `reporter.py` | Génération des rapports HTML |
| `comparator.py` | Comparaison entre deux versions |
| `main.py` | Point d'entrée principal |

### 2.2 Référentiel de règles

8 règles d'audit définies en YAML :

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

### 2.3 Résultats de tests

| Fichier | Anomalies | Score |
|---------|-----------|-------|
| ROUTER-CONFORME.txt | 1 anomalie | 7/8 — 87%  |
| ROUTER-ERREURS.txt | 7 anomalies | 1/8 — 12%  |

---

## 3. Architecture technique
---

## 4. Fonctionnalités finalisées

-  Chargement automatique des fichiers de configuration
-  Analyse par expressions régulières
-  Classification des anomalies par criticité
-  Génération de rapports HTML professionnels
-  Comparaison entre deux versions de configuration
-  Score de conformité calculé automatiquement

## 5. Fonctionnalités non réalisées

-  Interface web (Flask) — hors périmètre
-  Base de données SQLite — non prioritaire
-  Connexion à de vrais équipements Cisco — hors périmètre

---

## 6. Difficultés rencontrées

| Difficulté | Solution adoptée |
|------------|-----------------|
| Encodage UTF-16 des fichiers | Détection et conversion en UTF-8 |
| Configuration Git remote | Ajout manuel du remote origin |
| Module yaml manquant | Installation via pip install pyyaml |
| Mauvais emplacement de reporter.py | Déplacement vers src/ |

---

## 7. Apports techniques

- Maîtrise de Python modulaire
- Utilisation des expressions régulières
- Gestion de fichiers YAML
- Génération de rapports HTML
- Versioning avec Git/GitHub
- Documentation technique professionnelle

---

## 8. Perspectives d'amélioration

- Ajouter une interface web avec Flask
- Connecter l'outil à de vrais équipements via SSH (Paramiko)
- Stocker les résultats dans une base SQLite
- Enrichir le référentiel avec plus de règles d'audit
- Générer des rapports PDF en plus du HTML

---

## 9. Conclusion

Le prototype est fonctionnel et répond aux objectifs 
du cahier des charges. L'outil permet d'auditer 
automatiquement des configurations réseau Cisco, 
de détecter les anomalies de sécurité et de conformité, 
et de générer des rapports clairs et exploitables.