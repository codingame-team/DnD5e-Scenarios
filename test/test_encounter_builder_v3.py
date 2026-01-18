"""
Test du système de rencontre D&D 5e avec un groupe de 6 aventuriers
AMÉLIORÉ v3.0:
- Gestion complète des conditions avec effets au fil des tours
- Sorts de guérison et de défense
- Objets magiques (potions, magic items)
- IA intelligente pour utiliser les ressources de guérison
- Monstres avec conditions (poison, paralysie, etc.)
"""
from dnd_5e_core import load_monster
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.data import load_weapon, load_armor, load_spell
from dnd_5e_core.data.collections import load_all_monsters
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.equipment import (
    create_ring_of_protection,
    create_cloak_of_protection,
    HealingPotion
)
from dnd_5e_core.mechanics.encounter_builder import (
    select_monsters_by_encounter_table,
    get_encounter_info
)
from dnd_5e_core.mechanics.gold_rewards import get_encounter_gold
from random import randint, choice


# =============================================================================
# FONCTIONS HELPER POUR LA GESTION DES CONDITIONS
# =============================================================================

def display_conditions(creature):
    """Affiche les conditions actives d'une créature"""
    if hasattr(creature, 'conditions') and creature.conditions:
        conditions_str = ", ".join([c.name for c in creature.conditions])
        return f"🔴 [{conditions_str}]"
    return ""


def check_condition_effects(character):
    """
    Vérifie les effets des conditions sur un personnage

    Returns:
        dict avec les informations sur les limitations et dégâts continus
    """
    effects = {
        'can_move': True,
        'has_disadvantage': False,
        'is_incapacitated': False,
        'attacks_have_advantage': False,
        'speed_zero': False,
        'auto_fail_saves': [],
        'conditions_list': [],
        'ongoing_damage': 0,  # Dégâts continus par tour (poison, etc.)
        'max_hp_reduction': 0,  # Réduction de HP max (mummy rot, etc.)
    }

    if not hasattr(character, 'conditions') or not character.conditions:
        return effects

    for condition in character.conditions:
        condition_name = condition.name.lower()
        effects['conditions_list'].append(condition.name)

        if condition_name == 'restrained':
            effects['speed_zero'] = True
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True

        elif condition_name == 'grappled':
            effects['speed_zero'] = True

        elif condition_name == 'paralyzed':
            effects['is_incapacitated'] = True
            effects['auto_fail_saves'] = ['str', 'dex']
            effects['attacks_have_advantage'] = True

        elif condition_name == 'stunned':
            effects['is_incapacitated'] = True
            effects['auto_fail_saves'] = ['str', 'dex']
            effects['attacks_have_advantage'] = True

        elif condition_name == 'incapacitated':
            effects['is_incapacitated'] = True

        elif condition_name == 'poisoned':
            effects['has_disadvantage'] = True
            effects['ongoing_damage'] += randint(1, 4)  # 1d4 dégâts de poison par tour

        elif condition_name == 'frightened':
            effects['has_disadvantage'] = True

        elif condition_name == 'blinded':
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True

        elif condition_name == 'prone':
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True

    return effects


def apply_ongoing_condition_effects(character, verbose=True):
    """
    Applique les effets continus des conditions (dégâts de poison, etc.)

    Returns:
        int: Total de dégâts subis ce tour
    """
    effects = check_condition_effects(character)
    total_damage = 0

    if effects['ongoing_damage'] > 0:
        damage = effects['ongoing_damage']
        character.hit_points = max(0, character.hit_points - damage)
        total_damage += damage

        if verbose:
            print(f"      ☠️  {character.name} subit {damage} dégâts de poison!")

    if effects['max_hp_reduction'] > 0:
        if hasattr(character, 'max_hit_points'):
            reduction = effects['max_hp_reduction']
            character.max_hit_points = max(1, character.max_hit_points - reduction)
            if verbose:
                print(f"      ⚠️  HP max de {character.name} réduits de {reduction}!")

    return total_damage


def attempt_escape_conditions(character, verbose=True):
    """Tente d'échapper aux conditions actives"""
    escaped = []

    if not hasattr(character, 'conditions') or not character.conditions:
        return escaped

    for condition in character.conditions[:]:
        if condition.dc_type and condition.dc_value:
            if verbose:
                print(f"   🎲 {character.name} tente de se libérer de {condition.name} (DC {condition.dc_value} {condition.dc_type.value})...")

            if condition.attempt_save(character):
                if verbose:
                    print(f"      ✅ Réussi! {character.name} se libère de {condition.name}")
                escaped.append(condition.name)
            else:
                if verbose:
                    print(f"      ❌ Échoué! {character.name} reste {condition.name}")

    return escaped


def display_character_status(character, show_conditions=True):
    """Affiche le statut complet d'un personnage"""
    hp_percent = (character.hit_points / character.max_hit_points) * 100 if character.max_hit_points > 0 else 0

    status_icon = "❤️" if hp_percent > 75 else "💛" if hp_percent > 50 else "🧡" if hp_percent > 25 else "💔"

    status = f"{status_icon} {character.name}: {character.hit_points}/{character.max_hit_points} HP"

    if show_conditions:
        cond_str = display_conditions(character)
        if cond_str:
            status += f" {cond_str}"

    return status


def should_use_healing(character, is_poisoned=False):
    """
    Détermine si un personnage devrait utiliser une guérison

    Returns:
        (bool, str): (should_heal, reason)
    """
    hp_percent = (character.hit_points / character.max_hit_points) * 100

    # Proche de la mort
    if hp_percent < 25:
        return True, "critique"

    # Empoisonné et blessé
    if is_poisoned and hp_percent < 50:
        return True, "empoisonné et blessé"

    # Blessé modérément
    if hp_percent < 40:
        return True, "blessé"

    return False, ""


def try_use_healing(character, party, verbose=True):
    """
    Tente d'utiliser une potion ou un sort de guérison

    Returns:
        bool: True si une guérison a été utilisée
    """
    effects = check_condition_effects(character)
    is_poisoned = 'Poisoned' in effects['conditions_list']

    should_heal, reason = should_use_healing(character, is_poisoned)

    if not should_heal:
        return False

    if verbose:
        print(f"   💊 {character.name} est {reason} et a besoin de soins!")

    # 1. Essayer d'utiliser une potion de soin
    if hasattr(character, 'inventory'):
        for item in character.inventory:
            if item and isinstance(item, HealingPotion):
                # Calculer la guérison (roll des dés)
                from dnd_5e_core.mechanics.dice import DamageDice
                dice = DamageDice(item.hit_dice)
                healing = dice.roll() + item.bonus

                old_hp = character.hit_points
                character.hit_points = min(character.max_hit_points, character.hit_points + healing)
                actual_healing = character.hit_points - old_hp

                if verbose:
                    print(f"      🧪 {character.name} boit une Potion de Soin!")
                    print(f"         Soigne {actual_healing} HP ({old_hp} → {character.hit_points})")

                character.inventory.remove(item)
                return True

    # 2. Essayer qu'un allié clerc/druide lance un sort de soin
    healers = [c for c in party if c != character and c.hit_points > 0 and
               hasattr(c, 'class_type') and c.class_type.index in ['cleric', 'druid']]

    for healer in healers:
        if hasattr(healer, 'sc') and healer.sc:
            # Vérifier si le healer a un slot de sort
            for level in range(1, 6):
                if level < len(healer.sc.spell_slots) and healer.sc.spell_slots[level] > 0:
                    # Utiliser le sort
                    healing = randint(1, 8) + healer.sc.ability_modifier
                    old_hp = character.hit_points
                    character.hit_points = min(character.max_hit_points, character.hit_points + healing)
                    actual_healing = character.hit_points - old_hp

                    healer.sc.spell_slots[level] -= 1

                    if verbose:
                        print(f"      ✨ {healer.name} lance Cure Wounds sur {character.name}!")
                        print(f"         Soigne {actual_healing} HP ({old_hp} → {character.hit_points})")

                    return True

    # 3. Utiliser une action de soin sur soi-même (lay on hands pour paladin, etc.)
    if hasattr(character, 'class_type') and character.class_type.index == 'paladin':
        healing = randint(1, 8) + 3
        old_hp = character.hit_points
        character.hit_points = min(character.max_hit_points, character.hit_points + healing)
        actual_healing = character.hit_points - old_hp

        if verbose:
            print(f"      🙏 {character.name} utilise Imposition des Mains!")
            print(f"         Soigne {actual_healing} HP ({old_hp} → {character.hit_points})")

        return True

    return False


def try_cast_defensive_spell(character, verbose=True):
    """
    Tente de lancer un sort de défense si disponible

    Returns:
        bool: True si un sort a été lancé
    """
    if not hasattr(character, 'sc') or not character.sc:
        return False

    # Shield (niveau 1) - +5 AC jusqu'au prochain tour
    if hasattr(character, 'class_type') and character.class_type.index in ['wizard', 'sorcerer']:
        if character.sc.spell_slots[0] > 0:  # Slot niveau 1
            character.sc.spell_slots[0] -= 1
            old_ac = character.armor_class
            character.armor_class += 5

            if verbose:
                print(f"      🛡️  {character.name} lance Shield! AC: {old_ac} → {character.armor_class}")

            # Marquer pour retirer le bonus au prochain tour
            if not hasattr(character, 'temp_ac_bonus'):
                character.temp_ac_bonus = 0
            character.temp_ac_bonus += 5

            return True

    return False


# =============================================================================
# FONCTIONS D'ÉQUIPEMENT ET DE PRÉPARATION
# =============================================================================

def equip_party_with_magic_items(party, verbose=True):
    """Équipe le groupe avec des objets magiques"""
    if verbose:
        print(f"\n💎 ÉQUIPEMENT MAGIQUE DU GROUPE")
        print("=" * 80)

    for i, char in enumerate(party):
        # Alterner Ring of Protection et Cloak of Protection
        if i % 2 == 0:
            item = create_ring_of_protection()
            item_type = "anneau"
        else:
            item = create_cloak_of_protection()
            item_type = "cape"

        # Ajouter à l'inventaire
        if not hasattr(char, 'inventory'):
            char.inventory = [None] * 20

        for j, inv_item in enumerate(char.inventory):
            if inv_item is None:
                char.inventory[j] = item
                break

        # Attunement
        if item.requires_attunement:
            if not hasattr(char, 'attuned_items'):
                char.attuned_items = []
            char.attuned_items.append(item)
            item.attune(char)

        # Équiper et appliquer les bonus
        item.equipped = True
        item.apply_to_character(char)

        if verbose:
            print(f"   ✨ {char.name} reçoit {item.name}")
            print(f"      +{item.ac_bonus} CA, +{item.saving_throw_bonus} jets de sauvegarde")


def give_healing_potions(party, potions_per_char=2, verbose=True):
    """Donne des potions de soin à chaque membre du groupe"""
    if verbose:
        print(f"\n🧪 DISTRIBUTION DES POTIONS DE SOIN")
        print("=" * 80)

    from dnd_5e_core.equipment import PotionRarity

    for char in party:
        if not hasattr(char, 'inventory'):
            char.inventory = [None] * 20

        potions_given = 0
        for i, item in enumerate(char.inventory):
            if item is None and potions_given < potions_per_char:
                potion = HealingPotion(
                    name="Potion of Healing",
                    rarity=PotionRarity.COMMON,
                    hit_dice="2d4",
                    bonus=2,
                    min_cost=50,
                    max_cost=50
                )
                char.inventory[i] = potion
                potions_given += 1

        if verbose:
            print(f"   {char.name}: {potions_given} potion(s) de soin")


def select_monsters_with_conditions(all_monsters, avg_level, count=3):
    """
    Sélectionne des monstres qui peuvent appliquer des conditions

    Priorité aux monstres avec: poison, paralysie, frightened, restrained
    """
    # Monstres connus pour avoir des conditions
    monsters_with_conditions = [
        'giant-spider',      # Restrained, Poisoned
        'ghoul',            # Paralyzed
        'giant-poisonous-snake',  # Poisoned
        'ettercap',         # Poisoned, Restrained
        'giant-centipede',  # Poisoned
        'mummy',            # Frightened, Paralyzed (Dreadful Glare)
        'cockatrice',       # Petrified
        'giant-scorpion',   # Poisoned
    ]

    # Filtrer par CR approprié (CR proche du niveau moyen)
    suitable_monsters = []

    for monster_index in monsters_with_conditions:
        monster = load_monster(monster_index)
        if monster and 0.5 <= monster.challenge_rating <= avg_level + 2:
            suitable_monsters.append(monster)

    # Si pas assez de monstres avec conditions, ajouter des monstres normaux
    if len(suitable_monsters) < count:
        for monster in all_monsters[:20]:
            if monster.challenge_rating <= avg_level + 1:
                suitable_monsters.append(monster)

    # Sélectionner aléatoirement
    selected = []
    for _ in range(min(count, len(suitable_monsters))):
        if suitable_monsters:
            monster = choice(suitable_monsters)
            selected.append(monster)

    return selected


# =============================================================================
# SCRIPT PRINCIPAL
# =============================================================================

def main():
    print("\n" + "🎲" * 40)
    print("TEST ENCOUNTER BUILDER v3.0 - ÉDITION COMPLÈTE")
    print("🎲" * 40)

    # =============================================================================
    # ÉTAPE 1: Création du groupe de 6 aventuriers
    # =============================================================================
    print(f"\n📖 ÉTAPE 1: CRÉATION DU GROUPE")
    print("=" * 80)

    party_size = 6
    avg_level = 4

    # Composition du groupe (variété de classes)
    party_config = [
        ('fighter', 'Grok'),
        ('paladin', 'Theron'),
        ('cleric', 'Sœur Elara'),
        ('wizard', 'Gandalf'),
        ('rogue', 'Shadowblade'),
        ('ranger', 'Legolas')
    ]

    party = []
    for class_name, name in party_config:
        level = avg_level + randint(-1, 1)  # Niveau légèrement variable
        char = simple_character_generator(
            level=level,
            race_name=choice(['human', 'elf', 'dwarf', 'halfling']),
            class_name=class_name,
            name=name
        )
        party.append(char)

    print(f"\n✨ Groupe de {len(party)} aventuriers créé:")
    for char in party:
        print(f"   - {char.name} ({char.race.name} {char.class_type.name} Niv.{char.level})")
        print(f"     HP: {char.hit_points}/{char.max_hit_points}, AC: {char.armor_class}")

    # =============================================================================
    # ÉTAPE 2: Équipement magique et potions
    # =============================================================================
    equip_party_with_magic_items(party, verbose=True)
    give_healing_potions(party, potions_per_char=3, verbose=True)

    # =============================================================================
    # ÉTAPE 3: Génération de la rencontre avec monstres à conditions
    # =============================================================================
    print(f"\n⚔️ ÉTAPE 3: GÉNÉRATION DE LA RENCONTRE")
    print("=" * 80)

    # Charger tous les monstres
    all_monsters = load_all_monsters()

    # Calculer le niveau moyen
    avg_party_level = sum(c.level for c in party) // len(party)
    print(f"Niveau moyen du groupe: {avg_party_level}")

    # Sélectionner des monstres avec conditions
    monsters = select_monsters_with_conditions(all_monsters, avg_party_level, count=4)

    print(f"\n✨ Rencontre générée:")
    print(f"   Nombre de monstres: {len(monsters)}")

    # Afficher les monstres avec leurs capacités
    for monster in monsters:
        print(f"\n   👹 {monster.name} (CR {monster.challenge_rating})")
        print(f"      HP: {monster.hit_points}, AC: {monster.armor_class}")

        # Afficher les actions avec conditions
        actions_with_conditions = [a for a in monster.actions if hasattr(a, 'effects') and a.effects]
        if actions_with_conditions:
            print(f"      🔴 Actions avec conditions:")
            for action in actions_with_conditions:
                cond_names = [e.name for e in action.effects]
                print(f"         - {action.name}: {', '.join(cond_names)}")

    # =============================================================================
    # ÉTAPE 4: Combat avec gestion avancée
    # =============================================================================
    print(f"\n⚔️ ÉTAPE 4: COMBAT!")
    print("=" * 80)

    # Formation: combattants devant, lanceurs de sorts derrière
    front_row_classes = ["fighter", "paladin", "ranger"]
    party_sorted = sorted(party, key=lambda c: 0 if c.class_type.index in front_row_classes else 1)

    print(f"\n📊 Formation du groupe:")
    for i, char in enumerate(party_sorted):
        position = "Front (Mêlée)" if i < 3 else "Back (Distance/Sorts)"
        print(f"  [{i}] {char.name}: {position} - {char.hit_points} HP, AC {char.armor_class}")

    input("\n[Appuyez sur ENTRÉE pour commencer le combat]")

    # Combat
    combat = CombatSystem(verbose=True)
    alive_chars = [c for c in party_sorted if c.hit_points > 0]
    alive_monsters = monsters.copy()

    round_num = 1
    max_rounds = 20

    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n{'='*80}")
        print(f"🎲 ROUND {round_num}")
        print(f"{'='*80}")

        # Statut du groupe
        print(f"\n📊 Statut du groupe:")
        for char in alive_chars:
            print(f"   {display_character_status(char)}")

        # Phase des aventuriers
        print(f"\n⚔️ PHASE DES AVENTURIERS")
        print("-" * 80)

        for char in alive_chars[:]:
            if not alive_monsters:
                break
            if char.hit_points <= 0:
                if char in alive_chars:
                    alive_chars.remove(char)
                continue

            print(f"\n🎯 Tour de {char.name}")

            # Appliquer les effets continus des conditions (poison, etc.)
            ongoing_damage = apply_ongoing_condition_effects(char, verbose=True)

            # Vérifier si le personnage est mort suite aux dégâts continus
            if char.hit_points <= 0:
                print(f"   💀 {char.name} succombe aux effets des conditions!")
                if char in alive_chars:
                    alive_chars.remove(char)
                continue

            # Vérifier les conditions
            effects = check_condition_effects(char)

            if effects['conditions_list']:
                print(f"   🔴 Conditions actives: {', '.join(effects['conditions_list'])}")

            # Essayer de se soigner si nécessaire
            if try_use_healing(char, party_sorted, verbose=True):
                # Recalculer les effets après guérison
                pass

            # Si incapacité, tenter de se libérer
            if effects['is_incapacitated']:
                print(f"   ⚠️  {char.name} est incapable d'agir")
                escaped = attempt_escape_conditions(char, verbose=True)
                if not escaped:
                    continue
                effects = check_condition_effects(char)
                if effects['is_incapacitated']:
                    continue

            # Tenter de se libérer des autres conditions
            if effects['conditions_list']:
                attempt_escape_conditions(char, verbose=True)
                effects = check_condition_effects(char)

            # Lancer un sort de défense si en danger
            hp_percent = (char.hit_points / char.max_hit_points) * 100
            if hp_percent < 50 and not effects['has_disadvantage']:
                try_cast_defensive_spell(char, verbose=True)

            # Action de combat normale
            if effects['has_disadvantage']:
                print(f"   ⚠️  Désavantage aux attaques")

            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party_sorted
            )

        # Phase des monstres
        print(f"\n👹 PHASE DES MONSTRES")
        print("-" * 80)

        for monster in alive_monsters[:]:
            if not alive_chars:
                break
            if monster.hit_points <= 0:
                if monster in alive_monsters:
                    alive_monsters.remove(monster)
                continue

            print(f"\n🐉 Tour de {monster.name}")

            # Cibler les personnages vulnérables
            targets_with_advantage = [
                c for c in alive_chars
                if check_condition_effects(c)['attacks_have_advantage']
            ]

            if targets_with_advantage:
                print(f"   🎯 Cibles vulnérables: {', '.join([c.name for c in targets_with_advantage])}")

            combat.monster_turn(
                monster=monster,
                alive_monsters=alive_monsters,
                alive_chars=alive_chars,
                party=party_sorted,
                round_num=round_num
            )

        round_num += 1

        # Pause entre rounds
        if round_num <= max_rounds and alive_chars and alive_monsters:
            input(f"\n⏸️  Appuyez sur ENTRÉE pour Round {round_num}...")

    # =============================================================================
    # RÉSULTATS
    # =============================================================================
    print(f"\n{'='*80}")
    print("📊 RÉSULTATS DU COMBAT")
    print(f"{'='*80}")

    if alive_chars:
        print(f"\n✅ VICTOIRE!")
        print(f"\n   Survivants ({len(alive_chars)}/{len(party_sorted)}):")
        for char in party_sorted:
            if char.hit_points > 0:
                hp_percent = (char.hit_points / char.max_hit_points) * 100
                status = "❤️" if hp_percent > 50 else "💔"
                cond_str = display_conditions(char)
                print(f"     {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP {cond_str}")
            else:
                print(f"     💀 {char.name}: MORT")

        print(f"\n   💰 Récompense: {get_encounter_gold(avg_party_level)} pièces d'or")
    else:
        print(f"\n❌ DÉFAITE!")

    print(f"\n📈 Statistiques:")
    print(f"   - Rounds: {round_num - 1}")
    print(f"   - Monstres vaincus: {len(monsters) - len(alive_monsters)}")

    print(f"\n{'='*80}")
    print("✅ TEST TERMINÉ")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
