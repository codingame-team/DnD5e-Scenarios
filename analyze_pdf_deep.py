#!/usr/bin/env python3
"""
Analyseur PDF Approfondi pour Scénarios D&D
Extrait et affiche le contenu détaillé pour enrichissement manuel
"""

from pathlib import Path
from src.utils.pdf_reader import PDFScenarioReader
import sys

class DetailedPDFAnalyzer:
    """Analyse approfondie d'un PDF de scénario"""

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.scenario_name = pdf_path.stem

    def analyze(self):
        """Analyser le PDF en profondeur et afficher les résultats"""
        print("=" * 80)
        print(f"📖 ANALYSE APPROFONDIE: {self.scenario_name}")
        print("=" * 80)

        with PDFScenarioReader(self.pdf_path) as reader:
            # 1. Texte complet
            full_text = reader.get_full_text()
            print(f"\n📄 TEXTE COMPLET ({len(full_text)} caractères)")
            print("-" * 80)

            # 2. Sections détaillées
            sections = reader.extract_sections()
            print(f"\n📚 SECTIONS ({len(sections)} trouvées)")
            print("-" * 80)

            for i, (section_name, content) in enumerate(sections.items(), 1):
                print(f"\n{i}. {section_name.upper()}")
                print("   " + "=" * 75)
                # Afficher les premiers 1000 caractères de chaque section
                preview = content[:1000]
                if len(content) > 1000:
                    preview += "\n   [...suite...]"
                print("   " + preview.replace("\n", "\n   "))
                print()

            # 3. NPCs
            npcs = reader.extract_npcs()
            print(f"\n👥 NPCs ({len(npcs)} trouvés)")
            print("-" * 80)
            for npc in npcs[:15]:  # Limiter à 15
                print(f"- {npc['name']}: {npc['description'][:100]}")

            # 4. Lieux
            locations = reader.extract_locations()
            print(f"\n🗺️  LIEUX ({len(locations)} trouvés)")
            print("-" * 80)
            for loc in locations[:20]:
                print(f"- {loc}")

            # 5. Rencontres
            encounters = reader.extract_encounters()
            print(f"\n⚔️  RENCONTRES ({len(encounters)} trouvées)")
            print("-" * 80)
            for enc in encounters[:10]:
                print(f"- {enc['count']} {enc['creature']}")
                print(f"  Contexte: {enc['context'][:100]}...")

            # 6. Extraits clés
            print(f"\n🔍 EXTRAITS CLÉS")
            print("-" * 80)

            # Rechercher des mots-clés importants
            keywords = [
                "mission", "objectif", "quête",
                "combat", "rencontre", "ennemi",
                "trésor", "récompense",
                "PNJ", "personnage",
                "lieu", "endroit", "zone"
            ]

            for keyword in keywords:
                if keyword.lower() in full_text.lower():
                    # Trouver contexte autour du mot-clé
                    idx = full_text.lower().find(keyword.lower())
                    if idx != -1:
                        start = max(0, idx - 100)
                        end = min(len(full_text), idx + 200)
                        context = full_text[start:end]
                        print(f"\n[{keyword.upper()}]:")
                        print(f"...{context}...")

            # 7. Sauvegarder l'analyse complète
            output_file = Path("analysis") / f"{self.scenario_name}_analysis.txt"
            output_file.parent.mkdir(exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"ANALYSE COMPLÈTE: {self.scenario_name}\n")
                f.write("=" * 80 + "\n\n")

                f.write("TEXTE COMPLET:\n")
                f.write("-" * 80 + "\n")
                f.write(full_text)
                f.write("\n\n")

                f.write("SECTIONS:\n")
                f.write("-" * 80 + "\n")
                for name, content in sections.items():
                    f.write(f"\n### {name.upper()} ###\n")
                    f.write(content)
                    f.write("\n\n")

            print(f"\n\n✅ Analyse complète sauvegardée: {output_file}")
            print(f"📊 Taille du fichier: {output_file.stat().st_size} octets")

            return {
                'full_text': full_text,
                'sections': sections,
                'npcs': npcs,
                'locations': locations,
                'encounters': encounters,
                'output_file': output_file
            }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf_deep.py <nom_du_pdf>")
        print("\nExemples:")
        print("  python analyze_pdf_deep.py Cryptes-de-Kelemvor")
        print("  python analyze_pdf_deep.py Fort-Roanoke")
        print("  python analyze_pdf_deep.py Harceles-a-Monteloy")
        sys.exit(1)

    pdf_name = sys.argv[1]
    if not pdf_name.endswith('.pdf'):
        pdf_name += '.pdf'

    pdf_path = Path("scenarios") / pdf_name

    if not pdf_path.exists():
        print(f"❌ PDF non trouvé: {pdf_path}")
        print("\nPDFs disponibles:")
        for p in sorted(Path("scenarios").glob("*.pdf")):
            if "Liste" not in p.name and "Tales" not in p.name:
                print(f"  - {p.stem}")
        sys.exit(1)

    analyzer = DetailedPDFAnalyzer(pdf_path)
    result = analyzer.analyze()

    print("\n" + "=" * 80)
    print("✅ ANALYSE TERMINÉE")
    print("=" * 80)
    print(f"\nConsultez le fichier: {result['output_file']}")
    print("\nVous pouvez maintenant utiliser ce contenu pour enrichir manuellement le scénario!")


if __name__ == "__main__":
    main()

