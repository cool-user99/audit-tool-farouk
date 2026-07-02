#  NOTE DE CADRAGE

**Projet :** Outil d'Audit Automatisé des Configurations Réseau  
**Stagiaire :** Farouk  
**Responsable :** [Nom encadrant]  
**Date :** 01 Juillet 2026  
**Durée :** 30 jours  

---

## 1️ OBJECTIF GÉNÉRAL

Concevoir et développer un outil capable d'automatiser l'audit des configurations réseau en :
- Collectant automatiquement les configurations
- Les archivant avec versioning Git
- Vérifiant leur conformité selon un référentiel de 8 règles
- Détectant les changements entre versions
- Générant des rapports exploitables

---

## 2️ PÉRIMÈTRE

###  IN SCOPE (À faire)

**Collecte :**
- Import depuis fichiers locaux (texte)
- Format : Cisco IOS (show running-config)

**Archivage :**
- Sauvegarde centralisée
- Versioning avec Git
- Structure : equipment_name/version_X.txt

**Audit :**
- Vérification de 8 règles précises
- Classification par criticité
- Détection anomalies

**Reporting :**
- Génération HTML
- Export JSON
- Historique conservé

###  OUT OF SCOPE (À exclure)

-  Connexion SSH directe aux équipements (optionnel S6)
-  Supervision temps réel (Grafana, Prometheus)
-  Cloud (Azure, AWS)
-  Intégration SIEM
-  Machine Learning
-  Administration Linux classique

---

## 3️ TYPES DE CONFIGURATIONS SUPPORTÉS

**Équipements :** Routeurs Cisco IOS 15.x  
**Format fichier :** Texte brut (.txt)  
**Exemple :** Résultat de `show running-config`  

**Équipements de test :**
- ROUTER-PARIS (conforme)
- ROUTER-LYON (conforme)
- ROUTER-MARSEILLE (erreurs intentionnelles)

---

## 4️RÈGLES D'AUDIT PRIORITAIRES (8 au total)

| # | Règle | Criticité | Détection |
|---|-------|-----------|-----------|
| R1 | Hostname obligatoire | CRITICAL | `^hostname ` |
| R2 | Pas de secrets en clair | CRITICAL | `password .+` sans chiffrement |
| R3 | VLAN configurés |  MAJOR | `^vlan ` |
| R4 | Adresses IP valides |  MAJOR | Format X.X.X.X (X≤255) |
| R5 | Interfaces documentées |  MEDIUM | Interface avec `description` |
| R6 | Routes documentées |  MEDIUM | `ip route` avec commentaire |
| R7 | SSH obligatoire |  MEDIUM | `ssh version 2` |
| R8 | NTP configuré |  MEDIUM | `^ntp server` |

---

## 5 ARCHITECTURE CIBLE

### Flux Global