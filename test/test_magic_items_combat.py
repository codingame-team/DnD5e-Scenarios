"""
Test d'intégration complète:
- Magic Items en combat
- Sorts de défense
- Système de trésors
- Menu de gestion de personnage
"""
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.data import load_monster, load_weapon, load_armor
from dnd_5e_core.equipment import (
    create_ring_of_protection,
    create_wand_of_magic_missiles,
    create_staff_of_healing,
    create_cloak_of_protection
)
from dnd_5e_core.combat import CombatSystem


def display_character_sheet(character):
    """Afficher la feuille de personnage complète"""
    print("\n" + "=" * 80)
    print(f"📜 FEUILLE DE PERSONNAGE - {character.name}")
    print("=" * 80)

    # Informations de base
    print(f"\n🎭 IDENTITÉ")
    print(f"   Nom: {character.name}")
    print(f"   Race: {character.race.name}")
    print(f"   Classe: {character.class_type.name}")
    print(f"   Niveau: {character.level}")
    print(f"   XP: {character.xp}")

    # Caractéristiques
    print(f"\n💪 CARACTÉRISTIQUES")
    print(f"   FOR: {character.abilities.str} ({character.ability_modifiers.str:+d})")
    print(f"   DEX: {character.abilities.dex} ({character.ability_modifiers.dex:+d})")
    print(f"   CON: {character.abilities.con} ({character.ability_modifiers.con:+d})")
    print(f"   INT: {character.abilities.int} ({character.ability_modifiers.int:+d})")
    print(f"   SAG: {character.abilities.wis} ({character.ability_modifiers.wis:+d})")
    print(f"   CHA: {character.abilities.cha} ({character.ability_modifiers.cha:+d})")

    # Combat
    print(f"\n⚔️ COMBAT")
    print(f"   Points de vie: {character.hit_points}/{character.max_hit_points}")
    print(f"   Classe d'armure: {character.armor_class}")
    print(f"   Vitesse: {character.speed} ft")
    print(f"   Bonus de maîtrise: +{character.proficiency_bonus}")

    # Inventaire
    print(f"\n🎒 INVENTAIRE")
    print(f"   Or: {character.gold} gp")

    items_count = sum(1 for item in character.inventory if item is not None)
    print(f"   Objets: {items_count}/20")

    if items_count > 0:
        # Armes
        weapons = [item for item in character.inventory if item and hasattr(item, 'damage_dice')]
        if weapons:
            print(f"\n   Armes:")
            for weapon in weapons:
                equipped = "✓" if weapon.equipped else " "
                print(f"      [{equipped}] {weapon.name}")

        # Armures
        armors = [item for item in character.inventory if item and hasattr(item, 'armor_class') and 'base' in getattr(item, 'armor_class', {})]
        if armors:
            print(f"\n   Armures:")
            for armor in armors:
                equipped = "✓" if armor.equipped else " "
                ac = armor.armor_class.get('base', 0)
                print(f"      [{equipped}] {armor.name} (AC {ac})")

        # Magic Items
        magic_items = [item for item in character.inventory if item and hasattr(item, 'rarity')]
        if magic_items:
            print(f"\n   Objets magiques:")
            for item in magic_items:
                equipped = "✓" if item.equipped else " "
                attuned = "⭐" if getattr(item, 'attuned', False) else ""
                print(f"      [{equipped}] {item.name} {attuned}")
                if item.ac_bonus:
                    print(f"            +{item.ac_bonus} CA")
                if item.saving_throw_bonus:
                    print(f"            +{item.saving_throw_bonus} aux jets de sauvegarde")

    # Sorts
    if hasattr(character, 'sc') and character.sc:
        print(f"\n🔮 SORTS")
        print(f"   Modificateur d'incantation: {character.sc.ability_modifier:+d}")
        print(f"   DD des sorts: {character.dc_value}")

        # Emplacements de sorts
        print(f"\n   Emplacements de sorts:")
        for level in range(1, 10):
            if level - 1 < len(character.sc.spell_slots) and character.sc.spell_slots[level - 1] > 0:
                slots = character.sc.spell_slots[level - 1]
                print(f"      Niveau {level}: {slots}")

        # Sorts connus
        print(f"\n   Sorts connus: {len(character.sc.learned_spells)}")

        # Cantrips
        cantrips = [s for s in character.sc.learned_spells if s.level == 0]
        if cantrips:
            print(f"\n   Cantrips:")
            for spell in cantrips[:5]:
                print(f"      - {spell.name}")

        # Sorts de niveau 1+
        leveled_spells = [s for s in character.sc.learned_spells if s.level > 0]
        if leveled_spells:
            print(f"\n   Sorts de niveau supérieur:")
            for spell in leveled_spells[:10]:
                spell_type = ""
                if hasattr(spell, 'is_defensive') and spell.is_defensive:
                    spell_type = " 🛡️"
                elif hasattr(spell, 'damage_type') and spell.damage_type:
                    spell_type = " ⚔️"
                elif hasattr(spell, 'heal_at_slot_level') and spell.heal_at_slot_level:
                    spell_type = " 💚"
                print(f"      - {spell.name} (Niv. {spell.level}){spell_type}")

    # Conditions
    if hasattr(character, 'conditions') and character.conditions:
        print(f"\n⚠️ CONDITIONS")
        for condition in character.conditions:
            print(f"   - {condition.index}")

    print("=" * 80)


def demonstrate_magic_items_in_combat():
    """Démonstration complète: Magic Items + Defensive Spells + Treasure System"""

    print("\n" + "🎲" * 40)
    print("TEST D'INTÉGRATION: MAGIC ITEMS & DEFENSIVE SPELLS")
    print("🎲" * 40)

    # Créer un groupe d'aventuriers
    print("\n📖 CRÉATION DU GROUPE D'AVENTURIERS")
    print("=" * 80)

    wizard = simple_character_generator(level=5, class_name='wizard', name='Merlin')
    cleric = simple_character_generator(level=5, class_name='cleric', name='Elara')
    fighter = simple_character_generator(level=5, class_name='fighter', name='Grok')

    party = [fighter, cleric, wizard]

    print(f"\n✨ Groupe créé:")
    for char in party:
        print(f"   - {char.name} ({char.class_type.name} niveau {char.level})")

    # Équiper le groupe avec des armes et armures normales
    print(f"\n⚔️ ÉQUIPEMENT DE BASE")
    print("=" * 80)

    # Guerrier
    longsword = load_weapon("longsword")
    chain_mail = load_armor("chain-mail")

    if longsword and chain_mail:
        for i, item in enumerate(fighter.inventory):
            if item is None:
                fighter.inventory[i] = longsword
                break
        fighter.equip(longsword)

        for i, item in enumerate(fighter.inventory):
            if item is None:
                fighter.inventory[i] = chain_mail
                break
        fighter.equip(chain_mail)

        print(f"   {fighter.name}: {longsword.name} + {chain_mail.name}")

    # Clerc
    mace = load_weapon("mace")
    scale_mail = load_armor("scale-mail")

    if mace and scale_mail:
        for i, item in enumerate(cleric.inventory):
            if item is None:
                cleric.inventory[i] = mace
                break
        cleric.equip(mace)

        for i, item in enumerate(cleric.inventory):
            if item is None:
                cleric.inventory[i] = scale_mail
                break
        cleric.equip(scale_mail)

        print(f"   {cleric.name}: {mace.name} + {scale_mail.name}")

    # Ajouter des TRÉSORS MAGIQUES au groupe
    print(f"\n💎 TRÉSORS DÉCOUVERTS")
    print("=" * 80)

    # Ring of Protection pour le wizard
    ring = create_ring_of_protection()
    print(f"\n   {wizard.name} trouve: {ring.name} ({ring.rarity.value})")
    print(f"      Bonus: +{ring.ac_bonus} CA, +{ring.saving_throw_bonus} jets de sauvegarde")

    # Ajouter à l'inventaire
    for i, item in enumerate(wizard.inventory):
        if item is None:
            wizard.inventory[i] = ring
            break

    # Attunement et équipement
    if ring.requires_attunement:
        if not hasattr(wizard, 'attuned_items'):
            wizard.attuned_items = []
        wizard.attuned_items.append(ring)
        ring.attune(wizard)
        print(f"      ⭐ {wizard.name} s'harmonise avec l'anneau")

    ring.equipped = True
    ring.apply_to_character(wizard)
    print(f"      ✅ Anneau équipé! CA: {wizard.armor_class}")

    # Staff of Healing pour le clerc
    staff = create_staff_of_healing()
    print(f"\n   {cleric.name} trouve: {staff.name} ({staff.rarity.value})")
    print(f"      {staff.actions[0].uses_per_day} charges de soin par jour")

    for i, item in enumerate(cleric.inventory):
        if item is None:
            cleric.inventory[i] = staff
            break

    if staff.requires_attunement:
        if not hasattr(cleric, 'attuned_items'):
            cleric.attuned_items = []
        cleric.attuned_items.append(staff)
        staff.attune(cleric)
        print(f"      ⭐ {cleric.name} s'harmonise avec le bâton")

    staff.equipped = True

    # Cloak of Protection pour le fighter
    cloak = create_cloak_of_protection()
    print(f"\n   {fighter.name} trouve: {cloak.name} ({cloak.rarity.value})")
    print(f"      Bonus: +{cloak.ac_bonus} CA, +{cloak.saving_throw_bonus} jets de sauvegarde")

    for i, item in enumerate(fighter.inventory):
        if item is None:
            fighter.inventory[i] = cloak
            break

    if cloak.requires_attunement:
        if not hasattr(fighter, 'attuned_items'):
            fighter.attuned_items = []
        fighter.attuned_items.append(cloak)
        cloak.attune(fighter)
        print(f"      ⭐ {fighter.name} s'harmonise avec la cape")

    cloak.equipped = True
    cloak.apply_to_character(fighter)
    print(f"      ✅ Cape équipée! CA: {fighter.armor_class}")

    # Afficher les feuilles de personnage
    print(f"\n📜 FEUILLES DE PERSONNAGE")
    print("=" * 80)

    for char in party:
        display_character_sheet(char)
        input("\n[Appuyez sur ENTRÉE pour continuer]")

    # Combat contre des gobelins
    print(f"\n⚔️ COMBAT: EMBUSCADE DE GOBELINS!")
    print("=" * 80)

    goblin1 = load_monster('goblin')
    goblin2 = load_monster('goblin')
    goblin3 = load_monster('goblin')

    monsters = [m for m in [goblin1, goblin2, goblin3] if m]

    print(f"\n👹 {len(monsters)} gobelins attaquent!")
    for i, monster in enumerate(monsters, 1):
        print(f"   Goblin {i}: HP {monster.hit_points}, AC {monster.armor_class}")

    # Combat
    combat = CombatSystem(verbose=True)
    alive_chars = [c for c in party if c.hit_points > 0]
    alive_monsters = [m for m in monsters if m.hit_points > 0]

    round_num = 1
    max_rounds = 10

    print(f"\n🎲 Début du combat!")

    while alive_chars and alive_monsters and round_num <= max_rounds:
        print(f"\n" + "=" * 80)
        print(f"ROUND {round_num}")
        print("=" * 80)

        # Tours des personnages
        for char in alive_chars[:]:
            if not alive_monsters:
                break
            if char.hit_points <= 0:
                if char in alive_chars:
                    alive_chars.remove(char)
                continue

            print(f"\n🎯 Tour de {char.name}")

            combat.character_turn(
                character=char,
                alive_chars=alive_chars,
                alive_monsters=alive_monsters,
                party=party
            )

        # Tours des monstres
        for monster in alive_monsters[:]:
            if not alive_chars:
                break
            if monster.hit_points <= 0:
                if monster in alive_monsters:
                    alive_monsters.remove(monster)
                continue

            print(f"\n👹 Tour de {monster.name}")

            combat.monster_turn(
                monster=monster,
                alive_monsters=alive_monsters,
                alive_chars=alive_chars,
                party=party,
                round_num=round_num
            )

        round_num += 1

    # Résultats
    print(f"\n" + "=" * 80)
    if alive_chars:
        print(f"✅ VICTOIRE!")
        print(f"\nÉtat du groupe:")
        for char in party:
            status = "💀" if char.hit_points <= 0 else "✅"
            print(f"   {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP")

        # Récompenses
        print(f"\n💰 RÉCOMPENSES")
        print(f"   Or trouvé: {len(alive_monsters) * 10} gp")
        print(f"   XP gagnée: {len(alive_monsters) * 50} XP")

        for char in alive_chars:
            char.gold += (len(monsters) * 10) // len(alive_chars)
            char.xp += (len(monsters) * 50) // len(alive_chars)
    else:
        print(f"❌ DÉFAITE!")

    print("=" * 80)

    # Menu final
    print(f"\n📋 MENU DE GESTION")
    print("=" * 80)
    print(f"1. Afficher les feuilles de personnage")
    print(f"2. Réorganiser l'inventaire")
    print(f"3. Recharger les objets magiques")
    print(f"4. Repos long (récupération)")
    print(f"5. Quitter")

    choice = input("\nVotre choix: ")

    if choice == "1":
        for char in party:
            display_character_sheet(char)
    elif choice == "3":
        print(f"\n🔄 Rechargement des objets magiques...")
        for char in party:
            for item in char.inventory:
                if item and hasattr(item, 'recharge_actions'):
                    item.recharge_actions("long rest")
                    print(f"   {char.name}: {item.name} rechargé")


if __name__ == "__main__":
    demonstrate_magic_items_in_combat()

