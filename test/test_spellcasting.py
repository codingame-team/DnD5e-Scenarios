"""
Simple test to demonstrate character spellcasting in combat
"""
from dnd_5e_core import load_monster
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.data import load_weapon
from dnd_5e_core.combat import CombatSystem

print("="*80)
print("CHARACTER SPELLCASTING DEMONSTRATION")
print("="*80)

# Create a wizard
wizard = simple_character_generator(level=5, race_name='elf', class_name='wizard', name='Gandalf')

print(f"\n✨ Created: {wizard.name} (Level {wizard.level} {wizard.class_type.name})")
print(f"   HP: {wizard.hit_points}")
print(f"   Spellcaster: {wizard.is_spell_caster}")

if hasattr(wizard, 'sc') and wizard.sc:
    print(f"\n📖 Spells Known: {len(wizard.sc.learned_spells)}")
    print(f"   Spell Slots: {wizard.sc.spell_slots[1:6]}")
    print(f"\n   Attack Spells:")
    attack_spells = [s for s in wizard.sc.learned_spells if hasattr(s, 'damage_type') and s.damage_type]
    for spell in attack_spells[:5]:
        spell_info = f"Cantrip" if spell.level == 0 else f"Level {spell.level}"
        print(f"      - {spell.name} ({spell_info})")

# Load a monster
ogre = load_monster('ogre')
print(f"\n🎯 Target: {ogre.name}")
print(f"   HP: {ogre.hit_points}")
print(f"   AC: {ogre.armor_class}")

# Create party with wizard in BACK ROW (position 3+) for spellcasting
# Front row fighters ensure wizard is in ranged position
fighter1 = simple_character_generator(level=5, class_name='fighter', name='Fighter1')
fighter2 = simple_character_generator(level=5, class_name='fighter', name='Fighter2')
fighter3 = simple_character_generator(level=5, class_name='fighter', name='Fighter3')

# Équiper les guerriers avec des armes et armures
from dnd_5e_core.data import load_weapon, load_armor

print(f"\n⚔️ Équipement des guerriers...")

# Armes pour les guerriers
longsword = load_weapon("longsword")
battleaxe = load_weapon("battleaxe")
greatsword = load_weapon("greatsword")

# Armures pour les guerriers (vérifier qu'elles existent)
chain_mail = load_armor("chain-mail")
scale_mail = load_armor("scale-mail")
ring_mail = load_armor("ring-mail")  # Armure plus courante

# Équiper Fighter1 avec longsword et chain mail
if fighter1.inventory and longsword:
    for i, item in enumerate(fighter1.inventory):
        if item is None:
            fighter1.inventory[i] = longsword
            break
    fighter1.equip(longsword)

if fighter1.inventory and chain_mail:
    for i, item in enumerate(fighter1.inventory):
        if item is None:
            fighter1.inventory[i] = chain_mail
            break
    fighter1.equip(chain_mail)
    print(f"   {fighter1.name}: {longsword.name} + {chain_mail.name} (AC {chain_mail.armor_class['base']})")
else:
    print(f"   {fighter1.name}: Équipement partiel")

# Équiper Fighter2 avec battleaxe et scale mail
if fighter2.inventory and battleaxe:
    for i, item in enumerate(fighter2.inventory):
        if item is None:
            fighter2.inventory[i] = battleaxe
            break
    fighter2.equip(battleaxe)

if fighter2.inventory and scale_mail:
    for i, item in enumerate(fighter2.inventory):
        if item is None:
            fighter2.inventory[i] = scale_mail
            break
    fighter2.equip(scale_mail)
    print(f"   {fighter2.name}: {battleaxe.name} + {scale_mail.name} (AC {scale_mail.armor_class['base']})")
else:
    print(f"   {fighter2.name}: Équipement partiel")

# Équiper Fighter3 avec greatsword et ring mail
if fighter3.inventory and greatsword:
    for i, item in enumerate(fighter3.inventory):
        if item is None:
            fighter3.inventory[i] = greatsword
            break
    fighter3.equip(greatsword)

if fighter3.inventory and ring_mail:
    for i, item in enumerate(fighter3.inventory):
        if item is None:
            fighter3.inventory[i] = ring_mail
            break
    fighter3.equip(ring_mail)
    print(f"   {fighter3.name}: {greatsword.name} + {ring_mail.name} (AC {ring_mail.armor_class['base']})")
else:
    print(f"   {fighter3.name}: Équipement partiel")

party = [fighter1, fighter2, fighter3, wizard]  # Wizard is at position 3 (back row)

print(f"\n⚔️ Party Formation:")
print(f"   Positions 0-2 (Front/Melee): {fighter1.name}, {fighter2.name}, {fighter3.name}")
print(f"   Position 3 (Back/Ranged): {wizard.name} 🔮")
print(f"   → {wizard.name} will CAST SPELLS because they're in ranged position!")

# Start combat
combat = CombatSystem(verbose=True)
alive_chars = [c for c in party if c.hit_points > 0]
alive_monsters = [ogre]

print(f"\n" + "="*80)
print("COMBAT START")
print("="*80)

round_num = 1
max_rounds = 5

while alive_chars and alive_monsters and round_num <= max_rounds:
    print(f"\n=== Round {round_num} ===")

    # Character turns
    for char in alive_chars[:]:
        if not alive_monsters:
            break
        if char.hit_points <= 0:
            if char in alive_chars:
                alive_chars.remove(char)
            continue

        combat.character_turn(
            character=char,
            alive_chars=alive_chars,
            alive_monsters=alive_monsters,
            party=party
        )

    # Monster turn
    for monster in alive_monsters[:]:
        if not alive_chars:
            break
        if monster.hit_points <= 0:
            if monster in alive_monsters:
                alive_monsters.remove(monster)
            continue

        combat.monster_turn(
            monster=monster,
            alive_monsters=alive_monsters,
            alive_chars=alive_chars,
            party=party,
            round_num=round_num
        )

    round_num += 1

# Results
print(f"\n" + "="*80)
if alive_chars:
    print(f"✅ VICTORY!")
    print(f"\n{wizard.name}'s Status:")
    print(f"   HP: {wizard.hit_points}/{wizard.max_hit_points}")
    if hasattr(wizard, 'sc'):
        print(f"   Spell Slots Before: [4, 3, 2, 0, 0]")
        print(f"   Spell Slots After:  {wizard.sc.spell_slots[1:6]}")
        slots_used = (4 - wizard.sc.spell_slots[1]) + (3 - wizard.sc.spell_slots[2]) + (2 - wizard.sc.spell_slots[3])
        print(f"   ✨ Total Spells Cast: {slots_used}")
else:
    print(f"❌ DEFEAT!")

print("="*80)

