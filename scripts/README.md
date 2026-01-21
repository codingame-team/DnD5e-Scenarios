# Scripts de Génération de Personnages

Ce dossier contient des scripts pour générer des personnages DnD 5e pour les scénarios, en utilisant `simple_character_generator` du package `dnd-5e-core`.

## Scripts Disponibles

### 1. `create_character.py` - Créer un personnage individuel

Crée un seul personnage avec affichage détaillé de toutes ses caractéristiques.

**Exemples d'utilisation:**

```bash
# Créer Gandalf le magicien elfe niveau 10
python scripts/create_character.py --name Gandalf --class wizard --race elf --level 10

# Créer un guerrier niveau 5 (nom et race aléatoires)
python scripts/create_character.py --class fighter --level 5

# Créer un personnage complètement aléatoire niveau 3
python scripts/create_character.py --level 3

# Créer un personnage et le sauvegarder en JSON
python scripts/create_character.py --name Aragorn --class fighter --race human --level 5 --out data/aragorn.json
```

**Options:**
- `--name` : Nom du personnage (aléatoire si non spécifié)
- `--class` : Classe (fighter, wizard, rogue, cleric, ranger, paladin, barbarian, monk, etc.)
- `--race` : Race (human, elf, dwarf, halfling, half-elf, half-orc, tiefling, gnome, etc.)
- `--level` : Niveau du personnage (défaut: 1)
- `--out` : Fichier de sortie JSON (optionnel)
- `--no-display` : Ne pas afficher les détails (juste sauvegarder)

### 2. `create_party.py` - Créer un groupe d'aventuriers

Crée un groupe complet de personnages prêts pour un scénario.

**Exemples d'utilisation:**

```bash
# Créer le groupe classique (Aragorn, Gandalf, Bilbo, Gimli) niveau 5
python scripts/create_party.py --classic --level 5

# Créer un groupe aléatoire de 4 personnages niveau 3
python scripts/create_party.py --level 3 --size 4

# Créer un groupe de 6 personnages niveau 7 et sauvegarder
python scripts/create_party.py --level 7 --size 6 --out data/party_level7.json

# Afficher seulement sans sauvegarder
python scripts/create_party.py --classic --level 10 --display-only
```

**Options:**
- `--level` : Niveau des personnages (défaut: 5)
- `--size` : Taille du groupe (défaut: 4)
- `--classic` : Utiliser le groupe classique (Aragorn, Gandalf, Bilbo, Gimli)
- `--out` : Fichier de sortie JSON (défaut: data/party.json)
- `--display-only` : Afficher seulement, ne pas sauvegarder

### 3. `create_scenario_parties.py` - Créer des groupes pour des scénarios spécifiques

Crée des groupes pré-configurés adaptés à chaque scénario du projet.

**Exemples d'utilisation:**

```bash
# Lancer le script en mode interactif
python scripts/create_scenario_parties.py

# Créer tous les groupes pour tous les scénarios
# (entrer 'all' quand demandé)
python scripts/create_scenario_parties.py
```

**Scénarios disponibles:**
1. **chasse_gobelins** (Niveau 3) - Thorgrim, Elara, Durin, Pippin
2. **masque_utruz** (Niveau 2) - Ser Aldric (paladin), Lysandre (wizard), Finwick (rogue), Grimnar (cleric)
3. **cryptes_kelemvor** (Niveau 4) - Père Erasmus (cleric), Thorald (paladin), Silvanus (wizard), Merric (rogue)
4. **oeil_gruumsh** (Niveau 3) - Grok (barbarian), Marcus (fighter), Arathorn (ranger), Balin (cleric)
5. **tombe_rois_serpents** (Niveau 2) - Indiana (fighter), Azura (wizard), Lara (rogue), Brok (cleric)

Les groupes sont sauvegardés dans `data/parties/[scenario]_party.json`.

### 4. `generate_scenario_characters.py` - Générateur flexible (version avancée)

Version plus technique avec options détaillées de génération.

## Format de Sortie JSON

Les fichiers JSON générés contiennent toutes les informations nécessaires pour les scénarios :

```json
{
  "name": "Gandalf",
  "level": 10,
  "race": "Elf",
  "class": "Wizard",
  "hp": 52,
  "max_hp": 52,
  "abilities": {
    "str": 10,
    "dex": 14,
    "con": 12,
    "int": 18,
    "wis": 15,
    "cha": 11
  },
  "ability_modifiers": {
    "str": 0,
    "dex": 2,
    "con": 1,
    "int": 4,
    "wis": 2,
    "cha": 0
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
    "spell_list": ["Fire Bolt", "Mage Hand", "Magic Missile", "Shield", ...]
  },
  "darkvision": 60
}
```

## Utilisation dans les Scénarios

Une fois les personnages générés, vous pouvez les charger dans vos scripts de scénario :

```python
import json
from pathlib import Path

# Charger un groupe
with open('data/party.json', 'r', encoding='utf-8') as f:
    party_data = json.load(f)

print(f"Groupe de {len(party_data)} aventuriers chargé")
for char in party_data:
    print(f"- {char['name']}: {char['race']} {char['class']} niveau {char['level']}")
```

## Intégration avec dnd-5e-core

Ces scripts utilisent directement `simple_character_generator` du package `dnd-5e-core` qui :

- Génère automatiquement les caractéristiques (méthode 4d6 drop lowest)
- Applique les capacités de classe appropriées au niveau
- Applique les traits raciaux automatiquement
- Génère les sorts pour les lanceurs de sorts
- Calcule les emplacements de sorts selon la progression de classe

## Classes Disponibles

- **fighter** : Guerrier avec Extra Attack
- **wizard** : Magicien avec sorts d'Intelligence
- **rogue** : Roublard avec Sneak Attack
- **cleric** : Clerc avec sorts de Sagesse
- **ranger** : Rôdeur (demi-lanceur) avec sorts de Sagesse
- **paladin** : Paladin (demi-lanceur) avec sorts de Charisme et Lay on Hands
- **barbarian** : Barbare avec système de Rage
- **monk** : Moine avec points de ki
- **bard** : Barde avec sorts de Charisme
- **druid** : Druide avec sorts de Sagesse
- **sorcerer** : Ensorceleur avec sorts de Charisme
- **warlock** : Occultiste avec sorts de Charisme

## Races Disponibles

- **human** : Humain
- **elf** : Elfe (darkvision, fey ancestry, trance)
- **dwarf** : Nain (darkvision, resilience, stonecunning)
- **halfling** : Halfelin (lucky, brave, nimbleness)
- **half-elf** : Demi-elfe (darkvision, fey ancestry)
- **half-orc** : Demi-orque (darkvision, relentless endurance, savage attacks)
- **tiefling** : Tieffelin (darkvision, hellish resistance)
- **gnome** : Gnome (darkvision, gnome cunning)
- **dragonborn** : Drakéide (breath weapon)

## Notes

- Les personnages sont générés avec équipement minimal (inventaire vide)
- Les sorts sont sélectionnés aléatoirement parmi ceux disponibles pour la classe
- Les capacités spéciales de classe et traits raciaux sont appliqués automatiquement
- Pour des personnages plus personnalisés, modifiez les fichiers JSON générés
