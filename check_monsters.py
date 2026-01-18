#!/usr/bin/env python3
"""Script pour vérifier les monstres disponibles"""

from dnd_5e_core.entities.extended_monsters import FiveEToolsMonsterLoader

loader = FiveEToolsMonsterLoader()

# Rechercher des monstres de type feu/élémentaire
print('🔥 Monstres de type feu/élémentaire disponibles:')
fire_monsters = loader.search_monsters(name_contains='fire', use_all=True)
print(f'  - fire: {len(fire_monsters)} résultats')
for m in fire_monsters[:5]:
    print(f'    * {m.get("index", "?")} - {m.get("name", "?")} (CR {m.get("challenge_rating", "?")})')

elemental_monsters = loader.search_monsters(name_contains='elemental', use_all=True)
print(f'\n  - elemental: {len(elemental_monsters)} résultats')
for m in elemental_monsters[:5]:
    print(f'    * {m.get("index", "?")} - {m.get("name", "?")} (CR {m.get("challenge_rating", "?")})')

# Rechercher magmin (petit élémentaire de feu)
magmin_monsters = loader.search_monsters(name_contains='magmin', use_all=True)
print(f'\n  - magmin: {len(magmin_monsters)} résultats')
for m in magmin_monsters[:5]:
    print(f'    * {m.get("index", "?")} - {m.get("name", "?")} (CR {m.get("challenge_rating", "?")})')

# Rechercher armor
print('\n🛡️ Monstres type armor:')
armor_monsters = loader.search_monsters(name_contains='armor', use_all=True)
for m in armor_monsters[:3]:
    print(f'    * {m.get("index", "?")} - {m.get("name", "?")} (CR {m.get("challenge_rating", "?")})')

# Rechercher shadow
print('\n👻 Monstres type shadow:')
shadow_monsters = loader.search_monsters(name_contains='shadow', use_all=True)
for m in shadow_monsters[:3]:
    print(f'    * {m.get("index", "?")} - {m.get("name", "?")} (CR {m.get("challenge_rating", "?")})')

# Rechercher mage
print('\n🧙 Monstres type mage:')
mage_monsters = loader.search_monsters(name_contains='mage', use_all=True)
for m in mage_monsters[:3]:
    print(f'    * {m.get("index", "?")} - {m.get("name", "?")} (CR {m.get("challenge_rating", "?")})')

