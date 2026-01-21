# 🎭 Guide Complet de Génération de Personnages

Ce guide explique comment utiliser `simple_character_generator` du package `dnd-5e-core` pour créer des personnages pour vos scénarios DnD 5e.

## 📋 Table des Matières

1. [Scripts Disponibles](#scripts-disponibles)
2. [Exemples d'Utilisation](#exemples-dutilisation)
3. [Format JSON des Personnages](#format-json-des-personnages)
4. [Intégration dans les Scénarios](#intégration-dans-les-scénarios)
5. [Personnalisation Avancée](#personnalisation-avancée)

---

## Scripts Disponibles

### 🎯 Scripts Principaux

| Script | Usage | Résultat |
|--------|-------|----------|
| `create_character.py` | Créer un personnage individuel | Affichage détaillé + JSON optionnel |
| `create_party.py` | Créer un groupe d'aventuriers | Groupe complet en JSON |
| `create_scenario_parties.py` | Groupes pré-configurés pour scénarios | JSON dans `data/parties/` |
| `example_usage.py` | Exemples d'utilisation | Démonstrations complètes |

### 📚 Exemples de Commandes

```bash
# Personnage unique
python scripts/create_character.py --name Gandalf --class wizard --race elf --level 10

# Groupe classique
python scripts/create_party.py --classic --level 5 --out data/party.json

# Groupe pour un scénario
python scripts/create_scenario_parties.py
```

---

## Exemples d'Utilisation

### Exemple 1 : Créer un Magicien

```bash
python scripts/create_character.py \
  --name Gandalf \
  --class wizard \
  --race elf \
  --level 10 \
  --out data/gandalf.json
```

**Résultat :**
- Gandalf, Elfe Magicien niveau 10
- Sorts générés automatiquement (Intelligence)
- Vision dans le noir, Fey Ancestry, Trance
- Fichier `data/gandalf.json` créé

### Exemple 2 : Groupe pour "La Chasse aux Gobelins"

```bash
# Option 1: Script interactif
python scripts/create_scenario_parties.py
# Choisir "1" pour chasse_gobelins

# Option 2: Groupe personnalisé
python scripts/create_party.py --level 3 --size 4 --out data/goblin_hunters.json
```

**Résultat :**
- Groupe de 4 personnages niveau 3
- Équilibré (guerrier, magicien, clerc, roublard)
- Prêt pour le combat

### Exemple 3 : Groupe Complet avec Affichage

```python
# Dans votre script Python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'dnd-5e-core'))

from dnd_5e_core.data.loaders import simple_character_generator

# Créer le groupe
party = [
    simple_character_generator(5, 'human', 'fighter', 'Conan'),
    simple_character_generator(5, 'elf', 'wizard', 'Elara'),
    simple_character_generator(5, 'dwarf', 'cleric', 'Durin'),
    simple_character_generator(5, 'halfling', 'rogue', 'Pippin'),
]

# Utiliser dans le combat
for char in party:
    print(f"{char.name}: {char.hit_points}/{char.max_hit_points} HP")
```

---

## Format JSON des Personnages

### Structure Complète

```json
{
  "name": "Gandalf",
  "level": 10,
  "race": "Elf",
  "class": "Wizard",
  "hp": 52,
  "max_hp": 52,
  "abilities": {
    "str": 10, "dex": 14, "con": 12,
    "int": 18, "wis": 15, "cha": 11
  },
  "ability_modifiers": {
    "str": 0, "dex": 2, "con": 1,
    "int": 4, "wis": 2, "cha": 0
  },
  "speed": 30,
  "gold": 142,
  "proficiency_bonus": 4,
  "spellcasting": {
    "ability": "int",
    "spell_dc": 16,
    "ability_modifier": 4,
    "spell_slots": [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],
    "spells_known": 15,
    "spell_list": ["Fire Bolt", "Mage Hand", "Magic Missile", ...]
  },
  "darkvision": 60
}
```

### Champs Disponibles

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string | Nom du personnage |
| `level` | int | Niveau (1-20) |
| `race` | string | Race (Elf, Dwarf, etc.) |
| `class` | string | Classe (Fighter, Wizard, etc.) |
| `hp` / `max_hp` | int | Points de vie |
| `abilities` | object | Caractéristiques (FOR, DEX, etc.) |
| `ability_modifiers` | object | Modificateurs de caractéristiques |
| `speed` | int | Vitesse en pieds |
| `gold` | int | Pièces d'or |
| `proficiency_bonus` | int | Bonus de maîtrise |
| `spellcasting` | object | Infos de lancement de sorts (si applicable) |
| `extra_attacks` | int | Attaques supplémentaires (Fighter, etc.) |
| `sneak_attack` | string | Dégâts de Sneak Attack (Rogue) |
| `rage_uses` | int | Utilisations de Rage (Barbarian) |
| `ki_points` | int | Points de ki (Monk) |
| `lay_on_hands` | int | Points de Lay on Hands (Paladin) |
| `darkvision` | int | Distance en pieds |

---

## Intégration dans les Scénarios

### Méthode 1 : Charger depuis JSON

```python
import json

# Charger un groupe pré-généré
with open('data/parties/chasse_gobelins_party.json', 'r') as f:
    party_data = json.load(f)

print(f"Groupe de {len(party_data)} aventuriers")
for char in party_data:
    print(f"- {char['name']}: {char['class']} niveau {char['level']}")
```

### Méthode 2 : Générer à la Volée

```python
from dnd_5e_core.data.loaders import simple_character_generator

# Créer directement dans le code
party = [
    simple_character_generator(3, 'human', 'fighter', 'Thorgrim'),
    simple_character_generator(3, 'elf', 'wizard', 'Elara'),
    simple_character_generator(3, 'dwarf', 'cleric', 'Durin'),
    simple_character_generator(3, 'halfling', 'rogue', 'Pippin'),
]

# Prêt à utiliser dans le scénario
print(f"Le groupe entre dans le donjon...")
```

### Méthode 3 : Intégration dans un Scénario Existant

```python
# Dans un fichier de scénario (ex: chasse_gobelins_refactored.py)

def init_party():
    """Initialise le groupe d'aventuriers"""
    party_file = Path('data/parties/chasse_gobelins_party.json')
    
    if party_file.exists():
        # Charger depuis JSON
        with open(party_file, 'r') as f:
            party_data = json.load(f)
        print("✅ Groupe chargé depuis le fichier")
    else:
        # Générer à la volée
        party = [
            simple_character_generator(3, 'human', 'fighter', 'Thorgrim'),
            simple_character_generator(3, 'elf', 'wizard', 'Elara'),
            simple_character_generator(3, 'dwarf', 'cleric', 'Durin'),
            simple_character_generator(3, 'halfling', 'rogue', 'Pippin'),
        ]
        print("✅ Groupe généré à la volée")
    
    return party
```

---

## Personnalisation Avancée

### Classes Disponibles

| Classe | Dé de Vie | Capacité Principale | Spécial |
|--------|-----------|---------------------|---------|
| `fighter` | d10 | FOR/DEX | Extra Attack (niv 5+) |
| `wizard` | d6 | INT | Sorts (full caster) |
| `rogue` | d8 | DEX | Sneak Attack |
| `cleric` | d8 | SAG | Sorts (full caster) |
| `ranger` | d10 | DEX/SAG | Sorts (half caster) |
| `paladin` | d10 | FOR/CHA | Sorts (half caster), Lay on Hands |
| `barbarian` | d12 | FOR | Rage |
| `monk` | d8 | DEX/SAG | Ki Points |
| `bard` | d8 | CHA | Sorts (full caster) |
| `druid` | d8 | SAG | Sorts (full caster) |
| `sorcerer` | d6 | CHA | Sorts (full caster) |
| `warlock` | d8 | CHA | Sorts (pact caster) |

### Races Disponibles

| Race | Vitesse | Traits Principaux |
|------|---------|-------------------|
| `human` | 30 | Polyvalent |
| `elf` | 30 | Darkvision 60', Fey Ancestry, Trance |
| `dwarf` | 30 | Darkvision 60', Dwarven Resilience, Stonecunning |
| `halfling` | 25 | Lucky, Brave, Nimbleness |
| `half-elf` | 30 | Darkvision 60', Fey Ancestry |
| `half-orc` | 30 | Darkvision 60', Relentless Endurance, Savage Attacks |
| `tiefling` | 30 | Darkvision 60', Hellish Resistance |
| `gnome` | 25 | Darkvision 60', Gnome Cunning |
| `dragonborn` | 30 | Breath Weapon |

### Paramètres de Génération

```python
character = simple_character_generator(
    level=5,                      # Niveau (1-20)
    race_name='elf',              # Race (optionnel, aléatoire si None)
    class_name='wizard',          # Classe (optionnel, aléatoire si None)
    name='Gandalf',               # Nom (optionnel, généré si None)
    apply_class_abilities=True,   # Appliquer les capacités de classe
    apply_racial_traits=True      # Appliquer les traits raciaux
)
```

### Désactiver les Capacités Automatiques

```python
# Créer un personnage "basique" sans capacités spéciales
basic_char = simple_character_generator(
    level=5,
    class_name='fighter',
    apply_class_abilities=False,  # Pas d'Extra Attack
    apply_racial_traits=False      # Pas de traits raciaux
)
```

---

## 🎯 Cas d'Usage Recommandés

### Pour les Scénarios Courts (1-2h)
```bash
python scripts/create_party.py --classic --level 3
```
Groupe équilibré, prêt à l'emploi.

### Pour les Campagnes Longues
```bash
# Créer le groupe au niveau 1
python scripts/create_party.py --classic --level 1 --out data/campaign_party.json

# Faire monter de niveau avec level_up_character() dans le code
```

### Pour Tester un Scénario
```bash
# Groupe de test niveau 5
python scripts/create_party.py --level 5 --size 6 --display-only
```

### Pour des PNJ Importants
```bash
python scripts/create_character.py --name "Elminster" --class wizard --race human --level 20 --out data/npcs/elminster.json
```

---

## 📚 Ressources Supplémentaires

- **Documentation dnd-5e-core :** Voir le package pour plus de détails sur les classes et capacités
- **Exemples :** `scripts/example_usage.py` pour des démonstrations complètes
- **Tests :** `dnd-5e-core/examples/demo_phase1.py` pour voir toutes les capacités en action

---

## 🐛 Dépannage

### Problème : "ModuleNotFoundError: No module named 'dnd_5e_core'"

**Solution :**
```bash
# Installer le package
pip install dnd-5e-core

# Ou utiliser le repo local
cd /path/to/dnd-5e-core
pip install -e .
```

### Problème : Les sorts ne sont pas générés

**Cause :** Le package ne peut pas charger les sorts depuis l'API.

**Solution :** Les sorts sont chargés automatiquement depuis l'API D&D 5e. Vérifiez votre connexion internet.

### Problème : Les personnages ont des caractéristiques faibles

**Explication :** Les caractéristiques sont générées aléatoirement avec la méthode "4d6 drop lowest" (réaliste D&D 5e).

**Alternative :** Modifier les valeurs dans le fichier JSON après génération.

---

## ✨ Conclusion

Vous avez maintenant tous les outils pour créer des personnages riches et complets pour vos scénarios DnD 5e !

**Prochaines étapes :**
1. Créez votre premier groupe avec `create_party.py`
2. Testez-le dans un scénario existant
3. Personnalisez les fichiers JSON selon vos besoins
4. Profitez de vos aventures ! 🎲
