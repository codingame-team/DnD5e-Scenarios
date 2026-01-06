# DnD5e-Test

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![dnd-5e-core](https://img.shields.io/badge/dnd--5e--core-0.1.8-success.svg)](https://pypi.org/project/dnd-5e-core/)

**Scripts de démonstration du package [dnd-5e-core](https://github.com/codingame-team/dnd-5e-core)**

Exemples pratiques montrant comment utiliser `dnd-5e-core` pour créer des systèmes de combat D&D 5e, générer des personnages, et construire des rencontres équilibrées.

## 🚀 Installation

```bash
# Installer le package dnd-5e-core
pip install dnd-5e-core

# Cloner ce dépôt
git clone https://github.com/codingame-team/DND5e-Test.git
cd DND5e-Test

# Les scripts sont prêts à l'emploi !
python demo_quick_combat.py
```

## ⚔️ Scripts de Combat

### Démarrage Rapide

```bash
# 1. Première découverte - Combat rapide et simple
python demo_quick_combat.py

# 2. Combat automatique avec personnages aléatoires
python auto_random_combat_standalone.py

# 3. Simulation avancée avec statistiques détaillées
python advanced_random_combat.py
```

### Tous les Scripts de Combat

| Script | Description | Complexité |
|--------|-------------|------------|
| **`demo_quick_combat.py`** | Combat rapide 1v1 pour découvrir le système | ⭐ Débutant |
| **`auto_random_combat_standalone.py`** | Combat automatique, personnages aléatoires | ⭐⭐ Intermédiaire |
| **`random_party_combat.py`** | Groupe de 6 aventuriers vs monstres | ⭐⭐⭐ Avancé |
| **`advanced_random_combat.py`** | Système complet avec stats détaillées | ⭐⭐⭐⭐ Expert |
| `party_combat.py` | Combat personnalisé avec groupe fixe | ⭐⭐ |
| `combat.py` | Combat de base 1v1 simple | ⭐ |
| `epic_combat.py` | Combat épique avec dragons et boss | ⭐⭐⭐ |

### Scripts avec Système de Rencontres Officiel D&D 5e

| Script | Description |
|--------|-------------|
| **`official_encounter_combat.py`** | Utilise les tables DMG pour générer des rencontres équilibrées |
| **`demo_encounter_systems.py`** | Compare différents systèmes de génération de rencontres |

## 👥 Scripts de Création

| Script | Description |
|--------|-------------|
| **`create_character.py`** | Création de personnages avec races, classes et équipement |
| **`create_monster.py`** | Chargement et recherche de monstres dans la base de données |

## 📖 Exemples de Code

### Créer un Personnage

```python
from dnd_5e_core.data import simple_character_generator

# Générer un personnage aléatoire
fighter = simple_character_generator(
    level=5,
    class_name="fighter",
    name="Conan"
)

print(f"{fighter.name} - Level {fighter.level} {fighter.class_type.name}")
print(f"HP: {fighter.hit_points}/{fighter.max_hit_points}")
```

### Charger des Monstres

```python
from dnd_5e_core.data import load_monster

# Charger un monstre spécifique
goblin = load_monster('goblin')
print(f"{goblin.name} - CR {goblin.challenge_rating}")
print(f"HP: {goblin.hit_points}, AC: {goblin.armor_class}")
```

### Générer une Rencontre Équilibrée

```python
from dnd_5e_core.mechanics import (
    select_monsters_by_encounter_table,
    get_encounter_gold
)
from dnd_5e_core.data import load_monsters_database

# Charger tous les monstres
monsters_db = load_monsters_database()

# Générer une rencontre pour un groupe niveau 5
monsters, encounter_type = select_monsters_by_encounter_table(
    encounter_level=5,
    available_monsters=monsters_db,
    allow_pairs=True
)

print(f"Encounter: {encounter_type}")
print(f"Monsters: {[m.name for m in monsters]}")
print(f"Gold reward: {get_encounter_gold(5)} gp")
```

### Combat Complet

```python
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.data import simple_character_generator, load_monster

# Créer personnages et monstres
fighter = simple_character_generator(level=3, class_name="fighter")
wizard = simple_character_generator(level=3, class_name="wizard")
orc = load_monster('orc')

# Initialiser le système de combat
combat = CombatSystem()

# Tour de combat
combat.character_turn(
    character=fighter,
    targets=[orc],
    action_type='attack'
)

combat.monster_turn(
    monster=orc,
    targets=[fighter, wizard]
)
```

## 🎲 Fonctionnalités Démontrées

### Système de Combat D&D 5e

- ✅ Jets d'attaque avec bonus et modificateurs
- ✅ Calcul des dégâts avec dés multiples
- ✅ Classe d'armure (AC) et jets de sauvegarde
- ✅ Actions multiples et attaques spéciales
- ✅ Gestion des points de vie et des conditions

### Génération de Personnages

- ✅ Création manuelle avec races et classes
- ✅ Génération aléatoire complète
- ✅ Équipement et armes
- ✅ Calcul automatique des bonus

### Système de Rencontres

- ✅ Tables DMG officielles (niveaux 1-20)
- ✅ Challenge Rating (CR) conforme D&D 5e
- ✅ Calcul de difficulté (Easy, Medium, Hard, Deadly)
- ✅ Récompenses en or selon le niveau

### Base de Données

- ✅ 332 monstres avec stats complètes
- ✅ 319 sorts D&D 5e
- ✅ Armes, armures et équipement
- ✅ Recherche et filtres avancés

## 📚 Documentation Complète

Pour plus de détails sur le package `dnd-5e-core` :

- **Documentation:** [GitHub dnd-5e-core](https://github.com/codingame-team/dnd-5e-core)
- **PyPI:** [pypi.org/project/dnd-5e-core](https://pypi.org/project/dnd-5e-core/)
- **Guide de Combat:** [README_COMBAT.md](README_COMBAT.md)

## 🎯 Structure du Projet

```
DnD5e-Test/
├── README.md                           # Ce fichier
├── README_COMBAT.md                    # Guide détaillé des scripts de combat
│
├── Scripts de Combat (Combat rapide et démonstrations)
│   ├── demo_quick_combat.py           # ⭐ Démo rapide
│   ├── auto_random_combat_standalone.py # ⭐⭐ Combat automatique
│   ├── random_party_combat.py         # ⭐⭐⭐ Groupe vs monstres
│   ├── advanced_random_combat.py      # ⭐⭐⭐⭐ Version avancée
│   ├── official_encounter_combat.py   # Tables DMG officielles
│   ├── demo_encounter_systems.py      # Comparaison de systèmes
│   ├── party_combat.py                # Combat personnalisé
│   ├── combat.py                      # Combat simple
│   └── epic_combat.py                 # Combat épique
│
├── Scripts de Création
│   ├── create_character.py            # Création de personnages
│   └── create_monster.py              # Chargement de monstres
│
├── savegames/                         # Sauvegardes de parties
│   ├── party.pkl
│   └── roster/                        # Personnages sauvegardés
│
├── tokens/                            # Images de monstres
└── archive/                           # Documentation archivée
    ├── docs/                          # Docs techniques internes
    ├── migration_docs/                # Historique de migration
    └── backup_scripts/                # Scripts de backup
```

## 🤝 Contribution

Ce projet est un ensemble d'exemples pour démontrer les capacités de `dnd-5e-core`. 

Pour contribuer au package principal : [dnd-5e-core](https://github.com/codingame-team/dnd-5e-core)

## 📄 License

MIT License - voir [LICENSE](LICENSE)

## 🔗 Liens Utiles

- **Package Principal:** [dnd-5e-core sur PyPI](https://pypi.org/project/dnd-5e-core/)
- **Code Source:** [GitHub dnd-5e-core](https://github.com/codingame-team/dnd-5e-core)
- **Application Complète:** [DnD-5th-Edition-API](https://github.com/codingame-team/DnD-5th-Edition-API)

---

**Installation rapide:** `pip install dnd-5e-core`  
**Démarrage rapide:** `python demo_quick_combat.py`  
**Documentation:** https://github.com/codingame-team/dnd-5e-core

