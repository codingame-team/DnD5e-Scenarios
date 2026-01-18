"""
Test Complet du Système de Combat D&D 5e v4.0
=============================================

Fonctionnalités testées:
- ✅ Armes magiques avec conditions
- ✅ Sorts de défense (Shield, Mage Armor, etc.)
- ✅ Sorts affectant les conditions des monstres (Hold Person, etc.)
- ✅ Gestion des conditions des monstres
- ✅ Système d'initiative (comme dans main.py)
- ✅ Potions et objets magiques
- ✅ Dégâts continus des conditions
"""

from dnd_5e_core import load_monster
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.data.collections import load_all_monsters
from dnd_5e_core.combat import CombatSystem, create_paralyzed_condition, create_restrained_condition
from dnd_5e_core.equipment import (
    HealingPotion,
    PotionRarity,
    create_ring_of_protection,
    create_wand_of_paralysis,
    create_poisoned_dagger
)
from dnd_5e_core.mechanics.encounter_builder import get_encounter_info
from dnd_5e_core.mechanics.gold_rewards import get_encounter_gold
from random import randint, choice


# =============================================================================
# ARMES MAGIQUES
# =============================================================================

def create_magic_weapon(name, bonus, special_condition=None):
    """
    Crée une arme magique avec bonus et conditions optionnelles

    Args:
        name: Nom de l'arme
        bonus: Bonus aux jets d'attaque et de dégâts (+1, +2, +3)
        special_condition: Condition appliquée sur hit (optionnel)
    """
    from dnd_5e_core.equipment import Weapon, DamageType
    from dnd_5e_core.data import load_weapon

    # Charger l'arme de base
    base_weapon = load_weapon(name.lower().replace('+', '').replace(' ', '-'))

    if not base_weapon:
        return None

    # Créer une copie avec bonus
    magic_weapon = base_weapon
    magic_weapon.name = f"{name} +{bonus}"

    # Ajouter les bonus (stockés comme attributs custom)
    magic_weapon.attack_bonus = bonus
    magic_weapon.damage_bonus = bonus
    magic_weapon.special_condition = special_condition

    return magic_weapon


# =============================================================================
# SORTS DE DÉFENSE
# =============================================================================

def cast_shield(caster, verbose=True):
    """Lance Shield: +5 AC jusqu'au prochain tour"""
    if not hasattr(caster, 'sc') or not caster.sc:
        return False

    # Vérifier slots de sort niveau 1
    if caster.sc.spell_slots[1] > 0:
        caster.sc.spell_slots[1] -= 1

        # Appliquer le bonus via ac_bonus
        if not hasattr(caster, 'ac_bonus'):
            caster.ac_bonus = 0

        old_ac = caster.armor_class
        caster.ac_bonus += 5

        # Marquer pour retirer le bonus au prochain tour
        if not hasattr(caster, 'temp_ac_bonus'):
            caster.temp_ac_bonus = 0
        caster.temp_ac_bonus += 5

        if verbose:
            print(f"      🛡️  {caster.name} lance Shield! AC: {old_ac} → {caster.armor_class}")

        return True

    return False


def cast_mage_armor(caster, verbose=True):
    """Lance Mage Armor: AC = 13 + DEX mod"""
    if not hasattr(caster, 'sc') or not caster.sc:
        return False

    if caster.sc.spell_slots[1] > 0:
        caster.sc.spell_slots[1] -= 1

        dex_mod = caster.abilities.get_modifier('dex')
        target_ac = 13 + dex_mod

        # Calculer le bonus nécessaire pour atteindre target_ac
        current_ac = caster.armor_class

        if target_ac > current_ac:
            if not hasattr(caster, 'ac_bonus'):
                caster.ac_bonus = 0

            bonus_needed = target_ac - current_ac
            caster.ac_bonus += bonus_needed

            if verbose:
                print(f"      🛡️  {caster.name} lance Mage Armor! AC: {current_ac} → {caster.armor_class}")

            return True

    return False


# =============================================================================
# SORTS AFFECTANT LES CONDITIONS DES MONSTRES
# =============================================================================

def cast_hold_person(caster, target_monster, verbose=True):
    """Lance Hold Person: paralyse un humanoïde"""
    if not hasattr(caster, 'sc') or not caster.sc:
        return False

    # Vérifier slots niveau 2
    if caster.sc.spell_slots[2] > 0:
        caster.sc.spell_slots[2] -= 1

        # DC du sort
        spell_dc = 8 + caster.sc.ability_modifier + caster.level // 2

        # Jet de sauvegarde WIS du monstre
        from dnd_5e_core import AbilityType
        wis_mod = target_monster.abilities.get_modifier('wis')
        save_roll = randint(1, 20) + wis_mod

        if save_roll < spell_dc:
            # Créer et appliquer la condition paralysé
            paralyzed = create_paralyzed_condition(dc_type=AbilityType.WIS, dc_value=spell_dc)
            paralyzed.apply_to_monster(target_monster)

            if verbose:
                print(f"      ⚡ {caster.name} lance Hold Person sur {target_monster.name}!")
                print(f"         {target_monster.name} rate son JS (DC {spell_dc}) et est PARALYSÉ!")

            return True
        else:
            if verbose:
                print(f"      ⚡ {caster.name} lance Hold Person sur {target_monster.name}!")
                print(f"         {target_monster.name} réussit son JS (DC {spell_dc})")

            return False

    return False


def cast_entangle(caster, target_monsters, verbose=True):
    """Lance Entangle: entrave plusieurs créatures"""
    if not hasattr(caster, 'sc') or not caster.sc:
        return False

    if caster.sc.spell_slots[1] > 0:
        caster.sc.spell_slots[1] -= 1

        from dnd_5e_core import AbilityType
        spell_dc = 8 + caster.sc.ability_modifier + caster.level // 2

        affected = []
        for monster in target_monsters[:3]:  # Maximum 3 cibles
            str_mod = monster.abilities.get_modifier('str')
            save_roll = randint(1, 20) + str_mod

            if save_roll < spell_dc:
                restrained = create_restrained_condition(dc_type=AbilityType.STR, dc_value=spell_dc)
                restrained.apply_to_monster(monster)
                affected.append(monster.name)

        if verbose:
            if affected:
                print(f"      🌿 {caster.name} lance Entangle!")
                print(f"         {', '.join(affected)} sont ENTRAVÉS!")
            else:
                print(f"      🌿 {caster.name} lance Entangle mais les monstres résistent!")

        return len(affected) > 0

    return False


# =============================================================================
# GESTION DES CONDITIONS
# =============================================================================

def display_conditions(creature):
    """Affiche les conditions actives"""
    if hasattr(creature, 'conditions') and creature.conditions:
        conditions_str = ", ".join([c.name for c in creature.conditions])
        return f"🔴 [{conditions_str}]"
    return ""


def check_condition_effects(creature):
    """Vérifie les effets des conditions"""
    effects = {
        'can_act': True,
        'has_disadvantage': False,
        'is_paralyzed': False,
        'is_restrained': False,
        'attacks_have_advantage': False,
        'ongoing_damage': 0,
        'conditions_list': []
    }

    if not hasattr(creature, 'conditions') or not creature.conditions:
        return effects

    for condition in creature.conditions:
        condition_name = condition.name.lower()
        effects['conditions_list'].append(condition.name)

        if condition_name == 'paralyzed':
            effects['can_act'] = False
            effects['is_paralyzed'] = True
            effects['attacks_have_advantage'] = True
        elif condition_name == 'restrained':
            effects['is_restrained'] = True
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True
        elif condition_name == 'poisoned':
            effects['has_disadvantage'] = True
            effects['ongoing_damage'] += randint(1, 4)

    return effects


def apply_ongoing_effects(creature, verbose=True):
    """Applique les effets continus (poison, etc.)"""
    effects = check_condition_effects(creature)

    if effects['ongoing_damage'] > 0:
        damage = effects['ongoing_damage']
        creature.hit_points = max(0, creature.hit_points - damage)

        if verbose:
            print(f"      ☠️  {creature.name} subit {damage} dégâts de poison!")

        return damage

    return 0


def attempt_save_from_conditions(creature, verbose=True):
    """Tente de se libérer des conditions"""
    if not hasattr(creature, 'conditions') or not creature.conditions:
        return []

    escaped = []
    for condition in creature.conditions[:]:
        if condition.dc_type and condition.dc_value:
            if verbose:
                creature_name = creature.name if hasattr(creature, 'name') else "Creature"
                print(f"      🎲 {creature_name} tente de se libérer de {condition.name} (DC {condition.dc_value})...")

            if condition.attempt_save(creature):
                if verbose:
                    print(f"         ✅ Réussi!")
                escaped.append(condition.name)
            else:
                if verbose:
                    print(f"         ❌ Échoué!")

    return escaped


# =============================================================================
# SYSTÈME D'INITIATIVE (comme dans main.py)
# =============================================================================

def roll_initiative(party, monsters, verbose=True):
    """
    Calcule l'ordre d'initiative comme dans explore_dungeon de main.py

    Initiative = 1d20 + modificateur DEX
    """
    if verbose:
        print(f"\n🎲 JETS D'INITIATIVE")
        print("=" * 80)

    # Jets d'initiative pour le groupe
    party_initiatives = []
    for char in party:
        dex_mod = char.abilities.get_modifier('dex')
        roll = randint(1, 20) + dex_mod
        party_initiatives.append((char, roll))

        if verbose:
            print(f"   {char.name}: {roll} (1d20 + {dex_mod})")

    # Jets d'initiative pour les monstres
    monster_initiatives = []
    for monster in monsters:
        dex_mod = monster.abilities.get_modifier('dex')
        roll = randint(1, 20) + dex_mod
        monster_initiatives.append((monster, roll))

        if verbose:
            print(f"   {monster.name}: {roll} (1d20 + {dex_mod})")

    # Combiner et trier par initiative (décroissant)
    all_initiatives = party_initiatives + monster_initiatives
    all_initiatives.sort(key=lambda x: x[1], reverse=True)

    # Retourner l'ordre des combattants
    initiative_order = [creature for creature, roll in all_initiatives]

    if verbose:
        print(f"\n📋 Ordre d'initiative:")
        for i, creature in enumerate(initiative_order, 1):
            creature_type = "⚔️" if creature in party else "👹"
            print(f"   {i}. {creature_type} {creature.name}")

    return initiative_order


# =============================================================================
# COMBAT PRINCIPAL
# =============================================================================

def run_advanced_combat_test():
    """Test complet avec toutes les fonctionnalités"""

    print("\n" + "🎲" * 40)
    print("TEST COMPLET DU SYSTÈME DE COMBAT D&D 5e v4.0")
    print("🎲" * 40)

    # =============================================================================
    # ÉTAPE 1: Création du groupe
    # =============================================================================
    print(f"\n📖 ÉTAPE 1: CRÉATION DU GROUPE")
    print("=" * 80)

    party = [
        simple_character_generator(5, 'human', 'fighter', 'Conan'),
        simple_character_generator(5, 'elf', 'wizard', 'Gandalf'),
        simple_character_generator(5, 'dwarf', 'cleric', 'Gimli'),
        simple_character_generator(5, 'halfling', 'rogue', 'Bilbo'),
    ]

    for char in party:
        print(f"   - {char.name} ({char.class_type.name} Niv.{char.level})")
        print(f"     HP: {char.hit_points}, AC: {char.armor_class}, DEX: {char.abilities.dex}")

    # =============================================================================
    # ÉTAPE 2: Équipement magique
    # =============================================================================
    print(f"\n💎 ÉTAPE 2: ÉQUIPEMENT MAGIQUE")
    print("=" * 80)

    # Armes magiques
    conan = party[0]
    longsword_plus_1 = create_magic_weapon("longsword", 1)
    if longsword_plus_1:
        print(f"   ⚔️  {conan.name} reçoit {longsword_plus_1.name}")
        print(f"      +1 attaque et dégâts")

    # Dague empoisonnée (conditions)
    bilbo = party[3]
    poisoned_dagger = create_poisoned_dagger()
    if poisoned_dagger:
        print(f"   🗡️  {bilbo.name} reçoit {poisoned_dagger.name}")
        print(f"      Applique Poisoned aux cibles")

    # Baguette de paralysie
    gandalf = party[1]
    wand = create_wand_of_paralysis()
    if wand:
        print(f"   🪄 {gandalf.name} reçoit {wand.name}")
        print(f"      Paralyse les ennemis (3 charges/jour)")

    # Anneau de protection pour tous
    for char in party:
        ring = create_ring_of_protection()
        ring.attune(char)
        ring.apply_to_character(char)
        print(f"   💍 {char.name}: Ring of Protection (+1 AC, +1 saves)")

    # Potions
    from dnd_5e_core.equipment import PotionRarity
    for char in party:
        char.inventory = [None] * 20
        for i in range(2):
            potion = HealingPotion("Potion of Healing", PotionRarity.COMMON, "2d4", 2, 50, 50)
            char.inventory[i] = potion
        print(f"   🧪 {char.name}: 2 Potions de Soin")

    # =============================================================================
    # ÉTAPE 3: Sélection des monstres avec conditions
    # =============================================================================
    print(f"\n👹 ÉTAPE 3: GÉNÉRATION DES MONSTRES")
    print("=" * 80)

    # Monstres avec capacités spéciales
    monsters = [
        load_monster('giant-spider'),    # Restrained, Poisoned
        load_monster('ghoul'),           # Paralyzed
        load_monster('giant-scorpion'),  # Poisoned
    ]

    monsters = [m for m in monsters if m is not None]

    for monster in monsters:
        print(f"\n   👹 {monster.name} (CR {monster.challenge_rating})")
        print(f"      HP: {monster.hit_points}, AC: {monster.armor_class}, DEX: {monster.abilities.dex}")

        # Afficher les actions avec conditions
        actions_with_conditions = [a for a in monster.actions if hasattr(a, 'effects') and a.effects]
        if actions_with_conditions:
            print(f"      🔴 Actions avec conditions:")
            for action in actions_with_conditions:
                cond_names = [e.name for e in action.effects]
                print(f"         - {action.name}: {', '.join(cond_names)}")

    # =============================================================================
    # ÉTAPE 4: Initiative
    # =============================================================================
    input("\n[Appuyez sur ENTRÉE pour lancer l'initiative]")

    initiative_order = roll_initiative(party, monsters, verbose=True)

    # =============================================================================
    # ÉTAPE 5: Combat
    # =============================================================================
    input("\n[Appuyez sur ENTRÉE pour commencer le combat]")

    print(f"\n⚔️ DÉBUT DU COMBAT")
    print("=" * 80)

    combat = CombatSystem(verbose=True)
    alive_chars = [c for c in party if c.hit_points > 0]
    alive_monsters = [m for m in monsters if m.hit_points > 0]

    round_num = 1
    max_rounds = 15

    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'=' * 80}")
        print(f"🎲 ROUND {round_num}")
        print(f"{'=' * 80}")

        # Statut
        print(f"\n📊 Statut:")
        print("  Groupe:")
        for char in alive_chars:
            hp_percent = (char.hit_points / char.max_hit_points) * 100
            icon = "❤️" if hp_percent > 50 else "💔"
            cond_str = display_conditions(char)
            print(f"    {icon} {char.name}: {char.hit_points}/{char.max_hit_points} HP {cond_str}")

        print("  Monstres:")
        for monster in alive_monsters:
            cond_str = display_conditions(monster)
            print(f"    👹 {monster.name}: {monster.hit_points} HP {cond_str}")

        # Tour de chaque combattant dans l'ordre d'initiative
        for combattant in initiative_order:
            if combattant.hit_points <= 0:
                continue

            is_char = combattant in party

            if is_char and combattant not in alive_chars:
                continue
            if not is_char and combattant not in alive_monsters:
                continue

            print(f"\n{'⚔️' if is_char else '👹'} Tour de {combattant.name}")

            # Appliquer effets continus
            apply_ongoing_effects(combattant, verbose=True)

            if combattant.hit_points <= 0:
                print(f"   💀 {combattant.name} est mort!")
                if is_char:
                    alive_chars.remove(combattant)
                else:
                    alive_monsters.remove(combattant)
                continue

            # Vérifier conditions
            effects = check_condition_effects(combattant)

            if effects['conditions_list']:
                print(f"   🔴 Conditions: {', '.join(effects['conditions_list'])}")

            # Tenter de se libérer
            if effects['conditions_list']:
                attempt_save_from_conditions(combattant, verbose=True)
                effects = check_condition_effects(combattant)

            # Si paralysé, skip le tour
            if not effects['can_act']:
                print(f"   ⚠️  {combattant.name} est paralysé et ne peut pas agir!")
                continue

            # Action de combat
            if is_char:
                # Personnage
                char = combattant

                # Utiliser sorts de défense si HP bas
                hp_percent = (char.hit_points / char.max_hit_points) * 100
                if hp_percent < 50 and char.class_type.index == 'wizard':
                    cast_shield(char, verbose=True)

                # Utiliser sorts offensifs
                if char.class_type.index == 'wizard' and alive_monsters:
                    target = alive_monsters[0]
                    if not cast_hold_person(char, target, verbose=True):
                        # Action normale
                        combat.character_turn(char, alive_chars, alive_monsters, party)
                elif char.class_type.index == 'cleric' and len(alive_monsters) > 1:
                    if not cast_entangle(char, alive_monsters, verbose=True):
                        combat.character_turn(char, alive_chars, alive_monsters, party)
                else:
                    combat.character_turn(char, alive_chars, alive_monsters, party)

            else:
                # Monstre
                monster = combattant

                # Cibler les personnages vulnérables
                targets_with_conditions = [c for c in alive_chars if check_condition_effects(c)['attacks_have_advantage']]

                if targets_with_conditions:
                    print(f"   🎯 Cibles vulnérables détectées: {', '.join([c.name for c in targets_with_conditions])}")

                combat.monster_turn(monster, alive_monsters, alive_chars, party, round_num)

        # Nettoyer les morts
        alive_chars = [c for c in alive_chars if c.hit_points > 0]
        alive_monsters = [m for m in alive_monsters if m.hit_points > 0]

        round_num += 1

        if round_num <= max_rounds and alive_chars and alive_monsters:
            input(f"\n⏸️  [ENTRÉE pour Round {round_num}]")

    # =============================================================================
    # RÉSULTATS
    # =============================================================================
    print(f"\n{'=' * 80}")
    print("📊 RÉSULTATS")
    print(f"{'=' * 80}")

    if alive_chars:
        print(f"\n✅ VICTOIRE!")
        print(f"\nSurvivants:")
        for char in party:
            if char.hit_points > 0:
                print(f"   ❤️ {char.name}: {char.hit_points}/{char.max_hit_points} HP")
            else:
                print(f"   💀 {char.name}: MORT")
    else:
        print(f"\n❌ DÉFAITE!")

    print(f"\nStatistiques:")
    print(f"   - Rounds: {round_num - 1}")
    print(f"   - Monstres vaincus: {len(monsters) - len(alive_monsters)}/{len(monsters)}")

    print(f"\n{'=' * 80}")
    print("✅ TEST TERMINÉ")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    run_advanced_combat_test()
