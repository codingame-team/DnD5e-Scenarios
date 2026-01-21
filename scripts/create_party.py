#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de groupe d'aventuriers pour les scénarios DnD 5e
Utilise simple_character_generator du package dnd_5e_core

Usage:
    # Créer un groupe classique niveau 5
    python scripts/create_party.py --level 5

    # Créer un groupe personnalisé
    python scripts/create_party.py --level 3 --size 6 --out data/my_party.json

Basé sur les exemples de dnd-5e-core/examples/demo_phase1.py
"""

import sys
from pathlib import Path

# Ajouter le chemin vers dnd-5e-core
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'dnd-5e-core'))

from dnd_5e_core.data.loaders import simple_character_generator
import json
import argparse


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


def create_classic_party(level=5):
    """
    Crée un groupe classique d'aventuriers
    Basé sur dnd-5e-core/examples/demo_phase1.py
    """
    print(f"\n🎲 Création d'un groupe d'aventuriers niveau {level}")
    print("=" * 80)

    party_config = [
        {'class': 'fighter', 'race': 'human', 'name': 'Aragorn'},
        {'class': 'wizard', 'race': 'elf', 'name': 'Gandalf'},
        {'class': 'rogue', 'race': 'halfling', 'name': 'Bilbo'},
        {'class': 'cleric', 'race': 'dwarf', 'name': 'Gimli'},
    ]

    party = []
    for config in party_config:
        char = simple_character_generator(
            level=level,
            class_name=config['class'],
            race_name=config['race'],
            name=config['name']
        )
        party.append(char)

        # Afficher les infos
        print(f"\n✅ {char.name} - {char.race.name} {char.class_type.name} (Niveau {char.level})")
        print(f"   HP: {char.hit_points}/{char.max_hit_points}")
        print(f"   FOR {char.abilities.str} | DEX {char.abilities.dex} | CON {char.abilities.con}")
        print(f"   INT {char.abilities.int} | SAG {char.abilities.wis} | CHA {char.abilities.cha}")

        # Afficher les capacités spéciales
        if hasattr(char, 'multi_attack_bonus') and char.multi_attack_bonus:
            print(f"   ⚔️  Extra Attack: {char.multi_attack_bonus + 1} attaques")

        if hasattr(char, 'sneak_attack_dice') and char.sneak_attack_dice:
            print(f"   🗡️  Sneak Attack: {char.sneak_attack_dice}d6")

        if hasattr(char, 'rage_uses_left'):
            print(f"   💢 Rage: {char.rage_uses_left} utilisations")

        if hasattr(char, 'sc') and char.sc:
            print(f"   ✨ Spellcaster: {len(char.sc.learned_spells) if char.sc.learned_spells else 0} sorts connus")
            print(f"   📜 Spell DC: {char.sc.dc_value}")

    return party


def create_custom_party(level=5, size=4):
    """Crée un groupe aléatoire de la taille demandée"""
    print(f"\n🎲 Création d'un groupe aléatoire de {size} personnages niveau {level}")
    print("=" * 80)

    available_classes = ["fighter", "wizard", "cleric", "rogue", "ranger", "paladin", "barbarian", "monk"]
    available_races = ["human", "elf", "dwarf", "halfling", "half-elf", "half-orc", "tiefling", "gnome"]

    party = []
    for i in range(size):
        import random
        char = simple_character_generator(
            level=level,
            class_name=random.choice(available_classes),
            race_name=random.choice(available_races)
        )
        party.append(char)
        print(f"✅ {char.name} - {char.race.name} {char.class_type.name}")

    return party


def save_party_to_json(party, output_file):
    """Sauvegarde le groupe en JSON"""
    party_data = [character_to_dict(char) for char in party]

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(party_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Groupe sauvegardé dans: {output_path}")
    print(f"   {len(party)} personnages")


def main():
    parser = argparse.ArgumentParser(
        description='Crée un groupe d\'aventuriers pour les scénarios DnD 5e'
    )
    parser.add_argument('--level', type=int, default=5,
                        help='Niveau des personnages (défaut: 5)')
    parser.add_argument('--size', type=int, default=4,
                        help='Taille du groupe (défaut: 4)')
    parser.add_argument('--classic', action='store_true',
                        help='Utiliser le groupe classique (Aragorn, Gandalf, Bilbo, Gimli)')
    parser.add_argument('--out', type=str, default='data/party.json',
                        help='Fichier de sortie JSON (défaut: data/party.json)')
    parser.add_argument('--display-only', action='store_true',
                        help='Afficher seulement, ne pas sauvegarder')

    args = parser.parse_args()

    try:
        if args.classic:
            party = create_classic_party(args.level)
        else:
            party = create_custom_party(args.level, args.size)

        if not args.display_only:
            save_party_to_json(party, args.out)

        print("\n✨ Terminé!")

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
