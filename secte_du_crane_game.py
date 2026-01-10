#!/usr/bin/env python3
"""
La Secte du Crâne - Scénario D&D 5e
Un groupe d'aventuriers doit infiltrer les catacombes et arrêter un culte nécromantique
Version utilisant fichiers JSON
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class SecteDuCraneScenario(BaseScenario):
    """
    La Secte du Crâne - Infiltration de catacombes et culte nécromantique
    Utilise le fichier JSON data/scenes/secte_du_crane.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "La Secte du Crâne"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Aldric", level=4),
            self.create_basic_cleric("Seraphine", level=4),
            self.create_basic_fighter("Gareth", level=4),
            self.create_basic_cleric("Elara", level=4),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        # Charger le scénario depuis JSON
        json_path = Path("data/scenes/secte_du_crane.json")

        if not json_path.exists():
            print(f"⚠️  Fichier JSON non trouvé: {json_path}")
            print("Utilisation du scénario par défaut...")
            self._build_default_scenes()
            return

        # Charger les scènes depuis JSON avec SceneFactory
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)

        # Créer les scènes depuis le JSON
        for scene_data in scenario_data.get('scenes', []):
            scene = SceneFactory.create_scene_from_dict(scene_data, self.monster_factory)
            if scene:
                self.scene_manager.add_scene(scene)

        print(f"✅ Scénario chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")

    def _build_default_scenes(self):
        """Scènes par défaut si le JSON n'est pas trouvé"""
        from src.scenes.scene_system import NarrativeScene

        # Scène d'intro minimale
        intro_text = """La paisible ville de Ravencrest est troublée par d'étranges événements.

Des disparitions mystérieuses, des symboles inquiétants gravés sur les murs, des 
chuchotements nocturnes... Les habitants parlent à voix basse d'une secte du Crâne 
qui opérerait dans les ombres.

Le bourgmestre, désespéré, vous a convoqués pour enquêter."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🌃 VILLE DE RAVENCREST",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario La Secte du Crâne"""
    import argparse

    parser = argparse.ArgumentParser(description="La Secte du Crâne")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = SecteDuCraneScenario(
        pdf_path="scenarios/Secte-du-crane.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

