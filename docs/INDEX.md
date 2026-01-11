# 📚 Index de la Documentation

Guide de navigation pour tous les documents du projet DnD5e-Scenarios

---

## 🚀 Démarrage Rapide

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | **Point d'entrée principal** - Installation et lancement |
| [LISTE_SCENARIOS.md](LISTE_SCENARIOS.md) | **Liste complète** des 36 scénarios disponibles |

---

## 📖 Guides pour Utilisateurs

### Jouer aux Scénarios

- **[README.md](../README.md)** - Comment lancer les scénarios
- **[LISTE_SCENARIOS.md](LISTE_SCENARIOS.md)** - Tableau complet avec niveaux, durées, difficultés

### Utiliser le Launcher

```bash
python launcher.py  # Interface colorée pour choisir un scénario
```

---

## 🛠️ Guides pour Créateurs

### Enrichir un Scénario

| Document | Contenu |
|----------|---------|
| **[GUIDE_ENRICHISSEMENT.md](GUIDE_ENRICHISSEMENT.md)** | Guide complet étape par étape |
| **[ENRICHISSEMENT_MANUEL.md](ENRICHISSEMENT_MANUEL.md)** | Méthode d'analyse approfondie |
| **[ENRICHISSEMENT_SCENARIO.md](ENRICHISSEMENT_SCENARIO.md)** | Exemple : Le Masque Utruz |

### Outils Disponibles

1. **`analyze_pdf_deep.py`** - Analyser un PDF en profondeur
2. **`enrich_batch.py`** - Analyser plusieurs PDFs en batch
3. **`launcher.py`** - Lanceur universel

---

## 📊 Documentation Technique

### Système de Scénarios

- **[README_SCENARIOS_JSON.md](README_SCENARIOS_JSON.md)** - Format JSON des scénarios
- **src/scenarios/** - Code source du système
- **src/scenes/** - Système de scènes

### Enrichissement

| Document | Description |
|----------|-------------|
| [ENRICHISSEMENT_MANUEL.md](ENRICHISSEMENT_MANUEL.md) | Méthode manuelle vs automatique |
| [ENRICHISSEMENT_MASSIF.md](ENRICHISSEMENT_MASSIF.md) | Enrichissement de 25 scénarios |
| [ENRICHISSEMENT_SCENARIO.md](ENRICHISSEMENT_SCENARIO.md) | Exemple détaillé (Masque Utruz) |

---

## 📦 Organisation du Projet

### Structure des Dossiers

```
DnD5e-Scenarios/
├── launcher.py              # 🚀 POINT D'ENTRÉE
├── README.md                # Documentation principale
│
├── *_game.py                # Scripts de scénarios
├── data/scenes/             # Scénarios JSON
├── scenarios/               # PDFs officiels
├── analysis/                # Analyses de PDFs
│
├── docs/                    # 📚 Documentation
│   ├── INDEX.md                      # Ce fichier
│   ├── GUIDE_ENRICHISSEMENT.md       # Guide complet
│   ├── ENRICHISSEMENT_MANUEL.md      # Méthode approfondie
│   ├── ENRICHISSEMENT_SCENARIO.md    # Exemple
│   ├── ENRICHISSEMENT_MASSIF.md      # Batch
│   ├── LISTE_SCENARIOS.md            # Tous les scénarios
│   ├── README_SCENARIOS_JSON.md      # Format JSON
│   └── archive/                      # Docs obsolètes
│
├── src/                     # Code source
├── savegames/               # Sauvegardes
└── tokens/                  # Images
```

---

## 🎯 Par Cas d'Usage

### Je veux jouer à un scénario

1. Lisez [README.md](../README.md) - Section "Lancement Rapide"
2. Lancez `python launcher.py`
3. Choisissez un scénario dans le menu

### Je veux créer un scénario

1. Lisez [GUIDE_ENRICHISSEMENT.md](GUIDE_ENRICHISSEMENT.md)
2. Utilisez `python analyze_pdf_deep.py Mon-Scenario`
3. Suivez le processus étape par étape

### Je veux voir tous les scénarios

1. Consultez [LISTE_SCENARIOS.md](LISTE_SCENARIOS.md)
2. Ou lancez `python launcher.py`

### Je veux comprendre le système

1. [README_SCENARIOS_JSON.md](README_SCENARIOS_JSON.md) - Format JSON
2. [ENRICHISSEMENT_MANUEL.md](ENRICHISSEMENT_MANUEL.md) - Méthode
3. `src/` - Code source

---

## ⭐ Documents par Qualité de Scénarios

### ⭐⭐⭐⭐⭐ Qualité Professionnelle

- [ENRICHISSEMENT_SCENARIO.md](ENRICHISSEMENT_SCENARIO.md) - Exemple du Masque Utruz (33 scènes)
- Méthode utilisée : [ENRICHISSEMENT_MANUEL.md](ENRICHISSEMENT_MANUEL.md)

### ⭐⭐⭐ Bonne Qualité

- 9 scénarios originaux créés manuellement
- Voir [LISTE_SCENARIOS.md](LISTE_SCENARIOS.md)

### ⭐⭐ Prototypes

- [ENRICHISSEMENT_MASSIF.md](ENRICHISSEMENT_MASSIF.md) - 25 scénarios auto
- À améliorer avec la méthode manuelle

---

## 📈 Évolution du Projet

### Documents Historiques (Archive)

Les documents suivants sont archivés dans `docs/archive/` :

- `ARCHIVAGE_COMPLET.md`
- `BUGFIX_VICTORY_LOOP.md`
- `CORRECTIONS.md`
- `FACTORISATION_JSON.md`
- `MISSION_COMPLETE.md`
- `NOUVEAUX_SCENARIOS.md`
- `RAPPORT_SESSION_COMPLETE.md`
- `RENAMING_GUIDE.md`
- `SCENARIOS_RESUME.md`
- `TRANSFORMATION_COMPLETE.md`
- `AJOUT_SCENARIOS_COMPLET.md`

Ces documents retracent l'historique du développement mais ne sont plus nécessaires pour l'utilisation courante.

---

## 🔍 Recherche Rapide

### Par Mot-Clé

- **Installation** → [README.md](../README.md)
- **Lancement** → [README.md](../README.md) ou `python launcher.py`
- **Scénarios** → [LISTE_SCENARIOS.md](LISTE_SCENARIOS.md)
- **Enrichissement** → [GUIDE_ENRICHISSEMENT.md](GUIDE_ENRICHISSEMENT.md)
- **PDF** → [ENRICHISSEMENT_MANUEL.md](ENRICHISSEMENT_MANUEL.md)
- **JSON** → [README_SCENARIOS_JSON.md](README_SCENARIOS_JSON.md)
- **Qualité** → [ENRICHISSEMENT_MANUEL.md](ENRICHISSEMENT_MANUEL.md)

---

## 💡 Conseils

### Pour les Joueurs

- Commencez par les scénarios ⭐⭐⭐⭐⭐ (Le Masque Utruz, Les Cryptes de Kelemvor)
- Utilisez `python launcher.py` pour une expérience optimale

### Pour les Créateurs

- Lisez d'abord [GUIDE_ENRICHISSEMENT.md](GUIDE_ENRICHISSEMENT.md)
- Suivez la méthode manuelle pour une qualité professionnelle
- Temps estimé : 1h30-2h30 par scénario

---

## 📞 Support

- **Issues GitHub** : [DnD5e-Scenarios/issues](https://github.com/codingame-team/DnD5e-Scenarios/issues)
- **Documentation** : Vous êtes au bon endroit !
- **README principal** : [README.md](../README.md)

---

*Index créé le 11 janvier 2026*  
*Version 2.0*

