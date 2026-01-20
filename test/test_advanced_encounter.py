#!/usr/bin/env python3
"""
Test de combat avancé avec encounter_builder et groupe de niveaux variés
"""

import sys
from pathlib import Path

# Ajouter le chemin du package dnd-5e-core
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'dnd-5e-core'))

from dnd_5e_core import Character, Monster, AbilityType
from dnd_5e_core.data.loaders import (
    simple_character_generator,
    load_monsters_database
)
from dnd_5e_core.combat.combat_system import CombatSystem
from dnd_5e_core.mechanics.encounter_builder import (
    select_monsters_by_encounter_table,
    get_encounter_info
)
from random import randint, choice


def print_separator(title="", char="="):
    """Afficher un séparateur avec titre optionnel"""
    width = 80
    if title:
        padding = (width - len(title) - 2) // 2
        print(f"\n{char * padding} {title} {char * padding}")
    else:
        print(f"\n{char * width}")


def create_varied_party() -> list:
    """
    Créer un groupe de 6 personnages avec des niveaux variés (3-8)

    Composition:
    - 2 guerriers de mêlée (niveaux 6-8)
    - 2 lanceurs de sorts (niveaux 4-6)
    - 2 hybrides (rogue/monk) (niveaux 3-5)
    """
    print_separator("CRÉATION DU GROUPE AVEC NIVEAUX VARIÉS")

    party = []

    # Guerrier de mêlée niveau élevé
    print("\n🗡️  Création du guerrier (niveau 8)...")
    fighter = simple_character_generator(
        level=8,
        race_name='mountain-dwarf',
        class_name='fighter',
        name='Thorin Bouclier-de-Fer'
    )

    party.append(fighter)
    print(f"   ✅ {fighter.name}: {fighter.class_type.name} {fighter.level} ({fighter.race.name})")
    print(f"      HP: {fighter.max_hit_points}, AC: {fighter.armor_class}")

    # Barbare niveau 7
    print("\n⚔️  Création du barbare (niveau 7)...")
    barbarian = simple_character_generator(
        level=7,
        race_name='half-orc',
        class_name='barbarian',
        name='Grok le Furieux'
    )

    party.append(barbarian)
    print(f"   ✅ {barbarian.name}: {barbarian.class_type.name} {barbarian.level} ({barbarian.race.name})")
    print(f"      HP: {barbarian.max_hit_points}, AC: {barbarian.armor_class}")

    # Clerc niveau 6
    print("\n✨ Création du clerc (niveau 6)...")
    cleric = simple_character_generator(
        level=6,
        race_name='human',
        class_name='cleric',
        name='Sœur Elara'
    )

    party.append(cleric)
    print(f"   ✅ {cleric.name}: {cleric.class_type.name} {cleric.level} ({cleric.race.name})")
    print(f"      HP: {cleric.max_hit_points}, AC: {cleric.armor_class}")

    # Sorcier niveau 5
    print("\n🔮 Création du sorcier (niveau 5)...")
    wizard = simple_character_generator(
        level=5,
        race_name='high-elf',
        class_name='wizard',
        name='Aldric le Sage'
    )

    party.append(wizard)
    print(f"   ✅ {wizard.name}: {wizard.class_type.name} {wizard.level} ({wizard.race.name})")
    print(f"      HP: {wizard.max_hit_points}, AC: {wizard.armor_class}")

    # Roublard niveau 4
    print("\n🗡️  Création du roublard (niveau 4)...")
    rogue = simple_character_generator(
        level=4,
        race_name='lightfoot-halfling',
        class_name='rogue',
        name='Pippin Doigts-Légers'
    )

    party.append(rogue)
    print(f"   ✅ {rogue.name}: {rogue.class_type.name} {rogue.level} ({rogue.race.name})")
    print(f"      HP: {rogue.max_hit_points}, AC: {rogue.armor_class}")

    # Moine niveau 3
    print("\n🥋 Création du moine (niveau 3)...")
    monk = simple_character_generator(
        level=3,
        race_name='wood-elf',
        class_name='monk',
        name='Li Mei'
    )

    party.append(monk)
    print(f"   ✅ {monk.name}: {monk.class_type.name} {monk.level} ({monk.race.name})")
    print(f"      HP: {monk.max_hit_points}, AC: {monk.armor_class}")

    # Calculer le niveau moyen
    avg_level = sum(c.level for c in party) / len(party)
    print_separator()
    print(f"\n📊 Groupe constitué: {len(party)} personnages")
    print(f"   Niveau moyen: {avg_level:.1f}")
    print(f"   Niveaux: {', '.join(str(c.level) for c in party)}")
    print(f"   HP total: {sum(c.max_hit_points for c in party)}")

    return party


def select_encounter_monsters(party: list, difficulty: str = "medium") -> list:
    """
    Sélectionner des monstres pour une rencontre basée sur le niveau du groupe

    Args:
        party: Liste des personnages
        difficulty: "easy", "medium", "hard", "deadly"

    Returns:
        Liste de monstres sélectionnés
    """
    avg_level = round(sum(c.level for c in party) / len(party))

    # Ajuster le niveau de rencontre selon la difficulté
    difficulty_modifiers = {
        "easy": -1,
        "medium": 0,
        "hard": 2,
        "deadly": 5
    }

    encounter_level = max(1, min(20, avg_level + difficulty_modifiers.get(difficulty, 0)))

    print_separator(f"SÉLECTION DES MONSTRES (Difficulté: {difficulty.upper()})")
    print(f"\n📊 Niveau moyen du groupe: {avg_level}")
    print(f"   Niveau de rencontre: {encounter_level}")

    # Obtenir les infos de rencontre
    encounter_info = get_encounter_info(encounter_level)
    print(f"\n   Options de paires: CR {encounter_info['pair_crs'][0]} + CR {encounter_info['pair_crs'][1]}")
    print(f"   Options de groupes: {list(encounter_info['group_options'].keys())}")

    # Charger tous les monstres disponibles
    all_monsters = load_monsters_database()
    print(f"\n   Monstres disponibles: {len(all_monsters)}")

    # Sélectionner les monstres via encounter_builder
    monsters, encounter_type = select_monsters_by_encounter_table(
        encounter_level=encounter_level,
        available_monsters=all_monsters,
        allow_pairs=True
    )

    print(f"\n   Type de rencontre: {encounter_type}")
    print(f"   Nombre de monstres: {len(monsters)}")

    if monsters:
        print(f"\n👹 Ennemis sélectionnés:")
        for i, m in enumerate(monsters, 1):
            print(f"   {i}. {m.name} (CR {m.challenge_rating})")
            print(f"      HP: {m.max_hit_points}, AC: {m.armor_class}")

    return monsters


def run_advanced_encounter():
    """Exécuter un combat avancé avec encounter_builder"""

    print_separator("TEST DE COMBAT AVANCÉ AVEC ENCOUNTER BUILDER", "═")

    # Créer le groupe
    party = create_varied_party()

    # Sélectionner les monstres (difficulté medium par défaut)
    monsters = select_encounter_monsters(party, difficulty="medium")

    if not monsters:
        print("\n❌ Aucun monstre n'a pu être sélectionné!")
        return

    # Initialiser le système de combat
    print_separator("DÉBUT DU COMBAT")
    combat = CombatSystem()

    # Calculer l'initiative
    print("\n🎲 Calcul de l'initiative...")

    # Initiative des personnages
    char_initiatives = []
    for char in party:
        init_roll = randint(1, 20) + char.abilities.get_modifier(AbilityType.DEX.value)
        char_initiatives.append((init_roll, char, "character"))
        print(f"   {char.name}: {init_roll}")

    # Initiative des monstres
    monster_initiatives = []
    for monster in monsters:
        init_roll = randint(1, 20) + monster.abilities.get_modifier(AbilityType.DEX.value)
        monster_initiatives.append((init_roll, monster, "monster"))
        print(f"   {monster.name}: {init_roll}")

    # Ordre d'initiative
    all_initiatives = sorted(
        char_initiatives + monster_initiatives,
        key=lambda x: x[0],
        reverse=True
    )

    print("\n📋 Ordre d'initiative:")
    for i, (roll, creature, ctype) in enumerate(all_initiatives, 1):
        name = creature.name
        print(f"   {i}. {name} ({roll})")

    # Combat
    round_num = 1
    max_rounds = 20

    while round_num <= max_rounds:
        print_separator(f"ROUND {round_num}")

        # Vérifier si le combat est terminé
        alive_party = [c for c in party if c.hit_points > 0]
        alive_monsters = [m for m in monsters if m.hit_points > 0]

        if not alive_party:
            print("\n💀 DÉFAITE! Tous les personnages sont tombés!")
            break

        if not alive_monsters:
            print("\n🎉 VICTOIRE! Tous les monstres sont vaincus!")
            break

        # Tour par tour selon l'initiative
        for init_roll, creature, ctype in all_initiatives:
            if creature.hit_points <= 0:
                continue

            print(f"\n🎯 Tour de {creature.name} (HP: {creature.hit_points}/{creature.max_hit_points})")

            if ctype == "character":
                # Tour du personnage
                if alive_monsters:
                    target = choice(alive_monsters)

                    # Attaque de base manuelle
                    attack_bonus = creature.abilities.get_modifier(AbilityType.STR.value) + creature.proficiency_bonus
                    attack_roll = randint(1, 20) + attack_bonus

                    if attack_roll >= target.armor_class:
                        # Dégâts basiques (1d8 + modificateur de Force)
                        damage = randint(1, 8) + creature.abilities.get_modifier(AbilityType.STR.value)
                        target.hit_points -= damage
                        print(f"   ✅ Inflige {damage} dégâts à {target.name}")
                        print(f"      {target.name}: {max(0, target.hit_points)}/{target.max_hit_points} HP")

                        if target.hit_points <= 0:
                            print(f"   💀 {target.name} est vaincu!")
                            alive_monsters.remove(target)
                    else:
                        print(f"   ❌ Manque {target.name} (jet: {attack_roll} vs AC {target.armor_class})")

            else:
                # Tour du monstre
                if alive_party:
                    target = choice(alive_party)

                    # Utiliser l'attaque du monstre
                    available_attacks = [
                        a for a in creature.actions
                        if a.attack_bonus is not None and a.damages
                    ]

                    if available_attacks:
                        attack = choice(available_attacks)
                        attack_roll = randint(1, 20) + attack.attack_bonus

                        if attack_roll >= target.armor_class:
                            # Calculer les dégâts à partir de la moyenne (avec gestion des erreurs)
                            try:
                                damage = max(1, attack.total_damage_average)
                            except:
                                # Fallback: dégâts basés sur le CR du monstre
                                damage = max(1, int(creature.challenge_rating * 5))

                            target.hit_points -= damage
                            print(f"   ✅ {attack.name} touche {target.name}! {damage} dégâts")
                            print(f"      {target.name}: {max(0, target.hit_points)}/{target.max_hit_points} HP")

                            if target.hit_points <= 0:
                                print(f"   💀 {target.name} est tombé!")
                                alive_party.remove(target)
                        else:
                            print(f"   ❌ {attack.name} manque {target.name} (jet: {attack_roll} vs AC {target.armor_class})")

        round_num += 1

    # Résumé final
    print_separator("RÉSUMÉ DU COMBAT")

    alive_party = [c for c in party if c.hit_points > 0]
    alive_monsters = [m for m in monsters if m.hit_points > 0]

    if alive_party and not alive_monsters:
        print("\n🎉 VICTOIRE!")
        print(f"\n👥 Survivants ({len(alive_party)}/{len(party)}):")
        for char in alive_party:
            hp_percent = (char.hit_points / char.max_hit_points) * 100
            print(f"   • {char.name}: {char.hit_points}/{char.max_hit_points} HP ({hp_percent:.0f}%)")
    elif alive_monsters and not alive_party:
        print("\n💀 DÉFAITE!")
        print(f"\n👹 Monstres survivants:")
        for monster in alive_monsters:
            print(f"   • {monster.name}: {monster.hit_points}/{monster.max_hit_points} HP")
    else:
        print("\n⚔️ Combat interrompu (limite de rounds atteinte)")

    print()


if __name__ == "__main__":
    run_advanced_encounter()
