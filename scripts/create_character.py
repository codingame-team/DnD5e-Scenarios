#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de personnage individuel pour les scénarios DnD 5e
Utilise simple_character_generator du package dnd_5e_core

Usage:
    # Créer Gandalf le magicien niveau 10
    python scripts/create_character.py --name Gandalf --class wizard --race elf --level 10

    # Créer un guerrier aléatoire niveau 5
    python scripts/create_character.py --class fighter --level 5

    # Créer un personnage complètement aléatoire
    python scripts/create_character.py --level 3

Basé sur dnd-5e-core/test/test.py et dnd-5e-core/examples/demo_phase1.py
"""

import sys
from pathlib import Path

# Ajouter le chemin vers dnd-5e-core
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'dnd-5e-core'))

from dnd_5e_core.data.loaders import simple_character_generator
import json
import argparse


def display_character(char):
    """Affiche toutes les informations d'un personnage"""
    print("\n" + "=" * 80)
    print(f"✨ {char.name} - {char.race.name} {char.class_type.name}")
    print("=" * 80)

    print(f"\n📊 STATISTIQUES DE BASE")
    print(f"   Niveau: {char.level}")
    print(f"   Points de vie: {char.hit_points}/{char.max_hit_points}")
    print(f"   Vitesse: {char.speed} pieds")
    print(f"   Or: {char.gold} po")

    print(f"\n💪 CARACTÉRISTIQUES")
    print(f"   Force:        {char.abilities.str:2d} (modificateur: {char.ability_modifiers.str:+d})")
    print(f"   Dextérité:    {char.abilities.dex:2d} (modificateur: {char.ability_modifiers.dex:+d})")
    print(f"   Constitution: {char.abilities.con:2d} (modificateur: {char.ability_modifiers.con:+d})")
    print(f"   Intelligence: {char.abilities.int:2d} (modificateur: {char.ability_modifiers.int:+d})")
    print(f"   Sagesse:      {char.abilities.wis:2d} (modificateur: {char.ability_modifiers.wis:+d})")
    print(f"   Charisme:     {char.abilities.cha:2d} (modificateur: {char.ability_modifiers.cha:+d})")

    proficiency_bonus = 2 + ((char.level - 1) // 4)
    print(f"\n   Bonus de maîtrise: +{proficiency_bonus}")

    # Capacités de classe
    print(f"\n⚔️  CAPACITÉS DE CLASSE")

    if hasattr(char, 'multi_attack_bonus') and char.multi_attack_bonus:
        total_attacks = char.multi_attack_bonus + 1
        print(f"   Extra Attack: {total_attacks} attaques par action")

    if hasattr(char, 'sneak_attack_dice') and char.sneak_attack_dice:
        print(f"   Sneak Attack: +{char.sneak_attack_dice}d6 dégâts")

    if hasattr(char, 'rage_uses_left'):
        print(f"   Rage: {char.rage_uses_left} utilisations par repos long")
        if hasattr(char, 'rage_damage_bonus'):
            print(f"   Bonus de rage: +{char.rage_damage_bonus} dégâts")

    if hasattr(char, 'ki_points'):
        print(f"   Points de ki: {char.ki_points}/{char.ki_points_max if hasattr(char, 'ki_points_max') else char.ki_points}")

    if hasattr(char, 'lay_on_hands_pool'):
        print(f"   Lay on Hands: {char.lay_on_hands_pool} points de soin")

    # Traits raciaux
    print(f"\n🧝 TRAITS RACIAUX")

    if hasattr(char, 'darkvision'):
        print(f"   Vision dans le noir: {char.darkvision} pieds")

    if hasattr(char, 'fey_ancestry'):
        print(f"   Fey Ancestry: avantage aux JS contre charme, immunité au sommeil magique")

    if hasattr(char, 'trance'):
        print(f"   Trance: méditation de 4h au lieu de 8h de sommeil")

    if hasattr(char, 'lucky'):
        print(f"   Lucky: relancer les 1 naturels")

    if hasattr(char, 'brave'):
        print(f"   Brave: avantage aux JS contre la peur")

    if hasattr(char, 'dwarven_resilience'):
        print(f"   Dwarven Resilience: avantage aux JS contre poison")

    if hasattr(char, 'relentless_endurance'):
        print(f"   Relentless Endurance: 1 fois par repos, rester à 1 PV au lieu de tomber à 0")

    if hasattr(char, 'savage_attacks'):
        print(f"   Savage Attacks: lancer un dé de dégâts supplémentaire lors d'un coup critique")

    # Sorts
    if hasattr(char, 'sc') and char.sc:
        sc = char.sc
        print(f"\n✨ MAGIE")
        print(f"   Caractéristique d'incantation: {sc.dc_type.upper()}")
        print(f"   DD des sorts: {sc.dc_value}")
        print(f"   Modificateur d'attaque: +{proficiency_bonus + sc.ability_modifier}")

        print(f"\n   Emplacements de sorts:")
        for level in range(1, 10):
            if level < len(sc.spell_slots) and sc.spell_slots[level] > 0:
                print(f"      Niveau {level}: {sc.spell_slots[level]} emplacements")

        if sc.learned_spells:
            print(f"\n   Sorts connus ({len(sc.learned_spells)}):")

            # Grouper par niveau
            spells_by_level = {}
            for spell in sc.learned_spells:
                spell_level = spell.level if hasattr(spell, 'level') else 0
                if spell_level not in spells_by_level:
                    spells_by_level[spell_level] = []
                spells_by_level[spell_level].append(spell)

            for level in sorted(spells_by_level.keys()):
                level_name = "Tours de magie" if level == 0 else f"Niveau {level}"
                print(f"\n      {level_name}:")
                for spell in spells_by_level[level]:
                    spell_name = spell.name if hasattr(spell, 'name') else str(spell)
                    print(f"         • {spell_name}")

    print("\n" + "=" * 80)


def save_character_to_json(char, output_file):
    """Sauvegarde le personnage en JSON"""
    from scripts.create_party import character_to_dict

    char_data = character_to_dict(char)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(char_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Personnage sauvegardé dans: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Crée un personnage pour les scénarios DnD 5e'
    )
    parser.add_argument('--name', type=str,
                        help='Nom du personnage (aléatoire si non spécifié)')
    parser.add_argument('--class', dest='char_class', type=str,
                        help='Classe (fighter, wizard, rogue, cleric, etc.)')
    parser.add_argument('--race', type=str,
                        help='Race (human, elf, dwarf, halfling, etc.)')
    parser.add_argument('--level', type=int, default=1,
                        help='Niveau du personnage (défaut: 1)')
    parser.add_argument('--out', type=str,
                        help='Fichier de sortie JSON (optionnel)')
    parser.add_argument('--no-display', action='store_true',
                        help='Ne pas afficher les détails (juste sauvegarder)')

    args = parser.parse_args()

    try:
        print(f"\n🎲 Création d'un personnage niveau {args.level}...")

        char = simple_character_generator(
            level=args.level,
            class_name=args.char_class,
            race_name=args.race,
            name=args.name
        )

        if not args.no_display:
            display_character(char)

        if args.out:
            save_character_to_json(char, args.out)

        print("\n✨ Terminé!")

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
