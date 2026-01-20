#!/usr/bin/env python3
"""Test spell loading"""

print("Step 1: Importing...")
try:
    from dnd_5e_core.data.collections import get_collections_directory
    print(f"  Collections dir: {get_collections_directory()}")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 2: Getting spells list...")
try:
    from dnd_5e_core.data.collections import get_spells_list
    spells_list = get_spells_list()
    print(f"  Found {len(spells_list)} spell indexes")
    print(f"  First 3: {spells_list[:3]}")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 3: Loading first spell...")
try:
    from dnd_5e_core.data.loader import load_spell
    first_spell = load_spell(spells_list[0])
    print(f"  Loaded: {first_spell.name if first_spell else 'None'}")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 4: Loading all spells...")
try:
    from dnd_5e_core.data.collections import load_all_spells
    all_spells = load_all_spells()
    print(f"  Loaded {len(all_spells)} spells")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
