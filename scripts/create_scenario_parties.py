#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'intégration de personnages générés dans un scénario existant
Démontre comment utiliser les scripts de génération avec un scénario réel
"""

import sys
from pathlib import Path

# Ajouter le chemin vers dnd-5e-core
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'dnd-5e-core'))

from dnd_5e_core.data.loaders import simple_character_generator
import json


def create_party_for_scenario(scenario_name, level=5):
    """
    Crée un groupe d'aventuriers adapté à un scénario spécifique

    Args:
        scenario_name: Nom du scénario
        level: Niveau recommandé
    """

    # Configurations par scénario
    scenario_configs = {
        'chasse_gobelins': {
            'level': 3,
            'party': [
                {'class': 'fighter', 'race': 'human', 'name': 'Thorgrim'},
                {'class': 'wizard', 'race': 'elf', 'name': 'Elara'},
                {'class': 'cleric', 'race': 'dwarf', 'name': 'Durin'},
                {'class': 'rogue', 'race': 'halfling', 'name': 'Pippin'},
            ]
        },
        'masque_utruz': {
            'level': 2,
            'party': [
                {'class': 'paladin', 'race': 'human', 'name': 'Ser Aldric'},
                {'class': 'wizard', 'race': 'elf', 'name': 'Lysandre'},
                {'class': 'rogue', 'race': 'halfling', 'name': 'Finwick'},
                {'class': 'cleric', 'race': 'dwarf', 'name': 'Grimnar'},
            ]
        },
        'cryptes_kelemvor': {
            'level': 4,
            'party': [
                {'class': 'cleric', 'race': 'human', 'name': 'Père Erasmus'},
                {'class': 'paladin', 'race': 'dwarf', 'name': 'Thorald'},
                {'class': 'wizard', 'race': 'elf', 'name': 'Silvanus'},
                {'class': 'rogue', 'race': 'halfling', 'name': 'Merric'},
            ]
        },
        'oeil_gruumsh': {
            'level': 3,
            'party': [
                {'class': 'barbarian', 'race': 'half-orc', 'name': 'Grok'},
                {'class': 'fighter', 'race': 'human', 'name': 'Marcus'},
                {'class': 'ranger', 'race': 'elf', 'name': 'Arathorn'},
                {'class': 'cleric', 'race': 'dwarf', 'name': 'Balin'},
            ]
        },
        'tombe_rois_serpents': {
            'level': 2,
            'party': [
                {'class': 'fighter', 'race': 'human', 'name': 'Indiana'},
                {'class': 'wizard', 'race': 'elf', 'name': 'Azura'},
                {'class': 'rogue', 'race': 'halfling', 'name': 'Lara'},
                {'class': 'cleric', 'race': 'dwarf', 'name': 'Brok'},
            ]
        },
    }

    # Utiliser la config du scénario ou une config par défaut
    if scenario_name in scenario_configs:
        config = scenario_configs[scenario_name]
        level = config['level']
        party_setup = config['party']
    else:
        # Config par défaut
        party_setup = [
            {'class': 'fighter', 'race': 'human', 'name': 'Aragorn'},
            {'class': 'wizard', 'race': 'elf', 'name': 'Gandalf'},
            {'class': 'rogue', 'race': 'halfling', 'name': 'Bilbo'},
            {'class': 'cleric', 'race': 'dwarf', 'name': 'Gimli'},
        ]

    print(f"\n🎲 Création d'un groupe pour: {scenario_name}")
    print(f"   Niveau recommandé: {level}")
    print("=" * 80)

    party = []
    for config in party_setup:
        char = simple_character_generator(
            level=level,
            class_name=config['class'],
            race_name=config['race'],
            name=config['name']
        )
        party.append(char)

        print(f"\n✅ {char.name} - {char.race.name} {char.class_type.name} (Niveau {char.level})")
        print(f"   HP: {char.hit_points}/{char.max_hit_points}")
        print(f"   FOR {char.abilities.str} | DEX {char.abilities.dex} | CON {char.abilities.con}")
        print(f"   INT {char.abilities.int} | SAG {char.abilities.wis} | CHA {char.abilities.cha}")

        # Capacités spéciales
        if hasattr(char, 'multi_attack_bonus') and char.multi_attack_bonus:
            print(f"   ⚔️ Extra Attack: {char.multi_attack_bonus + 1} attaques")
        if hasattr(char, 'sneak_attack_dice') and char.sneak_attack_dice:
            print(f"   🗡️ Sneak Attack: {char.sneak_attack_dice}d6")
        if hasattr(char, 'rage_uses_left'):
            print(f"   💢 Rage: {char.rage_uses_left} utilisations")
        if hasattr(char, 'sc') and char.sc:
            print(f"   ✨ {len(char.sc.learned_spells) if char.sc.learned_spells else 0} sorts (DC {char.sc.dc_value})")

    return party


def character_to_dict(char):
    """Convertit un Character en dictionnaire sérialisable"""
    data = {
        'name': char.name,
        'level': char.level,
        'race': char.race.name,
        'class': char.class_type.name,
        'hp': char.hit_points,
        'max_hp': char.max_hit_points,
        'abilities': {
            'str': char.abilities.str,
            'dex': char.abilities.dex,
            'con': char.abilities.con,
            'int': char.abilities.int,
            'wis': char.abilities.wis,
            'cha': char.abilities.cha,
        },
        'ability_modifiers': {
            'str': char.ability_modifiers.str,
            'dex': char.ability_modifiers.dex,
            'con': char.ability_modifiers.con,
            'int': char.ability_modifiers.int,
            'wis': char.ability_modifiers.wis,
            'cha': char.ability_modifiers.cha,
        },
        'speed': char.speed,
        'gold': char.gold,
        'proficiency_bonus': 2 + ((char.level - 1) // 4),
    }

    # Ajouter les infos de spellcaster si applicable
    if hasattr(char, 'sc') and char.sc:
        sc = char.sc
        data['spellcasting'] = {
            'ability': sc.dc_type,
            'spell_dc': sc.dc_value,
            'ability_modifier': sc.ability_modifier,
            'spell_slots': sc.spell_slots,
            'spells_known': len(sc.learned_spells) if sc.learned_spells else 0,
            'spell_list': [s.name if hasattr(s, 'name') else str(s) for s in sc.learned_spells] if sc.learned_spells else []
        }

    # Ajouter les capacités spéciales de classe
    if hasattr(char, 'multi_attack_bonus') and char.multi_attack_bonus:
        data['extra_attacks'] = char.multi_attack_bonus

    if hasattr(char, 'sneak_attack_dice') and char.sneak_attack_dice:
        data['sneak_attack'] = f"{char.sneak_attack_dice}d6"

    if hasattr(char, 'rage_uses_left'):
        data['rage_uses'] = char.rage_uses_left

    if hasattr(char, 'ki_points'):
        data['ki_points'] = char.ki_points

    if hasattr(char, 'lay_on_hands_pool'):
        data['lay_on_hands'] = char.lay_on_hands_pool

    # Ajouter les traits raciaux
    if hasattr(char, 'darkvision'):
        data['darkvision'] = char.darkvision

    return data


def save_party_for_scenario(party, scenario_name):
    """Sauvegarde le groupe dans data/parties/"""
    party_data = [character_to_dict(char) for char in party]

    output_dir = Path('data/parties')
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{scenario_name}_party.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(party_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Groupe sauvegardé dans: {output_file}")
    return output_file


def main():
    """Créer des groupes pour plusieurs scénarios"""

    print("\n" + "🎲" * 40)
    print("GÉNÉRATION DE GROUPES POUR LES SCÉNARIOS")
    print("🎲" * 40)

    scenarios = [
        'chasse_gobelins',
        'masque_utruz',
        'cryptes_kelemvor',
        'oeil_gruumsh',
        'tombe_rois_serpents',
    ]

    print("\nScénarios disponibles:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario}")

    print("\nChoisissez:")
    print("  - Un numéro pour créer un groupe spécifique")
    print("  - 'all' pour créer tous les groupes")
    print("  - 'q' pour quitter")

    choice = input("\nVotre choix: ").strip().lower()

    if choice == 'q':
        print("Au revoir!")
        return 0

    if choice == 'all':
        for scenario in scenarios:
            party = create_party_for_scenario(scenario)
            save_party_for_scenario(party, scenario)
            print("\n" + "-" * 80)
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scenarios):
                scenario = scenarios[idx]
                party = create_party_for_scenario(scenario)
                save_party_for_scenario(party, scenario)
            else:
                print("Choix invalide")
                return 1
        except ValueError:
            print("Choix invalide")
            return 1

    print("\n✨ Terminé!")
    print("\nPour charger un groupe dans un scénario:")
    print("  import json")
    print("  with open('data/parties/scenario_party.json') as f:")
    print("      party_data = json.load(f)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
