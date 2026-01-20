# 🎲 DnD5e-Scenarios

Collection de scénarios D&D 5e enrichis et prêts à jouer, basés sur les règles du package `dnd-5e-core`.

![D&D 5e](https://img.shields.io/badge/D&D-5e-red)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![dnd-5e-core](https://img.shields.io/badge/dnd--5e--core-0.4.0-green)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 À Propos

Ce projet propose une **collection de 36 scénarios D&D 5e en français**, dont :
- **2 scénarios enrichis manuellement** (⭐⭐⭐⭐⭐) - Qualité professionnelle, 95% fidèles aux PDFs
- **9 scénarios originaux** (⭐⭐⭐) - Créés avec soin
- **25 scénarios prototypes** (⭐⭐) - Enrichis automatiquement

Les scénarios utilisent le système de jeu du package **[dnd-5e-core v0.4.0](https://pypi.org/project/dnd-5e-core/)** pour gérer les règles D&D 5e.

### 🆕 Nouvelles Fonctionnalités (v0.4.0)

- ✨ **ClassAbilities & RacialTraits** - Appliqués automatiquement aux personnages
- ⚡ **Conditions System** - Poisoned, Restrained, Paralyzed, etc. (affichage en combat)
- 🎁 **Magic Items** - 10+ items magiques prédéfinis (Ring of Protection, Wand of Magic Missiles, etc.)
- 🎭 **Multiclassing** - Support complet du multiclassing
- 🎒 **Inventaire Amélioré** - Trésors et magic items intégrés aux inventaires

---

## 📦 Installation Rapide

### 1. Cloner le Projet

```bash
git clone https://github.com/codingame-team/DnD5e-Scenarios.git
cd DnD5e-Scenarios
```

### 2. Créer un Environnement Virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Installer les Dépendances

```bash
pip install dnd-5e-core
```

---

## 🚀 Lancement Rapide

### Méthode 1: Launcher Universel (Recommandé)

Le launcher offre une interface colorée pour choisir parmi tous les scénarios :

```bash
python launcher.py
```

Vous verrez un menu avec :
- 📖 Scénarios enrichis manuellement (qualité ⭐⭐⭐⭐⭐)
- 📚 Scénarios originaux (qualité ⭐⭐⭐)
- 📋 Scénarios prototypes (qualité ⭐⭐)

Entrez le numéro du scénario ou 'q' pour quitter.

### Méthode 2: Lancement Direct

Lancez directement un scénario spécifique :

```bash
# Scénarios enrichis manuellement (⭐⭐⭐⭐⭐)
python masque_utruz_enrichi_game.py
python cryptes_de_kelemvor_manual_game.py

# Scénarios originaux (⭐⭐⭐)
python chasse_gobelins_refactored.py
python yawning_portal_game.py
python tombe_rois_serpents_game.py
python oeil_gruumsh_game.py
python secte_du_crane_game.py
python collier_de_zark_game.py
python auberge_sanglier_gris_game.py

# Nouveaux scénarios (⭐⭐⭐)
python cryptes_de_kelemvor_game.py
python masque_utruz_game.py
python defis_a_phlan_game.py
```

### Méthode 3: Menu Play Scenarios

```bash
python play_scenarios.py
```

---

## 📖 Scénarios Disponibles

### ⭐⭐⭐⭐⭐ Enrichis Manuellement (Qualité Professionnelle)

| Scénario | Niveau | Durée | Scènes | Description |
|----------|--------|-------|--------|-------------|
| **🎭 Le Masque Utruz** | 3 | 3-4h | 33 | Cité sur une faille, usurier, Utruz, Dieu-Poisson |
| **⚰️ Les Cryptes de Kelemvor** | 4 | 3-4h | 27 | Temple profané, 7 sceaux, braseros sacrés, nécrophage |

### ⭐⭐⭐ Scénarios Originaux (Bonne Qualité)

| Scénario | Niveau | Durée | Description |
|----------|--------|-------|-------------|
| 🏰 La Chasse aux Gobelins | 3 | 1-2h | Sauvez le Village de Brume |
| 🏛️ The Sunless Citadel | 1 | 2-3h | Explorez une citadelle engloutie |
| 🔺 La Tombe des Rois Serpents | 2 | 2h | Pillez une pyramide ancienne |
| 👁️ L'Oeil de Gruumsh | 3 | 2-3h | Affrontez une tribu d'orques |
| 💀 La Secte du Crâne | 4 | 2-3h | Infiltrez les catacombes |
| 💎 Le Collier de Zark | 2 | 1-2h | Enquête sur un vol de collier |
| 🍺 L'Auberge du Sanglier Gris | 1 | 1-2h | Nuit mouvementée dans une auberge |

### 🆕 Nouveaux Scénarios (⭐⭐⭐)

| Scénario | Niveau | Durée | Description |
|----------|--------|-------|-------------|
| ⚰️ Cryptes de Kelemvor | 3 | 2-3h | Version alternative |
| 🎭 Le Masque Utruz | 2 | 2-3h | Version alternative |
| 🏰 Défis à Phlan | 1 | 1-2h | Mini-missions variées |

### 📋 Prototypes (⭐⭐)

25 scénarios enrichis automatiquement disponibles comme prototypes.

---

## 🛠️ Outils pour Créateurs

### Analyser un PDF de Scénario

Pour enrichir un nouveau scénario depuis un PDF officiel :

```bash
# Analyser un seul PDF
python analyze_pdf_deep.py Nom-du-scenario

# Analyser 5 scénarios en batch
python enrich_batch.py
```

Résultat : Fichier d'analyse détaillé dans `analysis/Nom-du-scenario_analysis.txt`

### Processus d'Enrichissement

Consultez le **[Guide d'Enrichissement](docs/GUIDE_ENRICHISSEMENT.md)** pour :
- Extraire le contenu d'un PDF
- Créer un scénario enrichi manuellement
- Atteindre une qualité professionnelle (⭐⭐⭐⭐⭐)

---

## 📁 Structure du Projet

```
DnD5e-Scenarios/
├── launcher.py                  # 🚀 Lanceur universel (RECOMMANDÉ)
├── play_scenarios.py            # Menu alternatif
├── README.md                    # Ce fichier
│
├── *_game.py                    # Scripts de scénarios
│   ├── masque_utruz_enrichi_game.py      # ⭐⭐⭐⭐⭐
│   ├── cryptes_de_kelemvor_manual_game.py # ⭐⭐⭐⭐⭐
│   ├── chasse_gobelins_refactored.py      # ⭐⭐⭐
│   └── ...
│
├── data/
│   └── scenes/                  # Scénarios JSON
│       ├── masque_utruz_enrichi.json
│       ├── cryptes_de_kelemvor_manual.json
│       └── ...
│
├── scenarios/                   # PDFs des scénarios officiels
│   ├── Masque-utruz.pdf
│   ├── Cryptes-de-Kelemvor.pdf
│   └── ...
│
├── analysis/                    # Analyses de PDFs
│   ├── Cryptes-de-Kelemvor_analysis.txt
│   └── ...
│
├── src/                         # Code source
│   ├── scenarios/               # Système de scénarios
│   ├── scenes/                  # Système de scènes
│   └── utils/                   # Utilitaires (PDF reader)
│
├── docs/                        # Documentation
│   ├── GUIDE_ENRICHISSEMENT.md
│   ├── ENRICHISSEMENT_MANUEL.md
│   ├── LISTE_SCENARIOS.md
│   └── archive/                 # Docs obsolètes
│
├── savegames/                   # Sauvegardes
└── tokens/                      # Tokens de monstres
```

---

## 📚 Documentation

### Guides Principaux

- **[Guide d'Enrichissement](docs/GUIDE_ENRICHISSEMENT.md)** - Comment créer des scénarios de qualité
- **[Liste des Scénarios](docs/LISTE_SCENARIOS.md)** - Tous les scénarios disponibles
- **[Enrichissement Manuel](docs/ENRICHISSEMENT_MANUEL.md)** - Méthode approfondie

### Outils

- **`launcher.py`** - Lanceur avec interface colorée
- **`analyze_pdf_deep.py`** - Analyser un PDF en profondeur
- **`enrich_batch.py`** - Analyser plusieurs PDFs en batch

---

## 🎮 Exemples d'Utilisation

### Jouer un Scénario Enrichi

```bash
# Lancer le launcher
python launcher.py

# Choisir "1" pour Le Masque Utruz
# Le scénario démarre avec 33 scènes détaillées
```

### Créer un Nouveau Scénario

```bash
# 1. Analyser le PDF
python analyze_pdf_deep.py Mon-Scenario

# 2. Lire l'analyse
cat analysis/Mon-Scenario_analysis.txt

# 3. Créer le JSON enrichi (manuel)
# Voir docs/GUIDE_ENRICHISSEMENT.md

# 4. Créer le script Python
# Copier un script existant et adapter

# 5. Tester
python mon_scenario_game.py
```

---

## 🎯 Objectifs du Projet

### Actuels
- ✅ 2 scénarios enrichis manuellement (⭐⭐⭐⭐⭐)
- ✅ 9 scénarios originaux (⭐⭐⭐)
- ✅ 25 prototypes (⭐⭐)
- ✅ Launcher universel
- ✅ Outils d'enrichissement

### Futurs
- ⏳ Enrichir 3-5 scénarios prioritaires
- ⏳ Interface graphique (Pygame/PyQt)
- ⏳ Mode multijoueur
- ⏳ Éditeur de scénarios visuel
- ⏳ Système d'achievements

---

## 🤝 Contribution

Les contributions sont bienvenues ! Vous pouvez :

1. **Enrichir un scénario** - Suivez le [Guide d'Enrichissement](docs/GUIDE_ENRICHISSEMENT.md)
2. **Créer un nouveau scénario** - Utilisez les outils fournis
3. **Améliorer le code** - Pull requests bienvenues
4. **Signaler des bugs** - Issues GitHub

---

## 📜 Licence

Ce projet est sous licence MIT. Les scénarios sont basés sur des PDFs officiels D&D 5e disponibles sur [aidedd.org](https://www.aidedd.org).

---

## 🔗 Liens Utiles

- **Package dnd-5e-core** : [PyPI](https://pypi.org/project/dnd-5e-core/) | [GitHub](https://github.com/codingame-team/dnd-5e-core)
- **Scénarios source** : [aidedd.org](https://www.aidedd.org)
- **Repository GitHub** : [DnD5e-Scenarios](https://github.com/codingame-team/DnD5e-Scenarios)

---

## 💬 Support

Pour toute question ou problème :
- Ouvrez une [Issue GitHub](https://github.com/codingame-team/DnD5e-Scenarios/issues)
- Consultez la [documentation](docs/)

---

## 🎲 Bon Jeu !

**Que vos dés roulent favorablement, aventuriers !**

---

*Dernière mise à jour : 11 janvier 2026*  
*Version : 2.0*  
*36 scénarios disponibles*

