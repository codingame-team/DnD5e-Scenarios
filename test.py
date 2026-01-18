from dnd_5e_core import Character, load_monster, Monster
from dnd_5e_core.abilities import Abilities
from dnd_5e_core.data import load_race, load_class
from dnd_5e_core.data.loaders import simple_character_generator

abilities = Abilities(str=10, dex=14, con=12, int=16, wis=13, cha=8)
race = load_race("elf")
char_class = load_class("wizard")

wizard = simple_character_generator(level=5, race_name='elf', class_name='wizard', name='Gandalf')

from dnd_5e_core.data import load_weapon, load_armor

# Charger depuis les données
longsword = load_weapon("longsword")
longbow = load_weapon("longbow")
dagger = load_weapon("dagger")

# Add weapon to inventory and equip it
if wizard.inventory:
    # Find first empty slot
    for i, item in enumerate(wizard.inventory):
        if item is None:
            wizard.inventory[i] = longsword
            break
wizard.equip(longsword)

# Load a more interesting monster with special attacks
# Try a dragon (has special attacks like breath weapon)
# If not available, fall back to orc
try:
    monster = load_monster('young-red-dragon')
    print(f"✨ Loaded monster: {monster.name}")
    if hasattr(monster, 'sa') and monster.sa:
        print(f"   Special Attacks: {[sa.name for sa in monster.sa]}")
    if hasattr(monster, 'is_spell_caster') and monster.is_spell_caster:
        print(f"   Spellcaster: Yes")
except:
    try:
        # Try goblin boss with special abilities
        monster = load_monster('mage')
        print(f"✨ Loaded monster: {monster.name}")
        if hasattr(monster, 'is_spell_caster') and monster.is_spell_caster:
            print(f"   Spellcaster: Yes")
            if hasattr(monster, 'sc') and hasattr(monster.sc, 'learned_spells'):
                print(f"   Spells known: {len(monster.sc.learned_spells)}")
    except:
        monster = load_monster('orc')
        print(f"✨ Loaded monster: {monster.name}")

# Show character spellcasting info
print(f"\n📖 {wizard.name}'s abilities:")
if hasattr(wizard, 'sc') and wizard.sc:
    print(f"   Spellcaster: Yes")
    if hasattr(wizard.sc, 'learned_spells'):
        print(f"   Spells known: {len(wizard.sc.learned_spells)}")
        if wizard.sc.learned_spells:
            print(f"   Sample spells:")
            for spell in wizard.sc.learned_spells[:5]:
                spell_type = "Cantrip" if spell.level == 0 else f"Level {spell.level}"
                print(f"      - {spell.name} ({spell_type})")
    if hasattr(wizard.sc, 'spell_slots'):
        print(f"   Spell slots: {wizard.sc.spell_slots[1:6]}")  # Show levels 1-5
print()

from dnd_5e_core.combat import CombatSystem

combat = CombatSystem(verbose=True)  # Enable verbose mode to see more details

# Combat simulation
# Add dummy fighters to front row so wizard is in position 3 (back row)
dummy1 = simple_character_generator(level=5, class_name='fighter', name='Guard1')
dummy2 = simple_character_generator(level=5, class_name='fighter', name='Guard2')
dummy3 = simple_character_generator(level=5, class_name='fighter', name='Guard3')

# Party formation: fighters in front, wizard in back for spellcasting
party = [dummy1, dummy2, dummy3, wizard]
print(f"⚙️ Party Formation: 3 guards in front, {wizard.name} in back (position 3) for spellcasting")

monsters = [monster]

alive_chars = [c for c in party if c.hit_points > 0]
alive_monsters = [m for m in monsters if m.hit_points > 0]

round_num = 1
max_rounds = 10

print(f"\n⚔️ Starting combat: Party (focus on {wizard.name}) vs {monster.name}")
print(f"{wizard.name}: {wizard.hit_points} HP")
print(f"{monster.name}: {monster.hit_points} HP")
if hasattr(monster, 'armor_class'):
    print(f"{monster.name} AC: {monster.armor_class}")
print()

# Combat loop
while alive_chars and alive_monsters and round_num <= max_rounds:
    print(f"=== Round {round_num} ===")

    # Character turn
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

# Determine winners
if alive_chars:
    print(f"\n✅ Victory! {wizard.name} wins!")
    print(f"   Remaining HP: {wizard.hit_points}/{wizard.max_hit_points}")
    if hasattr(wizard, 'sc') and wizard.sc and hasattr(wizard.sc, 'spell_slots'):
        remaining_slots = [s for s in wizard.sc.spell_slots[1:6] if s > 0]
        if remaining_slots:
            print(f"   Remaining spell slots: {wizard.sc.spell_slots[1:6]}")
elif alive_monsters:
    print(f"\n❌ Defeat! {monster.name} wins!")
    print(f"   Remaining HP: {monster.hit_points}/{monster.max_hit_points}")
else:
    print(f"\n🤝 Draw!")

# Show combat statistics
print(f"\n📊 Combat Statistics:")
print(f"   Rounds fought: {round_num - 1}")
print(f"   Final {wizard.name} HP: {wizard.hit_points}/{wizard.max_hit_points}")
print(f"   Final {monster.name} HP: {monster.hit_points}/{monster.max_hit_points}")

# =============================================================================
# SECOND COMBAT: Wizard vs Spellcasting Monster (Mage)
# =============================================================================
print("\n" + "="*80)
print("SECOND COMBAT: Spellcaster vs Spellcaster")
print("="*80)

# Create a fresh wizard for second combat
wizard2 = simple_character_generator(level=5, race_name='elf', class_name='wizard', name='Elminster')
if wizard2.inventory:
    for i, item in enumerate(wizard2.inventory):
        if item is None:
            wizard2.inventory[i] = dagger
            break
wizard2.equip(dagger)

# Load a spellcasting monster
try:
    mage = load_monster('mage')
    print(f"\n✨ Loaded monster: {mage.name}")
    if hasattr(mage, 'is_spell_caster') and mage.is_spell_caster:
        print(f"   Spellcaster: Yes")
        if hasattr(mage, 'sc') and hasattr(mage.sc, 'learned_spells'):
            print(f"   Spells known: {len(mage.sc.learned_spells)}")
            if mage.sc.learned_spells:
                print(f"   Sample spells:")
                for spell in mage.sc.learned_spells[:5]:
                    spell_type = "Cantrip" if spell.level == 0 else f"Level {spell.level}"
                    print(f"      - {spell.name} ({spell_type})")
except:
    print("⚠️ Could not load mage, using regular orc")
    mage = load_monster('orc')

print(f"\n📖 {wizard2.name}'s abilities:")
if hasattr(wizard2, 'sc') and wizard2.sc:
    print(f"   Spellcaster: Yes")
    if hasattr(wizard2.sc, 'learned_spells'):
        print(f"   Spells known: {len(wizard2.sc.learned_spells)}")
    if hasattr(wizard2.sc, 'spell_slots'):
        print(f"   Spell slots: {wizard2.sc.spell_slots[1:6]}")

combat2 = CombatSystem(verbose=True)

# Add front row so wizard is in back
guard1 = simple_character_generator(level=5, class_name='fighter', name='Shield1')
guard2 = simple_character_generator(level=5, class_name='fighter', name='Shield2')
guard3 = simple_character_generator(level=5, class_name='fighter', name='Shield3')

party2 = [guard1, guard2, guard3, wizard2]
print(f"⚙️ Party Formation: 3 guards in front, {wizard2.name} in back for spellcasting")

monsters2 = [mage]

alive_chars2 = [c for c in party2 if c.hit_points > 0]
alive_monsters2 = [m for m in monsters2 if m.hit_points > 0]

round_num2 = 1
max_rounds2 = 10

print(f"\n⚔️ Starting combat: Party (focus on {wizard2.name}) vs {mage.name}")
print(f"{wizard2.name}: {wizard2.hit_points} HP")
print(f"{mage.name}: {mage.hit_points} HP")
if hasattr(mage, 'armor_class'):
    print(f"{mage.name} AC: {mage.armor_class}")
print()

# Combat loop
while alive_chars2 and alive_monsters2 and round_num2 <= max_rounds2:
    print(f"=== Round {round_num2} ===")

    # Character turn
    for char in alive_chars2[:]:
        if not alive_monsters2:
            break
        if char.hit_points <= 0:
            if char in alive_chars2:
                alive_chars2.remove(char)
            continue

        combat2.character_turn(
            character=char,
            alive_chars=alive_chars2,
            alive_monsters=alive_monsters2,
            party=party2
        )

    # Monster turn
    for m in alive_monsters2[:]:
        if not alive_chars2:
            break
        if m.hit_points <= 0:
            if m in alive_monsters2:
                alive_monsters2.remove(m)
            continue

        combat2.monster_turn(
            monster=m,
            alive_monsters=alive_monsters2,
            alive_chars=alive_chars2,
            party=party2,
            round_num=round_num2
        )

    round_num2 += 1

# Determine winners
if alive_chars2:
    print(f"\n✅ Victory! {wizard2.name} wins!")
    print(f"   Remaining HP: {wizard2.hit_points}/{wizard2.max_hit_points}")
elif alive_monsters2:
    print(f"\n❌ Defeat! {mage.name} wins!")
    print(f"   Remaining HP: {mage.hit_points}/{mage.max_hit_points}")
else:
    print(f"\n🤝 Draw!")

print(f"\n📊 Combat Statistics:")
print(f"   Rounds fought: {round_num2 - 1}")
print(f"   Final {wizard2.name} HP: {wizard2.hit_points}/{wizard2.max_hit_points}")
print(f"   Final {mage.name} HP: {mage.hit_points}/{mage.max_hit_points}")

# =============================================================================
# THIRD COMBAT: More Balanced - Wizard vs Appropriate Level Monster
# =============================================================================
print("\n" + "="*80)
print("THIRD COMBAT: Balanced Encounter (Level-appropriate)")
print("="*80)

# Create a wizard for third combat
wizard3 = simple_character_generator(level=5, race_name='elf', class_name='wizard', name='Merlin')
if wizard3.inventory:
    for i, item in enumerate(wizard3.inventory):
        if item is None:
            wizard3.inventory[i] = longsword
            break
wizard3.equip(longsword)

# Load a more balanced monster (CR ~2-3)
try:
    balanced_monster = load_monster('werewolf')  # CR 3
    print(f"\n✨ Loaded monster: {balanced_monster.name}")
except:
    try:
        balanced_monster = load_monster('ogre')  # CR 2
        print(f"\n✨ Loaded monster: {balanced_monster.name}")
    except:
        balanced_monster = load_monster('orc')  # CR 1/2
        print(f"\n✨ Loaded monster: {balanced_monster.name}")

if hasattr(balanced_monster, 'sa') and balanced_monster.sa:
    print(f"   Special Attacks: {[sa.name for sa in balanced_monster.sa]}")
if hasattr(balanced_monster, 'is_spell_caster') and balanced_monster.is_spell_caster:
    print(f"   Spellcaster: Yes")

print(f"\n📖 {wizard3.name}'s combat info:")
print(f"   HP: {wizard3.hit_points}/{wizard3.max_hit_points}")
print(f"   AC: {wizard3.armor_class}")
if hasattr(wizard3, 'sc') and wizard3.sc:
    if hasattr(wizard3.sc, 'learned_spells'):
        attack_spells = [s for s in wizard3.sc.learned_spells if hasattr(s, 'damage_type') and s.damage_type]
        print(f"   Attack spells available: {len(attack_spells)}")
        if attack_spells:
            print(f"   Top 3 attack spells:")
            for spell in sorted(attack_spells, key=lambda s: s.level, reverse=True)[:3]:
                spell_type = "Cantrip" if spell.level == 0 else f"Level {spell.level}"
                print(f"      - {spell.name} ({spell_type})")

combat3 = CombatSystem(verbose=True)

# Create a proper party formation:
# Front row (positions 0-2): Melee fighters
# Back row (positions 3+): Ranged/Spellcasters
fighter1 = simple_character_generator(level=5, class_name='fighter', name='Conan')
fighter2 = simple_character_generator(level=5, class_name='fighter', name='Aragorn')
cleric = simple_character_generator(level=5, class_name='cleric', name='Friar')

# Équiper les guerriers avec des armes et armures
print(f"\n⚔️ Équipement des combattants...")

# Charger les armes
longsword_f1 = load_weapon("longsword")
battleaxe_f2 = load_weapon("battleaxe")
mace_c = load_weapon("mace")

# Charger les armures
chain_mail_f1 = load_armor("chain-mail")
scale_mail_f2 = load_armor("scale-mail")
chain_mail_c = load_armor("chain-mail")

# Équiper Fighter1
if fighter1.inventory and longsword_f1:
    for i, item in enumerate(fighter1.inventory):
        if item is None:
            fighter1.inventory[i] = longsword_f1
            break
    fighter1.equip(longsword_f1)
if fighter1.inventory and chain_mail_f1:
    for i, item in enumerate(fighter1.inventory):
        if item is None:
            fighter1.inventory[i] = chain_mail_f1
            break
    fighter1.equip(chain_mail_f1)
    print(f"   {fighter1.name}: {longsword_f1.name} + {chain_mail_f1.name} (AC {chain_mail_f1.armor_class['base']})")

# Équiper Fighter2
if fighter2.inventory and battleaxe_f2:
    for i, item in enumerate(fighter2.inventory):
        if item is None:
            fighter2.inventory[i] = battleaxe_f2
            break
    fighter2.equip(battleaxe_f2)
if fighter2.inventory and scale_mail_f2:
    for i, item in enumerate(fighter2.inventory):
        if item is None:
            fighter2.inventory[i] = scale_mail_f2
            break
    fighter2.equip(scale_mail_f2)
    print(f"   {fighter2.name}: {battleaxe_f2.name} + {scale_mail_f2.name} (AC {scale_mail_f2.armor_class['base']})")

# Équiper Cleric
if cleric.inventory and mace_c:
    for i, item in enumerate(cleric.inventory):
        if item is None:
            cleric.inventory[i] = mace_c
            break
    cleric.equip(mace_c)
if cleric.inventory and chain_mail_c:
    for i, item in enumerate(cleric.inventory):
        if item is None:
            cleric.inventory[i] = chain_mail_c
            break
    cleric.equip(chain_mail_c)
    print(f"   {cleric.name}: {mace_c.name} + {chain_mail_c.name} (AC {chain_mail_c.armor_class['base']})")

# Party formation: fighters in front (0-2), wizard in back (3) for spellcasting
party3 = [fighter1, fighter2, cleric, wizard3]
print(f"\n⚙️ Party Formation:")
print(f"   Front Row (Melee): {fighter1.name}, {fighter2.name}, {cleric.name}")
print(f"   Back Row (Ranged/Spells): {wizard3.name} 🔮")
print(f"   → {wizard3.name} is in position 3, will use SPELLS!")

monsters3 = [balanced_monster]

alive_chars3 = [c for c in party3 if c.hit_points > 0]
alive_monsters3 = [m for m in monsters3 if m.hit_points > 0]

round_num3 = 1
max_rounds3 = 10

print(f"\n⚔️ Starting combat: Party vs {balanced_monster.name}")
print(f"\n📊 Party Status:")
for i, char in enumerate(party3):
    position = "Front" if i < 3 else "Back"
    print(f"   [{position}] {char.name}: {char.hit_points} HP (AC {char.armor_class})")
print(f"\n👹 {balanced_monster.name}: {balanced_monster.hit_points} HP (AC {balanced_monster.armor_class})")
print()

# Combat loop with more detailed tracking
spell_casts = 0
melee_attacks = 0
special_attacks_used = 0

while alive_chars3 and alive_monsters3 and round_num3 <= max_rounds3:
    print(f"=== Round {round_num3} ===")

    # Track spell slots before
    slots_before = wizard3.sc.spell_slots.copy() if hasattr(wizard3, 'sc') and wizard3.sc else None

    # Character turn
    for char in alive_chars3[:]:
        if not alive_monsters3:
            break
        if char.hit_points <= 0:
            if char in alive_chars3:
                alive_chars3.remove(char)
            continue

        combat3.character_turn(
            character=char,
            alive_chars=alive_chars3,
            alive_monsters=alive_monsters3,
            party=party3
        )

    # Track if spell was cast
    if slots_before:
        slots_after = wizard3.sc.spell_slots
        if slots_before != slots_after:
            spell_casts += 1
            print(f"   💫 {wizard3.name} used a spell slot!")

    # Monster turn
    for m in alive_monsters3[:]:
        if not alive_chars3:
            break
        if m.hit_points <= 0:
            if m in alive_monsters3:
                alive_monsters3.remove(m)
            continue

        combat3.monster_turn(
            monster=m,
            alive_monsters=alive_monsters3,
            alive_chars=alive_chars3,
            party=party3,
            round_num=round_num3
        )

    round_num3 += 1

# Determine winners
print("\n" + "="*80)
if alive_chars3:
    print(f"✅ VICTORY! The party wins!")
    print(f"\n📊 Party Status:")
    for char in party3:
        status = "💀 DEAD" if char.hit_points <= 0 else f"❤️ {char.hit_points}/{char.max_hit_points} HP"
        print(f"   {char.name}: {status}")

    # Show wizard's spell usage
    if hasattr(wizard3, 'sc') and wizard3.sc:
        print(f"\n🔮 {wizard3.name}'s Spell Slots:")
        print(f"   Before: [4, 3, 2, 0, 0]")
        print(f"   After:  {wizard3.sc.spell_slots[1:6]}")
        slots_used = sum([4-wizard3.sc.spell_slots[1], 3-wizard3.sc.spell_slots[2], 2-wizard3.sc.spell_slots[3]])
        print(f"   Spells Cast: {slots_used}")
elif alive_monsters3:
    print(f"❌ DEFEAT! {balanced_monster.name} wins!")
    print(f"   Remaining HP: {balanced_monster.hit_points}/{balanced_monster.max_hit_points}")
else:
    print(f"🤝 DRAW!")

print(f"\n📊 Detailed Combat Statistics:")
print(f"   Total rounds: {round_num3 - 1}")
print(f"   Spell casts tracked: {spell_casts}")
print(f"   Party survivors: {len([c for c in party3 if c.hit_points > 0])}/{len(party3)}")
print(f"   {balanced_monster.name}: {balanced_monster.hit_points}/{balanced_monster.max_hit_points} HP remaining")

