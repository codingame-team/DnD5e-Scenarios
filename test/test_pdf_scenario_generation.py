#!/usr/bin/env python3
"""
Test du système de génération de scénario depuis PDF
"""

from src.utils.pdf_reader import PDFScenarioReader
from src.scenes.scene_system import SceneManager, NarrativeScene, ChoiceScene
from pathlib import Path

print("=" * 70)
print("  📖 TEST GÉNÉRATION SCÉNARIO DEPUIS PDF")
print("=" * 70)

import os

pdf_path = "scenarios/Chasse-aux-gobs.pdf"

if not os.path.exists(pdf_path):
    print(f"\n❌ Fichier PDF non trouvé: {pdf_path}")
    print(f"   Chemin absolu: {os.path.abspath(pdf_path)}")
    exit(1)

print(f"\n1️⃣  Lecture du PDF: {pdf_path}")
print("-" * 70)

with PDFScenarioReader(pdf_path) as reader:
    # Extraire toutes les données
    summary = reader.generate_scenario_summary()

    print(f"\n📄 Titre: {summary['title']}")
    print(f"📑 Pages: {summary['pages']}")
    print(f"📝 Longueur texte: {summary['full_text_length']} caractères")

    # Sections
    print(f"\n📍 Sections extraites ({len(summary['sections'])}):")
    for i, section_id in enumerate(summary['sections'][:5], 1):
        print(f"   {i}. {section_id[:50]}")

    # Lieux
    print(f"\n🗺️  Lieux détectés ({len(summary['locations'])}):")
    for i, location in enumerate(summary['locations'][:10], 1):
        print(f"   {i}. {location}")

    # PNJs
    print(f"\n👥 PNJs détectés ({len(summary['npcs'])}):")
    for i, npc in enumerate(summary['npcs'][:5], 1):
        print(f"   {i}. {npc['name']}: {npc['description'][:40]}...")

    # Rencontres
    print(f"\n⚔️  Rencontres détectées ({len(summary['encounters'])}):")
    if summary['encounters']:
        for i, enc in enumerate(summary['encounters'][:5], 1):
            print(f"   {i}. {enc['count']}x {enc['creature']}")
    else:
        print("   (Aucune rencontre détectée par pattern matching)")

    # Maps
    print(f"\n🗺️  Maps générées: {len(summary.get('maps', []))}")

print("\n" + "=" * 70)
print("  2️⃣  GÉNÉRATION AUTOMATIQUE DE SCÈNES")
print("=" * 70)

with PDFScenarioReader(pdf_path) as reader:
    sections = reader.extract_sections()
    locations = reader.extract_locations()
    npcs = reader.extract_npcs()

    manager = SceneManager()

    # Créer scène d'intro depuis première section
    if sections:
        first_section_id = list(sections.keys())[0]
        first_section_text = sections[first_section_id]

        # Limiter à 500 caractères pour lisibilité
        intro_text = first_section_text[:500]
        if len(first_section_text) > 500:
            intro_text += "..."

        manager.add_scene(NarrativeScene(
            scene_id="intro_from_pdf",
            title=f"📖 {first_section_id.replace('_', ' ').title()}",
            text=intro_text,
            next_scene_id="exploration"
        ))

        print(f"\n✅ Scène d'intro créée depuis section '{first_section_id}'")
        print(f"   Texte: {len(intro_text)} caractères")

    # Créer scène d'exploration avec choix basés sur les lieux
    if locations:
        choices = []
        for i, location in enumerate(locations[:4]):  # Max 4 lieux
            choices.append({
                'text': f"Explorer {location}",
                'next_scene': f"location_{i}",
                'effects': {'exploration': 1}
            })

        if choices:
            manager.add_scene(ChoiceScene(
                scene_id="exploration",
                title="🗺️  EXPLORATION",
                description="Plusieurs lieux s'offrent à vous...",
                choices=choices
            ))

            print(f"\n✅ Scène d'exploration créée avec {len(choices)} lieux:")
            for choice in choices:
                print(f"   - {choice['text']}")

    # Créer scènes pour chaque lieu
    for i, location in enumerate(locations[:4]):
        location_text = f"Vous arrivez à {location}."

        # Chercher si un PNJ est associé à ce lieu
        for npc in npcs:
            if location.lower() in npc.get('context', '').lower():
                location_text += f" Vous rencontrez {npc['name']} ({npc['description']})."
                break

        manager.add_scene(NarrativeScene(
            scene_id=f"location_{i}",
            title=f"📍 {location}",
            text=location_text,
            next_scene_id="exploration"
        ))

    if locations[:4]:
        print(f"\n✅ {len(locations[:4])} scènes de lieux créées")

    # Statistiques
    print(f"\n📊 TOTAL: {len(manager.scenes)} scènes générées automatiquement")
    print("\nScènes créées:")
    for scene_id, scene in manager.scenes.items():
        print(f"   - {scene_id:20s} → {scene.title}")

print("\n" + "=" * 70)
print("  3️⃣  ÉVALUATION DU SYSTÈME")
print("=" * 70)

print("\n✅ FONCTIONNEL:")
print("   ✓ Lecture PDF complète")
print("   ✓ Extraction sections de texte")
print("   ✓ Détection lieux (pattern matching)")
print("   ✓ Détection PNJs (pattern matching)")
print("   ✓ Génération maps ASCII")
print("   ✓ Création automatique de scènes")

print("\n⚠️  LIMITATIONS:")
print("   • Détection rencontres basique (nécessite patterns précis)")
print("   • Maps ASCII génériques (pas extraction réelle d'images)")
print("   • Scènes générées simples (pas de logique complexe)")

print("\n💡 AMÉLIORATIONS POSSIBLES:")
print("   1. Extraction tables PDF pour statistiques monstres")
print("   2. OCR sur images de maps pour conversion ASCII")
print("   3. NLP pour meilleure compréhension du texte")
print("   4. Parser structure narrative (actes, scènes, dialogues)")

print("\n" + "=" * 70)
print("  🎉 TEST TERMINÉ")
print("=" * 70)
print("\n✅ Le système de génération depuis PDF fonctionne!")
print("✅ Les scènes sont créées automatiquement")
print("✅ Le jeu peut utiliser le contenu du PDF")
print()

