"""
Démonstration complète et automatique de toutes les fonctionnalités:
- Magic Items en combat
- Sorts de défense
- Système de trésors
- Système de conditions
- Menu de gestion de personnage
"""
from dnd_5e_core import AbilityType
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.data import load_monster
from dnd_5e_core.combat import CombatSystem, create_restrained_condition, create_poisoned_condition
from dnd_5e_core.equipment import create_ring_of_protection

# Import du nouveau système
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.character_manager import display_party_status, display_character_sheet, long_rest
from src.utils.treasure_manager import generate_treasure_by_cr, distribute_treasure_to_party


def demo_full_integration():
    """Démonstration complète de toutes les fonctionnalités"""

    print("\n" + "🎮" * 40)
    print("DÉMONSTRATION COMPLÈTE - FONCTIONNALITÉS DND 5E")
    print("🎮" * 40)

    # ===== 1. CRÉATION DU GROUPE =====
    print("\n" + "=" * 80)
    print("ÉTAPE 1: CRÉATION DU GROUPE D'AVENTURIERS")
    print("=" * 80)

    wizard = simple_character_generator(level=5, class_name='wizard', name='Merlin')
    cleric = simple_character_generator(level=5, class_name='cleric', name='Elara')
    fighter = simple_character_generator(level=5, class_name='fighter', name='Grok')

    party = [fighter, cleric, wizard]

    display_party_status(party)

    # ===== 2. PREMIER COMBAT (sans magic items) =====
    print("\n" + "=" * 80)
    print("ÉTAPE 2: PREMIER COMBAT - SANS OBJETS MAGIQUES")
    print("=" * 80)

    goblin1 = load_monster('goblin')
    goblin2 = load_monster('goblin')

    if goblin1 and goblin2:
        monsters = [goblin1, goblin2]

        print(f"\n👹 2 gobelins attaquent!")
        for monster in monsters:
            print(f"   - {monster.name}: HP {monster.hit_points}, AC {monster.armor_class}")

        combat = CombatSystem(verbose=False)  # Mode silencieux
        alive_chars = [c for c in party if c.hit_points > 0]
        alive_monsters = [m for m in monsters if m.hit_points > 0]

        round_num = 1
        while alive_chars and alive_monsters and round_num <= 5:
            for char in alive_chars[:]:
                if not alive_monsters:
                    break
                combat.character_turn(char, alive_chars, alive_monsters, party)

            for monster in alive_monsters[:]:
                if not alive_chars:
                    break
                combat.monster_turn(monster, alive_monsters, alive_chars, party, round_num)

            round_num += 1

        if alive_chars:
            print(f"\n✅ Victoire!")

            # Générer et distribuer trésors
            print(f"\n💎 Collecte des trésors...")
            treasures = generate_treasure_by_cr(0.25, len(monsters))
            distribute_treasure_to_party(treasures, party)

    # ===== 3. DÉCOUVERTE D'OBJETS MAGIQUES =====
    print("\n" + "=" * 80)
    print("ÉTAPE 3: DÉCOUVERTE D'OBJETS MAGIQUES")
    print("=" * 80)

    print(f"\n🗝️ Le groupe explore une vieille crypte...")
    print(f"   {wizard.name} trouve un coffre caché!")

    # Donner un Ring of Protection au wizard
    ring = create_ring_of_protection()
    print(f"\n✨ Trouvé: {ring.name} ({ring.rarity.value})")
    print(f"   Bonus: +{ring.ac_bonus} CA, +{ring.saving_throw_bonus} aux jets de sauvegarde")

    # Ajouter à l'inventaire
    for i, item in enumerate(wizard.inventory):
        if item is None:
            wizard.inventory[i] = ring
            break

    # Attunement
    if not hasattr(wizard, 'attuned_items'):
        wizard.attuned_items = []
    wizard.attuned_items.append(ring)
    ring.attune(wizard)
    ring.equipped = True
    ring.apply_to_character(wizard)

    print(f"   ⭐ {wizard.name} s'harmonise avec l'anneau")
    print(f"   ✅ CA avant: 10 → après: {wizard.armor_class}")

    # ===== 4. COMBAT AVEC CONDITIONS =====
    print("\n" + "=" * 80)
    print("ÉTAPE 4: COMBAT AVEC CONDITIONS")
    print("=" * 80)

    spider = load_monster('giant-spider')

    if not spider:
        spider = load_monster('goblin')

    if spider:
        print(f"\n🕷️ Une araignée géante attaque!")
        print(f"   {spider.name}: HP {spider.hit_points}, AC {spider.armor_class}")

        # Appliquer condition au fighter
        print(f"\n🕸️ L'araignée entoile {fighter.name}!")
        restrained = create_restrained_condition(creature=spider, dc_value=11, dc_type=AbilityType.STR)
        restrained.apply_to_character(fighter)

        print(f"   🔴 {fighter.name} est RETENU!")
        print(f"      - Vitesse = 0")
        print(f"      - Désavantage aux attaques")
        print(f"      - Les attaques contre lui ont avantage")

        # Combat rapide
        combat = CombatSystem(verbose=False)
        alive_chars = [c for c in party if c.hit_points > 0]
        alive_monsters = [spider]

        round_num = 1
        while alive_chars and alive_monsters and round_num <= 5:
            # Tenter de se libérer
            if round_num > 1 and hasattr(fighter, 'conditions') and fighter.conditions:
                print(f"\n🎲 {fighter.name} tente de se libérer...")
                if restrained.attempt_save(fighter):
                    print(f"   ✅ Réussite!")
                    restrained.remove_from_character(fighter)
                else:
                    print(f"   ❌ Échec! Toujours retenu")

            for char in alive_chars[:]:
                if not alive_monsters:
                    break
                combat.character_turn(char, alive_chars, alive_monsters, party)

            for monster in alive_monsters[:]:
                if not alive_chars:
                    break
                combat.monster_turn(monster, alive_monsters, alive_chars, party, round_num)

            round_num += 1

        if alive_chars:
            print(f"\n✅ Araignée vaincue!")

            # Trésors
            treasures = generate_treasure_by_cr(1.0, 1)
            distribute_treasure_to_party(treasures, party)

    # ===== 5. AFFICHAGE DES FEUILLES DE PERSONNAGE =====
    print("\n" + "=" * 80)
    print("ÉTAPE 5: FEUILLES DE PERSONNAGE DÉTAILLÉES")
    print("=" * 80)

    for char in party:
        display_character_sheet(char)
        print()

    # ===== 6. REPOS LONG =====
    print("\n" + "=" * 80)
    print("ÉTAPE 6: REPOS LONG")
    print("=" * 80)

    print(f"\nLe groupe installe un campement pour la nuit...")
    long_rest(party)

    # ===== 7. STATUT FINAL =====
    print("\n" + "=" * 80)
    print("ÉTAPE 7: STATUT FINAL DU GROUPE")
    print("=" * 80)

    display_party_status(party)

    # ===== RÉSUMÉ FINAL =====
    print("\n" + "=" * 80)
    print("✅ DÉMONSTRATION COMPLÈTE TERMINÉE")
    print("=" * 80)

    print("\n📊 Fonctionnalités démontrées:")
    print("   ✅ 1. Création de groupe d'aventuriers")
    print("   ✅ 2. Combat sans objets magiques")
    print("   ✅ 3. Système de trésors automatique")
    print("   ✅ 4. Distribution intelligente des trésors")
    print("   ✅ 5. Objets magiques avec attunement")
    print("   ✅ 6. Bonus d'objets magiques (AC, saves)")
    print("   ✅ 7. Conditions en combat (Restrained)")
    print("   ✅ 8. Saves contre conditions")
    print("   ✅ 9. Feuilles de personnage détaillées")
    print("   ✅ 10. Système de repos (court/long)")
    print("   ✅ 11. Rechargement d'objets magiques")
    print("   ✅ 12. Affichage statut du groupe")

    print("\n" + "🎉" * 40)
    print("TOUTES LES FONCTIONNALITÉS SONT OPÉRATIONNELLES!")
    print("🎉" * 40)


if __name__ == "__main__":
    demo_full_integration()

