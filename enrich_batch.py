#!/usr/bin/env python3
"""
Script pour enrichir plusieurs scénarios manuellement
Génère les analyses PDF et affiche les instructions
"""

import sys
from pathlib import Path
import subprocess


SCENARIOS_PRIORITAIRES = [
    ("Fort-Roanoke", "Fort Roanoke", 2, "Enquête dans un fort isolé"),
    ("Harceles-a-Monteloy", "Harcèlés à Montéloy", 2, "Défendre un village attaqué"),
    ("Defis-a-Phlan", "Défis à Phlan", 1, "Mini-missions dans une ville"),
    ("Chasse-sanglante", "Chasse Sanglante", 3, "Chasse épique en forêt"),
    ("Naufrages", "Naufrages", 2, "Survivre à un naufrage"),
]


def analyze_scenario(pdf_name):
    """Analyser un scénario PDF"""
    print(f"\n{'='*80}")
    print(f"📖 Analyse de: {pdf_name}")
    print(f"{'='*80}\n")

    result = subprocess.run(
        ["python3", "analyze_pdf_deep.py", pdf_name],
        capture_output=False
    )

    return result.returncode == 0


def main():
    print("="*80)
    print("🚀 ENRICHISSEMENT DE SCÉNARIOS PRIORITAIRES".center(80))
    print("="*80)

    print("\nCe script va analyser les PDFs et générer les fichiers d'analyse.")
    print("Ensuite, vous pourrez enrichir manuellement les scénarios.")
    print()

    print("📋 Scénarios prioritaires:")
    for i, (pdf, name, level, desc) in enumerate(SCENARIOS_PRIORITAIRES, 1):
        print(f"  {i}. {name} (Niveau {level})")
        print(f"     {desc}")
    print()

    response = input("Voulez-vous analyser tous ces scénarios? (o/n): ").strip().lower()

    if response != 'o':
        print("❌ Annulé")
        return

    print("\n" + "="*80)
    print("🔍 ANALYSE DES SCÉNARIOS")
    print("="*80)

    success_count = 0

    for pdf_name, name, level, desc in SCENARIOS_PRIORITAIRES:
        if analyze_scenario(pdf_name):
            success_count += 1
            print(f"✅ {name} analysé avec succès")
        else:
            print(f"❌ Erreur lors de l'analyse de {name}")

    print("\n" + "="*80)
    print("📊 RÉSUMÉ")
    print("="*80)
    print(f"\n✅ {success_count}/{len(SCENARIOS_PRIORITAIRES)} scénarios analysés")

    print("\n📁 Fichiers d'analyse générés:")
    for pdf_name, name, _, _ in SCENARIOS_PRIORITAIRES:
        analysis_file = Path(f"analysis/{pdf_name}_analysis.txt")
        if analysis_file.exists():
            size_kb = analysis_file.stat().st_size // 1024
            print(f"  ✅ {analysis_file} ({size_kb} KB)")

    print("\n" + "="*80)
    print("📝 PROCHAINES ÉTAPES")
    print("="*80)

    print("""
Pour chaque scénario:

1. Lire le fichier d'analyse:
   cat analysis/Nom-du-scenario_analysis.txt
   
2. Créer le JSON enrichi manuellement:
   - Copier les textes authentiques du PDF
   - Utiliser les noms exacts des NPCs et lieux
   - Intégrer les mécanismes de jeu spécifiques
   - Ajouter les combats avec nombres exacts
   
3. Créer le script Python:
   - Copier cryptes_de_kelemvor_manual_game.py
   - Adapter pour le nouveau scénario
   
4. Tester:
   python nom_du_scenario_manual_game.py

5. Ajouter au launcher.py

Estimation: 1-2 heures par scénario pour un résultat professionnel ⭐⭐⭐⭐⭐
""")


if __name__ == "__main__":
    main()

