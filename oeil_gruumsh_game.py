#!/usr/bin/env python3
"""
L'Oeil de Gruumsh - Scénario D&D 5e
Un groupe d'aventuriers doit affronter une tribu d'orques menée par un Oeil de Gruumsh
Version utilisant fichiers JSON
"""

from typing import List
from pathlib import Path
from dnd_5e_core import Character
from src.scenarios.base_scenario import BaseScenario
from src.scenes.scene_factory import SceneFactory


class OeilDeGruumshScenario(BaseScenario):
    """
    L'Oeil de Gruumsh - Affrontement avec une tribu d'orques
    Utilise le fichier JSON data/scenes/oeil_de_gruumsh.json
    """

    def __init__(self, pdf_path: str = "", use_ncurses: bool = False):
        super().__init__(pdf_path, use_ncurses)

    def get_scenario_name(self) -> str:
        return "L'Oeil de Gruumsh"

    def create_party(self) -> List[Character]:
        """Créer le groupe d'aventuriers"""
        party = [
            self.create_basic_fighter("Thorgrim", level=3),
            self.create_basic_cleric("Aria", level=3),
            self.create_basic_fighter("Kael", level=3),
            self.create_basic_cleric("Lyra", level=3),
        ]
        return party

    def build_custom_scenes(self):
        """Charger les scènes depuis le fichier JSON"""
        # Charger le scénario depuis JSON
        json_path = Path("data/scenes/oeil_de_gruumsh.json")

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
        intro_text = """Les Montagnes de Fer sont en proie à une nouvelle menace. 
Une tribu d'orques, menée par un redoutable Oeil de Gruumsh, a établi son campement 
dans les hauteurs.

Ces guerriers sanguinaires attaquent les caravanes marchandes et pillent les villages 
de la vallée. Le conseil des anciens vous a choisis pour mettre fin à cette menace."""

        self.scene_manager.add_scene(NarrativeScene(
            scene_id="intro",
            title="🏔️ MONTAGNES DE FER",
            text=intro_text,
            next_scene_id=None
        ))
        print("⚠️  Utilisation d'une scène d'intro par défaut (JSON manquant)")


def main():
    """Lancer le scénario L'Oeil de Gruumsh"""
    import argparse

    parser = argparse.ArgumentParser(description="L'Oeil de Gruumsh")
    parser.add_argument('--ncurses', action='store_true', help="Utiliser interface ncurses")
    args = parser.parse_args()

    scenario = OeilDeGruumshScenario(
        pdf_path="scenarios/Oeil-de-Gruumsh.pdf",
        use_ncurses=args.ncurses
    )
    scenario.play()


if __name__ == "__main__":
    main()

