# Guide d'utilisation — NetAudit Pro
## Deux modes d'utilisation

---

### Mode 1 — Audit d'une configuration

```bash
python main.py 
```

**Exemple :**
```bash
python main.py configs/tests/ROUTER-CONFORME.txt
python main.py configs/tests/ROUTER-ERREURS.txt
```

**Ce que l'outil fait :**
1. Charge le fichier de configuration
2. Applique les 8 règles d'audit
3. Affiche les anomalies dans le terminal
4. Génère un rapport HTML dans `reports/`