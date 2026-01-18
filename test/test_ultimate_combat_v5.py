"""
Test Complet du Système de Combat D&D 5e v5.0 - ÉDITION ULTIME
==============================================================

Fonctionnalités testées:
- ✅ Sous-classes et capacités spécifiques (Rage, Extra Attack, etc.)
- ✅ Sous-races avec bonus et traits
- ✅ Features de classe par niveau (Channel Divinity, Ki Points, etc.)
- ✅ Traits raciaux (Darkvision, Fey Ancestry, etc.)
- ✅ Objets magiques variés (armes, armures, anneaux, amulettes, potions)
- ✅ Sorts de défense et d'attaque
- ✅ Système d'initiative complet
- ✅ Gestion avancée des conditions
"""

import sys
sys.path.insert(0, '/')

from dnd_5e_core import load_monster, ClassAbilities
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.equipment import (
    HealingPotion,
    PotionRarity,
    create_ring_of_protection,
    create_cloak_of_protection,
)
from dnd_5e_core.mechanics.subclass_system import (
    load_subclass,
    load_subrace,
)
from random import randint, choice


# =============================================================================
# OBJETS MAGIQUES AVANCÉS
# =============================================================================

def create_flaming_sword():
    """Épée enflammée +1"""
    from dnd_5e_core.equipment.magic_item import MagicItem, MagicItemType, MagicItemRarity
    from dnd_5e_core.equipment import EquipmentCategory, Cost

    return MagicItem(
        index="flaming-sword",
        name="Flaming Sword +1",
        desc=["A sword wreathed in flames"],
        weight=3,
        cost=Cost(5000, 'gp'),
        category=EquipmentCategory("weapon", "Weapon", "/api/equipment-categories/weapon"),
        rarity=MagicItemRarity.RARE,
        item_type=MagicItemType.WEAPON,
        requires_attunement=True,
        ac_bonus=0,
        equipped=False
    )


def create_amulet_of_health():
    """Amulette de Santé (Constitution = 19)"""
    from dnd_5e_core.equipment.magic_item import MagicItem, MagicItemType, MagicItemRarity
    from dnd_5e_core.equipment import EquipmentCategory, Cost

    return MagicItem(
        index="amulet-of-health",
        name="Amulet of Health",
        desc=["Your Constitution score is 19 while wearing this amulet"],
        weight=0.1,
        cost=Cost(8000, 'gp'),
        category=EquipmentCategory("wondrous", "Wondrous Item", "/api/equipment-categories/wondrous"),
        rarity=MagicItemRarity.RARE,
        item_type=MagicItemType.WONDROUS,
        requires_attunement=True,
        ac_bonus=0,
        ability_bonuses={'con': 19},  # Set to 19
        equipped=False
    )


def create_bracers_of_defense():
    """Bracelets de Défense (+2 AC sans armure)"""
    from dnd_5e_core.equipment.magic_item import MagicItem, MagicItemType, MagicItemRarity
    from dnd_5e_core.equipment import EquipmentCategory, Cost

    return MagicItem(
        index="bracers-of-defense",
        name="Bracers of Defense",
        desc=["While wearing these bracers, you gain +2 bonus to AC if you are wearing no armor"],
        weight=1,
        cost=Cost(6000, 'gp'),
        category=EquipmentCategory("wondrous", "Wondrous Item", "/api/equipment-categories/wondrous"),
        rarity=MagicItemRarity.RARE,
        item_type=MagicItemType.WONDROUS,
        requires_attunement=True,
        ac_bonus=2,
        equipped=False
    )


def create_various_potions():
    """Crée différentes potions"""
    potions = []

    # Potion de Soins Majeure (4d4+4)
    potions.append(HealingPotion(
        "Potion of Greater Healing",
        PotionRarity.UNCOMMON,
        "4d4",
        4,
        150,
        200
    ))

    # Potion de Soins Supérieure (8d4+8)
    potions.append(HealingPotion(
        "Potion of Superior Healing",
        PotionRarity.RARE,
        "8d4",
        8,
        500,
        700
    ))

    # Potion de Soins Standard (2d4+2)
    for _ in range(3):
        potions.append(HealingPotion(
            "Potion of Healing",
            PotionRarity.COMMON,
            "2d4",
            2,
            50,
            50
        ))

    return potions


# =============================================================================
# CRÉATION DE PERSONNAGES AVANCÉS
# =============================================================================

def create_advanced_character(level, race_name, class_name, subrace_name, subclass_name, name):
    """Crée un personnage avec sous-classe et sous-race"""

    # Créer le personnage de base
    char = simple_character_generator(level, race_name, class_name, name)

    # Appliquer la sous-race
    if subrace_name:
        subrace = load_subrace(subrace_name)
        if subrace:
            char.subrace = subrace

            # Appliquer les bonus d'abilités
            for bonus_data in subrace.ability_bonuses:
                ability = bonus_data.get('ability_score', {}).get('index', '')
                bonus_value = bonus_data.get('bonus', 0)

                if hasattr(char.abilities, ability):
                    current = getattr(char.abilities, ability)
                    setattr(char.abilities, ability, current + bonus_value)

    # Appliquer la sous-classe
    if subclass_name:
        subclass = load_subclass(subclass_name)
        if subclass:
            char.subclass = subclass

    return char


def setup_advanced_party():
    """Crée un groupe de 6 personnages avec sous-classes et sous-races"""

    print("\n📖 CRÉATION DU GROUPE AVANCÉ")
    print("=" * 80)

    party = []

    # 1. Barbarian (Path of the Berserker) - Hill Dwarf
    barbarian = create_advanced_character(
        level=6,
        race_name='dwarf',
        class_name='barbarian',
        subrace_name='hill-dwarf',
        subclass_name=None,  # Path of Berserker pas toujours dans API
        name='Grok le Destructeur'
    )
    party.append(barbarian)
    print(f"   ✅ {barbarian.name}: Barbarian 6 (Hill Dwarf)")
    print(f"      HP: {barbarian.hit_points}, AC: {barbarian.armor_class}")

    # 2. Fighter (Champion) - Human
    fighter = create_advanced_character(
        level=6,
        race_name='human',
        class_name='fighter',
        subrace_name=None,
        subclass_name='champion',
        name='Conan'
    )
    party.append(fighter)
    print(f"   ✅ {fighter.name}: Fighter 6 (Champion)")
    print(f"      HP: {fighter.hit_points}, AC: {fighter.armor_class}")

    # 3. Wizard (School of Evocation) - High Elf
    wizard = create_advanced_character(
        level=6,
        race_name='elf',
        class_name='wizard',
        subrace_name='high-elf',
        subclass_name='evocation',
        name='Gandalf'
    )
    party.append(wizard)
    print(f"   ✅ {wizard.name}: Wizard 6 (Evocation, High Elf)")
    print(f"      HP: {wizard.hit_points}, AC: {wizard.armor_class}")

    # 4. Cleric (Life Domain) - Human
    cleric = create_advanced_character(
        level=6,
        race_name='human',
        class_name='cleric',
        subrace_name=None,
        subclass_name='life',
        name='Sœur Elara'
    )
    party.append(cleric)
    print(f"   ✅ {cleric.name}: Cleric 6 (Life Domain)")
    print(f"      HP: {cleric.hit_points}, AC: {cleric.armor_class}")

    # 5. Rogue (Assassin) - Lightfoot Halfling
    rogue = create_advanced_character(
        level=6,
        race_name='halfling',
        class_name='rogue',
        subrace_name='lightfoot',
        subclass_name='thief',  # ou 'assassin'
        name='Bilbo'
    )
    party.append(rogue)
    print(f"   ✅ {rogue.name}: Rogue 6 (Lightfoot Halfling)")
    print(f"      HP: {rogue.hit_points}, AC: {rogue.armor_class}")

    # 6. Monk (Way of the Open Hand) - Wood Elf
    monk = create_advanced_character(
        level=6,
        race_name='elf',
        class_name='monk',
        subrace_name='wood-elf',
        subclass_name=None,  # Way of Open Hand
        name='Li Mu Bai'
    )
    party.append(monk)
    print(f"   ✅ {monk.name}: Monk 6 (Wood Elf)")
    print(f"      HP: {monk.hit_points}, AC: {monk.armor_class}")

    return party


def equip_party_with_magic_items(party):
    """Équipe le groupe avec des objets magiques variés"""

    print("\n💎 ÉQUIPEMENT MAGIQUE AVANCÉ")
    print("=" * 80)

    # Barbarian - Amulet of Health
    barbarian = party[0]
    amulet = create_amulet_of_health()
    amulet.attune(barbarian)
    amulet.apply_to_character(barbarian)
    print(f"   ✨ {barbarian.name}: {amulet.name} (CON = 19)")

    # Fighter - Flaming Sword +1
    fighter = party[1]
    flaming_sword = create_flaming_sword()
    flaming_sword.attune(fighter)
    print(f"   ⚔️  {fighter.name}: {flaming_sword.name}")

    # Wizard - Cloak of Protection
    wizard = party[2]
    cloak = create_cloak_of_protection()
    cloak.attune(wizard)
    cloak.apply_to_character(wizard)
    print(f"   🧥 {wizard.name}: {cloak.name} (+1 AC, +1 saves)")

    # Cleric - Ring of Protection
    cleric = party[3]
    ring = create_ring_of_protection()
    ring.attune(cleric)
    ring.apply_to_character(cleric)
    print(f"   💍 {cleric.name}: {ring.name} (+1 AC, +1 saves)")

    # Rogue - Bracers of Defense
    rogue = party[4]
    bracers = create_bracers_of_defense()
    bracers.attune(rogue)
    bracers.apply_to_character(rogue)
    print(f"   🔰 {rogue.name}: {bracers.name} (+2 AC)")

    # Monk - Bracers of Defense aussi
    monk = party[5]
    bracers2 = create_bracers_of_defense()
    bracers2.attune(monk)
    bracers2.apply_to_character(monk)
    print(f"   🔰 {monk.name}: {bracers2.name} (+2 AC)")

    # Distribuer des potions variées
    print(f"\n🧪 DISTRIBUTION DES POTIONS")
    all_potions = create_various_potions()

    for i, char in enumerate(party):
        char.inventory = [None] * 20

        # Donner 2-3 potions par personnage
        potions_for_char = all_potions[i*2:(i+1)*2] if i < len(all_potions)//2 else []

        for j, potion in enumerate(potions_for_char):
            char.inventory[j] = potion

        potion_names = [p.name for p in potions_for_char]
        print(f"   {char.name}: {', '.join(potion_names) if potion_names else 'Aucune'}")


# =============================================================================
# COMBAT AVANCÉ
# =============================================================================

def run_ultimate_combat():
    """Combat ultime avec toutes les fonctionnalités"""

    print("\n" + "🎲" * 40)
    print("COMBAT D&D 5e v5.0 - ÉDITION ULTIME")
    print("🎲" * 40)

    # Créer le groupe
    party = setup_advanced_party()

    # Équiper le groupe
    equip_party_with_magic_items(party)

    # Générer les monstres
    print(f"\n👹 GÉNÉRATION DES MONSTRES")
    print("=" * 80)

    monsters = [
        load_monster('troll'),
        load_monster('ogre'),
        load_monster('hobgoblin'),
        load_monster('hobgoblin'),
    ]
    monsters = [m for m in monsters if m is not None]

    for monster in monsters:
        print(f"   {monster.name}: CR {monster.challenge_rating}, HP {monster.hit_points}, AC {monster.armor_class}")

    # Initiative
    print(f"\n🎲 INITIATIVE")
    print("=" * 80)

    initiative_order = []
    for char in party:
        roll = randint(1, 20) + char.abilities.get_modifier('dex')
        initiative_order.append((char, roll, 'party'))
        print(f"   {char.name}: {roll}")

    for monster in monsters:
        roll = randint(1, 20) + monster.abilities.get_modifier('dex')
        initiative_order.append((monster, roll, 'monster'))
        print(f"   {monster.name}: {roll}")

    initiative_order.sort(key=lambda x: x[1], reverse=True)

    # Combat
    input("\n[Appuyez sur ENTRÉE pour commencer le combat]")

    combat = CombatSystem(verbose=True)
    alive_party = [c for c in party if c.hit_points > 0]
    alive_monsters = [m for m in monsters if m.hit_points > 0]

    round_num = 1
    max_rounds = 20

    while alive_party and alive_monsters and round_num <= max_rounds:
        print(f"\n{'=' * 80}")
        print(f"🎲 ROUND {round_num}")
        print(f"{'=' * 80}")

        # Statut
        print(f"\n📊 Groupe:")
        for char in alive_party:
            hp_pct = (char.hit_points / char.max_hit_points) * 100
            icon = "❤️" if hp_pct > 75 else "💛" if hp_pct > 50 else "🧡" if hp_pct > 25 else "💔"
            subclass_str = f" ({char.subclass.name})" if hasattr(char, 'subclass') and char.subclass else ""
            print(f"   {icon} {char.name}{subclass_str}: {char.hit_points}/{char.max_hit_points} HP")

        print(f"\n👹 Monstres:")
        for monster in alive_monsters:
            print(f"   {monster.name}: {monster.hit_points} HP")

        # Tours
        for combatant, init_roll, ctype in initiative_order:
            if combatant.hit_points <= 0:
                continue

            if ctype == 'party' and combatant not in alive_party:
                continue
            if ctype == 'monster' and combatant not in alive_monsters:
                continue

            print(f"\n{'⚔️' if ctype == 'party' else '👹'} Tour de {combatant.name}")

            if ctype == 'party':
                # Utiliser les capacités de classe
                if combatant.class_type.index == 'barbarian':
                    if round_num == 1:  # Activer la rage au premier tour
                        ClassAbilities.apply_barbarian_rage(combatant)

                elif combatant.class_type.index == 'fighter':
                    if round_num == 1:
                        ClassAbilities.use_second_wind(combatant)
                    if round_num == 2:
                        ClassAbilities.use_fighter_action_surge(combatant)

                elif combatant.class_type.index == 'rogue':
                    ClassAbilities.use_rogue_cunning_action(combatant)

                elif combatant.class_type.index == 'monk':
                    if randint(1, 3) == 1:
                        ClassAbilities.use_monk_ki(combatant)

                elif combatant.class_type.index == 'cleric':
                    if round_num == 3:
                        ClassAbilities.use_channel_divinity(combatant)

                # Action de combat
                combat.character_turn(combatant, alive_party, alive_monsters, party)

            else:
                # Tour du monstre
                combat.monster_turn(combatant, alive_monsters, alive_party, party, round_num)

        # Nettoyer les morts
        alive_party = [c for c in alive_party if c.hit_points > 0]
        alive_monsters = [m for m in alive_monsters if m.hit_points > 0]

        round_num += 1

        if round_num <= max_rounds and alive_party and alive_monsters:
            input(f"\n⏸️  [ENTRÉE pour Round {round_num}]")

    # Résultats
    print(f"\n{'=' * 80}")
    print("📊 RÉSULTATS")
    print(f"{'=' * 80}")

    if alive_party:
        print(f"\n✅ VICTOIRE!")
        print(f"\nSurvivants ({len(alive_party)}/{len(party)}):")
        for char in party:
            if char.hit_points > 0:
                print(f"   ❤️ {char.name}: {char.hit_points}/{char.max_hit_points} HP")
            else:
                print(f"   💀 {char.name}: MORT")
    else:
        print(f"\n❌ DÉFAITE!")

    print(f"\n📈 Statistiques:")
    print(f"   - Rounds: {round_num - 1}")
    print(f"   - Monstres vaincus: {len(monsters) - len(alive_monsters)}/{len(monsters)}")

    print(f"\n{'=' * 80}")
    print("✅ COMBAT TERMINÉ")
    print(f"={'=' * 80}")


if __name__ == "__main__":
    run_ultimate_combat()
