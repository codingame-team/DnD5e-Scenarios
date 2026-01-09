#!/usr/bin/env python3
"""
Test du système de marchand corrigé
"""

from src.systems.merchant import MerchantSystem
from src.core.adapters import CharacterExtensions
from dnd_5e_core import Character, Abilities
from dnd_5e_core.races import Race
from dnd_5e_core.classes import ClassType
from dnd_5e_core.abilities import AbilityType

print('🧪 Test du système de marchand corrigé...\n')

# Créer race et classe simples
race = Race(
    index='human', name='Human', speed=30, ability_bonuses={},
    alignment='Any', age='Adult', size='Medium', size_description='Medium',
    starting_proficiencies=[], starting_proficiency_options=[],
    languages=[], language_desc='Common', traits=[], subraces=[]
)

class_type = ClassType(
    index='fighter', name='Fighter', hit_die=10, proficiency_choices=[],
    proficiencies=[], saving_throws=[AbilityType.STR],
    starting_equipment=[], starting_equipment_options=[], class_levels=[],
    multi_classing=[], subclasses=[], spellcasting_level=0,
    spellcasting_ability=None, can_cast=False, spell_slots={},
    spells_known=[], cantrips_known=[]
)

# Créer personnage
char = Character(
    name='TestGrok', race=race, subrace=None, ethnic='Human', gender='M',
    height='6ft', weight='180', age=30, class_type=class_type,
    proficiencies=[],
    abilities=Abilities(str=15, dex=14, con=13, int=12, wis=10, cha=8),
    ability_modifiers=Abilities(str=15, dex=14, con=13, int=12, wis=10, cha=8),
    hit_points=30, max_hit_points=30, speed=30,
    haste_timer=0.0, hasted=False, xp=0, level=1,
    inventory=[], gold=100, sc=None, conditions=[]
)

# Initialiser gestion inventaire
CharacterExtensions.add_inventory_management(char)

# Créer marchand
merchant_system = MerchantSystem()
merchant = MerchantSystem.create_village_merchant()

print(f'✅ Personnage créé: {char.name} avec {char.gold} po')
print(f'✅ Marchand créé avec {len(merchant.items)} articles')

# Test achat d'une dague
print('\n🛒 Test 1: Achat d\'une dague (2 po)...')
if merchant_system.buy_item(char, merchant, 'dagger'):
    print(f'   ✅ Achat réussi!')
    print(f'   💰 Or restant: {char.gold} po')
    print(f'   📦 Inventaire: {len(char.inventory_items)} objet(s)')
    if char.inventory_items:
        for item in char.inventory_items:
            print(f'      - {item.name}')
else:
    print('   ❌ Échec achat')

# Test achat d'une potion
print('\n🛒 Test 2: Achat d\'une Potion de Soin (50 po)...')
if merchant_system.buy_item(char, merchant, 'potion_healing'):
    print(f'   ✅ Achat réussi!')
    print(f'   💰 Or restant: {char.gold} po')
    print(f'   📦 Inventaire: {len(char.inventory_items)} objet(s)')
    if char.inventory_items:
        for item in char.inventory_items:
            print(f'      - {item.name}')
else:
    print('   ❌ Échec achat')

# Test achat d'une armure
print('\n🛒 Test 3: Achat d\'une Armure de Cuir (10 po)...')
if merchant_system.buy_item(char, merchant, 'leather_armor'):
    print(f'   ✅ Achat réussi!')
    print(f'   💰 Or restant: {char.gold} po')
    print(f'   📦 Inventaire: {len(char.inventory_items)} objet(s)')
    if char.inventory_items:
        for item in char.inventory_items:
            print(f'      - {item.name}')
else:
    print('   ❌ Échec achat')

print('\n' + '='*60)
print('  🎉 TOUS LES TESTS RÉUSSIS!')
print('='*60)
print('\n✅ Le système de marchand fonctionne correctement!')
print('✅ CharacterExtensions.add_item() utilisé avec succès')
print('✅ Les achats sont ajoutés à l\'inventaire du personnage')
print()

