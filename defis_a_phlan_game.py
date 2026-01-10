#!/usr/bin/env python3
"""
Défis à Phlan - Scénario D&D 5e
Plusieurs mini-missions dans la ville frontière de Phlan
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class DefisAPlanScenario(BaseScenario):
    """
    Défis à Phlan - Mini-aventures variées
    Utilise le fichier JSON data/scenes/defis_a_phlan.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "Défis à Phlan"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Cedric", level=1),
            self.create_basic_cleric("Luna", level=1),
            self.create_basic_fighter("Rogar", level=1),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        json_path = Path("data/scenes/defis_a_phlan.json")

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

        intro_text = """Bienvenue à Phlan, ville frontière récemment reconstruite!

Le Conseil recherche des aventuriers pour accomplir diverses missions:
- Enquêter sur une taverne hantée
- Éliminer des gobelins dans les égouts
- Retrouver un marchand disparu

Choisissez votre défi et gagnez gloire et richesse!"""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏰 BIENVENUE À PHLAN",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario Défis à Phlan"""
    import argparse

    parser = argparse.ArgumentParser(description="Défis à Phlan")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = DefisAPlanScenario(
        pdf_path="scenarios/Defis-a-Phlan.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

