# NetAudit Pro — audit-tool-farouk

> Outil automatisé d'audit des configurations réseau Cisco
> Développé par Farouk dans le cadre d'un stage d'été

## Description
NetAudit Pro est un outil Python qui analyse automatiquement 
les fichiers de configuration réseau, détecte les anomalies 
de sécurité et génère des rapports HTML professionnels.

##  Objectif

Automatiser l'audit des configurations réseau :
- Collecte automatisée des configurations
- Archivage versionné avec Git
- Vérification des règles d'audit
- Comparaison entre versions
- Génération de rapports

## 📋 Périmètre

### ✅ IN SCOPE
- Configurations Cisco IOS
- Fichiers locaux (texte)
- 8 règles d'audit
- Archivage + versioning Git
- Comparaison entre versions
- Rapports HTML/JSON

###  OUT OF SCOPE
- Connexion SSH directe (optionnel S6)
- Cloud (Azure/AWS)
- Supervision temps réel
- Machine Learning
