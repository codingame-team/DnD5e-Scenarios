# Enhanced Combat Test - Spellcasting and Special Attacks

## Summary

The test file has been enhanced to showcase:

### ✅ Features Demonstrated

1. **Character Spellcasting**
   - Wizards are created with `simple_character_generator()` which loads actual spells
   - Spell lists are displayed (cantrips and leveled spells)
   - Spell slots are tracked and displayed
   - The `CombatSystem.character_turn()` method handles spell casting automatically

2. **Monster Spellcasting**
   - Mage monster demonstrates powerful spells like "CONE OF COLD" and "ICE STORM"
   - Monster spells are cast automatically by `CombatSystem.monster_turn()`
   - Spell damage is calculated and applied correctly

3. **Monster Special Attacks**
   - Young Red Dragon demonstrates multi-attack capability
   - Special attacks are managed by the combat system internally

4. **Combat Intelligence**
   - The `CombatSystem` automatically chooses between:
     - Healing spells (if wounded)
     - Attack spells (cantrips and slot spells)
     - Special abilities
     - Normal weapon attacks

### 🎮 Test Scenarios

**Combat 1: Wizard vs Young Red Dragon**
- Demonstrates monster multi-attack
- Shows character spellcasting capabilities
- Very challenging fight (Dragon has 178 HP)

**Combat 2: Wizard vs Mage**
- Spellcaster vs Spellcaster battle
- Mage demonstrates high-level spell casting
- Shows spell damage mechanics

**Combat 3: Wizard vs Ogre**
- More balanced level-appropriate encounter
- Shows spell slot tracking
- Demonstrates combat rounds progression

### 📊 Combat Display Features

- Character spell lists with levels
- Spell slot tracking before and after combat
- Monster special abilities listing
- Detailed round-by-round combat log
- Combat statistics (rounds, HP remaining, spells cast)
- Victory/defeat determination

### 🔧 How It Works

The `CombatSystem` class handles all combat logic:

```python
# Character turn - automatically handles:
combat.character_turn(
    character=char,
    alive_chars=alive_chars,
    alive_monsters=alive_monsters,
    party=party
)
# - Checks for healing needs
# - Casts attack spells if available
# - Uses potions if needed
# - Falls back to weapon attacks

# Monster turn - automatically handles:
combat.monster_turn(
    monster=monster,
    alive_monsters=alive_monsters,
    alive_chars=alive_chars,
    party=party,
    round_num=round_num
)
# - Heals allies if wounded
# - Casts attack spells (cantrips/slot spells)
# - Uses special attacks (breath weapons, etc.)
# - Falls back to melee/ranged attacks
```

### 💡 Key Observations

1. **Spell Selection**: The combat system prioritizes higher-level spells for maximum damage
2. **Spell Slots**: Tracked accurately - cantrips don't consume slots, leveled spells do
3. **Special Attacks**: Monsters with special abilities (like dragon breath) use them intelligently
4. **Combat Balance**: CR (Challenge Rating) matters - Young Red Dragon is deadly for a level 5 wizard
5. **Automatic Decision Making**: The system handles all tactical decisions automatically

### 📝 Notes

- Character spellcasting is determined by `character.is_spell_caster` and `character.sc` (SpellCaster object)
- Monster spellcasting works the same way - checked via `monster.is_spell_caster` and `monster.sc`
- Special attacks are in `monster.sa` (list of SpecialAbility objects)
- The combat system uses verbose mode to show detailed combat messages
- All spell damage, DC checks, and attack rolls are handled internally

### 🎯 Result

The enhanced test successfully demonstrates:
- ✅ Character spellcasting capabilities
- ✅ Monster spellcasting (Cone of Cold, Ice Storm, etc.)
- ✅ Monster special attacks (Multi-attack)
- ✅ Spell slot tracking
- ✅ Combat round progression
- ✅ Detailed combat logging

The `dnd-5e-core` package's `CombatSystem` fully supports spellcasting and special attacks!

