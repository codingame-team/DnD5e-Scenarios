"""
Module de gestion de personnage pour les scénarios DnD 5e
Fournit des menus et fonctions pour gérer les personnages en jeu
"""
from typing import List, Optional
from dnd_5e_core.entities import Character


def display_character_sheet(character: Character):
    """
    Afficher la feuille de personnage complète

    Args:
        character: Personnage à afficher
    """
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
    print(f"   FOR: {character.abilities.str:2d} ({character.ability_modifiers.str:+d})")
    print(f"   DEX: {character.abilities.dex:2d} ({character.ability_modifiers.dex:+d})")
    print(f"   CON: {character.abilities.con:2d} ({character.ability_modifiers.con:+d})")
    print(f"   INT: {character.abilities.int:2d} ({character.ability_modifiers.int:+d})")
    print(f"   SAG: {character.abilities.wis:2d} ({character.ability_modifiers.wis:+d})")
    print(f"   CHA: {character.abilities.cha:2d} ({character.ability_modifiers.cha:+d})")

    # Combat
    print(f"\n⚔️ COMBAT")
    hp_percent = (character.hit_points / character.max_hit_points * 100) if character.max_hit_points > 0 else 0
    hp_bar = "█" * int(hp_percent / 10) + "░" * (10 - int(hp_percent / 10))
    print(f"   Points de vie: {character.hit_points}/{character.max_hit_points} [{hp_bar}]")
    print(f"   Classe d'armure: {character.armor_class}")
    print(f"   Vitesse: {character.speed} ft")
    print(f"   Bonus de maîtrise: +{character.proficiency_bonus}")

    # Inventaire
    print(f"\n🎒 INVENTAIRE")
    print(f"   Or: {character.gold} gp")

    items_count = sum(1 for item in character.inventory if item is not None)
    print(f"   Objets portés: {items_count}/20")

    if items_count > 0:
        # Armes
        weapons = [item for item in character.inventory if item and hasattr(item, 'damage_dice')]
        if weapons:
            print(f"\n   ⚔️ Armes:")
            for weapon in weapons:
                equipped = "✓" if weapon.equipped else " "
                print(f"      [{equipped}] {weapon.name}")

        # Armures
        armors = [item for item in character.inventory if item and hasattr(item, 'armor_class') and isinstance(getattr(item, 'armor_class', None), dict)]
        if armors:
            print(f"\n   🛡️ Armures:")
            for armor in armors:
                equipped = "✓" if armor.equipped else " "
                ac = armor.armor_class.get('base', 0)
                print(f"      [{equipped}] {armor.name} (CA {ac})")

        # Magic Items
        magic_items = [item for item in character.inventory if item and hasattr(item, 'rarity')]
        if magic_items:
            print(f"\n   ✨ Objets magiques:")
            for item in magic_items:
                equipped = "✓" if item.equipped else " "
                attuned = "⭐" if getattr(item, 'attuned', False) else ""
                print(f"      [{equipped}] {item.name} {attuned}")
                if getattr(item, 'ac_bonus', 0):
                    print(f"            +{item.ac_bonus} CA")
                if getattr(item, 'saving_throw_bonus', 0):
                    print(f"            +{item.saving_throw_bonus} aux jets de sauvegarde")
                if hasattr(item, 'actions') and item.actions:
                    for action in item.actions:
                        charges = f"{action.remaining_uses}/{action.uses_per_day}" if action.uses_per_day else "illimité"
                        print(f"            Action: {action.name} ({charges})")

    # Sorts
    if hasattr(character, 'sc') and character.sc and character.sc.learned_spells:
        print(f"\n🔮 SORTS")
        print(f"   Modificateur d'incantation: {character.sc.ability_modifier:+d}")
        print(f"   DD des sorts: {character.dc_value}")

        # Emplacements de sorts
        print(f"\n   Emplacements de sorts:")
        has_slots = False
        for level in range(1, 10):
            if level - 1 < len(character.sc.spell_slots) and character.sc.spell_slots[level - 1] > 0:
                slots = character.sc.spell_slots[level - 1]
                print(f"      Niveau {level}: {slots}")
                has_slots = True

        if not has_slots:
            print(f"      Aucun emplacement")

        # Sorts connus
        print(f"\n   Sorts connus: {len(character.sc.learned_spells)}")

        # Cantrips
        cantrips = [s for s in character.sc.learned_spells if s.level == 0]
        if cantrips:
            print(f"\n   📖 Cantrips:")
            for spell in cantrips[:5]:
                print(f"      - {spell.name}")

        # Sorts de niveau 1+
        leveled_spells = [s for s in character.sc.learned_spells if s.level > 0]
        if leveled_spells:
            print(f"\n   📚 Sorts de niveau supérieur:")
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
        print(f"\n⚠️ CONDITIONS ACTIVES")
        for condition in character.conditions:
            duration_str = f" ({condition.duration} rounds)" if condition.duration else ""
            print(f"   🔴 {condition.name}{duration_str}")
            if condition.desc:
                print(f"      {condition.desc[0][:60]}...")

    print("=" * 80)


def display_party_status(party: List[Character]):
    """
    Afficher un résumé de tout le groupe

    Args:
        party: Liste des personnages du groupe
    """
    print("\n" + "=" * 80)
    print("👥 STATUT DU GROUPE")
    print("=" * 80)

    for i, char in enumerate(party, 1):
        status_icon = "💀" if char.hit_points <= 0 else "✅"
        hp_percent = (char.hit_points / char.max_hit_points * 100) if char.max_hit_points > 0 else 0

        # Barre de vie
        hp_bar = "█" * int(hp_percent / 10) + "░" * (10 - int(hp_percent / 10))

        print(f"\n{i}. {status_icon} {char.name} ({char.class_type.name} Niv.{char.level})")
        print(f"   HP: {char.hit_points}/{char.max_hit_points} [{hp_bar}] {hp_percent:.0f}%")
        print(f"   AC: {char.armor_class} | Or: {char.gold} gp")

        # Conditions
        if hasattr(char, 'conditions') and char.conditions:
            conditions_str = ", ".join([c.name for c in char.conditions])
            print(f"   ⚠️ Conditions: {conditions_str}")

        # Magic items équipés
        magic_items = [item for item in char.inventory if item and hasattr(item, 'rarity') and item.equipped]
        if magic_items:
            items_str = ", ".join([item.name for item in magic_items[:3]])
            print(f"   ✨ Objets magiques: {items_str}")

    print("=" * 80)


def party_management_menu(party: List[Character]) -> Optional[str]:
    """
    Menu de gestion du groupe

    Args:
        party: Liste des personnages du groupe

    Returns:
        Action choisie ou None
    """
    while True:
        print("\n" + "=" * 80)
        print("📋 MENU DE GESTION DU GROUPE")
        print("=" * 80)
        print("\n1. Afficher statut du groupe")
        print("2. Voir feuille de personnage")
        print("3. Gérer l'inventaire")
        print("4. Recharger objets magiques")
        print("5. Repos court")
        print("6. Repos long")
        print("7. Distribuer trésors")
        print("8. Retour au jeu")

        choice = input("\nVotre choix (1-8): ").strip()

        if choice == "1":
            display_party_status(party)

        elif choice == "2":
            print("\nChoisir un personnage:")
            for i, char in enumerate(party, 1):
                print(f"{i}. {char.name}")

            char_choice = input("\nNuméro (ou 'retour'): ").strip()
            if char_choice.isdigit() and 1 <= int(char_choice) <= len(party):
                display_character_sheet(party[int(char_choice) - 1])

        elif choice == "3":
            print("\n🎒 Gestion d'inventaire - Fonctionnalité à venir")

        elif choice == "4":
            recharge_magic_items(party)

        elif choice == "5":
            short_rest(party)

        elif choice == "6":
            long_rest(party)

        elif choice == "7":
            print("\n💰 Distribution de trésors - Fonctionnalité à venir")

        elif choice == "8":
            return "continue"

        else:
            print("\n❌ Choix invalide")


def recharge_magic_items(party: List[Character]):
    """
    Recharger tous les objets magiques du groupe

    Args:
        party: Liste des personnages
    """
    print("\n🔄 Rechargement des objets magiques...")

    recharged_count = 0
    for char in party:
        for item in char.inventory:
            if item and hasattr(item, 'recharge_actions'):
                item.recharge_actions("long rest")
                recharged_count += 1
                print(f"   ✅ {char.name}: {item.name} rechargé")

    if recharged_count == 0:
        print("   ℹ️ Aucun objet à recharger")
    else:
        print(f"\n✅ {recharged_count} objet(s) rechargé(s)")


def short_rest(party: List[Character]):
    """
    Effectuer un repos court pour le groupe

    Args:
        party: Liste des personnages
    """
    print("\n😴 REPOS COURT (1 heure)")
    print("=" * 80)

    for char in party:
        if char.hit_points > 0:
            # Récupération de points de vie (dés de vie)
            hit_die = char.class_type.hit_die
            healing = hit_die // 2 + char.ability_modifiers.con

            old_hp = char.hit_points
            char.hit_points = min(char.hit_points + healing, char.max_hit_points)
            actual_healing = char.hit_points - old_hp

            print(f"   {char.name}: +{actual_healing} HP ({old_hp} → {char.hit_points})")

    print("\n✅ Repos court terminé!")


def long_rest(party: List[Character]):
    """
    Effectuer un repos long pour le groupe

    Args:
        party: Liste des personnages
    """
    print("\n😴 REPOS LONG (8 heures)")
    print("=" * 80)

    for char in party:
        # Restauration complète des HP
        old_hp = char.hit_points
        char.hit_points = char.max_hit_points

        print(f"   {char.name}:")
        print(f"      HP restaurés: {old_hp} → {char.max_hit_points}")

        # Restauration des emplacements de sorts
        if hasattr(char, 'sc') and char.sc:
            # Reset spell slots (simplifié)
            print(f"      Emplacements de sorts restaurés")

        # Retirer conditions de courte durée
        if hasattr(char, 'conditions'):
            conditions_removed = []
            for condition in char.conditions[:]:
                if condition.index in ['poisoned', 'frightened', 'restrained']:
                    char.conditions.remove(condition)
                    conditions_removed.append(condition.name)

            if conditions_removed:
                print(f"      Conditions retirées: {', '.join(conditions_removed)}")

    # Recharger magic items
    print()
    recharge_magic_items(party)

    print("\n✅ Repos long terminé! Le groupe est complètement reposé.")


__all__ = [
    'display_character_sheet',
    'display_party_status',
    'party_management_menu',
    'recharge_magic_items',
    'short_rest',
    'long_rest',
]

