#!/usr/bin/env python3
"""
Les Cryptes de Kelemvor - Scénario D&D 5e
Exploration de cryptes hantées et affrontement avec un nécromancien
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class CryptesDeKelemvorScenario(BaseScenario):
    """
    Les Cryptes de Kelemvor - Donjon mort-vivant
    Utilise le fichier JSON data/scenes/cryptes_de_kelemvor.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "Les Cryptes de Kelemvor"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Paladine", level=3),
            self.create_basic_cleric("Luminara", level=3),
            self.create_basic_fighter("Dorian", level=3),
            self.create_basic_cleric("Thalia", level=3),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        json_path = Path("data/scenes/cryptes_de_kelemvor.json")

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

        intro_text = """Le Temple de Kelemvor, dieu de la Mort, a été profané!

Des morts-vivants se réveillent dans les cryptes. Un nécromancien cherche à voler 
le Crâne de Kelemvor, un artefact sacré.

Descendez dans les cryptes et arrêtez-le!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="⚰️ LE TEMPLE DE KELEMVOR",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario Les Cryptes de Kelemvor"""
    import argparse

    parser = argparse.ArgumentParser(description="Les Cryptes de Kelemvor")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = CryptesDeKelemvorScenario(
        pdf_path="scenarios/Cryptes-de-Kelemvor.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

