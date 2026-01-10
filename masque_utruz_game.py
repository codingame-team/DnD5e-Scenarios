#!/usr/bin/env python3
"""
Le Masque Utruz - Scénario D&D 5e
Enquête et intrigue autour d'un masque maudit lors d'un bal masqué
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class MasqueUtruzScenario(BaseScenario):
    """
    Le Masque Utruz - Intrigue et mystère
    Utilise le fichier JSON data/scenes/masque_utruz.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "Le Masque Utruz"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Aramis", level=2),
            self.create_basic_cleric("Elise", level=2),
            self.create_basic_fighter("Marcus", level=2),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        json_path = Path("data/scenes/masque_utruz.json")

        if not json_path.exists():
            print(f"⚠️  Fichier JSON non trouvé: {json_path}")
            print("Utilisation du scénario par défaut...")
            self._build_default_scenes()
            return

        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)

        for scene_data in scenario_data.get('scenes', []):
            scene = SceneFactory.create_scene_from_dict(scene_data, self.monster_factory)
            if scene:
                self.scene_manager.add_scene(scene)

        print(f"✅ Scénario chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")

    def _build_default_scenes(self):
        """Scènes par défaut si le JSON n'est pas trouvé"""
        from src.scenes.scene_system import NarrativeScene

        intro_text = """La cité de Belport se prépare pour le Grand Bal Masqué.

Mais le légendaire Masque Utruz, un artefact maudit, a refait surface!

Le Duc vous engage pour protéger le bal et empêcher que le masque ne tombe 
entre de mauvaises mains."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🎭 LA CITÉ DE BELPORT",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario Le Masque Utruz"""
    import argparse

    parser = argparse.ArgumentParser(description="Le Masque Utruz")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = MasqueUtruzScenario(
        pdf_path="scenarios/Masque-utruz.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

