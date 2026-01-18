#!/usr/bin/env python3
"""
La Tour du Mage Fou - Scénario D&D 5e
Un mage puissant est devenu fou et menace la région depuis sa tour.
Ce scénario met l'accent sur le spellcasting et les affrontements magiques.
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class TourMageFouScenario(BaseScenario):
    """
    La Tour du Mage Fou
    Utilise le fichier JSON data/scenes/tour_mage_fou.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "La Tour du Mage Fou"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Grok", level=3),
            self.create_basic_cleric("Sœur Elara", level=3),
            self.create_basic_fighter("Thrain", level=3),
            self.create_basic_fighter("Aldric", level=3),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        json_path = Path("data/scenes/tour_mage_fou.json")

        if not json_path.exists():
            print(f"⚠️  Fichier JSON non trouvé: {json_path}")
            print("Utilisation du scénario par défaut...")
            self._build_default_scenes()
            return

        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)

        # Utiliser SceneFactory pour créer les scènes depuis le JSON
        for scene_data in scenario_data.get('scenes', []):
            scene = SceneFactory.create_scene_from_dict(scene_data, self.monster_factory)
            if scene:
                self.scene_manager.add_scene(scene)

        print(f"✅ Scénario chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")

    def _build_default_scenes(self):
        """Scènes par défaut si le JSON n'est pas trouvé"""
        from src.scenes.scene_system import NarrativeScene

        intro_text = """Une tour imposante se dresse à l'horizon, entourée d'une aura magique menaçante.
        
Le puissant mage Valdaron, autrefois respecté, est devenu fou de pouvoir.
Depuis sa tour, il menace toute la région avec ses créations magiques.

Les villageois vous supplient de l'arrêter avant qu'il ne soit trop tard..."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🗼 LA TOUR DU MAGE FOU",
            text=intro_text,
            next_scene_id="approche_tour"
        ))


if __name__ == "__main__":
    # Test du scénario
    scenario = TourMageFouScenario()
    scenario.play()

