#!/usr/bin/env python3
"""
Test rapide de goblin_hunt_v3.py
Vérifie que tous les imports et l'initialisation fonctionnent
"""

print("🧪 Test de goblin_hunt_v3.py\n")

# Test 1: Imports
print("1️⃣  Test des imports...")
try:
    from goblin_hunt_v3 import GoblinHuntV3
    from src.rendering.renderer import create_renderer
    from src.utils.pdf_reader import PDFScenarioReader
    from src.scenes.scene_system import SceneManager
    from src.systems.spellcasting_v2 import SpellcastingManager
    from src.systems.merchant import MerchantSystem
    from src.core.adapters import CharacterExtensions
    print("   ✅ Tous les imports réussis")
except ImportError as e:
    print(f"   ❌ Erreur d'import: {e}")
    exit(1)

# Test 2: Initialisation du jeu
print("\n2️⃣  Test initialisation du jeu...")
try:
    game = GoblinHuntV3(use_ncurses=False)
    print(f"   ✅ Jeu initialisé")
    print(f"   ✅ Renderer: {type(game.renderer).__name__}")
    print(f"   ✅ Combat system: {type(game.combat_system).__name__}")
    print(f"   ✅ Spellcasting: {type(game.spellcasting).__name__}")
    print(f"   ✅ Merchant: {type(game.merchant_system).__name__}")
    print(f"   ✅ Scene manager: {type(game.scene_manager).__name__}")
except Exception as e:
    print(f"   ❌ Erreur initialisation: {e}")
    exit(1)

# Test 3: Renderer
print("\n3️⃣  Test du renderer...")
try:
    renderer = create_renderer(use_ncurses=False)
    print(f"   ✅ Renderer créé: {type(renderer).__name__}")
except Exception as e:
    print(f"   ❌ Erreur renderer: {e}")
    exit(1)

# Test 4: PDF Reader (sans ouvrir de fichier)
print("\n4️⃣  Test du PDF reader...")
try:
    from pathlib import Path
    pdf_path = "scenarios/Chasse-aux-gobs.pdf"
    if Path(pdf_path).exists():
        print(f"   ✅ PDF trouvé: {pdf_path}")
    else:
        print(f"   ⚠️  PDF non trouvé (optionnel): {pdf_path}")
except Exception as e:
    print(f"   ❌ Erreur PDF reader: {e}")

# Test 5: Scene Manager
print("\n5️⃣  Test du scene manager...")
try:
    manager = SceneManager()
    from src.scenes.scene_system import NarrativeScene

    manager.add_scene(NarrativeScene(
        scene_id="test",
        title="Test",
        text="Test scene"
    ))

    print(f"   ✅ Scene manager fonctionnel")
    print(f"   ✅ {len(manager.scenes)} scène(s) créée(s)")
except Exception as e:
    print(f"   ❌ Erreur scene manager: {e}")
    exit(1)

# Résumé
print("\n" + "="*60)
print("  🎉 TOUS LES TESTS RÉUSSIS!")
print("="*60)
print("\n📝 Le jeu est prêt à être lancé:")
print("   python goblin_hunt_v3.py")
print("\n   Ou avec ncurses:")
print("   python goblin_hunt_v3.py --ncurses")
print()

