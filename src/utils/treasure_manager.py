"""
Système de gestion des trésors pour les scénarios DnD 5e
Permet de générer et distribuer des trésors au groupe
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from random import choice, randint
from dnd_5e_core.entities import Character
from dnd_5e_core.data import load_weapon, load_armor
from dnd_5e_core.equipment import (
    create_ring_of_protection,
    create_cloak_of_protection,
    create_wand_of_magic_missiles,
    create_staff_of_healing,
    create_belt_of_giant_strength,
    create_amulet_of_health,
    create_bracers_of_defense,
    create_necklace_of_fireballs,
    MagicItem
)


class TreasureType:
    """Types de trésors disponibles"""
    GOLD = "gold"
    WEAPON = "weapon"
    ARMOR = "armor"
    MAGIC_ITEM = "magic_item"
    POTION = "potion"
    GEM = "gem"


@dataclass
class Treasure:
    """Un trésor trouvé"""
    type: str  # Type de trésor (TreasureType)
    name: str
    value: int  # Valeur en pièces d'or
    item: Optional[object] = None  # L'objet lui-même (weapon, armor, magic item)
    quantity: int = 1

    def __repr__(self):
        if self.quantity > 1:
            return f"{self.quantity}x {self.name} ({self.value} gp)"
        return f"{self.name} ({self.value} gp)"


def generate_treasure_by_cr(challenge_rating: float, num_monsters: int = 1) -> List[Treasure]:
    """
    Générer des trésors en fonction du CR des monstres vaincus

    Args:
        challenge_rating: CR du monstre
        num_monsters: Nombre de monstres vaincus

    Returns:
        Liste de trésors générés
    """
    treasures = []

    # Or de base (selon CR)
    base_gold = int(10 * challenge_rating * num_monsters)
    variation = randint(-5, 15)
    gold = max(base_gold + base_gold * variation // 100, 1)

    treasures.append(Treasure(
        type=TreasureType.GOLD,
        name=f"{gold} pièces d'or",
        value=gold,
        quantity=gold
    ))

    # Chance d'objets magiques (augmente avec CR)
    magic_item_chance = min(challenge_rating * 10, 50)

    if randint(1, 100) <= magic_item_chance:
        # Générer un objet magique aléatoire
        magic_item = generate_random_magic_item(challenge_rating)
        if magic_item:
            treasures.append(magic_item)

    # Chance d'armes/armures (CR >= 1)
    if challenge_rating >= 1 and randint(1, 100) <= 30:
        equipment = generate_random_equipment()
        if equipment:
            treasures.append(equipment)

    return treasures


def generate_random_magic_item(challenge_rating: float) -> Optional[Treasure]:
    """
    Générer un objet magique aléatoire approprié au CR

    Args:
        challenge_rating: CR pour déterminer la rareté

    Returns:
        Trésor contenant l'objet magique
    """
    # Objets magiques par rareté
    common_items = []
    uncommon_items = [
        ("Ring of Protection", create_ring_of_protection, 1000),
        ("Cloak of Protection", create_cloak_of_protection, 800),
        ("Wand of Magic Missiles", create_wand_of_magic_missiles, 2000),
    ]
    rare_items = [
        ("Staff of Healing", create_staff_of_healing, 3000),
        ("Belt of Giant Strength", create_belt_of_giant_strength, 5000),
        ("Amulet of Health", create_amulet_of_health, 4000),
        ("Bracers of Defense", create_bracers_of_defense, 1500),
        ("Necklace of Fireballs", create_necklace_of_fireballs, 2000),
    ]

    # Sélection selon CR
    if challenge_rating < 2:
        # Uncommon seulement
        items_pool = uncommon_items
    elif challenge_rating < 5:
        # Uncommon + Rare
        items_pool = uncommon_items + rare_items
    else:
        # Rare seulement
        items_pool = rare_items

    if not items_pool:
        return None

    name, creator_func, value = choice(items_pool)
    item = creator_func()

    return Treasure(
        type=TreasureType.MAGIC_ITEM,
        name=name,
        value=value,
        item=item
    )


def generate_random_equipment() -> Optional[Treasure]:
    """
    Générer une arme ou armure aléatoire

    Returns:
        Trésor contenant l'équipement
    """
    # Armes communes
    weapons = [
        ("longsword", 15),
        ("shortsword", 10),
        ("battleaxe", 10),
        ("mace", 5),
        ("longbow", 50),
        ("crossbow-light", 25),
    ]

    # Armures communes
    armors = [
        ("leather-armor", 10),
        ("chain-mail", 75),
        ("scale-mail", 50),
        ("breastplate", 400),
    ]

    # Choisir aléatoirement arme ou armure
    if randint(0, 1) == 0:
        # Arme
        index, value = choice(weapons)
        item = load_weapon(index)
        if item:
            return Treasure(
                type=TreasureType.WEAPON,
                name=item.name,
                value=value,
                item=item
            )
    else:
        # Armure
        index, value = choice(armors)
        item = load_armor(index)
        if item:
            return Treasure(
                type=TreasureType.ARMOR,
                name=item.name,
                value=value,
                item=item
            )

    return None


def distribute_treasure_to_party(treasures: List[Treasure], party: List[Character]):
    """
    Distribuer les trésors au groupe

    Args:
        treasures: Liste des trésors à distribuer
        party: Groupe de personnages
    """
    print("\n" + "=" * 80)
    print("💰 DISTRIBUTION DES TRÉSORS")
    print("=" * 80)

    if not treasures:
        print("\n   Aucun trésor à distribuer")
        return

    print("\n📦 Trésors trouvés:")
    for treasure in treasures:
        print(f"   - {treasure}")

    # Or: diviser entre tous les personnages vivants
    alive_chars = [c for c in party if c.hit_points > 0]

    for treasure in treasures:
        if treasure.type == TreasureType.GOLD:
            gold_per_char = treasure.value // len(alive_chars) if alive_chars else 0

            print(f"\n💰 Or: {treasure.value} gp divisés entre {len(alive_chars)} personnages")
            for char in alive_chars:
                char.gold += gold_per_char
                print(f"   {char.name}: +{gold_per_char} gp (total: {char.gold} gp)")

        elif treasure.type == TreasureType.MAGIC_ITEM:
            # Proposer à qui donner l'objet magique
            print(f"\n✨ Objet magique: {treasure.name}")
            print(f"   À qui donner cet objet?")

            for i, char in enumerate(alive_chars, 1):
                attuned_count = len(getattr(char, 'attuned_items', []))
                print(f"   {i}. {char.name} (Objets harmonisés: {attuned_count}/3)")

            # Auto-attribuer selon la classe
            best_recipient = choose_best_recipient_for_magic_item(treasure.item, alive_chars)

            if best_recipient:
                add_item_to_inventory(best_recipient, treasure.item)
                print(f"   → Donné à {best_recipient.name}")

        elif treasure.type in [TreasureType.WEAPON, TreasureType.ARMOR]:
            # Proposer à qui donner l'équipement
            print(f"\n⚔️ Équipement: {treasure.name}")

            best_recipient = choose_best_recipient_for_equipment(treasure.item, alive_chars)

            if best_recipient:
                add_item_to_inventory(best_recipient, treasure.item)
                print(f"   → Donné à {best_recipient.name}")

    print("\n✅ Distribution terminée!")


def choose_best_recipient_for_magic_item(item: MagicItem, party: List[Character]) -> Optional[Character]:
    """
    Choisir le meilleur destinataire pour un objet magique

    Args:
        item: Objet magique
        party: Liste des personnages

    Returns:
        Meilleur destinataire
    """
    # Logique simple: selon le type d'objet
    item_name = item.name.lower()

    # Staff/Wand → Spellcaster
    if 'staff' in item_name or 'wand' in item_name:
        for char in party:
            if hasattr(char, 'is_spell_caster') and char.is_spell_caster:
                return char

    # Belt of Strength → Fighter/Barbarian
    if 'strength' in item_name or 'belt' in item_name:
        for char in party:
            if char.class_type.name.lower() in ['fighter', 'barbarian', 'paladin']:
                return char

    # Ring/Cloak of Protection → Quiconque
    # Donner au personnage avec le plus bas AC
    if 'protection' in item_name:
        return min(party, key=lambda c: c.armor_class)

    # Par défaut, premier personnage
    return party[0] if party else None


def choose_best_recipient_for_equipment(item, party: List[Character]) -> Optional[Character]:
    """
    Choisir le meilleur destinataire pour un équipement

    Args:
        item: Équipement (arme ou armure)
        party: Liste des personnages

    Returns:
        Meilleur destinataire
    """
    # Si c'est une armure, donner au personnage avec le plus bas AC
    if hasattr(item, 'armor_class'):
        return min(party, key=lambda c: c.armor_class)

    # Si c'est une arme, donner au premier guerrier
    for char in party:
        if char.class_type.name.lower() in ['fighter', 'barbarian', 'paladin', 'ranger']:
            return char

    # Par défaut, premier personnage
    return party[0] if party else None


def add_item_to_inventory(character: Character, item):
    """
    Ajouter un objet à l'inventaire d'un personnage

    Args:
        character: Personnage
        item: Objet à ajouter
    """
    # Trouver un emplacement vide
    for i, slot in enumerate(character.inventory):
        if slot is None:
            character.inventory[i] = item

            # Si c'est un objet magique, proposer d'harmoniser
            if hasattr(item, 'requires_attunement') and item.requires_attunement:
                if not hasattr(character, 'attuned_items'):
                    character.attuned_items = []

                if len(character.attuned_items) < 3:
                    character.attuned_items.append(item)
                    item.attune(character)
                    item.equipped = True

                    if hasattr(item, 'apply_to_character'):
                        item.apply_to_character(character)

                    print(f"      ⭐ Harmonisé et équipé")

            return True

    print(f"      ⚠️ Inventaire plein!")
    return False


from dataclasses import dataclass

__all__ = [
    'TreasureType',
    'Treasure',
    'generate_treasure_by_cr',
    'generate_random_magic_item',
    'generate_random_equipment',
    'distribute_treasure_to_party',
    'add_item_to_inventory',
]

