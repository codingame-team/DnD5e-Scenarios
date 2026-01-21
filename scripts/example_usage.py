#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation des personnages générés dans un scénario
Montre comment charger et utiliser les personnages créés avec create_party.py ou create_character.py
"""

import sys
from pathlib import Path

# Ajouter le chemin vers dnd-5e-core
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'dnd-5e-core'))

from dnd_5e_core.data.loaders import simple_character_generator
import json


def load_party_from_json(json_file):
    """Charge les données d'un groupe depuis un fichier JSON"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def display_party_summary(party_data):
    """Affiche un résumé du groupe"""
    print("\n" + "=" * 80)
    print(f"🎭 GROUPE D'AVENTURIERS ({len(party_data)} membres)")
    print("=" * 80)

    for i, char in enumerate(party_data, 1):
        print(f"\n{i}. {char['name']} - {char['race']} {char['class']} (Niveau {char['level']})")
        print(f"   HP: {char['hp']}/{char['max_hp']}")
        print(f"   FOR {char['abilities']['str']} | DEX {char['abilities']['dex']} | CON {char['abilities']['con']}")
        print(f"   INT {char['abilities']['int']} | SAG {char['abilities']['wis']} | CHA {char['abilities']['cha']}")

        # Capacités spéciales
        special = []
        if 'extra_attacks' in char:
            special.append(f"⚔️ {char['extra_attacks'] + 1} attaques")
        if 'sneak_attack' in char:
            special.append(f"🗡️ Sneak Attack {char['sneak_attack']}")
        if 'rage_uses' in char:
            special.append(f"💢 {char['rage_uses']} rages")
        if 'spellcasting' in char:
            special.append(f"✨ {char['spellcasting']['spells_known']} sorts, DC {char['spellcasting']['spell_dc']}")

        if special:
            print(f"   {' | '.join(special)}")


def example_combat_scenario():
    """Exemple de scénario de combat avec un groupe pré-généré"""

    print("\n" + "🎲" * 40)
    print("EXEMPLE: Chargement d'un groupe pour un scénario")
    print("🎲" * 40)

    # Option 1: Charger depuis JSON
    print("\n📂 Option 1: Charger un groupe depuis JSON")
    try:
        party_data = load_party_from_json('data/party_test.json')
        display_party_summary(party_data)
    except FileNotFoundError:
        print("   ⚠️  Fichier data/party_test.json non trouvé")
        print("   Générez-le d'abord avec: python scripts/create_party.py --classic --level 5 --out data/party_test.json")

    # Option 2: Générer à la volée
    print("\n\n🎲 Option 2: Générer un groupe à la volée")
    print("-" * 80)

    party_config = [
        {'class': 'fighter', 'race': 'human', 'name': 'Thorgrim', 'level': 5},
        {'class': 'wizard', 'race': 'elf', 'name': 'Elara', 'level': 5},
        {'class': 'cleric', 'race': 'dwarf', 'name': 'Durin', 'level': 5},
        {'class': 'rogue', 'race': 'halfling', 'name': 'Pippin', 'level': 5},
    ]

    party_chars = []
    for config in party_config:
        char = simple_character_generator(
            level=config['level'],
            class_name=config['class'],
            race_name=config['race'],
            name=config['name']
        )
        party_chars.append(char)
        print(f"✅ {char.name} créé: {char.class_type.name} niveau {char.level}")

    # Exemple d'interaction avec les personnages
    print("\n\n⚔️  Exemple: Affichage des capacités offensives")
    print("-" * 80)

    for char in party_chars:
        print(f"\n{char.name} ({char.class_type.name}):")

        # Attaques de base
        if hasattr(char, 'multi_attack_bonus') and char.multi_attack_bonus:
            print(f"   • {char.multi_attack_bonus + 1} attaques par tour")
        else:
            print(f"   • 1 attaque par tour")

        # Sneak attack
        if hasattr(char, 'sneak_attack_dice') and char.sneak_attack_dice:
            print(f"   • Sneak Attack: +{char.sneak_attack_dice}d6 dégâts supplémentaires")

        # Sorts offensifs
        if hasattr(char, 'sc') and char.sc and char.sc.learned_spells:
            offensive_spells = [
                s for s in char.sc.learned_spells
                if hasattr(s, 'damage_type') and s.damage_type
            ]
            if offensive_spells:
                print(f"   • Sorts offensifs ({len(offensive_spells)}):")
                for spell in offensive_spells[:3]:  # Afficher les 3 premiers
                    spell_name = spell.name if hasattr(spell, 'name') else str(spell)
                    print(f"      - {spell_name}")

    print("\n\n🛡️  Exemple: Affichage des capacités défensives")
    print("-" * 80)

    for char in party_chars:
        print(f"\n{char.name}:")
        print(f"   • HP: {char.hit_points}/{char.max_hit_points}")
        print(f"   • CA estimée: {10 + char.ability_modifiers.dex}")

        # Sorts de soins
        if hasattr(char, 'sc') and char.sc and char.sc.learned_spells:
            healing_spells = [
                s for s in char.sc.learned_spells
                if hasattr(s, 'heal_at_slot_level') and s.heal_at_slot_level
            ]
            if healing_spells:
                print(f"   • Sorts de soin: {len(healing_spells)}")

        # Lay on Hands (Paladin)
        if hasattr(char, 'lay_on_hands_pool'):
            print(f"   • Lay on Hands: {char.lay_on_hands_pool} points de soin")

        # Traits spéciaux
        if hasattr(char, 'relentless_endurance'):
            print(f"   • Relentless Endurance (1/repos long)")

        if hasattr(char, 'lucky'):
            print(f"   • Lucky: relancer les 1")


def example_scenario_integration():
    """Montre comment intégrer les personnages dans un scénario complet"""

    print("\n\n" + "📖" * 40)
    print("EXEMPLE: Intégration dans un scénario")
    print("📖" * 40)

    print("""
    
Pour utiliser ces personnages dans vos scénarios, vous pouvez :

1. **Pré-générer le groupe** avant de lancer le scénario:
   ```python
   # Dans votre script de scénario
   party_data = load_party_from_json('data/ma_party.json')
   
   # Ou générer à la volée
   party = [
       simple_character_generator(5, 'human', 'fighter', 'Conan'),
       simple_character_generator(5, 'elf', 'wizard', 'Gandalf'),
       # etc.
   ]
   ```

2. **Stocker les personnages** dans le fichier de scénario JSON:
   ```json
   {
     "scenario": "La Quête du Dragon",
     "party": [
       {
         "name": "Aragorn",
         "level": 5,
         "class": "Fighter",
         ...
       }
     ],
     "encounters": [...]
   }
   ```

3. **Utiliser avec le système de combat** existant:
   - Les personnages générés sont des instances complètes de Character
   - Ils ont toutes les capacités de classe et traits raciaux
   - Ils peuvent utiliser le système de combat de dnd-5e-core

4. **Sauvegardes et progression**:
   - Sauvegarder l'état après chaque session
   - Faire monter de niveau avec level_up_character()
   - Gérer l'inventaire et l'équipement

Exemples de scénarios existants qui pourraient utiliser ce système:
   - chasse_gobelins_refactored.py
   - masque_utruz_game.py
   - cryptes_de_kelemvor_game.py
   - etc.
    """)


if __name__ == '__main__':
    example_combat_scenario()
    example_scenario_integration()

    print("\n" + "=" * 80)
    print("✨ Pour plus d'exemples, voir scripts/README.md")
    print("=" * 80 + "\n")
