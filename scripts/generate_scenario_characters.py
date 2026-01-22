#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de groupes d'aventuriers pour les scénarios D&D 5e
Crée des fichiers JSON dans data/parties/ utilisables par base_scenario.py
"""

import sys
from pathlib import Path

# Ajouter le chemin vers dnd-5e-core
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'dnd-5e-core'))

from dnd_5e_core.data.loaders import simple_character_generator
import json


# Configuration des groupes par scénario
SCENARIO_PARTIES = {
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
    'tour_mage_fou': {
        'level': 3,
        'party': [
            {'class': 'wizard', 'race': 'elf', 'name': 'Alaric'},
            {'class': 'fighter', 'race': 'human', 'name': 'Brienne'},
            {'class': 'cleric', 'race': 'dwarf', 'name': 'Moradin'},
            {'class': 'rogue', 'race': 'halfling', 'name': 'Nimble'},
        ]
    },
    'Le Masque Utruz (Version Enrichie)': {
        'level': 2,
        'party': [
            {'class': 'paladin', 'race': 'human', 'name': 'Ser Aldric'},
            {'class': 'wizard', 'race': 'elf', 'name': 'Lysandre'},
            {'class': 'rogue', 'race': 'halfling', 'name': 'Finwick'},
            {'class': 'cleric', 'race': 'dwarf', 'name': 'Grimnar'},
        ]
    },
}


def character_to_dict(char):
    """Convertit un Character en dictionnaire sérialisable pour JSON"""
    data = {
        'name': char.name,
        'level': char.level,
        'race': char.race.name if hasattr(char.race, 'name') else str(char.race),
        'class': char.class_type.name if hasattr(char.class_type, 'name') else str(char.class_type),
        'hit_points': char.hit_points,
        'max_hit_points': char.max_hit_points,
        'armor_class': char.armor_class,
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

    # Ajouter spellcasting si présent
    if hasattr(char, 'sc') and char.sc:
        sc = char.sc
        data['spellcasting'] = {
            'ability': getattr(sc, 'dc_type', 'wis'),
            'spell_dc': getattr(sc, 'dc_value', 10),
            'ability_modifier': getattr(sc, 'ability_modifier', 0),
            'spell_slots': getattr(sc, 'spell_slots', {}),
            'spell_list': [
                s.name if hasattr(s, 'name') else str(s)
                for s in (getattr(sc, 'learned_spells', None) or getattr(sc, 'spells', []))
            ]
        }

    # Capacités spéciales de classe
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
    if hasattr(char, 'darkvision'):
        data['darkvision'] = char.darkvision

    return data


def create_party_for_scenario(scenario_name):
    """Crée un groupe d'aventuriers pour un scénario"""

    config = SCENARIO_PARTIES.get(scenario_name)
    if not config:
        print(f"⚠️  Scénario '{scenario_name}' non trouvé dans la configuration")
        return None

    level = config['level']
    party_setup = config['party']

    print(f"\n🎲 Création d'un groupe pour: {scenario_name}")
    print(f"   Niveau: {level}")
    print("=" * 80)

    party = []
    for setup in party_setup:
        try:
            char = simple_character_generator(
                level=level,
                class_name=setup['class'],
                race_name=setup['race'],
                name=setup['name']
            )
            party.append(char)

            print(f"\n✅ {char.name} - {char.race.name} {char.class_type.name} (Niveau {char.level})")
            print(f"   HP: {char.hit_points}/{char.max_hit_points} | CA: {char.armor_class}")
            print(f"   FOR {char.abilities.str} DEX {char.abilities.dex} CON {char.abilities.con} "
                  f"INT {char.abilities.int} SAG {char.abilities.wis} CHA {char.abilities.cha}")

            # Afficher capacités spéciales
            if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'learned_spells'):
                spells = char.sc.learned_spells or []
                if spells:
                    print(f"   ✨ {len(spells)} sorts connus")

        except Exception as e:
            print(f"❌ Erreur création {setup['name']}: {e}")
            continue

    return party


def save_party(party, scenario_name):
    """Sauvegarde le groupe en JSON dans data/parties/"""
    if not party:
        print("⚠️  Aucun personnage à sauvegarder")
        return None

    party_data = [character_to_dict(char) for char in party]

    output_dir = Path('data/parties')
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{scenario_name}_party.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(party_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Groupe sauvegardé: {output_file}")
    print(f"   {len(party)} personnages exportés")
    return output_file


def main():
    """Point d'entrée principal"""

    print("\n" + "🎲" * 40)
    print("GÉNÉRATEUR DE GROUPES POUR SCÉNARIOS D&D 5e")
    print("🎲" * 40)

    scenarios = sorted(SCENARIO_PARTIES.keys())

    print(f"\n{len(scenarios)} scénarios disponibles:")
    for i, scenario in enumerate(scenarios, 1):
        config = SCENARIO_PARTIES[scenario]
        print(f"  {i:2d}. {scenario:<40} (Niveau {config['level']}, {len(config['party'])} PJ)")

    print("\nOptions:")
    print("  - Numéro : Générer un groupe spécifique")
    print("  - 'all'  : Générer tous les groupes")
    print("  - 'q'    : Quitter")

    choice = input("\n➤ Votre choix: ").strip().lower()

    if choice == 'q':
        print("Au revoir!")
        return 0

    if choice == 'all':
        print("\n📦 Génération de tous les groupes...")
        success = 0
        for scenario in scenarios:
            try:
                party = create_party_for_scenario(scenario)
                if party:
                    save_party(party, scenario)
                    success += 1
                print("\n" + "-" * 80)
            except Exception as e:
                print(f"❌ Erreur pour {scenario}: {e}")
        print(f"\n✨ {success}/{len(scenarios)} groupes créés avec succès!")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scenarios):
                scenario = scenarios[idx]
                party = create_party_for_scenario(scenario)
                if party:
                    save_party(party, scenario)
                    print("\n✨ Terminé!")
            else:
                print("❌ Choix invalide")
                return 1
        except ValueError:
            print("❌ Choix invalide")
            return 1

    print("\n📖 Pour charger dans un scénario:")
    print("   Dans BaseScenario.setup_party(), le fichier sera chargé automatiquement")
    print("   si data/parties/{scenario_name}_party.json existe.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
