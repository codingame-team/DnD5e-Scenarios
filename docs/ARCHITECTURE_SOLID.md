"""
ARCHITECTURE SOLID - Refonte du Jeu D&D 5e
==========================================

Ce document décrit l'architecture complète de la refonte SOLID du jeu.

## Structure des Dossiers

```
DnD5e-Test/
├── src/
│   ├── core/                    # Entités de base
│   │   ├── entities.py          # GameCharacter, GameMonster, Item, Weapon, Armor, Potion
│   │   ├── inventory.py         # Système d'inventaire
│   │   └── __init__.py
│   ├── systems/                 # Systèmes de jeu (Strategy pattern)
│   │   ├── spellcasting.py      # Gestion des sorts
│   │   ├── equipment.py         # Gestion équipement
│   │   ├── merchant.py          # Système de marchand
│   │   ├── combat.py            # Système de combat enrichi
│   │   └── __init__.py
│   ├── scenes/                  # Scènes de jeu (Composite pattern)
│   │   ├── base_scene.py        # Interface Scene abstraite
│   │   ├── narrative_scene.py   # Scènes narratives
│   │   ├── combat_scene.py      # Scènes de combat
│   │   ├── choice_scene.py      # Scènes à choix
│   │   ├── merchant_scene.py    # Scène marchand
│   │   └── __init__.py
│   ├── scenarios/               # Gestion de scénarios
│   │   ├── scenario.py          # Classe Scenario, Act, Scene
│   │   ├── builder.py           # ScenarioBuilder (Builder pattern)
│   │   ├── registry.py          # ScenarioRegistry
│   │   └── __init__.py
│   ├── rendering/               # Rendu (Adapter pattern)
│   │   ├── renderer.py          # Interface Renderer
│   │   ├── console_renderer.py  # Rendu console
│   │   ├── ncurses_renderer.py  # Rendu ncurses (optionnel)
│   │   └── __init__.py
│   ├── utils/                   # Utilitaires
│   │   ├── pdf_reader.py        # Lecture PDF scénarios
│   │   ├── map_extractor.py     # Extraction mini-maps
│   │   ├── dice.py              # Système de dés
│   │   └── __init__.py
│   └── __init__.py
├── data/                        # Données de jeu
│   ├── weapons.json             # Armes disponibles
│   ├── armors.json              # Armures disponibles
│   ├── potions.json             # Potions disponibles
│   ├── spells.json              # Sorts disponibles
│   └── maps/                    # Mini-maps extraites
├── scenarios/                   # Fichiers de scénarios
│   ├── goblin_hunt.yaml         # Scénario Chasse aux Gobelins
│   ├── template.yaml            # Template pour nouveaux scénarios
│   └── Chasse-aux-gobs.pdf      # PDF original
├── tests/                       # Tests unitaires
│   ├── test_entities.py
│   ├── test_systems.py
│   ├── test_scenes.py
│   └── ...
├── goblin_hunt_v2.py            # Nouveau jeu principal (SOLID)
├── game_engine.py               # Moteur de jeu principal
└── README_V2.md                 # Documentation v2
```

## Principes SOLID Appliqués

### Single Responsibility Principle (SRP)
- **Une classe = une responsabilité**
- `GameCharacter` : gérer état personnage
- `SpellcastingSystem` : gérer lanceurs de sorts uniquement
- `MerchantSystem` : gérer transactions uniquement
- `Scene` : gérer déroulement d'une scène

### Open/Closed Principle (OCP)
- **Ouvert à l'extension, fermé à la modification**
- Nouvelles scènes via héritage de `BaseScene`
- Nouveaux renderers via `Renderer` interface
- Nouveaux scénarios via `ScenarioBuilder`

### Liskov Substitution Principle (LSP)
- **Les sous-classes sont substituables**
- Toute `Scene` peut être utilisée de manière polymorphe
- Tout `Renderer` peut remplacer un autre

### Interface Segregation Principle (ISP)
- **Interfaces spécifiques**
- `Combatant` interface pour entités combattantes
- `Merchant` interface pour marchands
- `Spellcaster` interface pour lanceurs de sorts

### Dependency Inversion Principle (DIP)
- **Dépendre d'abstractions, pas de concrétions**
- `GameEngine` dépend de `Renderer` (interface), pas `ConsoleRenderer`
- `Scene` dépend de `System` (interface), pas implémentations concrètes

## Design Patterns Utilisés

### Factory Pattern
- `CharacterFactory` : créer personnages avec équipement depuis collections
- `MonsterFactory` : créer monstres avec loot
- `ItemFactory` : créer objets depuis JSON

### Strategy Pattern
- Systèmes interchangeables (`SpellcastingSystem`, `EquipmentSystem`)
- Différentes stratégies de combat

### Builder Pattern
- `ScenarioBuilder` : construire scénarios complexes depuis YAML

### Composite Pattern
- Hiérarchie de scènes (Scenario → Act → Scene)

### Observer Pattern
- Événements de jeu (victoire, mort, découverte)
- Notifications entre systèmes

### Adapter Pattern
- Adapter dnd-5e-core vers nos entités enrichies
- Adapter rendu console/ncurses

## Flux de Jeu

```
1. Chargement Scénario (YAML)
   ↓
2. Création Personnages (Factory)
   ↓
3. Équipement Initial (EquipmentSystem)
   ↓
4. Boucle de Jeu
   ├── Affichage Scène (Renderer)
   ├── Choix Joueur (ChoiceScene)
   ├── Combat (CombatScene + CombatSystem)
   ├── Marchand (MerchantScene + MerchantSystem)
   ├── Sorts (SpellcastingSystem)
   └── Transition vers Scène Suivante
   ↓
5. Fin de Scénario
   ├── Statistiques
   └── Sauvegarde (optionnel)
```

## Exemple de Scénario YAML

```yaml
scenario:
  name: "La Chasse aux Gobelins"
  description: "Sauver le village des gobelins"
  difficulty: "medium"
  party_size: 4
  
  acts:
    - id: "village"
      name: "Village de Brume"
      description: "Point de départ"
      scenes:
        - type: "narrative"
          id: "intro"
          text: "Le village est en émoi..."
          next: "tavern_choice"
        
        - type: "choice"
          id: "tavern_choice"
          text: "Que voulez-vous faire?"
          choices:
            - text: "Interroger les villageois"
              next: "gather_info"
              effects:
                reputation: +1
            - text: "Visiter le marchand"
              next: "merchant_1"
            - text: "Partir vers la forêt"
              next: "forest_path"
        
        - type: "merchant"
          id: "merchant_1"
          merchant_name: "Boutique du Village"
          stock:
            - {item: "potion_healing", quantity: 5, price: 50}
            - {item: "potion_greater_healing", quantity: 2, price: 100}
          next: "tavern_choice"
        
        - type: "combat"
          id: "goblin_ambush"
          description: "Embuscade de gobelins!"
          enemies:
            - {type: "goblin", count: 3}
          on_victory: "goblin_camp"
          on_defeat: "game_over"
          
    - id: "forest"
      name: "Forêt Sombre"
      map: "data/maps/forest_map.txt"
      # ... etc
```

## Intégration dnd-5e-core

### Armes et Armures
```python
from dnd_5e_core.data import request_equipment

# Charger épée longue depuis API
longsword_data = request_equipment("longsword")
longsword = Weapon.from_dnd_weapon(longsword_data, value=15)

character.equip_weapon(longsword)
```

### Sorts
```python
from dnd_5e_core.data import request_spell

# Charger sort de soin
cure_wounds = request_spell("cure-wounds")

# Utiliser dans SpellcastingSystem
spellcasting_system.cast_spell(character, cure_wounds, target)
```

### Potions
```python
# Définir dans potions.json
{
  "potion_healing": {
    "name": "Potion de Soin",
    "effect_type": "healing",
    "effect_value": "2d4+2",
    "value": 50
  }
}

# Acheter chez marchand
merchant_system.buy(character, "potion_healing")
```

## Système de Mini-Maps

### Format ASCII
```
#########
#.......#    # = Mur
#.P.....#    . = Sol exploré
#.......#    ? = Sol inexploré
#...G...#    P = Joueur
#.......#    G = Gobelin
#########
```

### Extraction depuis PDF
```python
from src.utils.pdf_reader import extract_maps

maps = extract_maps("scenarios/Chasse-aux-gobs.pdf")
# Sauve dans data/maps/
```

## Interface ncurses (Optionnel)

```
┌─────────── Carte ──────────────┐  ┌─── Stats ───┐
│  #########                     │  │ Grok        │
│  #.......#                     │  │ HP: 42/42   │
│  #.P.....#                     │  │ CA: 16      │
│  #...G...#                     │  │             │
│  #########                     │  │ Elara       │
│                                │  │ HP: 28/28   │
└────────────────────────────────┘  │ Sorts: 4/2  │
┌─────────── Narration ──────────┐  └─────────────┘
│ Vous entrez dans la forêt...   │
│ Des gobelins surgissent!       │
│                                │
│ Choix:                         │
│  1. Attaquer                   │
│  2. Fuir                       │
└────────────────────────────────┘
```

## Priorités d'Implémentation

### Phase 1: Core Systems (FAIT ✅)
- [x] Entités enrichies (entities.py)
- [x] Inventaire (inventory.py)
- [ ] Systèmes de base (spellcasting, equipment, merchant)

### Phase 2: Scènes (EN COURS)
- [ ] Base scenes et hiérarchie
- [ ] Factorisation des scènes actuelles
- [ ] Intégration sorts et équipement

### Phase 3: Scénarios
- [ ] Builder et Registry
- [ ] Format YAML
- [ ] Chargement dynamique

### Phase 4: Utilitaires
- [ ] Lecteur PDF
- [ ] Extracteur de maps
- [ ] Système de dés amélioré

### Phase 5: Rendu (Optionnel)
- [ ] Interface ncurses basique
- [ ] Affichage mini-maps
- [ ] Fenêtres multiples

## Fichiers à Créer/Modifier

### À Créer (Priorité Haute)
1. `src/systems/spellcasting.py`
2. `src/systems/equipment.py`
3. `src/systems/merchant.py`
4. `src/scenes/base_scene.py`
5. `src/scenarios/builder.py`
6. `data/potions.json`
7. `goblin_hunt_v2.py` (nouveau jeu SOLID)

### À Créer (Priorité Moyenne)
8. `src/utils/pdf_reader.py`
9. `src/utils/map_extractor.py`
10. `scenarios/goblin_hunt.yaml`

### À Créer (Optionnel)
11. `src/rendering/ncurses_renderer.py`
12. Tests unitaires

### À Garder
- `goblin_hunt_game.py` (v1, pour référence)
- Documentation existante

## Compatibilité Ascendante

- Les anciens scripts continuent de fonctionner
- Nouveaux scripts utilisent architecture SOLID
- Migration progressive possible

## Estimation du Code

- **Core (entities, inventory)**: ~500 lignes ✅
- **Systems (3 systèmes)**: ~600 lignes
- **Scenes (base + 4 types)**: ~800 lignes
- **Scenarios (builder, registry)**: ~400 lignes
- **Utils (PDF, maps)**: ~500 lignes
- **Rendering (console + ncurses)**: ~700 lignes
- **Jeu principal v2**: ~300 lignes
- **Data JSON**: ~200 lignes
- **Tests**: ~800 lignes

**Total estimé**: ~4,800 lignes (vs ~3,000 actuellement)

## Prochaines Étapes

1. Créer systèmes de jeu (spellcasting, equipment, merchant)
2. Créer base scenes et factoriser scènes actuelles
3. Créer potions.json avec données dnd-5e-core
4. Créer goblin_hunt_v2.py avec architecture SOLID
5. Tester l'intégration complète
6. (Optionnel) Ajouter ncurses
7. (Optionnel) Ajouter lecteur PDF
8. Documentation README_V2.md

